import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Simulation
from .serializers import (
    SimulationSerializer,
    CreateSimulationSerializer,
    StepSerializer,
    PatchSimulationSerializer,
)
from .engine import create_grid, step
from .weather import get_weather_params


class SimulationListView(APIView):
    """
    POST /api/simulations/
    Crea una nueva simulación.
    Parámetros: size (int, 20-200), p (float), f (float)
    Respuesta: estado completo de la simulación
    """

    def post(self, request):
        serializer = CreateSimulationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        size = serializer.validated_data['size']
        p = serializer.validated_data['p']
        f = serializer.validated_data['f']

        grid = create_grid(size)
        sim = Simulation(size=size, p=p, f=f)
        sim.set_grid(grid)
        sim.save()

        return Response(SimulationSerializer(sim).data, status=status.HTTP_201_CREATED)


class SimulationDetailView(APIView):
    """
    GET /api/simulations/{id}/
    Devuelve el estado actual completo de la simulación.
    Respuesta: UUID, cuadrícula, p, f, pasos ejecutados, densidad, histograma.

    PATCH /api/simulations/{id}/
    Modifica p y/o f en caliente.
    Parámetros: p (float, opcional), f (float, opcional)

    DELETE /api/simulations/{id}/
    Elimina la simulación.
    """

    def get(self, request, pk):
        sim = get_object_or_404(Simulation, pk=pk)
        return Response(SimulationSerializer(sim).data)

    def patch(self, request, pk):
        sim = get_object_or_404(Simulation, pk=pk)
        serializer = PatchSimulationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'p' in serializer.validated_data:
            sim.p = serializer.validated_data['p']
        if 'f' in serializer.validated_data:
            sim.f = serializer.validated_data['f']
        sim.save()

        return Response(SimulationSerializer(sim).data)

    def delete(self, request, pk):
        sim = get_object_or_404(Simulation, pk=pk)
        sim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SimulationStepView(APIView):
    """
    POST /api/simulations/{id}/step/
    Avanza la simulación N pasos.
    Parámetros: steps (int, por defecto 1)
    Respuesta: estado completo actualizado de la simulación.
    """

    def post(self, request, pk):
        sim = get_object_or_404(Simulation, pk=pk)
        serializer = StepSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        n_steps = serializer.validated_data['steps']
        grid = sim.get_grid()

        for _ in range(n_steps):
            grid, fire_size = step(grid, sim.p, sim.f)
            sim.update_histogram(fire_size)
            sim.steps_executed += 1

        sim.set_grid(grid)
        sim.save()

        return Response(SimulationSerializer(sim).data)


class WeatherView(APIView):
    """
    GET /api/weather/?city={ciudad}
    Consulta Open-Meteo y devuelve p y f sugeridos según el tiempo actual.
    Parámetros: city (str)
    Respuesta: p (float), f (float), datos meteorológicos usados.
    """

    def get(self, request):
        city = request.query_params.get('city', '').strip()
        if not city:
            return Response(
                {"error": "El parámetro 'city' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = get_weather_params(city)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result)
    