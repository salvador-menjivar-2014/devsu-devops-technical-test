import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User

class TestUserView(APITestCase):
    def setUp(self):
        user = User(name='Test1', dni='09876543210')
        user.save()
        self.url = reverse("users-list")
        self.data = {'name': 'Test2', 'dni': '09876543211'}

    def test_post(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
    #Verificamos que ahora hay 2 usuarios en la base de datos (el de setUp y el nuevo).
        self.assertEqual(User.objects.count(), 2)

    #Convertimos la respuesta JSON en un diccionario de Python.
        response_data = json.loads(response.content)

    #Eliminamos la clave 'id' del diccionario de respuesta.
    #No importa qué valor tenga, solo que exista.
        self.assertIn('id', response_data)
        del response_data['id'] 

    #Comparamos el resto de los datos de la respuesta con los datos que enviamos.
        self.assertEqual(response_data, self.data)

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get(self):
        response = self.client.get(self.url + '1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"id": 1, "name":"Test1", "dni":"09876543210"})