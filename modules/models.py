from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Module(models.Model):
    name = models.CharField(max_length=50)

    def clean(self):
        self.name = self.name.strip()
        if self.name == "":
            raise ValidationError({"name":"This field cannot be blank."})

        
    def __str__(self):
        return self.name