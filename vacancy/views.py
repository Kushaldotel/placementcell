from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JobVacancy, Application
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
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
import json

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
    # permission_classes = [IsStudentUser]
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

        try:
            # Generate feedback using LangChain & Gemini API
            result = generate_feedback(resume_text, job_description)

            # Return structured response with feedback and scores
            return JsonResponse({
                "feedback": result["feedback"],
                "current_score": result["current_score"],
                "expected_score": result["expected_score"]
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error generating feedback: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# Function-based views for template rendering
def index_view(request):
    """View for the home page"""
    return render(request, 'index.html')

def about_view(request):
    """View for the about page"""
    return render(request, 'about.html')

def career_view(request):
    """View for the career page with job listings"""
    # Get search parameters
    search_query = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')

    # Start with all open jobs
    jobs = JobVacancy.objects.filter(is_open=True).order_by('-posted_on')

    # Apply filters if provided
    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if location:
        jobs = jobs.filter(location__icontains=location)

    # Pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get unique locations for filter dropdown
    locations = JobVacancy.objects.filter(is_open=True).values_list('location', flat=True).distinct().order_by('location')

    # import pdb; pdb.set_trace()
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'job_type': job_type,
        'location': location,
        'locations': locations,
        'job_types': JobVacancy.JOB_TYPE_CHOICES,
    }

    return render(request, 'career.html', context)

def contact_view(request):
    """View for the contact page and form handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Compose email
        email_subject = f"Contact Form: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],  # Send to your email
                fail_silently=False,
            )

            # Send confirmation email to the user
            confirmation_subject = "Thank you for contacting Placement Cell"
            confirmation_message = f"Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you shortly.\n\nBest regards,\nPlacement Cell Team"

            send_mail(
                confirmation_subject,
                confirmation_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],  # Send to user's email
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully. We'll get back to you soon!")
        except Exception as e:
            messages.error(request, f"There was an error sending your message. Please try again later. Error: {str(e)}")

    return render(request, 'contact.html')

def atsreport_view(request):
    """View for the ATS report page"""
    return render(request, 'atsreport.html')

def login_view(request):
    """View for the login page and login functionality"""
    # Redirect if user is already logged in
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # Set session expiry based on remember me checkbox
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)

            # Redirect to next parameter if it exists
            next_url = request.GET.get('next', 'index')
            messages.success(request, "You have successfully logged in!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')

def logout_view(request):
    """View for logging out"""
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')

@login_required
def job_detail_view(request, id):
    """View for displaying job vacancy details"""
    try:
        job = JobVacancy.objects.get(id=id, is_open=True)

        # Check if user has already applied
        user_has_applied = False
        if request.user.is_authenticated:
            user_has_applied = Application.objects.filter(
                student=request.user,
                job_vacancy=job
            ).exists()

        # Get current date for deadline comparison
        from django.utils import timezone
        now = timezone.now()

        context = {
            'job': job,
            'user_has_applied': user_has_applied,
            'now': now
        }
        return render(request, 'job_detail.html', context)
    except JobVacancy.DoesNotExist:
        messages.error(request, "Job vacancy not found or no longer available.")
        return redirect('career')

@login_required
def dashboard_view(request):
    """View for the user's dashboard"""
    # Get user's applications
    user_applications = Application.objects.filter(student=request.user)

    # Get counts
    total_applications = user_applications.count()
    pending_count = user_applications.filter(status='PENDING').count()
    accepted_count = user_applications.filter(status='ACCEPTED').count()
    rejected_count = user_applications.filter(status='REJECTED').count()

    # Get job type distribution
    job_type_distribution = user_applications.values(
        'job_vacancy__job_type'
    ).annotate(
        count=Count('id')
    )

    # Prepare data for job type pie chart
    job_type_data = [0, 0, 0]  # [FULL_TIME, PART_TIME, INTERNSHIP]
    for item in job_type_distribution:
        if item['job_vacancy__job_type'] == 'FULL_TIME':
            job_type_data[0] = item['count']
        elif item['job_vacancy__job_type'] == 'PART_TIME':
            job_type_data[1] = item['count']
        elif item['job_vacancy__job_type'] == 'INTERNSHIP':
            job_type_data[2] = item['count']

    # Prepare data for application timeline (by month)
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    one_month_ago = now - timedelta(days=30)
    three_months_ago = now - timedelta(days=90)

    # Count applications by time period
    recent_apps = user_applications.filter(applied_on__gte=one_month_ago).count()
    mid_term_apps = user_applications.filter(applied_on__lt=one_month_ago, applied_on__gte=three_months_ago).count()
    older_apps = user_applications.filter(applied_on__lt=three_months_ago).count()

    application_timeline_data = [recent_apps, mid_term_apps, older_apps]

    context = {
        'total_applications': total_applications,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'job_type_data': json.dumps(job_type_data),
        'application_timeline_data': json.dumps(application_timeline_data)
    }

    return render(request, 'dashboard.html', context)

@login_required
def application_list_view(request, status):
    """View for displaying applications by status"""
    # Validate status
    if status not in ['PENDING', 'ACCEPTED', 'REJECTED']:
        messages.error(request, "Invalid application status.")
        return redirect('dashboard')

    # Get applications
    applications = Application.objects.filter(
        student=request.user,
        status=status
    ).select_related('job_vacancy').order_by('-applied_on')

    context = {
        'applications': applications,
        'status': status
    }

    return render(request, 'application_list.html', context)