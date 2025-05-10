from rest_framework import serializers
from .models import JobVacancy, Application
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime

class JobVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobVacancy
        fields = [
            'id', 'title', 'description', 'job_type', 'is_open',
            'posted_by', 'posted_on', 'application_deadline',
            'salary', 'location', 'skills_required'
        ]

class JobVacancyDetailSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.name', read_only=True)

    class Meta:
        model = JobVacancy
        fields = [
            'id', 'title', 'description', 'job_type', 'is_open',
            'posted_by_name', 'posted_on', 'application_deadline',
            'salary', 'location', 'skills_required'
        ]

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']

    def validate(self, data):
        """Ensure student hasn't already applied for this job"""
        user = self.context['request'].user
        job_id = self.context['view'].kwargs['id']

        #making sure that the student has not already applied for this job
        if Application.objects.filter(student=user, job_vacancy_id=job_id).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        return data

    def create(self, validated_data):
        """Create job application linked to current user and job vacancy"""
        user = self.context['request'].user
        job_id = self.context['view'].kwargs['id']
        job = JobVacancy.objects.get(id=job_id)

        # Create the application
        application = Application.objects.create(student=user, job_vacancy=job, **validated_data)

        # Send confirmation email to student
        self._send_student_confirmation_email(application)

        # Send notification email to organization
        self._send_organization_notification_email(application)

        return application

    def _send_student_confirmation_email(self, application):
        """Send confirmation email to the student"""
        student = application.student
        job = application.job_vacancy
        organization = job.posted_by

        # Prepare context for the email template
        context = {
            'student_name': student.name,
            'job_title': job.title,
            'company_name': organization.name,
            'job_type': job.get_job_type_display(),
            'job_location': job.location or 'Not specified',
            'application_date': application.applied_on.strftime('%B %d, %Y'),
            'dashboard_url': f"{settings.SITE_URL}/api/v1/vacancy/dashboard/",
            'current_year': datetime.now().year
        }

        # Render HTML email
        html_content = render_to_string('email/application_confirmation_student.html', context)
        plain_text = strip_tags(html_content)

        # Send email
        send_mail(
            subject=f'Application Confirmation: {job.title} at {organization.name}',
            message=plain_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            html_message=html_content,
            fail_silently=False,
        )

    def _send_organization_notification_email(self, application):
        """Send notification email to the organization"""
        student = application.student
        job = application.job_vacancy
        organization = job.posted_by

        # Get resume URL if available
        resume_url = None
        if application.resume:
            resume_url = f"{settings.SITE_URL}{application.resume.url}"

        # Prepare context for the email template
        context = {
            'organization_name': organization.name,
            'job_title': job.title,
            'job_type': job.get_job_type_display(),
            'job_location': job.location or 'Not specified',
            'application_date': application.applied_on.strftime('%B %d, %Y'),
            'student_name': student.name,
            'student_email': student.email,
            'student_phone': getattr(student, 'phone', None),
            'resume_url': resume_url,
            'application_url': f"{settings.SITE_URL}/admin/vacancy/applications/{application.id}/change/",
            'current_year': datetime.now().year
        }

        # Render HTML email
        html_content = render_to_string('email/application_notification_organization.html', context)
        plain_text = strip_tags(html_content)

        # Send email
        send_mail(
            subject=f'New Application: {student.name} for {job.title}',
            message=plain_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[organization.email],
            html_message=html_content,
            fail_silently=False,
        )