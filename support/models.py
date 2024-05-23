from django.db import models
from myauth.models import User

# Create your models here.

class Message(models.Model):
    body = models.TextField()
    sent_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sent_by.name}-{self.body}'
    
    class Meta:
        ordering = ('created_at',)


class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    ROOM_STATUS = (
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    )

    room_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    messages = models.ManyToManyField(Message, blank=True)

    client = models.ForeignKey(User, related_name='client_rooms', blank=True, null=True, on_delete=models.SET_NULL)
    agent = models.ForeignKey(User, related_name='agent_rooms', blank=True, null=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=20, choices=ROOM_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.client.name}-{self.room_id}-{self.status}'
    
    class Meta:
        ordering = ('-created_at',)