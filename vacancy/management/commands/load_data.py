import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from faker import Faker
from django.contrib.auth import get_user_model
from vacancy.models import JobVacancy, Application

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with 10 fake job vacancies and applications'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("No users found in the database. Create some users first."))
            return

        job_types = ['FULL_TIME', 'PART_TIME', 'INTERNSHIP']

        for _ in range(10):
            job = JobVacancy.objects.create(
                title=fake.job(),
                description=fake.paragraph(nb_sentences=5),
                job_type=random.choice(job_types),
                is_open=random.choice([True, False]),
                posted_by=random.choice(users),
                posted_on=now(),
                application_deadline=now() + timedelta(days=random.randint(10, 60)),
                salary=fake.random_int(min=30000, max=120000, step=5000),
                location=fake.city(),
                skills_required=", ".join(fake.words(nb=5))
            )

            # Creating fake applications for the job

        self.stdout.write(self.style.SUCCESS('Successfully added 10 job vacancies with applications!'))
