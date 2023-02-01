import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

import pydiscord.settings as settings
from base.forms import RoomForm, UserForm, MyUserCreationForm
from base.models import Room, Topic, Message, User


def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, f"Password for user: {email} is incorrect")
        except User.DoesNotExist:
            messages.error(request, f"User: {email} does not exits")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect("home")


def register_page(request):
    page = "register"
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user=user)

            return redirect("home")
        else:
            messages.error(request, f"An error occurred during user registration:")
            for field in form:
                if field.errors:
                    messages.error(request, f"\tField Error: '{field.name}'")
                    for error in field.errors:
                        messages.error(request, f"\t\t'{error}'\n")

    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)


def home_page(request):
    q = request.GET.get("q")
    q = q if q else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages}
    return render(request, "base/home.html", context)


def topics_page(request):
    q = request.GET.get("q")
    q = q if q else ""
    topics = Topic.objects.filter(name__icontains=q)

    context = {"topics": topics}
    return render(request, "base/topics.html", context)


def activity_page(request):
    room_messages = Message.objects.all()
    context = {"room_messages": room_messages}
    return render(request, "base/activity.html", context)


def room_page(request, pk):
    _room = Room.objects.get(id=pk)
    room_messages = _room.message_set.all()
    participants = _room.participants.all()

    if request.method == "POST":
        Message.objects.create(
            user=request.user,
            room=_room,
            body=request.POST.get("body")
        )
        if request.user not in participants:
            _room.participants.add(request.user)
        return redirect("room", pk=_room.id)

    context = {"room": _room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def update_room(request, pk):
    _room = Room.objects.get(id=pk)
    form = RoomForm(instance=_room)
    topics = Topic.objects.all()

    if request.user != _room.host:
        return HttpResponse("You are not allowed to edit this room!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        _room.name = request.POST.get("name")
        _room.topic = topic
        _room.description = request.POST.get("description")
        _room.save()

        return redirect("home")

    context = {"form": form, "topics": topics, "room": _room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def delete_room(request, pk):
    _room = Room.objects.get(id=pk)

    if request.user != _room.host:
        return HttpResponse("You are not allowed to delete this room!")

    if request.method == "POST":
        _room.delete()
        return redirect("home")

    context = {"obj": _room}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def delete_message(request, pk):
    _message = Message.objects.get(id=pk)

    if request.user != _message.user:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        _message.delete()
        return redirect("home")

    context = {"obj": _message}
    return render(request, "base/delete.html", context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {"user": user, "rooms": rooms, "room_messages": room_messages, "topics": topics}
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
        else:
            messages.error(request, f"An error occurred during profile change:")
            for field in form:
                if field.errors:
                    messages.error(request, f"\tField Error: '{field.name}'")
                    for error in field.errors:
                        messages.error(request, f"\t\t'{error}'\n")

    context = {"form": form}
    return render(request, "base/update-user.html", context)


@login_required(login_url="login")
def reset_avatar(request):
    user: User = request.user
    if request.method == "POST":
        default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatar.svg')
        with open(default_avatar_path, "rb") as default_avatar:
            new_avatar_name = f"{user.avatar.url.split('.')[0]}.svg"
            user.avatar.delete(save=False)
            user.avatar.save(new_avatar_name, default_avatar)

        return redirect("user-profile", pk=user.id)

    context = {"user": user}
    return render(request, "base/reset_avatar.html", context)
