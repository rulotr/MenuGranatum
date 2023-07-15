from django.db import models

from my_utilities.fields import TrimpCharField
from .managers import (ModuleQuerySet, ModuleManager)
# Create your models here.



MyManager = ModuleManager.from_queryset(ModuleQuerySet)

class Module(models.Model):
    name = TrimpCharField(max_length=50,)

    class Meta:
        constraints = [ models.UniqueConstraint(
            fields=["name"], name="unique_name_module" 
        )]

    objects = MyManager()
         
    
        
    def __str__(self):
        return self.name