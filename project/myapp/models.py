from django.db import models
import datetime
# Create your models here.


class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    call_id = models.CharField(max_length=50)
    purpose = models.TextField()
    summary = models.TextField()
    analytics = models.JSONField()  # Requires Django 3.1+
    converted = models.BooleanField(default=False)
    # call_date = models.DateField()
    # call_id = models.CharField(max_length=100)
    call_date = models.DateField(default=datetime.date.today)  # Specify a default value
    # converted = models.BooleanField(default=False)
    # converted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    