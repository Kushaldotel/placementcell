from rest_framework import serializers
from .models import JobVacancy

class JobVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobVacancy
        fields = [
            'id', 'title', 'description', 'job_type', 'is_open',
            'posted_by', 'posted_on', 'application_deadline',
            'salary', 'location', 'skills_required'
        ]