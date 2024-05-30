
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Coalesce
from django.db.models import Max, F

class MenuQueryset(models.query.QuerySet):
    def _filter_by_path_parent(self, parent):
        return self.filter(path__startswith=parent.path + '/', depth=parent.depth+1
                           ).exclude(path=parent.path)
    
    def get_children(self, node ):
        children = self._filter_by_path_parent(node)

        return children

    def get_parent_from_path(self, path):
        parents_id = path.split('/')[-2]

        if parents_id == '' :
            return None

        return int(parents_id)
    
    def get_parent(self, node):
        parent_id = self.get_parent_from_path(node.path)
        if(parent_id is None):
            return None
        return self.get(id=parent_id)            
    
      
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

        
    def move_before_sibiling(self, node_origin_id, node_sibiling_id):
        node_origin = self.get(id=node_origin_id)
        node_sibiling = self.get(id=node_sibiling_id)
        parent_origin = self.get_parent(node_origin)
        parent_sibiling = self.get_parent(node_sibiling)

        if(node_sibiling.id == parent_origin.id and parent_sibiling==None):
            return
        
        if(parent_origin == parent_sibiling):
            if(node_origin.order < node_sibiling.order): 
                self.get_children(parent_origin).filter(order__gt=node_origin.order, order__lt=node_sibiling.order).update(order=F('order') - 1)
                node_origin.order = node_sibiling.order - 1

            if(node_origin.order > node_sibiling.order):
                self.get_children(parent_origin).filter( order__gte=node_sibiling.order, order__lt=node_origin.order).update(order=F('order') + 1)
                node_origin.order = node_sibiling.order

        if(parent_origin != parent_sibiling):
            new_path = f"{parent_sibiling.path}/{node_origin.id}" 
            node_origin.path = new_path
            node_origin.depth = node_sibiling.depth 
            node_origin.order = node_sibiling.order
            self.get_children(parent_origin).filter(order__gt=node_origin.order).update(order=F('order') - 1)
            self.get_children(parent_sibiling).filter(order__gte=node_sibiling.order).update(order=F('order') + 1)
  


        node_origin.save()