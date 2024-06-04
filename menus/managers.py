
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Coalesce, Replace
from django.db.models import Max, F, Q, Value as V

class MenuQueryset(models.query.QuerySet):
    
    def get_all_modules(self):
        return self.filter(depth=1)
    
    def get_next_num_order_module(self):
        order = self.get_all_modules().aggregate(
                num=Coalesce(Max("order"), 0))['num']
        
        return order + 1
    
    def get_module_tree(self, module_id):
        module_tree = self.filter(
            Q(id=module_id) |
            Q(path__startswith= f"/{module_id}/") 
            ).order_by('depth', 'order', 'id')                        

        return module_tree
    
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
        menu.order = parent.get_next_num_order_children if parent is not None else self.get_next_num_order_module()

      
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

        
    def move_before_sibling(self, node_origin_id, node_sibling_id):
        node_origin = self.get_node_by_id(node_origin_id)
        node_sibling = self.get_node_by_id(node_sibling_id)

        self.validate_move(node_origin, node_sibling)
        
        parent_origin = node_origin.get_parent
        parent_sibling = node_sibling.get_parent
    
        children_parent_origin =  parent_origin.get_children if parent_origin is not None else self.get_all_modules()
        children_parent_sibling = parent_sibling.get_children if parent_sibling is not None else self.get_all_modules()

        if(parent_origin is not None and node_sibling.id == parent_origin.id and parent_sibling==None):
            return
        
        self.ajust_order_when_is_the_same_parent(node_origin, node_sibling, parent_origin, parent_sibling, children_parent_origin)

        self.move_when_is_different_parent(node_origin, node_sibling, parent_origin, parent_sibling, children_parent_origin, children_parent_sibling)
        


    def move_when_is_different_parent(self, node_origin, node_sibling, parent_origin, parent_sibling, children_parent_origin, children_parent_sibling):
        if(parent_origin != parent_sibling):
            path_origin  = node_origin.path + "/"
            depth_diff = node_origin.depth - node_sibling.depth
            new_path = f"{parent_sibling.path}/{node_origin.id}"
            descendents = node_origin.get_descendants 
            node_origin.path = new_path
            node_origin.depth = node_sibling.depth 

            children_parent_origin.filter(order__gt=node_origin.order).update(order=F('order') - 1)
            children_parent_sibling.filter(order__gte=node_sibling.order).update(order=F('order') + 1)
            node_origin.order = node_sibling.order
            # Change the path of children
            descendents.update(path = Replace('path', V(path_origin), V(new_path +"/")), depth = F('depth') - depth_diff)
            
            node_origin.save()

    def ajust_order_when_is_the_same_parent(self, node_origin, node_sibling, parent_origin, parent_sibling, children_parent_origin):
        if(parent_origin == parent_sibling):
            if(node_origin.order < node_sibling.order): 
                children_parent_origin.filter(order__gt=node_origin.order, order__lt=node_sibling.order).update(order=F('order') - 1)
                node_origin.order = node_sibling.order - 1

            if(node_origin.order > node_sibling.order):
                children_parent_origin.filter( order__gte=node_sibling.order, order__lt=node_origin.order).update(order=F('order') + 1)
                node_origin.order = node_sibling.order
            
            node_origin.save()
            
    def get_node_by_id(self, node_id):
        return self.get(id=node_id)
    
    def validate_move(self, node_origin, node_sibling):
        if node_sibling.path.startswith(f"{node_origin.path}/"):
            raise ValidationError("El menu no se puede mover debajo de algun hijo suyo")