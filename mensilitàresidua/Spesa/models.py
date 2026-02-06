import uuid
from django.db import models
from Categoria.models import Categoria
# Create your models here.

class Spesa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descrizione = models.CharField(max_length=100)
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="spese"
    )
    note = models.TextField(
        blank=True,
        null=True,
        help_text="Note opzionali, es. 'ne valeva la pena'"
    )


    class Meta:
        db_table = "spesa"