from django.db import models

class StudentProfile(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    linkedin_profile = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    skills = models.CharField(max_length=1000, null=True, blank=True)
    projects = models.CharField(max_length=1000, null=True, blank=True)
    desired_role = models.CharField(max_length=100, null=True, blank=True)
    preferred_industry = models.CharField(max_length=100, null=True, blank=True)
    technology_interests = models.CharField(max_length=255, null=True, blank=True)
    current_year = models.IntegerField(null=True, blank=True)  # New field
    placement_year = models.IntegerField(null=True, blank=True)  # New field

    def __str__(self):
        return self.name


# models.py

from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,null=True, blank=True)
    text = models.CharField(max_length=255,null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)  # Add a topic field

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,null=True, blank=True)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class UserAnswer(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,null=True, blank=True)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE,null=True, blank=True)

    def is_correct(self):
        return self.selected_choice.is_correct
