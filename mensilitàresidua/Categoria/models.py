import uuid
from django.db import models

# Create your models here.

class Categoria(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nome = models.CharField(
        max_length=100,
        unique=True,
        help_text='Esempi: "Cibo", "Trasporti", "Svago", "Abbonamenti inutili"'
    )
    budget_mensile = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Budget mensile assegnato a questa categoria"
    )

    class Meta:
        db_table = "categorie"
    
    def __str__(self):
        return self.nome