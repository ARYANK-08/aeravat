from django.urls import path
from AIinterview_app.views import question_view

urlpatterns = [
    path('interview/', question_view, name='question_view'),
]
