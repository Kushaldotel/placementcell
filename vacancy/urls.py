from django.urls import path
from .views import JobVacancyListAPIView, JobVacancyDetailAPIView, resume_feedback

urlpatterns = [
    path('vacancies/', JobVacancyListAPIView.as_view(), name='job-vacancy-list'),
    path('jobs/<int:id>/', JobVacancyDetailAPIView.as_view(), name='job-detail'),
    path("resume-feedback/", resume_feedback, name="resume-feedback"),
]