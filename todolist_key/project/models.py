from django.db import models
from django.contrib.auth.models import User
import uuid

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="projects")

    class Meta:
        db_table = "projects"