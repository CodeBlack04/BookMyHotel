from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotel_list, name='hotels'),
    
    path('<str:hotel_id>/', views.hotel_detail, name='hotel-detail'),

    path('<str:hotel_id>/submit-rating/', views.submit_rating, name='submit-rating'),

    path('rooms/<str:hotel_room_id>/', views.hotel_room_detail, name='hotel-room-detail'),

    path('rooms/<str:hotel_room_id>/book-room/', views.book_room, name='book-room'),
]