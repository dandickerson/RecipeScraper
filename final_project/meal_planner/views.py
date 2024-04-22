from django.shortcuts import render, redirect
from django.views.generic import View
from schedule.models import Event
from .forms import EventForm


class CalendarView(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'calendar.html', {'events': events})


class CreateEventView(View):
    def get(self, request):
        form = EventForm()
        return render(request, 'event_add.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meal_planner:calendar')
        return render(request, 'event_add.html', {'form': form})


class EditEventView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        form = EventForm(instance=event)
        return render(request, 'event_edit.html', {'form': form})

    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('meal_planner:calendar')
        return render(request, 'event_edit.html', {'form': form})


class DeleteEventView(View):
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        return render(request, 'event_delete.html', {'event': event})

    def post(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return redirect('meal_planner:calendar')
