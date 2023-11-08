from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotels, name='hotels'),
    
    path('<str:hotel_id>/', views.hotel_detail, name='hotel-detail'),

    path('rooms/<str:hotel_room_id>/', views.hotel_room_detail, name='hotel-room-detail'),
]