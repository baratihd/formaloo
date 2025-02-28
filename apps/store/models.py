from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel


User = get_user_model()
__all__ = ('App',)


class App(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apps')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title
