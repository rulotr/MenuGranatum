from unittest import skip
import json
from django.urls import reverse
from rest_framework.test import APITestCase

from menus.models import Menu
from menugranatum.users.models import User

def create_simple_menu_four_levels_for_test():    
    Menu.objects.create(id=1, name="Module 1", path='/1',   depth=1,  order=1)
    Menu.objects.create(id=2, name="..Menu 1.1", path='/1/2',  depth=2, order=1)
    Menu.objects.create(id=3, name="..Menu 1.2", path='/1/3',  depth=2, order=2)
    Menu.objects.create(id=4, name="..Menu 1.3", path='/1/4',  depth=2, order=3)
    Menu.objects.create(id=5, name="....Menu 1.3.1", path='/1/4/5',  depth=3, order=1)
    Menu.objects.create(id=6, name="....Menu 1.3.2", path='/1/4/6',  depth=3, order=2)
    Menu.objects.create(id=7, name="....Menu 1.3.2.1", path='/1/4/6/7',  depth=4, order=1)
    Menu.objects.create(id=8, name="Module 2", path='/8',   depth=1,  order=2)
    Menu.objects.create(id=9, name="..Menu 2.1", path='/8/9',  depth=2, order=1)
    

class ModuleAPITestCase(APITestCase):
    def setUp(self):
        self.base_url_list = reverse('menus:module-list')
        self.user = User.objects.create_user("admin," "admin@django.com", "pass123")

    def test_url_list(self):
        url_list = '/api/modules/'
        self.assertEqual(url_list, self.base_url_list)

    def base_url_details(self, pk):
        return reverse('menus:module-detail', kwargs={'pk': pk})


    def test_url_detail(self):
        url_detail_expected = '/api/modules/2/'
        url_detail = self.base_url_details(2)

        self.assertEqual(url_detail, url_detail_expected)

    def test_list_modules(self):
        self.client.force_login(user = self.user)
        Menu.objects.create(id=1, name="Module 1", path='/1',   depth=1,  order=1)
        Menu.objects.create(id=2, name="Module 2", path='/2',   depth=1,  order=2)

        modules_expected = [{'id':1, 'name': 'Module 1', 'path': '/1', 'depth': 1, 'order': 1},
                            {'id':2, 'name': 'Module 2', 'path': '/2', 'depth': 1, 'order': 2}]
        
        response = self.client.get(self.base_url_list)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.data),2)
        self.assertEqual(response.data, modules_expected)
    
    def test_post_module_with_id(self):
        self.client.force_login(user = self.user)
        data = {'id':4, 'name': 'Module 4'}
        response = self.client.post(self.base_url_list, data, format='json')
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(result, {'id': 4, 'name': 'Module 4', 'path': '/4', 'depth': 1, 'order': 1})


    def test_post_module_without_id(self):  
        self.client.force_login(user = self.user)      
        data = {'name': 'Module 1'}
        response = self.client.post(self.base_url_list, data, format='json')
        result = json.loads(response.content)
        id_result = result.get('id')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(result, {'id':id_result, 'name': 'Module 1', 'path': f'/{id_result}', 'depth': 1, 'order': 1})

    def test_post_invalid_module(self):
        self.client.force_login(user = self.user)
        data = {'name': '     '}
        response = self.client.post(self.base_url_list, data, format='json')
        result = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(result, {'name': ['This field may not be blank.']})
        self.assertEqual(Menu.objects.count(), 0)

    def test_get_module_tree(self):
        self.client.force_login(user=self.user)
        create_simple_menu_four_levels_for_test()

        expected = [ { "id": 1, "name":"Module 1", "path": "/1", "depth": 1, "order": 1},
                 { "id": 2, "name":"..Menu 1.1", "path": "/1/2", "depth": 2, "order": 1},
                 { "id": 3, "name":"..Menu 1.2", "path": "/1/3", "depth": 2, "order": 2},
                 { "id": 4, "name":"..Menu 1.3", "path": "/1/4", "depth": 2, "order": 3},
                 { "id": 5, "name":"....Menu 1.3.1", "path": "/1/4/5", "depth": 3, "order": 1},
                 { "id": 6, "name":"....Menu 1.3.2", "path": "/1/4/6", "depth": 3, "order": 2},
                 { "id": 7, "name":"....Menu 1.3.2.1", "path": "/1/4/6/7", "depth": 4, "order": 1},
                ]

        response = self.client.get(self.base_url_details(pk=1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, expected)