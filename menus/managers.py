
from django.db import models

class MenuManager(models.Manager):

    def execute_create(self, name, parent_id=None):
        menu = self.model(name =name)
        menu.full_clean()

        menu.path = self.generate_path(parent_id= parent_id)
        menu.save()
        menu.path = self.generate_path(menu= menu)
        menu.save()
        return menu
    
    def generate_path(self,menu=None, parent_id=None):
        parent = ''
        if parent_id is not None:
            parent = self.get(id=parent_id)
            return f"/{str(parent.id)}"
        if menu is not None:
            return  str(menu.path) + "/" + str(menu.id)
        return ''
