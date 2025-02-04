from django.urls import path
from .views import JobVacancyListAPIView

urlpatterns = [
    path('vacancies/', JobVacancyListAPIView.as_view(), name='job-vacancy-list'),
]