import uuid
import numpy as np
from django.db import models


class Simulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.IntegerField()
    p = models.FloatField()
    f = models.FloatField()
    steps_executed = models.IntegerField(default=0)
    grid_data = models.BinaryField()  # guardamos el numpy array serializado
    fire_histogram = models.JSONField(default=dict)  # {tamaño: frecuencia}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_grid(self):
        """Deserializa el grid desde base de datos."""
        return np.frombuffer(self.grid_data, dtype=np.int8).reshape(self.size, self.size).copy()

    def set_grid(self, grid):
        """Serializa el grid para guardar en base de datos."""
        self.grid_data = grid.astype(np.int8).tobytes()

    def update_histogram(self, fire_size):
        """Acumula el tamaño del incendio en el histograma."""
        if fire_size > 0:
            key = str(fire_size)
            self.fire_histogram[key] = self.fire_histogram.get(key, 0) + 1

    def __str__(self):
        return f"Simulation {self.id} ({self.size}x{self.size})"