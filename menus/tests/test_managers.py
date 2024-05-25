
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

    def test_create_module_whith_no_id(self):
        module1 = Menu.objects.execute_create(name=" Module 1 ")
        expected_module_path = f"/{module1.id}"

        self.assertEqual(module1.name, "Module 1")
        self.assertEqual(module1.path, expected_module_path)
        self.assertEqual(Menu.objects.count(), 1)

    def test_create_module(self):
        module1 = Menu.objects.execute_create(name=" Module 1 ", id=1)
        expected_module_path = "/1"

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
        module1 = Menu.objects.create(name="Module 1", id=1)
        module1.path = "/1" 
        module1.save()
      
        menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=module1.id, id=2)
        expected_path = "/1/2"

        self.assertEqual(menu1.name, "Menu 1")
        self.assertEqual(menu1.path, expected_path)

    def test_create_menu_submenu(self):
        module1 = Menu.objects.create(name="Module 1", id=1)
        module1.path = "/1"
        module1.save()
      
        menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=module1.id, id=2)
        menu2 = Menu.objects.execute_create(name=" Menu 1.2", parent_id=menu1.id, id=3)

        expected_path = "/1/2/3"

        self.assertEqual(menu2.name, "Menu 1.2")
        self.assertEqual(menu2.path, expected_path)

    def test_create_two_menus_same_module(self):
        module1 = Menu.objects.create(name="Module 1", id=1)
        module1.path = "/1"
        module1.save()
      
        menu1 = Menu.objects.execute_create(name=" Menu 1 ",parent_id=module1.id, id=2)
        menu2 = Menu.objects.execute_create(name=" Menu 2", parent_id=module1.id, id=3)

        expected_path_menu1 = "/1/2"
        expected_path_menu2 = "/1/3"

        self.assertEqual(menu1.path, expected_path_menu1)
        self.assertEqual(menu2.path, expected_path_menu2)


    def test_create_menu_with_parent_not_exist(self):
        with self.assertRaisesMessage(ValidationError, "El nodo padre no existe"):
            menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=1)
        
        self.assertEqual(Menu.objects.count(), 0)
      
    def test_menu_depth(self):
        module1 = Menu.objects.execute_create(name=" Module 1 ",  id=1)
        menu1 = Menu.objects.execute_create(name=" Menu 1 ", parent_id=module1.id, id=2)
        menu2 = Menu.objects.execute_create(name=" Menu 1.2", parent_id=menu1.id, id=3)

        self.assertEqual(module1.depth, 1)
        self.assertEqual(menu1.depth, 2)
        self.assertEqual(menu2.depth, 3)


class TestMenuQueries(TestCase):

    def test_get_childrens(self):
        module1 = Menu.objects.create(name="Module 1", id=1, path='/1', depth=1)
        module2 = Menu.objects.create(name="Module 2", id=2, path='/2', depth=1)

        module3 = Menu.objects.create(name="Module 2", id=11, path='/11', depth=1)

        menu1 = Menu.objects.create(name="Menu 1.1", id=3, path='/1/3', depth=2)
        menu2 = Menu.objects.create(name="Menu 1.2", id=4, path='/1/4', depth=2)
        
        menu3 = Menu.objects.create(name="Menu 2.1",   id=5, path='/2/5', depth=2)
        menu4 = Menu.objects.create(name="Menu 2.1.1", id=6, path='/2/5/6', depth=3)
        # try that /1 is different from /11
        menu5 = Menu.objects.create(name="Menu 11.1",   id=7, path='/11/7', depth=2)
        
        m1_childrens = Menu.objects.get_children(node=module1)
        m2_childrens = Menu.objects.get_children(node=module2)
        m3_childrens = Menu.objects.get_children(node=menu3)

        self.assertEqual(m1_childrens[0].name, "Menu 1.1")
        self.assertEqual(m1_childrens[1].name, "Menu 1.2")
        self.assertEqual(len(m1_childrens), 2)
    
        self.assertEqual(m2_childrens[0].name, "Menu 2.1")
        self.assertEqual(len(m2_childrens), 1)

        self.assertEqual(m3_childrens[0].name, "Menu 2.1.1")
        self.assertEqual(len(m3_childrens), 1)

    def test_next_order_num_modules(self):
        Menu.objects.create(name=" Module 1 ", order=2, depth=1,  id=1)
        
        module2 = Menu.objects.execute_create(name=" Module 2 ",  id=2)
        
        self.assertEqual(module2.order, 3)

    def test_next_order_num_menu(self):
        module1 = Menu.objects.create(name=" Module 1 ", path='/1', depth=1,  id=1, order=1)
        menu1 = Menu.objects.create(name="Menu 1.1", id=3, path='/1/3', depth=2, order=1)
        menu2 = Menu.objects.create(name="Menu 1.2", id=4, path='/1/4', depth=2, order=3)
        menu3 = Menu.objects.create(name="Menu 1.1.1",   id=5, path='/1/3/5', depth=3,  order=1)
        # try that /1 is different from /11
        module11 = Menu.objects.create(name=" Module 11 ", path='/11', depth=1,  id=6, order=1)
        menu4 = Menu.objects.create(name="Menu 11.1",   id=7, path='/11/7', depth=2,  order=5 )
       
        menu5 = Menu.objects.execute_create(name="Menu 1.2.3", parent_id=module1.id, id=8)
        menu6 = Menu.objects.execute_create(name="Menu 1.1.1.1", parent_id=menu3.id, id=9)
        
        self.assertEqual(menu5.order, 4)
        self.assertEqual(menu6.order, 1)

