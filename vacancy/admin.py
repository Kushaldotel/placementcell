from django.contrib import admin
from .models import JobVacancy, Application

@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'job_type', 'is_open', 'posted_on', 'application_deadline')
    list_filter = ('job_type', 'is_open', 'posted_by')
    search_fields = ('title', 'description', 'skills_required')
    date_hierarchy = 'posted_on'
    ordering = ('-posted_on',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job_vacancy', 'status', 'applied_on')
    list_filter = ('status', 'job_vacancy', 'student')
    search_fields = ('student__name', 'job_vacancy__title', 'cover_letter')
    date_hierarchy = 'applied_on'
    ordering = ('-applied_on',)