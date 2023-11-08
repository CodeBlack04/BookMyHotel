from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotels, name='hotels'),
    
    path('<str:hotel_id>/', views.hotel_details, name='hotel-details'),
]