from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Usiamo i booleani per distinguere i ruoli
    is_admin = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "users"