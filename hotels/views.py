from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.db.models import Count

from .forms import BookRoomForm, RatingForm, HotelFilterForm
from .models import Booking


from datetime import datetime, timedelta
from .models import Hotel, HotelRoom

# Create your views here.

def generate_availability_calendar(hotel_room):
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

    return dict(availability_calendar)  # Convert defaultdict to dict for the template


def hotel_list(request):
    hotels = Hotel.objects.all()
    query = request.GET.get('query', '')
    form = HotelFilterForm(request.GET)

    if form.is_valid():
        amenities = form.cleaned_data['amenities']
        location_types = form.cleaned_data['location_types']

        if amenities:
            # Start with all hotels, then narrow down by those that have each amenity.
            for amenity in amenities:
                hotels = hotels.filter(amenities=amenity)
            # Make sure that the resulting hotels are distinct
            hotels = hotels.distinct()

        if location_types:
            location_based_hotels = []
            for location_type in location_types:
                location_based_hotels += hotels.filter(location_type=location_type)
            hotels = location_based_hotels

    if query:
        hotels = hotels.filter(hotel_name__icontains = query)

    return render(request, 'hotels/hotel_list.html', {
        'title': 'Hotels',
        'hotels': hotels,
        'query': query,
        'hotel_filter_form': form,
    })

def hotel_detail(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    rating_form = RatingForm()
    ratings = hotel.ratings.all().order_by('-created_at')

    return render(request, 'hotels/hotel_detail.html', {
        'title': hotel.hotel_name,
        'hotel': hotel,
        'rating_form': rating_form,
        'ratings': ratings,
    })


def hotel_room_detail(request, hotel_room_id):
    hotel_room = get_object_or_404(HotelRoom, id=hotel_room_id)
    availability_calendar = generate_availability_calendar(hotel_room)
    booking_form = BookRoomForm()

    return render(request, 'hotels/room_detail.html', {
        'title': f'{hotel_room.hotel.hotel_name}',
        'hotel_room': hotel_room,
        'availability_calendar': availability_calendar,
        'booking_form': booking_form,
    })


@login_required
def book_room(request, hotel_room_id):
    hotel_room = get_object_or_404(HotelRoom, id=hotel_room_id)
    availability_calendar = generate_availability_calendar(hotel_room)
    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['start_date']
            check_out = form.cleaned_data['end_date']

            date = check_in
            while date < check_out:
                if hotel_room.is_booked(date):
                    messages.error(request, f'The room is already booked on {date.strftime("%d-%m-%Y")}')
                    break
                date += timedelta(days=1)
            else:
                Booking.objects.create(room=hotel_room, start_date=check_in, end_date=check_out - timedelta(days=1))
                messages.success(request, 'Room booked successfully!')

                return redirect(f'/hotels/rooms/{hotel_room.id}/')
    else:
        # For GET requests or invalid POST requests, create an empty form
        form = BookRoomForm()

    messages.error(request, 'Booking failed!')
    return render(request, 'hotels/room_detail.html', {
        'title': 'Book Room',
        'hotel_room': hotel_room,
        'availability_calendar': availability_calendar,
        'booking_form': form
        })


@login_required
def submit_rating(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    ratings = hotel.ratings.all().order_by('-created_at')
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.hotel = Hotel.objects.get(id=hotel_id)
            rating.user = request.user
            rating.save()

            messages.success(request, 'Rating submited!')
            return redirect(f'/hotels/{hotel_id}/')
    else:
        form = RatingForm()
   
    messages.error(request, 'Rating submission error: Please rate between 1-5.')
    return render(request, 'hotels/hotel_detail.html', {
        'title': 'Rate Hotel',
        'hotel': hotel,
        'rating_form': form,
        'ratings': ratings,
    })

