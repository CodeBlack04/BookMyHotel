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

class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=255)

    def __str__(self):
        return self.hotel_name
    
class HotelImage(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images')

    def __str__(self):
        return f"Image for {self.hotel.hotel_name}"
    

    

class HotelRoom(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    facility = models.ManyToManyField(Facility, blank=True)
    room_number = models.IntegerField(unique=True)
    price = models.FloatField()

    def __str__(self):
        return f'{self.room_number} at {self.hotel.hotel_name}'
    
class HotelRoomImage(BaseModel):
    hotel_room = models.ForeignKey(HotelRoom, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_room_images')

    def __str__(self):
        return f"Image for room {self.hotel_room.room_number} at {self.hotel_room.hotel.hotel_name}"



    