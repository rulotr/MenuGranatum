from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
ERROR_PK_NOT_EXIST = "The module with the pk = {} doesnt exist"

class ModuleQuerySet(models.query.QuerySet):
    def find_by_pk(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist as ex:
            raise ValidationError(ERROR_PK_NOT_EXIST.format(pk)) from ex
        

class ModuleManager(models.Manager):
    def get_queryset(self):
        return ModuleQuerySet(self.model, using=self._db)
    
    def execute_create(self, name):
        module = self.model(name=name)
        module.full_clean()
        module.save()
        return module

    def execute_update(self, pk, name):
        module = self.get(pk=pk)
        module.name = name
        module.full_clean()
        module.save(update_fields=['name'])
        return module

    def execute_delete(self, pk):
        try:
            module = self.get(pk=pk)
        except self.model.DoesNotExist as e:
            raise self.model.DoesNotExist(f"Module pk={pk} doesn't exist") from e
        module.delete()


MyManager = ModuleManager.from_queryset(ModuleQuerySet)

class Module(models.Model):
    name = models.CharField(max_length=50,)

    class Meta:
        constraints = [ models.UniqueConstraint(
            fields=["name"], name="unique_name_module" 
        )]

    objects = MyManager()
         
    
    def clean(self):
        self.name = self.name.strip()
        if self.name == "":
            raise ValidationError({"name":"This field cannot be blank."})

        
    def __str__(self):
        return self.name