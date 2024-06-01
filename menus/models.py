from django.db import models
from django.db.models.functions import Coalesce, Replace
from django.db.models import Max, F, Value as V

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

   
    def _get_parent_id_from_path(self):
        parents_id = self.path.split('/')[-2]

        if parents_id == '' :
            return None

        return int(parents_id)
    
    @property
    def get_parent(self):
        parent_id = self._get_parent_id_from_path()
        if(parent_id is None):
            return None
        return Menu.objects.get(id=parent_id)         

    @property
    def get_children(self):
        return Menu.objects.filter(path__startswith=self.path + '/', depth=self.depth+1
                           ).exclude(path=self.path)
    
    @property
    def get_descendants(self):
        descendants = Menu.objects.filter(path__startswith=self.path + '/'
                           ).exclude(path=self.path)
        
        return descendants
    
    @property
    def get_next_num_order_children(self):        
        max_num_order = self.get_children.aggregate(
                num=Coalesce(Max("order"), 0))['num'] 
        
        return max_num_order + 1
    
    objects = MyManager()
