from django.contrib import admin
from .models import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'company_name', 'interview_date', 'start_time', 'end_time', 'panel')
    list_filter = ('interview_date', 'panel')
    search_fields = ('candidate_name', 'company_name')

