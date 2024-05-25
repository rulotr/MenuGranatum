
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Coalesce
from django.db.models import Max

class MenuQueryset(models.query.QuerySet):
    def _filter_by_path_parent(self, parent):
        return self.filter(path__startswith=parent.path + '/', depth=parent.depth+1
                           ).exclude(path=parent.path)
    
    def get_children(self, node ):
        children = self._filter_by_path_parent(node)

        return children
    
      
    def _get_next_order_num(self, parent):
        get_children = self.filter(depth=1)
        
        if parent is not None:     
            get_children = self._filter_by_path_parent(parent)       
        
        order = get_children.aggregate(
                num=Coalesce(Max("order"), 0))['num'] 
        
        return order + 1

class MenuManager(models.Manager):

    def get_queryset(self):
        return MenuQueryset(self.model, using=self._db)
    
    def execute_create(self, name, parent_id=None, id=None):
        if parent_id is not None:
            try:
                parent = self.get(id=parent_id)
            except self.model.DoesNotExist:
                raise ValidationError("El nodo padre no existe")
        else:
            parent = None

        menu = self.model(name =name)
        #call method _get_next_order_num to get the next order number
        menu.order = self.get_queryset()._get_next_order_num(parent)

        # For test you can create a menu with an id
        if id is not None:
            menu.id = id

        menu.full_clean()
        menu.save()

        menu.path = self.generate_path( menu= menu, parent= parent)
        menu.depth = 1 if parent is None else parent.depth + 1 
        menu.save()
        return menu
    
    def generate_path(self,menu, parent):
        if parent:
            return f"{parent.path}/{menu.id}"
        else:
            return f"/{menu.id}"  # Nodo principal
  