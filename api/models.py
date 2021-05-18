from django.db import models
from django.contrib.auth.models import User
import datetime


class department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name =  models.CharField(max_length=40)
    department = models.ForeignKey(department, on_delete=models.CASCADE )
    joining_date =  models.DateField(default=datetime.date.today)
    dob = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=12, null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return self.user.username
