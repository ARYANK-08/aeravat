from django.contrib import admin
from .models import Quiz, Question, StudentProfile, Choice, UserAnswer
# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserAnswer)

