import uuid
from django.db import models

# Create your models here.
class Project(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome=models.CharField(max_length=200)
    descrizione=models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
        ('pianificato', 'Pianificato'),
        ('in_corso', 'In Corso'),
        ('completato', 'Completato'),
        ('sospeso', 'Sospeso'),
    ]
    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pianificato'
    )
    data_inizio=models.DateTimeField(auto_now_add=True)
    data_fine=models.DateTimeField(auto_now=True)