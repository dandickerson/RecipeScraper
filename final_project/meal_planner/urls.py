from .import views
from django.urls import path
from schedule.views import CalendarView, CreateEventView, EditEventView, DeleteEventView


app_name = 'meal_planner'
urlpatterns = [
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('event/add/', CreateEventView.as_view(), name='event_add'),
    path('event/<int:pk>/edit/', EditEventView.as_view(), name='event_edit'),
    path('event/<int:pk>/delete/', DeleteEventView.as_view(), name='event_delete'),
]