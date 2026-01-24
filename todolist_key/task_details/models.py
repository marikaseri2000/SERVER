import uuid
from django.db import models
from tasks.models import Task

# Create your models here.
class TaskDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descrizione = models.CharField(max_length=200)

    """
    Con questa istruzione definisco la relazione 1:1 tra ProjectDetails e Project
    """
    task = models.OneToOneField(
        Task, on_delete=models.CASCADE, related_name='details_t'
    )

    class Meta:
        """Il nome della tabella viene definito con questa funzione."""
        db_table = "tasks_details"