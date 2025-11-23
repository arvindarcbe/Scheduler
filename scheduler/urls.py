from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_view, name='schedule_view'),
    path('add/', views.add_interviews, name='add_interviews'),
]

