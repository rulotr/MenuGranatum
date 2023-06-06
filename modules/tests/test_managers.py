

from django.test import TestCase
from django.core.exceptions import ValidationError

from modules.models import Module

class TestModuleOperations(TestCase):

    def test_module_str(self):
        module = Module.objects.create(name="Module 1")
        self.assertEqual(str(module),"Module 1")

    def test_create_module_with_spaces(self):
        module1 = Module.objects.execute_create(name="  Module 1  ")

        self.assertEqual(module1.name, 'Module 1')
        self.assertTrue(Module.objects.count() == 1)

    def test_create_module_empty(self):
        with self.assertRaisesMessage(ValidationError, "This field cannot be blank."):
            Module.objects.execute_create(name="     ")

    #TODO Los modulos tienen nombre unicos
    def test_module_name_must_be_unique(self):
        Module.objects.create(name="Module 1")

        with self.assertRaises(ValidationError) as err:
            Module.objects.execute_create(name="Module 1")
        self.assertEqual(err.exception.messages[0],'Module with this Name already exists.')
        
        
    #TODO Se puede cambiar el nombre del modulo
    def test_update_module_name(self):
        module1 = Module.objects.create(name="Module 2")

        module_update = Module.objects.execute_update(module1.id, "Module 1")

        self.assertEqual(module_update.id, module1.id)
        self.assertEqual(module_update.name, "Module 1")

    #TODO Se puede eliminar un modulo dando su pk
    def test_delete_module_by_id(self):
        module1 = Module.objects.create(name="Module 1")

        Module.objects.execute_delete(pk=module1.pk)

        self.assertTrue(Module.objects.count() == 0)

    #TODO Eliminar un id que no existe
    def test_delete_module_not_exist(self):
        with self.assertRaisesMessage(Module.DoesNotExist, "Module pk=1 doesn't exist"):
            Module.objects.execute_delete(pk=1)


class TestModuleQueries(TestCase):
    #TODO Consultar modulo por id
    def test_find_by_pk(self):
        module1 = Module.objects.create(name="Module 1")

        new_module = Module.objects.find_by_pk(pk=module1.pk)

        self.assertEqual(module1, new_module)

    #TODO Consultar modulo que no existe
    def test_find_by_pk_doesnotexist(self):
        with self.assertRaisesMessage(ValidationError, "The module with the pk = 1 doesnt exist"):
            Module.objects.find_by_pk(pk=1)






