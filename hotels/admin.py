from django.contrib import admin

from .models import Facility, Hotel, HotelRoom

# Register your models here.

admin.site.register(Facility)
admin.site.register(Hotel)
admin.site.register(HotelRoom)
