from django.db import models

# Create your models here.
from django.db import models
from my_utilities.fields import TrimpCharField
from .managers import MenuManager



# Crea el modelo Menu para que el test test_menu_str de la clase TestMenuOperations pueda funcionar
class Menu(models.Model):
    name = TrimpCharField(max_length=100)
    module = models.ForeignKey("modules.Module", on_delete=models.PROTECT)

    objects  = MenuManager()

    def __str__(self):
        return f"{self.module.name} - {self.name}"























