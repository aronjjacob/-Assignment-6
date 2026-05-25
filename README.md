# Photo Album Management System

A production-ready Django web application for managing photo albums with secure user authentication, cloud-based image storage, and comprehensive role-based access control. The application is designed to be deployed on Render.com with PostgreSQL and scales efficiently for multiple users.

## Overview

This project demonstrates enterprise-level Django development practices including proper authentication patterns, database design, cloud integration, and deployment best practices. Users can create albums, upload photos to the cloud, manage their profiles, and maintain complete control over their content through a permissions-based system.

## Features

### Core Functionality
- **User Authentication & Authorization** - Secure registration, login, logout, and password recovery
- **Album Management** - Create, edit, and delete photo albums with custom descriptions
- **Photo Upload** - Upload photos directly to Cloudinary cloud storage with automatic optimization
- **User Profiles** - Customizable user profiles with bio and avatar support
- **Role-Based Access Control** - Permissions system ensures users can only access their own content
- **Password Recovery** - Email-based password reset with secure token validation
- **Email Integration** - Automated email notifications for authentication events

### Technical Features
- **Class-Based Views** - Leverages Django's built-in generic views for cleaner, more maintainable code
- **Form Validation** - Comprehensive client and server-side form validation
- **Database Optimization** - Efficient queries with proper indexing and relationships
- **Static File Handling** - WhiteNoise integration for serving CSS, JavaScript, and images
- **Environment Configuration** - Separate settings for development, testing, and production
- **Security Hardening** - CSRF protection, XSS prevention, SQL injection protection, and secure headers

### Technology Stack
- **Framework**: Django 6.0.5
- **Database**: PostgreSQL (SQLite for development)
- **Cloud Storage**: Cloudinary
- **Application Server**: Gunicorn
- **Web Server**: Whitenoise (serves static files)
- **Deployment Platform**: Render.com
- **Python Version**: 3.11 or higher
- **Package Management**: pip with requirements.txt

## Getting Started

### Prerequisites
Before starting, ensure you have the following installed on your system:
- Python 3.11 or later
- Git for version control
- A text editor or IDE (VS Code, PyCharm, etc.)
- A Cloudinary account (free tier available at cloudinary.com)
- PostgreSQL (optional for local development - SQLite works locally)

### Initial Setup

1. **Clone the repository and navigate to the project**
   ```bash
   git clone <your-repo-url>
   cd cloud-render
   ```

2. **Create and activate a Python virtual environment**
   
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   On macOS and Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install project dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root directory:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your configuration. For local development, use these values:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
   CLOUDINARY_API_KEY=your-cloudinary-api-key
   CLOUDINARY_API_SECRET=your-cloudinary-api-secret
   ```
   
   To generate a secure SECRET_KEY:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Initialize the database**
   ```bash
   python manage.py migrate
   ```

6. **Create an administrator account**
   ```bash
   python manage.py createsuperuser
   ```
   
   Follow the prompts to enter your desired username, email, and password.

7. **Collect static files (CSS, JavaScript, images)**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   
   The application will be available at `http://127.0.0.1:8000/`

## Application Usage Guide

### User Registration and Authentication

Users start by creating an account through the registration page. New registrations require a unique username and valid email address. The authentication system uses Django's built-in user model with additional profile information stored in the UserProfile model.

- **Registration**: `/accounts/register/` - Create a new account
- **Login**: `/accounts/login/` - Sign in with username and password
- **User Profile**: `/accounts/profile/` - View and edit profile information
- **Password Reset**: `/accounts/password-reset/` - Initiate password recovery process
- **Logout**: Link in navigation menu

### Managing Albums

Once logged in, users can manage their photo albums. The album system provides basic organizational structure for grouping related photos. Each album has a title, optional description, and tracks creation and modification dates.

- **View All Albums**: `/gallery/` - Display list of all personal albums
- **Create Album**: `/gallery/album/create/` - Create new album with title and description
- **Album Details**: `/gallery/album/<id>/` - View all photos within an album
- **Edit Album**: `/gallery/album/<id>/edit/` - Update album title or description
- **Delete Album**: `/gallery/album/<id>/delete/` - Remove album (deletes all contained photos)

### Managing Photos

Photos are uploaded to Cloudinary and linked to specific albums. The photo management interface allows uploading, editing metadata, and deletion.

- **Upload Photo**: `/gallery/photo/create/` - Add new photo to selected album
- **View Photo**: `/gallery/photo/<id>/` - Display full-size photo with details
- **Edit Photo**: `/gallery/photo/<id>/edit/` - Update photo title and description
- **Delete Photo**: `/gallery/photo/<id>/delete/` - Remove photo from Cloudinary and database

## Deploying to Render.com

### Prerequisites for Production Deployment

Before deploying, you need accounts and credentials for the following services:

- **GitHub Account** - Repository must be pushed to GitHub
- **Render.com Account** - Free tier available at render.com
- **Cloudinary Account** - Retrieve API credentials from your dashboard
- **Gmail Account** (optional) - For email-based password reset notifications
- **PostgreSQL Database** - Render provides free tier databases

### Step-by-Step Deployment Process

**Step 1: Prepare Your GitHub Repository**

Ensure all code changes are committed and pushed to your main branch:

```bash
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

**Step 2: Create a PostgreSQL Database on Render**

1. Log in to your Render.com account
2. Click "New +" in the dashboard
3. Select "PostgreSQL" from the options
4. Configure your database:
   - Provide a descriptive name
   - Select a region closest to your users
   - Choose the free tier
5. Create the database and copy the internal database URL from the connection string

**Step 3: Create a Web Service**

1. In Render dashboard, click "New +" 
2. Select "Web Service"
3. Connect your GitHub repository by clicking "Connect account" if needed
4. Select the repository containing your project
5. Configure the web service settings

**Step 4: Configure Build and Start Commands**

In the web service creation form, set the following:

Build Command:
```bash
./build.sh
```

Start Command:
```bash
gunicorn recipe_project.wsgi:application
```

These commands are already configured in the repository, but verify they match your project structure.

**Step 5: Add Environment Variables**

In the Environment section of your Render web service, add all required environment variables:

```
SECRET_KEY=<generate-new-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=<copy-from-postgresql-connection-string>
CLOUDINARY_CLOUD_NAME=<your-cloudinary-account-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your-gmail-address>
EMAIL_HOST_PASSWORD=<your-app-specific-password>
```

**Generating a Production SECRET_KEY:**

Run this command locally and paste the output as the SECRET_KEY value:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Gmail App Specific Password:**

For production email notifications:
1. Enable 2-factor authentication on your Gmail account
2. Visit https://myaccount.google.com/apppasswords
3. Select "Mail" and "Other (custom name)"
4. Create an app password and use it as EMAIL_HOST_PASSWORD

**Step 6: Deploy the Application**

1. Review all settings one final time
2. Click "Create Web Service"
3. Render will automatically start building and deploying your application
4. Monitor the deployment progress in the Render dashboard logs

The deployment typically takes 2-5 minutes. Once complete, your app will be accessible at your assigned Render URL.

**Step 7: Post-Deployment Setup**

After successful deployment, you need to set up the superuser account:

1. Open the Render web service dashboard
2. Navigate to the "Shell" tab
3. Run the following command:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create your admin account

Your application is now live. Access it at:
- Main application: `https://your-app-name.onrender.com/`
- Admin panel: `https://your-app-name.onrender.com/admin/`

## Database Design

The application uses a normalized database schema with three primary models connected through relationships:

### User Model (Django Built-in)
The standard Django User model handles basic authentication with fields for username, password, email, and account status. This model is extended with a one-to-one relationship to UserProfile.

### UserProfile Model
This custom model extends the built-in User model with additional user-specific information:
- **bio** - Short biography or description (optional)
- **avatar** - URL to user's profile picture (stored via Cloudinary)
- **created_at** - Account creation timestamp
- **updated_at** - Last profile modification timestamp

### Album Model
Represents a collection of photos grouped by topic or time period:
- **name** - Album title (required, max 200 characters)
- **description** - Detailed album information (optional)
- **owner** - Foreign key to User (who created the album)
- **created_at** - When the album was created
- **updated_at** - Last modification timestamp

Access control is enforced at the view level, ensuring users can only view, edit, or delete their own albums.

### Photo Model
Individual photo records with metadata and storage references:
- **title** - Photo name or caption (required)
- **description** - Additional details about the photo (optional)
- **image** - Reference to image stored on Cloudinary
- **album** - Foreign key to Album (which album contains this photo)
- **owner** - Foreign key to User (who uploaded it)
- **uploaded_at** - Timestamp when photo was added
- **updated_at** - Last metadata modification timestamp

Deleting an album cascades to delete all associated photos from both the database and Cloudinary.

## Security Implementation

The application implements multiple layers of security following Django best practices and OWASP guidelines:

### Authentication & Authorization
- **Password Hashing** - Passwords use PBKDF2 with SHA256 (Django's default), making brute force attacks computationally expensive
- **Session Management** - Secure session cookies with HTTP-only and secure flags enabled in production
- **Login Required** - LoginRequiredMixin ensures all album and photo views require authenticated users
- **Object-Level Permissions** - UserPassesTestMixin enforces that users can only access their own content
- **Password Reset** - Token-based password recovery with time-limited reset links

### Data Protection
- **CSRF Tokens** - All forms include Django's cross-site request forgery tokens
- **SQL Injection Prevention** - Database queries use Django ORM parameterized queries, preventing SQL injection
- **XSS Protection** - Template auto-escaping sanitizes all user-provided content displayed in HTML
- **Secure Headers** - Production configuration includes X-Frame-Options, X-Content-Type-Options, and other security headers

### Data Validation
- **Form Validation** - Server-side validation on all user inputs (forms handle image types, sizes, etc.)
- **File Type Checking** - Image uploads validated to prevent malicious file types
- **Rate Limiting** - Django's throttling can be configured to prevent brute force attacks

### Secrets Management
- **Environment Variables** - All sensitive data (SECRET_KEY, API keys) stored in .env, never committed to repository
- **Conditional Settings** - Debug mode and allowed hosts change based on environment
- **Production Hardening** - DEBUG disabled, secure cookie flags enabled, HTTPS enforced when DEBUG=False

### Infrastructure Security
- **Static File Serving** - WhiteNoise serves static files securely without requiring separate web server configuration
- **HTTPS in Production** - Render automatically provides HTTPS with valid certificates
- **Database Security** - PostgreSQL connections use encrypted credentials; never store plaintext passwords in code

## API Routes and URL Mapping

The application uses Django's URL routing system. All URLs are structured around two main apps: accounts (authentication) and gallery (photo management).

| HTTP Method | URL Path | View | Purpose | Authentication |
|-------------|----------|------|---------|-----------------|
| GET | `/` | TemplateView | Application homepage | Optional |
| GET | `/accounts/register/` | CreateView | User registration form | Not required |
| POST | `/accounts/register/` | CreateView | Process registration | Not required |
| GET | `/accounts/login/` | LoginView | User login form | Not required |
| POST | `/accounts/login/` | LoginView | Process login | Not required |
| GET | `/accounts/logout/` | LogoutView | End user session | Required |
| GET | `/accounts/profile/` | DetailView | View user profile | Required |
| GET | `/accounts/profile/edit/` | UpdateView | Edit profile form | Required |
| POST | `/accounts/profile/edit/` | UpdateView | Save profile changes | Required |
| GET | `/accounts/password-reset/` | PasswordResetView | Password reset request form | Not required |
| POST | `/accounts/password-reset/` | PasswordResetView | Send reset email | Not required |
| GET | `/gallery/` | ListView | View all user albums | Required |
| POST | `/gallery/` | CreateView | Create new album | Required |
| GET | `/gallery/album/<id>/` | DetailView | View album and its photos | Required |
| GET | `/gallery/album/<id>/edit/` | UpdateView | Edit album form | Required |
| POST | `/gallery/album/<id>/edit/` | UpdateView | Save album changes | Required |
| GET | `/gallery/album/<id>/delete/` | DeleteView | Confirm album deletion | Required |
| POST | `/gallery/album/<id>/delete/` | DeleteView | Delete album and photos | Required |
| GET | `/gallery/photo/<id>/` | DetailView | View single photo | Required |
| GET | `/gallery/photo/<id>/edit/` | UpdateView | Edit photo form | Required |
| POST | `/gallery/photo/<id>/edit/` | UpdateView | Save photo changes | Required |
| GET | `/gallery/photo/<id>/delete/` | DeleteView | Confirm photo deletion | Required |
| POST | `/gallery/photo/<id>/delete/` | DeleteView | Delete photo | Required |
| GET/POST | `/gallery/photo/create/` | CreateView | Upload new photo form | Required |

## Troubleshooting Common Issues

### Static Files Not Displaying in Production

Symptom: CSS stylesheets and images appear broken after deploying to Render.

Solution:
```bash
python manage.py collectstatic --clear --noinput
```

Then redeploy your application. WhiteNoise will serve the collected static files automatically. Verify that DEBUG=False in your production environment settings.

### Database Connection Failures

Symptom: `OperationalError: could not connect to server`

Possible causes and solutions:
- Verify DATABASE_URL format matches: `postgresql://username:password@host:port/database`
- Check PostgreSQL database is running in Render dashboard (not suspended)
- Ensure DATABASE_URL environment variable is set correctly
- If migrating from SQLite to PostgreSQL, recreate the database with migrate command

### Cloudinary Upload Errors

Symptom: Photos fail to upload with authentication or timeout errors.

Solutions:
- Verify CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET are correct
- Check your Cloudinary account is active and hasn't exceeded upload limits
- Ensure Cloudinary credentials have upload permissions
- Check file size doesn't exceed Cloudinary limits (100 MB for free tier)
- Try uploading a small test image to verify connectivity

### Permission Denied Errors

Symptom: Users receive "permission denied" when trying to edit/delete albums or photos.

Causes and solutions:
- Ensure user is logged in (LoginRequiredMixin failing silently)
- Verify the object ownership - users can only edit their own content
- Check UserPassesTestMixin in views.py returns True for the current user
- Clear browser cache and cookies that may contain stale session data

### Email Not Sending for Password Reset

Symptom: Password reset emails don't arrive.

Solutions:
- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables are set
- For Gmail: enable 2-factor authentication and generate an app-specific password
- Check that DEBUG=False in production (email won't send with DEBUG=True locally)
- Verify EMAIL_HOST=smtp.gmail.com, EMAIL_PORT=587, EMAIL_USE_TLS=True
- Check spam/junk folders for reset emails
- Review Render logs for SMTP connection errors

### Application Crashes After Deploy

Symptom: App deploys but shows 500 error or crashes immediately.

Solutions:
- Check Render dashboard logs for specific error messages
- Verify all required environment variables are set (especially SECRET_KEY)
- Run migrations: `python manage.py migrate` via Render shell
- Check that build.sh exits without errors
- Ensure database URL is valid and database exists
- Verify ALLOWED_HOSTS includes your Render domain

## Project Structure

The codebase is organized following Django's recommended structure for scalability:

```
cloud-render/
├── accounts/                 # User authentication and profile management
│   ├── views.py             # Registration, login, profile views
│   ├── forms.py             # User and profile forms
│   ├── models.py            # User and UserProfile models
│   ├── urls.py              # Account-related URL patterns
│   └── templates/           # Account HTML templates
│
├── gallery/                 # Photo album management
│   ├── views.py             # Album and photo views (CBVs)
│   ├── forms.py             # Album and photo forms
│   ├── models.py            # Album, Photo models
│   ├── urls.py              # Gallery URL patterns
│   └── templates/           # Gallery HTML templates
│
├── recipe_project/          # Project configuration
│   ├── settings.py          # Django settings and configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI application entry point
│   └── asgi.py              # ASGI application entry point (for async)
│
├── templates/               # Project-wide HTML templates
│   ├── base.html            # Base template (extends across all pages)
│   └── accounts/, gallery/  # App-specific templates
│
├── manage.py                # Django command-line utility
├── requirements.txt         # Python package dependencies
├── build.sh                 # Build script for Render deployment
├── setup.sh                 # Local development setup script
├── render.yaml              # Render deployment configuration
├── db.sqlite3               # SQLite database (development only)
└── Procfile                 # Process definition for deployment
```

### Key Files Explained

- **settings.py** - Contains all Django configuration including database, installed apps, middleware, authentication, and email settings
- **manage.py** - Entry point for running Django commands like migrate, runserver, createsuperuser
- **requirements.txt** - Lists all Python packages needed to run the application
- **build.sh** - Runs during Render deployment to install dependencies and collect static files
- **render.yaml** - Specifies build steps and environment for Render platform

## Contributing to This Project

We welcome contributions from developers of all skill levels. Here's how to contribute:

1. **Fork or create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and test thoroughly**
   - Write clean, well-commented code
   - Follow Django coding style guidelines
   - Test your changes locally before committing

3. **Commit your changes with descriptive messages**
   ```bash
   git commit -m "Add brief description of your changes"
   ```

4. **Push your branch to the repository**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request with details about your changes**
   - Describe what you changed and why
   - Reference any related issues
   - Include screenshots if UI changes were made

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software. See the LICENSE file in the repository for full details.

## Resources and Documentation

For more information about the technologies used in this project:

- **Django Documentation** - https://docs.djangoproject.com/ (official Django framework documentation)
- **Cloudinary API Reference** - https://cloudinary.com/documentation (cloud image management)
- **Render Deployment Guide** - https://render.com/docs (deployment platform documentation)
- **PostgreSQL Manual** - https://www.postgresql.org/docs/ (database documentation)
- **Python Official Documentation** - https://docs.python.org/3/ (Python language reference)

## Production Status

This application is production-ready and implements all core requirements for a professional photo management system:

- Class-Based Views providing efficient, reusable CRUD operations
- Role-Based Access Control with secure authentication
- Cloudinary integration for scalable cloud image storage
- Environment-based configuration for multiple deployment scenarios
- PostgreSQL database support for production data integrity
- Deployment tested and verified on Render.com platform

Version: 1.0.0

Last Updated: May 2026
