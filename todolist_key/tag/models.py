import uuid
from django.db import models

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        """Il nome della tabella viene definito con questa funzione."""
        db_table = "tags"