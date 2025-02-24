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
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
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

@csrf_exempt
def resume_feedback(request):
    if request.method == "POST":
        # Ensure request is multipart/form-data
        if "resume" not in request.FILES or "job_description" not in request.POST:
            return JsonResponse({"error": "Resume and job description are required"}, status=400)

        resume_file = request.FILES["resume"]
        job_description = request.POST["job_description"]

        # Save the uploaded file
        file_name = default_storage.save(f"resumes/{resume_file.name}", ContentFile(resume_file.read()))
        file_path = default_storage.path(file_name)  # Get the absolute path

        # Extract file extension
        file_ext = os.path.splitext(file_name)[1].lower()

        # Extract text from the resume
        if file_ext == ".pdf":
            resume_text = extract_text_from_pdf(file_path)
        elif file_ext == ".docx":
            resume_text = extract_text_from_docx(file_path)
        else:
            return JsonResponse({"error": "Unsupported file format. Upload PDF or DOCX."}, status=400)

        # Generate feedback using LangChain & Gemini API
        feedback = generate_feedback(resume_text, job_description)

        # import pdb; pdb.set_trace()
        return JsonResponse({"feedback": feedback}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)
