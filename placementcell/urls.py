"""
URL configuration for placementcell project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static

# change the title from django administration to corp gems
admin.site.site_header = "Placement Administration"
# also change the login administration to login into corpgems admin
admin.site.site_title = "Placement Admin"

BASE_URL = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/auth/', include('authuser.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
