from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('upload/', upload_pdf, name='upload_pdf'),
    # path('skill_assessment/', skill_assessment, name='skill_assessment'),
        path('quiz/<int:quiz_id>/', quiz_view, name='quiz-view'),
    path('quiz/<int:quiz_id>/results/', quiz_results, name='quiz_results'),
    path('mentor/', mentor,name='mentor'),
    path('jobs/',job_listings, name='job_listings'),
    path('display_courses/', display_courses, name='display_courses'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile,name='profile'),
    path('', landing, name='landing'),
]
