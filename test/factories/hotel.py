from apps.bookings.models import Hotel
from apps.users.models import User 

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

from faker import Faker
faker = Faker()

image = Image.new('RGB', (100, 100))
image_io = BytesIO()
image.save(image_io, format='JPEG')
image_file = SimpleUploadedFile('test_image.jpg', image_io.getvalue())


class HotelFactory():
    
    def build_hotel_JSON(self):
        return {
            "name": faker.company(),
            "address": faker.address(),
            "description": faker.paragraph(),
            "photo": image_file,
            "services": "Wifi - TV - Parking"
        }
    
    def create_hotel(self, user):
        return Hotel.objects.create(user=user, **self.build_hotel_JSON())