from apps.bookings.models import Booking
from datetime import timedelta, datetime
from faker import Faker
faker = Faker()



class BookingFactory():
    start_booking = datetime.now() + timedelta(days=2)
    start_date = datetime.now() + timedelta(days=3)
    end_date = datetime.now() + timedelta(days=10)
    
    def build_booking_JSON(self):
        return {
            "start_booking": self.start_booking,
            "end_booking": faker.date_time_between(start_date=self.start_date, end_date=self.end_date),
            "room": 1
        }
    
    def create_booking(self):
        return Booking.objects.create(**self.build_booking_JSON())