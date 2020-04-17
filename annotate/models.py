from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import json

# Create your models here.
class Annotation(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lesson = models.IntegerField(default=0)
    page = models.TextField(default='')
    image = models.TextField(default='')
    content = JSONField()
