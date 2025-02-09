from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JobVacancy
from .serializers import JobVacancySerializer, JobVacancyDetailSerializer, ApplicationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .pagination import JobVacancyPagination
from .permissions import IsStudentUser
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser


class JobVacancyListAPIView(ListAPIView):
    """
    API view for listing job vacancies with pagination.
    Only students can access this endpoint.
    """
    permission_classes = [IsAuthenticated, IsStudentUser]
    queryset = JobVacancy.objects.filter(is_open=True).order_by('-posted_on')
    serializer_class = JobVacancySerializer
    pagination_class = JobVacancyPagination

class JobVacancyDetailAPIView(RetrieveAPIView, CreateAPIView):
    """
    API View to:
    1. Retrieve job details (GET)
    2. Apply for a job (POST)
    """
    permission_classes = [IsAuthenticated, IsStudentUser]
    queryset = JobVacancy.objects.filter(is_open=True)
    serializer_class = JobVacancyDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        """Return different serializers for GET and POST requests"""
        if self.request.method == 'POST':
            return ApplicationSerializer
        return JobVacancyDetailSerializer

    def get_serializer_context(self):
        """Pass request to serializer for validation"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    parser_classes = [MultiPartParser, FormParser]  # Allows file uploads