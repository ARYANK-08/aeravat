from django.db import models

# Create your models here.
class WeekTask(models.Model):
    date = models.DateField()
    task = models.TextField()

    def _str_(self):
        return f"{self.date}: {self.task}"