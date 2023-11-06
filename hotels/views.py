from django.shortcuts import render

from .models import Hotel

# Create your views here.

def hotels(request):
    hotels = Hotel.objects.all()

    return render(request, 'hotels/hotels.html', {
        'title': 'Hotels',
        'hotels': hotels,
    })