
from unittest import skip
from django.test import TestCase

from django.core.exceptions import ValidationError

from menus.models import Menu

def get_list_for_test():
    return [{"id": o.id, "path": o.path, "depth":  o.depth, "order": o.order} 
                for o in Menu.objects.all().order_by("depth", "order", "id")]



def create_simple_menu_for_test():
    Menu.objects.create(id=1, name="Module 1   ", path='/1',   depth=1,  order=1)
    Menu.objects.create(id=2, name="..Menu 1.1   ", path='/1/2',  depth=2, order=1)
    Menu.objects.create(id=3, name="..Menu 1.2   ", path='/1/3',  depth=2, order=2)
    Menu.objects.create(id=4, name="..Menu 1.3   ", path='/1/4',  depth=2, order=3)

    expected = [{"id": 1,  "path": "/1", "depth": 1, "order": 1},
                {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                {"id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},]

def create_simple_menu_four_levels_for_test():    
    Menu.objects.create(id=1, name="Module 1   ", path='/1',   depth=1,  order=1)
    Menu.objects.create(id=2, name="..Menu 1.1   ", path='/1/2',  depth=2, order=1)
    Menu.objects.create(id=3, name="..Menu 1.2   ", path='/1/3',  depth=2, order=2)
    Menu.objects.create(id=4, name="..Menu 1.3   ", path='/1/4',  depth=2, order=3)
    Menu.objects.create(id=5, name="..Menu 1.3.1   ", path='/1/4/5',  depth=3, order=1)
    Menu.objects.create(id=6, name="..Menu 1.3.2   ", path='/1/4/6',  depth=3, order=2)
    Menu.objects.create(id=7, name="..Menu 1.3.2.1   ", path='/1/4/6/7',  depth=4, order=1)
    
    expected = [ { "id": 1,  "path": "/1", "depth": 1, "order": 1},
                 { "id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                 { "id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                 { "id": 4,  "path": "/1/4", "depth": 2, "order": 3},
                 { "id": 5,  "path": "/1/4/5", "depth": 3, "order": 1},
                 { "id": 6,  "path": "/1/4/6", "depth": 3, "order": 2},
                 { "id": 7,  "path": "/1/4/6/7", "depth": 4, "order": 1},]

    return expected
                
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

    def test_get_parent(self):
        Menu.objects.create(id=1, name="Module 1   ", path='/1',   depth=1,  order=1)
        Menu.objects.create(id=2, name="..Menu 1.1   ", path='/1/2',  depth=2, order=1)
        Menu.objects.create(id=3, name="....Menu 1.1.1 ", path='/1/2/3', depth=3,order=1)
        Menu.objects.create(id=4, name="..Menu 1.2   ", path='/1/4',  depth=2, order=3)
     
        module1 = Menu.objects.get(id=1)
        menu1 = Menu.objects.get(id=2)
        menu2 = Menu.objects.get(id=3)

        parent1 = module1.get_parent
        parent2 = menu1.get_parent
        parent3 = menu2.get_parent 

        self.assertEqual(parent1, None)
        self.assertEqual(parent2.id, 1)  
        self.assertEqual(parent3.id, 2)      

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
        
        m1_childrens = module1.get_children
        m2_childrens = module2.get_children
        m3_childrens = menu3.get_children

        self.assertEqual(m1_childrens[0].name, "Menu 1.1")
        self.assertEqual(m1_childrens[1].name, "Menu 1.2")
        self.assertEqual(len(m1_childrens), 2)
    
        self.assertEqual(m2_childrens[0].name, "Menu 2.1")
        self.assertEqual(len(m2_childrens), 1)

        self.assertEqual(m3_childrens[0].name, "Menu 2.1.1")
        self.assertEqual(len(m3_childrens), 1)


    

    def test_get_descendants(self):
            create_simple_menu_four_levels_for_test()
            menu1 = Menu.objects.get(id=4)
            descendants = menu1.get_descendants
            
            self.assertEqual(descendants[0].path, "/1/4/5")
            self.assertEqual(descendants[1].path, "/1/4/6")
            self.assertEqual(descendants[2].path, "/1/4/6/7")
            self.assertEqual(len(descendants), 3)
            


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

    def test_next_order_num_modules(self):
        Menu.objects.create(id=1, name=" Module 1 ", depth=1, order=2)
        
        module2 = Menu.objects.execute_create(name=" Module 2 ",  id=2)
        
        self.assertEqual(module2.order, 3)

    def test_next_order_num_menu_creation(self):
        
        Menu.objects.create(id=1, name="Module 1   ", path='/1',   depth=1,  order=1)
        Menu.objects.create(id=2, name="..Menu 1.1   ", path='/1/2',  depth=2, order=1)
        Menu.objects.create(id=3, name="....Menu 1.1.1 ", path='/1/2/3', depth=3,order=1)
        Menu.objects.create(id=4, name="..Menu 1.2   ", path='/1/4',  depth=2, order=3)
        # try that /1 is different from /11 in the query path__startswith
        Menu.objects.create(id=11, name="Module 11  ", path='/11', depth=1, order=1)
        Menu.objects.create(id=12, name="..Menu 11.1  ", path='/11/6', depth=2,  order=5 )
        

        menu7 = Menu.objects.execute_create(id=7, name="Menu 1.3", parent_id=1)
        menu8 = Menu.objects.execute_create(id=8, name="Menu 1.1.1.1", parent_id=3)
        
        self.assertEqual(menu7.order, 4)
        self.assertEqual(menu8.order, 1)

    @skip
    def test_create_list_fot_test(self):
        create_simple_menu_for_test()
        
        expected = [{"id": 1,  "path": "/1", "depth": 1, "order": 1},
                    {"id": 5,  "path": "/5", "depth": 1, "order": 2},
                     
                    {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                    {"id": 6,  "path": "/5/6", "depth": 2, "order": 1},
                   
                    {"id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                    {"id": 7,  "path": "/5/7", "depth": 2, "order": 2},
                    
                    {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},
                    {"id": 8,  "path": "/5/8", "depth": 2, "order": 3},
                    
                    {"id": 9,  "path": "/5/8/9", "depth": 3, "order": 1},
                    {"id": 10,  "path": "/5/8/10", "depth": 3, "order": 2},
            ]

        complete_menu_list = get_list_for_test()

        self.assertEqual(complete_menu_list, expected)


    def test_change_order_module_up(self):
        create_simple_menu_for_test()
        Menu.objects.create(id=5, path="/5", name="Module 2 ", depth=1, order=2)                            
        Menu.objects.move_before_sibling(5, 1)

        expected = [ {"id": 5,  "path": "/5", "depth": 1, "order": 1},
                {"id": 1,  "path": "/1", "depth": 1, "order": 2},
                {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                {"id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},]

        
        complete_menu_list = get_list_for_test()
        self.assertEqual(complete_menu_list, expected)

    def test_change_order_module_down(self):
        create_simple_menu_for_test()
        Menu.objects.create(id=5, path="/5", name="Module 2 ", depth=1, order=2)                            
        Menu.objects.move_before_sibling(1, 5)

        expected = [ {"id": 1,  "path": "/1", "depth": 1, "order": 1},
                {"id": 5,  "path": "/5", "depth": 1, "order": 2},
                {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                {"id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},]

        
        complete_menu_list = get_list_for_test()
        self.assertEqual(complete_menu_list, expected)


    
    def test_move_before_first_sibling_same_parent(self):
        create_simple_menu_for_test()
        Menu.objects.move_before_sibling(4, 2)

        expected = [{"id": 1,  "path": "/1", "depth": 1, "order": 1},
                    {"id": 4,  "path": "/1/4", "depth": 2, "order": 1},
                    {"id": 2,  "path": "/1/2", "depth": 2, "order": 2},
                    {"id": 3,  "path": "/1/3", "depth": 2, "order": 3},
                ]
        
        complete_menu_list = get_list_for_test()
        self.assertEqual(complete_menu_list, expected)

    def test_move_before_last_sibling_same_parent(self):
        create_simple_menu_for_test()
        Menu.objects.move_before_sibling(2, 4)

        expected = [{"id": 1,  "path": "/1", "depth": 1, "order": 1},
                    {"id": 3,  "path": "/1/3", "depth": 2, "order": 1},
                    {"id": 2,  "path": "/1/2", "depth": 2, "order": 2},
                    {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},      
                ]
        
        complete_menu_list = get_list_for_test()
        self.assertEqual(complete_menu_list, expected)

    def test_move_before_middle_sibling_same_parent(self):
        create_simple_menu_for_test()
        Menu.objects.move_before_sibling(4, 3)

        expected = [{"id": 1,  "path": "/1", "depth": 1, "order": 1},
                    {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                    {"id": 4,  "path": "/1/4", "depth": 2, "order": 2},   
                    {"id": 3,  "path": "/1/3", "depth": 2, "order": 3},                 
                ]
        
        complete_menu_list = get_list_for_test()
        self.assertEqual(complete_menu_list, expected)
        # Si se mueve a su nodo padre no se hace nada

    def test_move_before_its_parent_dont_should_move(self):
        create_simple_menu_for_test()
        Menu.objects.move_before_sibling(3, 1)

        expected = [{"id": 1,  "path": "/1", "depth": 1, "order": 1},
                    {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                    {"id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                    {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},      
                ]
        
        complete_menu_list = get_list_for_test()
        self.assertEqual(complete_menu_list, expected)

    def test_move_before_first_sibling_different_parent(self):
            create_simple_menu_four_levels_for_test()
            
            Menu.objects.move_before_sibling(7, 5)

            expected = [{ "id": 1,  "path": "/1", "depth": 1, "order": 1},
                {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                {"id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},
                {"id": 7,  "path": "/1/4/7", "depth": 3, "order": 1},
                {"id": 5,  "path": "/1/4/5", "depth": 3, "order": 2},
                {"id": 6,  "path": "/1/4/6", "depth": 3, "order": 3},
               ]
            
            complete_menu_list = get_list_for_test()
            self.assertEqual(complete_menu_list, expected)

    def test_move_before_last_sibling_different_parent(self):
            create_simple_menu_four_levels_for_test()
            
            Menu.objects.move_before_sibling(7, 6)

            expected = [{ "id": 1,  "path": "/1", "depth": 1, "order": 1},
                {"id": 2,  "path": "/1/2", "depth": 2, "order": 1},
                {"id": 3,  "path": "/1/3", "depth": 2, "order": 2},
                {"id": 4,  "path": "/1/4", "depth": 2, "order": 3},
                {"id": 5,  "path": "/1/4/5", "depth": 3, "order": 1},
                {"id": 7,  "path": "/1/4/7", "depth": 3, "order": 2},
                {"id": 6,  "path": "/1/4/6", "depth": 3, "order": 3},
               ]
            
            complete_menu_list = get_list_for_test()
            self.assertEqual(complete_menu_list, expected)

    def test_move_last_node_before_first_node_different_parent(self):
            create_simple_menu_four_levels_for_test()
            
            Menu.objects.move_before_sibling(7, 2)

            expected = [{ "id": 1,  "path": "/1", "depth": 1, "order": 1},
                {"id": 7,  "path": "/1/7", "depth": 2, "order": 1},   
                {"id": 2,  "path": "/1/2", "depth": 2, "order": 2},
                {"id": 3,  "path": "/1/3", "depth": 2, "order": 3},
                {"id": 4,  "path": "/1/4", "depth": 2, "order": 4},
                {"id": 5,  "path": "/1/4/5", "depth": 3, "order": 1},                
                {"id": 6,  "path": "/1/4/6", "depth": 3, "order": 2},
               ]
            
            complete_menu_list = get_list_for_test()
            self.assertEqual(complete_menu_list, expected)

    def test_move_first_node_before_last_node_different_parent(self):
            create_simple_menu_four_levels_for_test()
            
            Menu.objects.move_before_sibling(2, 7)

            expected = [{ "id": 1,  "path": "/1", "depth": 1, "order": 1},
                {"id": 3,  "path": "/1/3", "depth": 2, "order": 1},
                {"id": 4,  "path": "/1/4", "depth": 2, "order": 2},
                {"id": 5,  "path": "/1/4/5", "depth": 3, "order": 1},                
                {"id": 6,  "path": "/1/4/6", "depth": 3, "order": 2},
                {"id": 2,  "path": "/1/4/6/2", "depth": 4, "order": 1},
                {"id": 7,  "path": "/1/4/6/7", "depth": 4, "order": 2},            
               ]
            
            complete_menu_list = get_list_for_test()
            self.assertEqual(complete_menu_list, expected)

    def test_move_node_with_children_before_first_sibling_different_parent(self):
            create_simple_menu_four_levels_for_test()
            
            Menu.objects.move_before_sibling(6, 2)
            
            expected = [ { "id": 1,  "path": "/1", "depth": 1, "order": 1},
                 { "id": 6,  "path": "/1/6", "depth": 2, "order": 1},
                 { "id": 2,  "path": "/1/2", "depth": 2, "order": 2},
                 { "id": 3,  "path": "/1/3", "depth": 2, "order": 3},
                 { "id": 4,  "path": "/1/4", "depth": 2, "order": 4},
                 { "id": 5,  "path": "/1/4/5", "depth": 3, "order": 1},
                 { "id": 7,  "path": "/1/6/7", "depth": 3, "order": 1},]


            complete_menu_list = get_list_for_test()
            self.assertEqual(complete_menu_list, expected)

    def test_move_node_with_children_before_last_sibling_different_parent(self):
            create_simple_menu_four_levels_for_test()

            Menu.objects.create(id=8, name="..Menu 1.2.1   ", path='/1/2/8',  depth=3, order=1)

            Menu.objects.move_before_sibling(2, 7)
            
            expected = [ { "id": 1,  "path": "/1", "depth": 1, "order": 1},
                 { "id": 3,  "path": "/1/3", "depth": 2, "order": 1},
                 { "id": 4,  "path": "/1/4", "depth": 2, "order": 2},
                 { "id": 5,  "path": "/1/4/5", "depth": 3, "order": 1},
                 { "id": 6,  "path": "/1/4/6", "depth": 3, "order": 2},
                 { "id": 2,  "path": "/1/4/6/2", "depth": 4, "order": 1},
                 { "id": 7,  "path": "/1/4/6/7", "depth": 4, "order": 2},
                 { "id": 8,  "path": "/1/4/6/2/8", "depth": 5, "order": 1},
              ]


            complete_menu_list = get_list_for_test()
            self.assertEqual(complete_menu_list, expected)


class TestMenuQueries(TestCase):
    def test_get_all_modules(self):
        module1 = Menu.objects.create(name="Module 1", id=1, path='/1', depth=1)
        module2 = Menu.objects.create(name="Module 2", id=2, path='/2', depth=1)
        menu1 = Menu.objects.create(name="Menu 1.1", id=3, path='/1/3', depth=2)
        
        modules = Menu.objects.get_all_modules()

        self.assertEqual(modules[0].name, "Module 1")
        self.assertEqual(modules[1].name, "Module 2")
        self.assertEqual(len(modules), 2)

    def test_get_last_num_order_modules(self):
        module1 = Menu.objects.create(name="Module 1", id=1, path='/1', depth=1, order=1)
        module2 = Menu.objects.create(name="Module 2", id=2, path='/2', depth=1, order=2)
        menu1 = Menu.objects.create(name="Menu 1.1", id=3, path='/1/3', depth=2, order=1)
        
        next_num_order = Menu.objects.get_next_num_order_module()

        self.assertEqual(next_num_order, 3)

            

  

