from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase

class TestSetUp(APITestCase):
    
    def setUp(self):
        from apps.users.models import User
        faker = Faker()

        self.login_url = '/users/login/'
        self.user = User.objects.create_superuser(
            first_name='Developer',
            last_name='Backend',
            username='developer',
            password='developer',
            email= faker.email()
        )

        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password': 'developer'
            },
            format='json'
        )

        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return super().setUp()