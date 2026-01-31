from django.db import models
import uuid
from django.conf import settings
from django.db import models


class Partecipante(models.Model):
    #riferimento a user con fk
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participant_profile",
        null=True,  # Permette di creare partecipanti senza utente collegato
        blank=True
    )
    matricola = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_preautorizzata = models.EmailField(unique=True)
    data_iscrizione = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = "partecipanti"