from rest_framework import serializers
from .models import Simulation


class SimulationSerializer(serializers.ModelSerializer):
    grid = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = Simulation
        fields = ['id', 'size', 'p', 'f', 'steps_executed', 
                  'grid', 'fire_histogram', 'stats', 'created_at']

    def get_grid(self, obj):
        """Devuelve la cuadrícula como lista de listas."""
        return obj.get_grid().tolist()

    def get_stats(self, obj):
        """Devuelve estadísticas actuales de la cuadrícula."""
        from .engine import get_stats
        return get_stats(obj.get_grid())


class CreateSimulationSerializer(serializers.Serializer):
    size = serializers.IntegerField(min_value=20, max_value=200)
    p = serializers.FloatField(min_value=0.0, max_value=1.0)
    f = serializers.FloatField(min_value=0.0, max_value=1.0)


class StepSerializer(serializers.Serializer):
    steps = serializers.IntegerField(min_value=1, default=1)


class PatchSimulationSerializer(serializers.Serializer):
    p = serializers.FloatField(min_value=0.0, max_value=1.0, required=False)
    f = serializers.FloatField(min_value=0.0, max_value=1.0, required=False)