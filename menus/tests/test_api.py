from unittest import skip
import json
from django.urls import reverse
from rest_framework.test import APITestCase

from menus.models import Menu
from menugranatum.users.models import User

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
