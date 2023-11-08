from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from django.contrib import messages

from .forms import BookRoomForm
from .models import Booking


from datetime import datetime, timedelta
from .models import Hotel, HotelRoom

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

def hotel_detail(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    return render(request, 'hotels/hotel_detail.html', {
        'title': hotel.hotel_name,
        'hotel': hotel,
    })

def hotel_room_detail(request, hotel_room_id):
    hotel_room = get_object_or_404(HotelRoom, id=hotel_room_id)

    # Find out the last day of the current month
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4)  # this will never fail
    last_day_of_month = next_month - timedelta(days=next_month.day)

    # Generate a list of all dates in the current month
    date_list = [today.replace(day=x) for x in range(1, last_day_of_month.day + 1)]

    # Use the is_booked method to determine room availability for each date
    availability = {date: not hotel_room.is_booked(date) for date in date_list}

    # Creating weeks for the calendar
    availability_calendar = defaultdict(lambda: [None] * 7)  # Default to None for days
        
    for date, is_available in availability.items():
        # .weekday() returns the day of the week as an integer (Monday is 0, Sunday is 6)
        availability_calendar[date.isocalendar()[1] - today.isocalendar()[1]][date.weekday()] = (date.day, 'Available' if is_available else 'Booked')

    # for week in sorted(availability_calendar):
    #     print("Week {}: {}".format(week, availability_calendar[week]))
    
    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['start_date']
            check_out = form.cleaned_data['end_date']

            date = check_in
            while date <= check_out:
                if hotel_room.is_booked(date):
                    messages.error(request, f'The room is already booked on {date.strftime("%d-%m-%Y")}')
                    break
                date += timedelta(days=1)
            else:
                Booking.objects.create(room=hotel_room, start_date=check_in, end_date=check_out)
                messages.success(request, 'Room booked successfully!')

                return redirect(f'/hotels/rooms/{hotel_room.id}/')
    else:
        form = BookRoomForm()

    return render(request, 'hotels/room_detail.html', {
        'title': f'{hotel_room.hotel.hotel_name}',
        'hotel_room': hotel_room,
        'availability_calendar': dict(availability_calendar),  # Convert defaultdict to dict for the template
        'form': form,
    })

