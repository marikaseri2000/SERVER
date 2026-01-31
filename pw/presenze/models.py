from django.db import models
import uuid
from partecipanti.models import Partecipante
from giorni_presenze.models import Giorno

class Presenza(models.Model):
   id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   giorno = models.ForeignKey(Giorno, on_delete= models.CASCADE, null = False, blank= False)
   stato = models.BooleanField(default = True, blank = True)
   partecipante = models.ForeignKey(Partecipante, on_delete= models.CASCADE, null = False, blank= False)
   #created_id = user_id
    

class Meta:
    db_table = "presenze"