from django.urls import path
from .views import (
    JobVacancyListAPIView,
    JobVacancyDetailAPIView,
    resume_feedback,
    index_view,
    about_view,
    career_view,
    contact_view,
    atsreport_view,
    login_view,
    logout_view,
    job_detail_view
)

urlpatterns = [
    # API endpoints
    path('jobs/', JobVacancyListAPIView.as_view(), name='job-list'),
    path('jobs/<int:id>/', JobVacancyDetailAPIView.as_view(), name='job-detail'),
    path('resume-feedback/', resume_feedback, name='resume-feedback'),

    # Template views
    path('', index_view, name='index'),
    path('about/', about_view, name='about'),
    path('career/', career_view, name='career'),
    path('contact/', contact_view, name='contact'),
    path('atsreport/', atsreport_view, name='atsreport'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('job/<int:id>/', job_detail_view, name='job-detail-view'),
]