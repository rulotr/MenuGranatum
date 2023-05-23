from django.test import TestCase
from .models import Module
from django.core.exceptions import ValidationError

#  Modulos

class ModuleModelTest(TestCase):

    def test_module_str(self):
        module = Module.objects.create(name="Module 1")
        self.assertEqual(str(module),"Module 1")

#TODO El nombre no puede tener espacios en blanco
    def test_name_with_space(self):
        module = Module(name="  Module 1  ")
        module.full_clean()
        module.save()
        self.assertEqual(module.name,"Module 1")
 

#TODO El nombre no puede ser vacio, debe tener una longitud de 1
    def test_module_name_empty(self):
        with self.assertRaises(ValidationError) as err:
            modules = Module(name="    ")
            modules.full_clean()
            modules.save()
        self.assertEqual(err.exception.message_dict["name"], ['This field cannot be blank.'])


#TODO Los modulos tienen nombre unicos

#TODO Se puede cambiar el nombre del modulo

#TODO Se puede eliminar un modulo dando su pk

#TODO Que pasa si se quiere modificar un modulo que no existe

#TODO Eliminar un id que no existe

#TODO Consultar modulo por id