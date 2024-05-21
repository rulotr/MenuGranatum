
from django.test import TestCase
from django.core.exceptions import ValidationError

from menus.models import Menu


class TestMenuModel(TestCase):
    def test_menu_str(self):
        menu = Menu.objects.create(name="Menu 1")
        self.assertEqual(str(menu), "Menu 1")
    
    def test_menu_with_spaces(self):
        menu = Menu(name=" Menu 1  ")
        menu.clean()
        self.assertEqual(menu.name, "Menu 1")

    def test_menu_with_spaces(self):
        with self.assertRaisesMessage(ValidationError, "El nombre no puede estar vacío"):
            menu = Menu(name="   ")
            menu.clean()
            menu.save()

class TestModuleOperations(TestCase):
    
    def test_create_module(self):
        module1 = Menu.objects.execute_create(name=" Module 1 ")
        expected_module_path = f"/{module1.id}"

        self.assertEqual(module1.name, "Module 1")
        self.assertEqual(module1.path, expected_module_path)
        self.assertEqual(Menu.objects.count(), 1)

    def test_create_module_empty(self):
        with self.assertRaisesMessage(ValidationError, "El nombre no puede estar vacío"):
            Menu.objects.execute_create(name="     ")

class TestMeuOperations(TestCase):
    
    def test_create_menu(self):
        module1 = Menu.objects.create(name="Module 1")
        module1.path = "/" + str(module1.id)
        module_path = f"/{module1.id}"
      
        menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=module1.id)
        expected_path = f"{module_path}/{menu1.id}"

        self.assertEqual(menu1.name, "Menu 1")
        self.assertEqual(menu1.path, expected_path)
