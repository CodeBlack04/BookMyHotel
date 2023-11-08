from django.db import models
from django.utils import timezone

import uuid

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class Facility(BaseModel):
    facility_name = models.CharField(max_length=255)

    def __str__(self):
        return self.facility_name
    

# Hotel related models    

class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=255)

    def __str__(self):
        return self.hotel_name
    
class HotelImage(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images')

    def __str__(self):
        return f"Image for {self.hotel.hotel_name}"
    


# Hotel-room related models    

class HotelRoom(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    facility = models.ManyToManyField(Facility, blank=True)
    room_number = models.IntegerField(unique=True)
    price = models.FloatField()

    def is_booked(self, check_date):
        return self.bookings.filter(start_date__lte=check_date, end_date__gte=check_date).exists()

    def __str__(self):
        return f'{self.room_number} at {self.hotel.hotel_name}'
    
class HotelRoomImage(BaseModel):
    hotel_room = models.ForeignKey(HotelRoom, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_room_images')

    def __str__(self):
        return f"Image for room {self.hotel_room.room_number} at {self.hotel_room.hotel.hotel_name}"
    

# Booking related models

class Booking(BaseModel):
    room = models.ForeignKey(HotelRoom, related_name='bookings', blank=True, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Booking for {self.room.room_number} at {self.room.hotel.hotel_name} from {self.start_date} to {self.end_date}'



    