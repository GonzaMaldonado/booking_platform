from rest_framework import status

from apps.bookings.models import Hotel

from .test_setup import TestSetUp
from .factories.hotel import HotelFactory


class HotelTestCase(TestSetUp):
    url = "/hotel"
    
    def test_get_hotels(self):
        hotel = HotelFactory().create_hotel(user=self.user)
        response = self.client.get(
            f'{self.url}/get_all_hotels/',
            format='json'
        )
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], hotel.name)

    def test_new_hotel(self):
        hotel = HotelFactory().build_hotel_JSON()
        new_hotel = Hotel.objects.create(user=self.user, **hotel)
        
        response = self.client.post(
            f'{self.url}/',
            new_hotel,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)