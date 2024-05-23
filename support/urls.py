from django.urls import path

from . import views

app_name = 'support'

urlpatterns = [
    path('create-room/<str:room_id>/', views.create_room, name='create-room'),

    path('admin/', views.admin, name='admin'),

    path('add-user/', views.add_user, name='add-user'),

    path('edit-user/<str:id>/', views.edit_user, name='edit-user'),

    path('room/<str:room_id>/', views.room, name='room'),

    path('delete-room/<str:room_id>/', views.delete_room, name='delete-room'),


]