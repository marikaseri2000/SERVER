from django.db import models
import uuid

from project.models import Project

class ProjectDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=200)

    """
    Con questa istruzione definisco la relazione 1:1 tra ProjectDetails e Project
    """
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="project"
    )

    class Meta:
        db_table = "projects_details"