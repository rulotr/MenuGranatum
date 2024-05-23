
from unittest import skip
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
        module1 = Menu.objects.execute_create(name=" Module 1 ", id=1)
        expected_module_path = f"/1"

        self.assertEqual(module1.name, "Module 1")
        self.assertEqual(module1.path, expected_module_path)
        self.assertEqual(Menu.objects.count(), 1)

    def test_create_module_empty(self):
        with self.assertRaisesMessage(ValidationError, "El nombre no puede estar vacío"):
            Menu.objects.execute_create(name="     ")

    @skip("Not implemented yet")
    def test_create_module_with_order(self):
        module1 = Menu.objects.execute_create(name=" Module 1 ")
        module2 = Menu.objects.execute_create(name=" Module 1 ")
                
        self.assertEqual(module1.order, 1)
        self.assertEqual(module2.order, 2)


class TestMeuOperations(TestCase):
    
    def test_create_menu(self):
        module1 = Menu.objects.create(name="Module 1",)
        module1.path = "/" + str(module1.id)
        module1.save()
      
        menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=module1.id)
        expected_path = f"/{module1.id}/{menu1.id}"

        self.assertEqual(menu1.name, "Menu 1")
        self.assertEqual(menu1.path, expected_path)

    def test_create_menu_submenu(self):
        module1 = Menu.objects.create(name="Module 1")
        module1.path = "/" + str(module1.id)
        module1.save()
      
        menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=module1.id)
        menu2 = Menu.objects.execute_create(name=" Menu 1.2", parent_id=menu1.id)

        expected_path = f"/{module1.id}/{menu1.id}/{menu2.id}"

        self.assertEqual(menu2.name, "Menu 1.2")
        self.assertEqual(menu2.path, expected_path)

    def test_create_two_menus_same_module(self):
        module1 = Menu.objects.create(name="Module 1")
        module1.path = "/" + str(module1.id)
        module1.save()
      
        menu1 = Menu.objects.execute_create(name=" Menu 1 ",parent_id=module1.id)
        menu2 = Menu.objects.execute_create(name=" Menu 2", parent_id=module1.id)

        expected_path_menu1 = f"/{module1.id}/{menu1.id}"
        expected_path_menu2 = f"/{module1.id}/{menu2.id}"

        self.assertEqual(menu1.path, expected_path_menu1)
        self.assertEqual(menu2.path, expected_path_menu2)


    def test_create_menu_with_parent_not_exist(self):
        with self.assertRaisesMessage(ValidationError, "El nodo padre no existe"):
            menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=1)
        
        self.assertEqual(Menu.objects.count(), 0)
      
@skip("Not implemented yet")
class TestMenuQueries(TestCase):
    def test_get_childrens(self):
        module1 = Menu.objects.create(name="Module 1", id=1)
        module1.path = "/" + str(module1.id)
        module1.save()

        module2 = Menu.objects.create(name="Module 2")
        module2.path = "/" + str(module1.id)
        module2.save()
    
        menu1 = Menu.objects.execute_create(name=" Menu 1.1", parent_id=module1.id)
        menu2 = Menu.objects.execute_create(name=" Menu 1.2", parent_id=module1.id)
        
        menu3 = Menu.objects.execute_create(name=" Menu 2.1", parent_id=module2.id)

    

        childrens = menu1.get_childrens()

        self.assertEqual(len(childrens), 2)
        self.assertEqual(childrens[0].name, "Menu 1.2")
        self.assertEqual(childrens[1].name, "Menu 1.3")
        menu = Menu.objects.execute_create(name="Menu 1")
        menu = Menu.objects.get(id=menu.id)
        self.assertEqual(menu.name, "Menu 1")
