from apps.bookings.models import Room
from faker import Faker
faker = Faker()

class RoomFactory():
    
    def build_room_JSON(self):
        return {
            "hotel": 1,
            "number": faker.random_number(),
            "capacity": faker.random_number(),
            "price_day": faker.random_number(),
            "description": faker.paragraph()
        }
    
    def create_room(self):
        return Room.objects.create(**self.build_room_JSON())