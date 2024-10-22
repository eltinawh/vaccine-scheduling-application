# Vaccine Scheduling Application

This Django website aims to bridge the potential patients with hospitals or health centers for vaccination to occur. Vaccination is really important for our collective health, especially for babies and younger children since their immune system is not very developed yet.

Users of the website will have one of these three roles:
- Admin. Admin has full access to the database. He will help assign users from health centers into administrative roles.
- Agent. Agent is responsible for the administration of the vaccination center, vaccine storage/stock, and vaccination campaign. 
- Patient. Patients can choose the vaccination schedule from the available centers and available campaign slots. They can download the vaccination appointment after confirming the schedule and then download the vaccination certificate after getting vaccinated.

## Key Features

### 1. User Authentication & Authorization
- **Description:** Secure login and registration system for users
- **Technologies Used:** 
  - Django's built-in authentication system
  - Python package pillow to handle ImageField for profile picture
  - Django's Signal to delete old profile picture when uploading a new one
- **Functionality:** 
  - User registration with email verification (currently using console backend)
  - Password reset functionality
  - User profile management with capability to upload profile picture
  - Authorization: controls access to various parts of the application based on user roles or permissions
    - Defines what authenticated users can and cannot do within the app

### 2. Database Management
- **Description:** Efficient data handling and storage
- **Technologies Used:** SQLite
- **Functionality:**
  - Migration management for easy updates
  - Support for complex queries and relationships

### 3. Admin Dashboard
- **Description:** Intuitive admin interface for managing application data
- **Technologies Used:** Django Admin
- **Functionality:** 
  - User permissions management
  - 

### 4. PDF Generation for Appointment Letters and Vaccination Certificates
- **Description:** Automatically generates official appointment letters and vaccination certificates in PDF format for patient users
- **Technologies Used:** ReportLab for PDF generation
- **Functionality:**
  - **Appointment Letters:** Users receive a personalized appointment letter upon scheduling their vaccination, ensuring they have all necessary details for their visit.
  - **Vaccination Certificates:** After completing their vaccination, users can download a vaccination certificate, which can be used for travel, employment, or health-related requirements.
  - **Easy Access:** Users can access and download their documents directly from their personal vaccination page.


## Demo
Deployed using Gunicorn and Nginx on AWS EC2 instance: http://18.143.77.255/

If you want to try out, you can use these credentials.

As an agent
- Username: lisa.sane@email.com
- Password: spreadHealth@707


As a patient
- Username: peter.forte@email.com
- Password: getVaccinated@102

## Local Development

The following instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites
Before you begin, make sure you have the following installed:
- Python 3.11 or higher
- pip (Python package installer)
- venv (Python virtual environment manager)
- git (version control system)

### Installation instruction

#### 1. Clone the repository
```bash
git clone https://github.com/eltinawh/vaccine-scheduling-application.git

# navigate to the project directory
cd vaccine-scheduling-application
```

#### 2. Set up a virtual environment
```bash
# Create a virtual environment
python3 -m venv env

# Activate the virtual environment (Linux/MacOS)
source env/bin/activate

# Activate the virtual environment (Windows)
env\Scripts\activate
```

#### 3. Install dependencies
```bash
cd vaccine_site
pip install -r requirements.txt
```

#### 4. Create a .env file for environment variables
Generate a new Django secret key
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
```

Create a `.env` file and copy these values in that file.
```
debug=False
SECRET_KEY=[some_secret_key_you_get_from_previous_step]
```

#### 5. Apply migrations

Run the following commands to create the necessary database tables 
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create a superuser

To access the Django admin panel, create a superuser account:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up the admin credentials.

#### 7. Run the development server

Start the development server to verify everything is working correctly.
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser to see the application.

## Technical Details

### Project Structure
This project consists of the following apps, each handling distinct functionalities within the vaccine scheduling system:

1. **User App**
   - **Purpose:** Manages user authentication and profiles.
   - **Routing:** Handles routes for user registration/signup, login, logout, password change, profile view, profile update, and email verification.

2. **Center App**
   - **Purpose:** Manages vaccination center, storage and inventory of vaccines within a given center.
   - **Routing:** Handles routes for adding, updating, retrieving, and deleting vaccination centers, tracking vaccine stock levels and updates.
   - **Glossary**:
     - Center: hospital or clinic where vaccination can occur
     - Storage: a storage for a certain vaccine in a center

3. **Vaccine App**
   - **Purpose:** Manages vaccine information.
   - **Routing:** Handles routes for adding, updating, retrieving, and deleting vaccines.

4. **Campaign App**
   - **Purpose:** Manages vaccination campaigns and campaign slots.
   - **Routing:** Handles routes for creating and managing campaigns and slots.
   - **Glossary**: 
     - Campaign: a vaccination campaign with a certain vaccine in a certain center that can span multiple days.
     - Slot: specific hour(s) in a day associated with a vaccination campaign from which a patient user can schedule vaccination.

5. **Vaccination App**
   - **Purpose:** Manages vaccination scheduling and record.
   - **Routing:** Handles routes for choosing vaccine, campaign, and slot for vaccination scheduling and routes for generating appointment letters and certificates.

### Entity Relationship Diagram (ERD)

To help us understand about the relationship between application models, here is the [ERD](https://dbdiagram.io/d/vaccine_scheduling_application-66e92c206dde7f4149544e4c). Details can be found in [database.dbml](vaccine_site/database.dbml) file. 

![Entity Relationship Diagram](/assets/00_ERD.png)

### Class-Based Generic Views
- **Description:** The project utilizes Django's class-based generic views to streamline the development of views.
- **Benefits:**
  - **Reusability:** Common patterns are encapsulated in CBVs, reducing code duplication.
  - **Maintainability:** Easier to manage and extend views as the project grows.
  - **Readability:** Enhances the organization of view logic, making it easier for developers to understand the flow of the application.

## Potential Improvements

- Change the database to PostgreSQL
- Change verify email from console backend to real emailing service
- Deploy using `https` instead of `http`

## Documentation

[Official Django Documentation](https://www.djangoproject.com/)