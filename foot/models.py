# foot/models.py
from django.db import models

class PowerGeneration(models.Model):
    region = models.CharField(max_length=100)
    power_generated = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.region} - {self.power_generated}W at {self.timestamp}"

class FootstepData(models.Model):
    location_name = models.CharField(max_length=100)
    footsteps = models.IntegerField()
    energy_generated = models.FloatField()  # kWh
    date_recorded = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.location_name} - {self.footsteps} footsteps, {self.energy_generated} kWh"
    
class FootfallData(models.Model):
    location_name = models.CharField(max_length=255)
    footsteps = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    dwell_time = models.FloatField()  # Average dwell time in minutes

    def __str__(self):
        return self.location_name