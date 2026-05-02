from django.urls import path
from .views import (
    SimulationListView,
    SimulationDetailView,
    SimulationStepView,
    WeatherView,
)

urlpatterns = [
    path('simulations/', SimulationListView.as_view()),
    path('simulations/<uuid:pk>/', SimulationDetailView.as_view()),
    path('simulations/<uuid:pk>/step/', SimulationStepView.as_view()),
    path('weather/', WeatherView.as_view()),
]