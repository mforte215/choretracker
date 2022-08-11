from tkinter import CASCADE
from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    activity = models.CharField(max_length=600)
    room = models.CharField(max_length=600)
    last_cleaned_date = models.DateField()
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return f"{self.activity} in {self.room}"