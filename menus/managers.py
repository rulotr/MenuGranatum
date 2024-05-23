
from django.db import models
from django.core.exceptions import ValidationError

class MenuManager(models.Manager):



    def execute_create(self, name, parent_id=None, id=None):
        if parent_id is not None:
            try:
                parent = self.get(id=parent_id)
            except self.model.DoesNotExist:
                raise ValidationError("El nodo padre no existe")
        else:
            parent = None

        menu = self.model(name =name)
        if id is not None:
            menu.id = id

        menu.full_clean()
        menu.save()

        menu.path = self.generate_path( menu= menu, parent= parent)
        menu.save()
        return menu
    
    def generate_path(self,menu, parent):
        if parent:
            return f"{parent.path}/{menu.id}"
        else:
            return f"/{menu.id}"  # Nodo principal
        
