from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Room
from myauth.models import User
from django.contrib.auth.models import Group

from .forms import AddUserForm, EditUserForm

# Create your views here.


@require_POST
@csrf_exempt
@login_required
def create_room(request, room_id):
    url = request.POST.get('url', '')

    room = Room.objects.create(room_id=room_id, client=request.user, url=url)

    return JsonResponse({'message': 'Room Created'})


@login_required
def admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True).filter(is_superuser=False)

    return render(request, 'support/admin.html', {
        'title': 'Chat Rooms',
        'rooms': rooms,
        'users': users,
    })


@login_required
def add_user(request):
    if request.user.has_perm('myauth.add_user'):
        if request.method == 'POST':
            form = AddUserForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True
                user.set_password(form.cleaned_data['password'])
                user.save()

                if user.role == User.MANAGER:
                    group = Group.objects.get(name='Managers')
                    group.user_set.add(user)

                    messages.success(request, f'Staff is crated and added to {group.name} group!')

                elif user.role == User.AGENT:
                    group = Group.objects.get(name='Agents')
                    group.user_set.add(user)

                    messages.success(request, f'Staff is crated and added to {group.name} group!')

                else:
                    user.is_staff = False
                    user.save()
                    messages.success(request, 'New client is crated!')

                return redirect ('/support/admin/')
        else:
            form = AddUserForm()

        return render(request, 'support/add_user.html', {
            'title': 'Add user',
            'form': form
        })
    else:
        messages.error(request, 'You do not have access to add staffs!')

        return redirect('/support/admin/')
    

@login_required
def edit_user(request, id):
    if request.user.has_perm('myauth.change_user'):
        user = User.objects.get(pk=id)
        if request.method == 'POST':
            form = EditUserForm(request.POST, instance=user)

            if form.is_valid():
                user = form.save()

                if user.role == User.MANAGER: 
                    agent_group = Group.objects.get(name='Agents')
                    agent_group.user_set.remove(user)

                    manager_group = Group.objects.get(name='Managers')
                    manager_group.user_set.add(user)

                elif user.role == User.AGENT: 
                    manager_group = Group.objects.get(name='Managers')
                    manager_group.user_set.remove(user)

                    agent_group = Group.objects.get(name='Agents')
                    agent_group.user_set.add(user)

                else:
                    user.is_staff = False
                    user.groups.clear()
                    user.save()

                messages.success(request, 'Staff details updated!')

                return redirect('/support/admin/')
            
        else:
            form = EditUserForm(instance=user)

        return render(request, 'support/edit_user.html', {
            'title': 'Edit Staff',
            'form': form,
        })
    
    else:
        messages.error(request, 'You do not have permission to edit staffs!!')

        return redirect('/support/admin/')


@login_required
def room(request, room_id):
    room = Room.objects.get(room_id=room_id)
    
    if room.status == Room.WAITING:    
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()

    return render(request, 'support/room.html', {
        'title': 'Room',
        'room': room,
    })


@login_required
def delete_room(request, room_id):
    if request.user.has_perm('support.delete_room'):
        room = Room.objects.get(room_id=room_id)
        room.delete()

        messages.success(request, 'Room was deleted!')

        return redirect('/support/admin/')
    
    else:
        messages.error(request, 'You do not have permission to delete rooms!')

        return redirect('/support/admin/')
    




