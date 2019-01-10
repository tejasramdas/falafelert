from django.db import models

# Create your models here.
class Reminder(models.Model):
    phone_number = models.CharField(max_length=30)
    food=models.CharField(max_length=12)
