from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import overall,category,personal,fullcalendar,hackathons
urlpatterns = [
    path('overall', overall, name='overall'),
    path('category/',category, name='category'),
    path('personal/',personal, name='personal'),
    path('fullcalendar/',fullcalendar, name='fullcalendar'),
    path('hackathons/',hackathons, name='hackathons'),


]