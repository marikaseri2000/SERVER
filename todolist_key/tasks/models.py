import uuid
from django.db import models
from project.models import Project

# Create your models here.
class Task(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=200)
    descrizione=models.TextField(blank=True, null=True)
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,  # Se elimini il progetto, elimini anche i task
        related_name='tasks',  # Permette di accedere ai task da un project: project.tasks.all()
        null=True, 
        blank=True
        )
    
    class Meta:
        db_table = "tasks"
