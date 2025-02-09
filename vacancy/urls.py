from django.urls import path
from .views import JobVacancyListAPIView, JobVacancyDetailAPIView

urlpatterns = [
    path('vacancies/', JobVacancyListAPIView.as_view(), name='job-vacancy-list'),
    path('jobs/<int:id>/', JobVacancyDetailAPIView.as_view(), name='job-detail'),
]