from django.db import models

from .managers import (MenuManager, MenuQueryset)
from django.core.exceptions import ValidationError

MyManager = MenuManager.from_queryset(MenuQueryset)

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=50, blank=True ,default='')
    order = models.PositiveSmallIntegerField(default=0)
    depth = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.name.strip():
            raise ValidationError('El nombre no puede estar vacío')
      
        self.name = self.name.strip()
        return super().clean()

    objects = MyManager()
