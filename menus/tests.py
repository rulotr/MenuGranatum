from django.test import TestCase

from modules.models import Module
from menus.models import Menu
from my_utilities.fields import TrimpCharField

# Create your tests here.


class TestMenuOperations(TestCase):

    def test_name_field_type(self):
            field = Menu._meta.get_field('name')

            self.assertEqual(type(field), TrimpCharField)

    def test_menu_str(self):
        module1 = Module.objects.create(name="Module 1")
        menu1 = Menu.objects.create(name="Menu 1", module=module1)
        self.assertEqual(str(menu1),"Module 1 - Menu 1")

    def test_create_menu(self):
        module1 = Module.objects.create(name="Module 1")
        
        menu1 = Menu.objects.execute_create(
            name='  Menu 1  ', module=module1)

        self.assertEqual(menu1.name, 'Menu 1')
        self.assertEqual(menu1.module, module1)

        self.assertTrue(Menu.objects.count() == 1)    











    