from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('ev-charger', 'EV Charger Installation'), ('solar', 'Solar Panel Installation'), ('smart-home', 'Smart Home Energy')])
    date = models.DateField()
    notes = models.TextField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} on {self.date}"
