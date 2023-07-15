from django.db import models

class MenuManager(models.Manager):
    def execute_create(self, name, module):
        menu = self.create(name=name, module=module)
        menu.full_clean()
        menu.save()
        return menu