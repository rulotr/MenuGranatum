from django.urls import reverse
from rest_framework.test import APITestCase

class ModuleAPITestCase(APITestCase):
    def setUp(self):
        self.base_url_list = reverse('menus:module-list')

    def test_url_list(self):
        url_list = '/api/modules/'
        self.assertEqual(url_list, self.base_url_list)

    def base_url_details(self, pk):
        return reverse('menus:module-detail', kwargs={'pk': pk})


    def test_url_detail(self):
        url_detail_expected = '/api/modules/2/'
        url_detail = self.base_url_details(2)

        self.assertEqual(url_detail, url_detail_expected)
