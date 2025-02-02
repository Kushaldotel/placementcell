from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from unfold.admin import ModelAdmin
class CustomUserAdmin(UserAdmin,ModelAdmin):
    list_display = ('email', 'user_type', 'name', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_type', 'name', 'description', 'website', 'roll_number', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),  # Removed 'created_at'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'name'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)