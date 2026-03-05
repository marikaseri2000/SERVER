from django.db import models
import uuid

class Giorno(models.Model):
    data = models.DateField(primary_key=True)
    is_active = models.BooleanField(default=True, blank=True)
    descrizione = models.TextField(max_length=500)

    def __str__(self):
        return self.data.strftime('%Y-%m-%d')

class Meta:
    db_table = "giorni"