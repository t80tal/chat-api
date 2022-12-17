from django.contrib.auth.models import AbstractUser
from django.db import models

class AuthUser(AbstractUser):
    email = models.EmailField(null=False, unique=True)
    full_name = models.TextField(null=True)

    def save(self, *args, **kwargs):
        super().set_password(self.password)
        return super(AuthUser, self).save(*args, **kwargs)

    class Meta:
            db_table = "user"
