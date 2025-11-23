from django.db import models
from django.utils import timezone
from datetime import datetime


class Interview(models.Model):
    candidate_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    interview_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    panel = models.IntegerField(default=1, choices=[(1, 'Panel 1'), (2, 'Panel 2'), (3, 'No Slots Available')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['interview_date', 'start_time']
        unique_together = ['interview_date', 'start_time', 'panel']

    def __str__(self):
        return f"{self.candidate_name} - {self.company_name} on {self.interview_date}"

