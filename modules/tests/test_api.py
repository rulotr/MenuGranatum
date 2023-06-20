import json
from django.urls import reverse
from rest_framework.test import APITestCase

from menugranatum.users.models import User
from modules.models import Module


class ModuleAPITest(APITestCase):
    def setUp(self):
        self.base_url_list = reverse('modules:module-list')
        self.user = User.objects.create_user("admin," "admin@django.com", "pass123")

    def test_url_list(self):
        url_list = '/api/modules/'
    
        self.assertEqual(self.base_url_list, url_list)

    def base_url_details(self, pk):
        return reverse('modules:module-details', kwargs={'pk': pk})
    
    def test_url_detail(self):
        url_detail_exp = '/api/modules/2/'
        url_detail = self.base_url_details(2)

        self.assertEqual(url_detail, url_detail_exp)

    def test_list_modules(self):
        self.client.force_login(user=self.user)
        module1 = Module.objects.create(name='Module 1')
        module2 = Module.objects.create(name='Module 2')

        modules_expected = [{'id':module1.id, 'name': 'Module 1'},
                            {'id': module2.id, 'name': 'Module 2'}]
        
        response = self.client.get(self.base_url_list)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.data),2)
        self.assertEqual(response.data, modules_expected)

    def test_post_module(self):
        self.client.force_login(user=self.user)
    
        new_module = {'name': '  New Module  '}
        response = self.client.post(self.base_url_list, new_module)
        result = json.loads(response.content)
        del result['id']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result, {'name': 'New Module'})
        self.assertEqual(Module.objects.count(), 1)

    def test_post_invalid_module(self):
        self.client.force_login(user=self.user)
    
        new_module = {'name':'   '}
        response = self.client.post(self.base_url_list, new_module)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result,  {'name': ['This field may not be blank.']})

    def test_post_module_exists(self):
        self.client.force_login(user=self.user)
        Module.objects.create(name="Module 1")
        new_module = {'name':'  Module 1 '}

        response = self.client.post(self.base_url_list, new_module)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result,  {'name': ['Module with this Name already exists.']})

    def test_get_single_module(self):
        self.client.force_login(user=self.user)
        module1 = Module.objects.create(name='Module 11')
        module2 = Module.objects.create(name='Module 12')

        modules_expected = {'id': module1.id, 'name': 'Module 11'}
        
        response = self.client.get(self.base_url_details(pk=module1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.data, modules_expected)

    def test_not_exists_single_module(self):
        self.client.force_login(user=self.user)
      
        response = self.client.get(self.base_url_details(pk=1))
        self.assertEqual(response.status_code, 404)

    def test_put_module(self):
        self.client.force_login(user=self.user)
        new_module = Module.objects.create(name='Module 2')
        update_module = {'name': 'Module 1'}

        response = self.client.put(
            self.base_url_details(pk=new_module.pk), update_module)
        module = Module.objects.all().first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(module.name, 'Module 1')

    def test_delete_module(self):
        self.client.force_login(user=self.user)
        module1 = Module.objects.create(name='Module 1')

        base_url = self.base_url_details(pk=module1.pk)
        response = self.client.delete(base_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Module.objects.all().count(), 0)

    def test_delete_module_doesnt_exist(self):
        self.client.force_login(user=self.user)

        base_url = self.base_url_details(pk=1)
        response = self.client.delete(base_url)
        self.assertEqual(response.status_code, 404)
