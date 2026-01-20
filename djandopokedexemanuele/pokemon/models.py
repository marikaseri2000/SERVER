from django.db import models
import uuid

# Create your models here.
class Pokemon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    pokedex_id = models.IntegerField()
    