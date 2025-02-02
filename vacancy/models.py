from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field  # Import CKEditor5Field
User = get_user_model()

class JobVacancy(models.Model):
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    description = CKEditor5Field('Description', config_name='extends')  # Use CKEditor5Field
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    is_open = models.BooleanField(default=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_vacancies')
    posted_on = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    salary = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    skills_required = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_job_type_display()})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='applications')
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    class Meta:
        unique_together = ('student', 'job_vacancy')

    def __str__(self):
        return f"{self.student.name} - {self.job_vacancy.title} ({self.status})"