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
from django.core.files.storage import default_storage
from .resume_parser import extract_text_from_pdf, extract_text_from_docx
from utils.feedback_on_resume import generate_feedback
from django.http import JsonResponse
import os

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


def resume_feedback(request):
    if request.method == "POST":
        # Get uploaded file
        resume_file = request.FILES.get("resume")
        job_description = request.POST.get("job_description")

        if not resume_file or not job_description:
            return JsonResponse({"error": "Resume and job description are required"}, status=400)

        # Save file temporarily
        file_path = default_storage.save(resume_file.name, resume_file)
        file_ext = os.path.splitext(resume_file.name)[1].lower()

        # Extract text from resume
        if file_ext == ".pdf":
            resume_text = extract_text_from_pdf(file_path)
        elif file_ext == ".docx":
            resume_text = extract_text_from_docx(file_path)
        else:
            return JsonResponse({"error": "Unsupported file format"}, status=400)

        # Generate feedback
        feedback = generate_feedback(resume_text, job_description)

        return JsonResponse({"feedback": feedback})

    return JsonResponse({"error": "Invalid request method"}, status=405)
