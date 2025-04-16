# University Placement System

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

## Overview

The University Placement System is a comprehensive web-based platform designed to streamline the placement process for universities, organizations, and students. It facilitates efficient job matching, application management, and career development through an intuitive interface built with Django's powerful template architecture.

## Mission

To bridge the gap between academic institutions and industry by providing a seamless, efficient, and user-friendly platform that enhances the placement process, ultimately helping students secure meaningful employment opportunities and organizations find the right talent.

## Vision

To become the leading placement management system that revolutionizes how universities, organizations, and students interact during the recruitment process, creating a more transparent, efficient, and successful placement ecosystem.

## Goals

- **For Universities**: Streamline placement activities, manage organizations and student profiles, and track application progress.
- **For Organizations**: Efficiently post job vacancies, review applications, and select candidates that match their requirements.
- **For Students**: Access relevant job opportunities, submit applications, track application status, and receive personalized career guidance.
- **For the System**: Continuously improve user experience, enhance security, and incorporate advanced features like ATS resume analysis.

## Features

### For Universities (Super Admin)
- **Placement Event Management**: Create, update, and delete placement events with detailed information.
- **Organization Management**: Invite, approve, and manage organizations that can post job vacancies.
- **Student Management**: Create and manage student accounts with comprehensive profiles.
- **Application Monitoring**: Track and analyze applications submitted by students for various job vacancies.
- **Analytics Dashboard**: View placement statistics, success rates, and trends.

### For Organizations
- **Job Posting**: Create and manage job vacancies (Full Time, Part Time, Internship) with detailed requirements.
- **Application Review**: Access and review applications submitted by students for their job postings.
- **Candidate Selection**: Accept or reject applications with personalized feedback.
- **Profile Management**: Maintain and update organization profiles and preferences.

### For Students
- **Job Search**: Browse and search for job vacancies based on various criteria.
- **Application Submission**: Apply for job vacancies with resume uploads and cover letters.
- **Application Tracking**: Monitor the status of applications (Pending, Accepted, Rejected).
- **ATS Resume Analysis**: Get AI-powered feedback on resume optimization for specific job descriptions.
- **Career Dashboard**: View application history, upcoming interviews, and placement statistics.

## Technologies Used

### Backend
- **Django**: A high-level Python web framework for rapid development and clean design.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **Django Template Language**: For creating dynamic, reusable HTML templates.
- **PostgreSQL**: A powerful, open-source relational database system.
- **LangChain & Gemini API**: For AI-powered resume analysis and feedback.

### Frontend
- **Bootstrap**: For responsive, mobile-first frontend design.
- **JavaScript**: For interactive user interface elements.
- **HTML/CSS**: For structured and styled web pages.

### Other Tools
- **Docker**: For containerization and easy deployment.
- **Git**: For version control.
- **GitHub Actions**: For CI/CD pipelines.

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Docker (optional)

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/university-placement-system.git
   cd university-placement-system
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   - Update the `DATABASES` configuration in `settings.py` with your PostgreSQL credentials.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Set up environment variables**:
   - Create a `.env` file in the root directory with the following variables:
     ```
     SECRET_KEY=your_secret_key
     DEBUG=True
     DATABASE_URL=postgres://user:password@localhost:5432/dbname
     GEMINI_API_KEY=your_gemini_api_key
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback/
     ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Backend: `http://localhost:8000`
   - Admin Panel: `http://localhost:8000/admin`

## Usage

### Admin Panel
- Access the Django admin panel at `http://localhost:8000/admin`.
- Log in with the superuser credentials created during setup.
- Manage organizations, students, job vacancies, and applications.

### Student Portal
- Students can register and log in to access job listings.
- They can apply for jobs, track application status, and use the ATS resume analysis tool.

### Organization Portal
- Organizations can log in to post job vacancies and manage applications.
- They can review student profiles and update application statuses.

## Project Structure

```
university-placement-system/
├── authuser/              # User authentication and management
├── vacancy/               # Job vacancy and application management
├── utils/                 # Utility functions and helpers
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Project dependencies
```

## Future Enhancements

- **Advanced Analytics**: Implement more sophisticated analytics for placement trends.
- **Interview Scheduling**: Add functionality for scheduling and managing interviews.
- **Mobile Application**: Develop a mobile app for easier access on the go.
- **AI-Powered Job Matching**: Enhance the system with AI algorithms for better job-student matching.
- **Integration with Learning Management Systems**: Connect with university LMS for seamless data flow.

## Acknowledgments

- Django community for their excellent documentation and support.
- PostgreSQL for being a reliable and scalable database.
- Google for providing the Gemini API for AI-powered resume analysis.
- All contributors and testers who have helped improve the system.

---

Thank you for exploring the University Placement System! 🚀