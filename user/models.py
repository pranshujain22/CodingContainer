from django.db import models

# Create your models here.


class UserProfile(models.Model):

    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    enrollment_id = models.IntegerField(unique=True, primary_key=True)
    email = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return str(self.enrollment_id)

