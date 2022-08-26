from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# class UserProfile(AbstractUser):
#     name = models.CharField(max_length=50)
#     mobile = models.CharField(max_length=30, null=True, blank=True)
#     profile_image = models.ImageField(upload_to='upload/profile', null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     def __str__(self):
#         return self.username
