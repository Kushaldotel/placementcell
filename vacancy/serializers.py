from rest_framework import serializers
from .models import JobVacancy, Application

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
        return Application.objects.create(student=user, job_vacancy=job, **validated_data)