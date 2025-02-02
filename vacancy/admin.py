from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget  # Import CKEditor5Widget
from django.db import models
from .models import JobVacancy, Application

@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'job_type', 'is_open', 'posted_on', 'application_deadline')
    list_filter = ('job_type', 'is_open', 'posted_by')
    search_fields = ('title', 'skills_required')
    date_hierarchy = 'posted_on'
    ordering = ('-posted_on',)

    # Add CKEditor 5 widget for the 'description' field
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job_vacancy', 'status', 'applied_on')
    list_filter = ('status', 'job_vacancy', 'student')
    search_fields = ('student__name', 'job_vacancy__title', 'cover_letter')
    date_hierarchy = 'applied_on'
    ordering = ('-applied_on',)

    # Add CKEditor 5 widget for the 'cover_letter' field
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }