from django.db import models
import uuid

class Giorno(models.Model):
    id_giorno = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.DateField(unique= True)
    is_active = models.BooleanField(default = True, blank = True)
    descrizione = models.TextField(max_length=500)
    
    

# Create your models here.
class Meta:
    db_table = "giorni"