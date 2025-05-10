from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63, verbose_name="Display name")
    email = models.EmailField()

    def __str__(self):
        return str(self.display_name)