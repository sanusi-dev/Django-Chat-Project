from django.shortcuts import render
from .models import Room
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserSettingsForm


# Create your views here.
def index(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
    return render(request, "index.html", context)


@login_required
def room(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    messages = room.messages.all()
    context = {"room": room, "messages": messages}
    return render(request, "room.html", context)


@login_required
def settings(request):
    if request.method == "POST":
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'partials/settings-form.html', {'form': form})

    else:
        form = UserSettingsForm(instance=request.user)
        context = {"form": form}
        return render(request, "settings.html", context)
