# University Placement System

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white)

The University Placement System is a web-based platform designed to help universities manage placement activities efficiently. It allows universities to post placement news, invite organizations to post job vacancies, and enable students to apply for these jobs. The system is built using Django for the backend and React for the frontend.



## Features

### For Universities (Super Admin)
- Manage Placement Events: Create, update, and delete placement events.
- Manage Organizations: Create and manage organizations that can post job vacancies.
- Manage Students: Create and manage student accounts.
- View Applications: Monitor applications submitted by students for job vacancies.

### For Organizations
- Post Job Vacancies: Create and manage job vacancies (Full Time, Part Time, Internship).
- View Applications: See applications submitted by students for their job vacancies.
- Update Application Status: Accept or reject student applications.

### For Students
- Apply for Jobs: Submit applications for job vacancies.
- View Application Status: Track the status of their applications (Pending, Accepted, Rejected).



## Technologies Used

### Backend
- Django: A high-level Python web framework for rapid development.
- Django REST Framework (DRF): A powerful toolkit for building Web APIs.
- Django CKEditor 5: A rich text editor for Django models.
- PostgreSQL: A powerful, open-source relational database system.

### Other Tools
- Docker: For containerization and easy deployment.
- Git: For version control.
- GitHub Actions: For CI/CD pipelines.

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL
- Docker (optional)

### Backend Setup

1. Clone the repository:


2. Create a virtual environment:
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install dependencies:
   bash
   pip install -r requirements.txt


4. Set up the database:
   - Update the `DATABASES` configuration in `settings.py` with your PostgreSQL credentials.
   - Run migrations:
     bash
     python manage.py migrate


5. Create a superuser:
   bash
   python manage.py createsuperuser


6. Run the development server:
   bash
   python manage.py runserver


## Usage

### Admin Panel
- Access the Django admin panel at `http://localhost:8000/admin`.
- Log in with the superuser credentials created during setup.
- Manage organizations, students, job vacancies, and applications.


3. Access the application:
   - Backend: `http://localhost:8000`



## Acknowledgments
- Django and React communities for their amazing documentation and support.
- CKEditor 5 for providing a rich text editor.
- PostgreSQL for being a reliable and scalable database.


Thank you for checking out the University Placement System! 🚀