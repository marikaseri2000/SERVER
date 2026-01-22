from django.db import models
import uuid
from allenatore.models import Allenatore

# Create your models here.
class Pokemon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)
    pokedex_id = models.IntegerField()
    allenatore=models.ForeignKey(Allenatore, on_delete=models.CASCADE, related_name="pokemon", null=True, blank=True)