from django.db import models

from menus.managers import MenuManager
from django.core.exceptions import ValidationError

MyManager = MenuManager()

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=50, blank=True ,default='')


    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.name.strip():
            raise ValidationError('El nombre no puede estar vacío')
      
        self.name = self.name.strip()
        return super().clean()

    objects = MyManager
