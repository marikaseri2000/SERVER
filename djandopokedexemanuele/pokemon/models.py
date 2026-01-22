from django.db import models
import uuid
from allenatore.models import Allenatore
from django.core.validators import MinValueValidator

# Create your models here.
class Pokemon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)
    pokedex_id = models.IntegerField()
    allenatore=models.ForeignKey(Allenatore, on_delete=models.CASCADE, related_name="pokemon", null=True, blank=True)
    SESSO_CHOICES = [
        ('M', 'Maschio'),
        ('F', 'Femmina'),
        ('N', 'Sconosciuto'),
    ]
    
    sesso = models.CharField(
        max_length=1,
        choices=SESSO_CHOICES,
        default='N')
    
    punti_salute = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=50)
    
    TIPO_CHOICES = [
        ('normale', 'Normale'),
        ('fuoco', 'Fuoco'),
        ('acqua', 'Acqua'),
        ('erba', 'Erba'),
        ('elettro', 'Elettro'),
        ('ghiaccio', 'Ghiaccio'),
        ('lotta', 'Lotta'),
        ('veleno', 'Veleno'),
        ('terra', 'Terra'),
        ('volante', 'Volante'),
        ('psico', 'Psico'),
        ('coleottero', 'Coleottero'),
        ('roccia', 'Roccia'),
        ('spettro', 'Spettro'),
        ('drago', 'Drago'),
        ('buio', 'Buio'),
        ('acciaio', 'Acciaio'),
        ('folletto', 'Folletto'),
    ]
    
    tipo_primario = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='normale'
    )