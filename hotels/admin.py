from django.contrib import admin

from .models import Facility, Hotel, HotelRoom, HotelImage, HotelRoomImage, Booking

# Register your models here.

admin.site.register(Facility)

admin.site.register(Hotel)
admin.site.register(HotelImage)

admin.site.register(HotelRoom)
admin.site.register(HotelRoomImage)

admin.site.register(Booking)
