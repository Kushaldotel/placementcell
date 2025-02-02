from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from django.db import models
from .models import JobVacancy, Application, User
from unfold.admin import ModelAdmin
# Custom Admin for JobVacancy
@admin.register(JobVacancy)
class JobVacancyAdmin(ModelAdmin):
    list_display = ('title', 'posted_by', 'job_type', 'is_open', 'posted_on', 'application_deadline')
    list_filter = ('job_type', 'is_open', 'posted_by')
    search_fields = ('title', 'skills_required')
    date_hierarchy = 'posted_on'
    ordering = ('-posted_on',)

    # Add CKEditor 5 widget for the 'description' field
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }

    # Restrict organizations to see only their job vacancies
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == 'ORGANIZATION':
            return qs.filter(posted_by=request.user)
        return qs

    # For JobVacancyAdmin

    def has_module_permission(self, request):
        try:
            if request.user.user_type == 'ORGANIZATION':
                return True  # Allow organizations to access the JobVacancy module
            return super().has_module_permission(request)
        except:
            return False
        # if request.user.user_type == 'ORGANIZATION':
        #     return True  # Allow organizations to access the JobVacancy module
        # return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        try:
            if request.user.user_type == 'ORGANIZATION':
                return True  # Allow organizations to view JobVacancy objects
            return super().has_view_permission(request, obj)

        except:
            return False
        # if request.user.user_type == 'ORGANIZATION':
        #     return True  # Allow organizations to view JobVacancy objects
        # return super().has_view_permission(request, obj)

    # Restrict organizations from editing the 'posted_by' field
    def get_readonly_fields(self, request, obj=None):
        if request.user.user_type == 'ORGANIZATION':
            return ('posted_by',)
        return super().get_readonly_fields(request, obj)

    # Automatically set the 'posted_by' field to the logged-in organization
    def save_model(self, request, obj, form, change):
        if not obj.pk and request.user.user_type == 'ORGANIZATION':
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)


# Custom Admin for Application
@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ('student', 'job_vacancy', 'status', 'applied_on')
    list_filter = ('status', 'job_vacancy', 'student')
    search_fields = ('student__name', 'job_vacancy__title', 'cover_letter')
    date_hierarchy = 'applied_on'
    ordering = ('-applied_on',)

    # Add CKEditor 5 widget for the 'cover_letter' field
    # formfield_overrides = {
    #     models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    # }

    # For ApplicationAdmin

    def has_module_permission(self, request):

        try:
            if request.user.user_type == 'ORGANIZATION':
                return True  # Allow organizations to access the Application module
            return super().has_module_permission(request)
        except:
            return False
        # if request.user.user_type == 'ORGANIZATION':
        #     return True  # Allow organizations to access the Application module
        # return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        try:
            if request.user.user_type == 'ORGANIZATION':
                return True  # Allow organizations to view Application objects
            return super().has_view_permission(request, obj)
        except:
            return False
        # if request.user.user_type == 'ORGANIZATION':
        #     return True  # Allow organizations to view Application objects
        # return super().has_view_permission(request, obj)

    # Restrict organizations to see only applications for their job vacancies
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.user_type == 'ORGANIZATION':
            return qs.filter(job_vacancy__posted_by=request.user)
        return qs

    # Restrict organizations from editing the 'job_vacancy' field
    def get_readonly_fields(self, request, obj=None):
        if request.user.user_type == 'ORGANIZATION':
            return ('job_vacancy',)
        return super().get_readonly_fields(request, obj)
