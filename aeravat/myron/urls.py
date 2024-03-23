from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns=[
    path('companies/',companies,name='companies'),
    path('aboutamazon/',aboutamazon,name='aboutamazon'),
    path('amazonaptitude/',amazonaptitude,name='amazonaptitude'),

    # URL for displaying quiz detail
    path('quiz1/<int:quiz_id>/', quiz_detail, name='quiz_detail'),    
    path('quiz_list/', quiz_list, name='quiz_list'),
    path('save_response/', save_response, name='save_response'),

     # Your existing quiz URLs
    path('quiz_list/', quiz_list, name='quiz_list'),
    path('save_response/', save_response, name='save_response'),

]