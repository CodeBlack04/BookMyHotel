from django.shortcuts import render

from .models import Hotel

# Create your views here.

def hotels(request):
    hotels = Hotel.objects.all()
    query = request.GET.get('query', '')

    if query:
        hotels = hotels.filter(hotel_name__icontains = query)

    return render(request, 'hotels/hotels.html', {
        'title': 'Hotels',
        'hotels': hotels,
        'query': query,
    })

def hotel_details(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    return render(request, 'hotels/hotel_details.html', {
        'title': hotel.hotel_name,
        'hotel': hotel,
    })

