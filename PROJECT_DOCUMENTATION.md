# Photo Album Management System - Project Documentation

## Executive Summary

The Photo Album Management System is a production-ready Django web application that enables users to create, manage, and organize photo albums with cloud-based image storage. Built with Django 6.0.5, the application leverages PostgreSQL for data persistence, Cloudinary for image hosting, and is optimized for deployment on Render.com.

**Key Statistics:**
- Framework: Django 6.0.5
- Database: PostgreSQL (SQLite for development)
- Cloud Storage: Cloudinary
- Python Version: 3.11+
- Total Dependencies: 19 packages

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Core Features](#core-features)
5. [Database Design](#database-design)
6. [Installation & Setup](#installation--setup)
7. [Development Guide](#development-guide)
8. [Deployment Guide](#deployment-guide)
9. [API & Views Documentation](#api--views-documentation)
10. [Security Considerations](#security-considerations)
11. [Troubleshooting](#troubleshooting)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer (Browser)                    │
│                 HTML/CSS/JavaScript Frontend                │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│                 Django Application Server                    │
│         (Gunicorn WSGI server running on Render)            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  URLs Router → Views (CBV) → Forms → Templates       │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │ Accounts App    │ Gallery App               │    │   │
│  │  │ - Register      │ - Album CRUD              │    │   │
│  │  │ - Login         │ - Photo CRUD              │    │   │
│  │  │ - Profile       │ - Cloud Upload            │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼────────┐ ┌──▼──────────────┐
│  PostgreSQL  │ │ Cloudinary  │ │ Email Service  │
│   Database   │ │   Storage   │ │  (SMTP)        │
└──────────────┘ └─────────────┘ └────────────────┘
```

### Application Flow

1. **User Access**: User browses to the application URL
2. **Authentication**: Django authenticates the user or redirects to login
3. **Request Processing**: URL router directs request to appropriate view
4. **View Logic**: Class-based view processes the request
5. **Database Query**: ORM queries PostgreSQL database
6. **File Operations**: If needed, upload/serve files via Cloudinary
7. **Template Rendering**: Server renders HTML template with context data
8. **Response**: HTML sent back to client browser

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Django | 6.0.5 | Web framework |
| Python | 3.11+ | Programming language |
| PostgreSQL | Latest | Production database |
| SQLite3 | - | Development database |
| Gunicorn | 26.0.0 | WSGI application server |

### Frontend
| Technology | Purpose |
|---|---|
| HTML5 | Markup structure |
| CSS3 | Styling and layout |
| Bootstrap | Responsive design framework |
| JavaScript | Client-side interactivity |

### Cloud Services
| Service | Purpose |
|---|---|
| Cloudinary | Image storage and optimization |
| Render.com | Application hosting |

### Key Dependencies
```
asgiref==3.11.1              # ASGI utilities
Django==6.0.5                # Web framework
django-cloudinary-storage    # Cloudinary integration
cloudinary==1.44.2           # Cloudinary API client
psycopg2-binary==2.9.12     # PostgreSQL adapter
dj-database-url==3.1.2      # Database URL parsing
python-dotenv==1.2.2         # Environment variable management
pillow==12.2.0               # Image processing
whitenoise==6.12.0           # Static file serving
gunicorn==26.0.0             # WSGI server
```

---

## Project Structure

```
cloud-render/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── build.sh                       # Build script for Render
├── setup.sh                       # Local setup script
├── render.yaml                    # Render deployment config
├── Procfile                       # Process management
├── db.sqlite3                     # Development database
├── README.md                      # README file
├── QUICKSTART.md                  # Quick start guide
│
├── recipe_project/                # Main Django project
│   ├── __init__.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # URL configuration
│   ├── wsgi.py                   # WSGI configuration
│   └── asgi.py                   # ASGI configuration
│
├── accounts/                      # User authentication app
│   ├── models.py                 # UserProfile model
│   ├── views.py                  # Auth views (Register, Login, Profile)
│   ├── forms.py                  # Registration & profile forms
│   ├── urls.py                   # Auth URL patterns
│   ├── admin.py                  # Admin configuration
│   ├── apps.py                   # App configuration
│   ├── migrations/               # Database migrations
│   └── templates/accounts/       # Auth templates
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── profile_edit.html
│       └── password_reset*.html
│
├── gallery/                       # Photo gallery app
│   ├── models.py                 # Album & Photo models
│   ├── views.py                  # Gallery CRUD views
│   ├── forms.py                  # Album & Photo forms
│   ├── urls.py                   # Gallery URL patterns
│   ├── admin.py                  # Admin configuration
│   ├── apps.py                   # App configuration
│   ├── migrations/               # Database migrations
│   └── templates/gallery/        # Gallery templates
│       ├── album_list.html
│       ├── album_detail.html
│       ├── album_form.html
│       ├── photo_form.html
│       └── photo_detail.html
│
└── templates/                     # Project-wide templates
    ├── base.html                 # Base template
    ├── index.html                # Home page
    └── base/                     # Base templates
        └── base.html
```

---

## Core Features

### 1. User Authentication & Authorization
**Location**: `accounts/` app

**Features:**
- User registration with email validation
- Secure login/logout functionality
- Password hashing using Django's security middleware
- Password reset via email tokens
- Session-based authentication
- Login required mixins for protected views

**Key Components:**
- `RegisterView`: Handles user registration
- `ProfileView`: Displays user profile and statistics
- `ProfileUpdateView`: Allows users to update their profile
- Built-in Django authentication system

### 2. Album Management
**Location**: `gallery/` app → `Album` model

**Features:**
- Create personal photo albums
- Edit album details (name, description)
- Delete albums with confirmation
- View all personal albums with pagination
- Automatic timestamps (created_at, updated_at)
- Unique album names per user (no duplicate album names)

**Key Components:**
- `AlbumListView`: Lists all user's albums
- `AlbumCreateView`: Create new album
- `AlbumDetailView`: View album details and photos
- `AlbumUpdateView`: Edit album information
- `AlbumDeleteView`: Delete album with confirmation

**Permissions:**
- Only album owner can view details
- Only album owner can edit/delete
- Django's UserPassesTestMixin enforces ownership

### 3. Photo Upload & Management
**Location**: `gallery/` app → `Photo` model

**Features:**
- Upload photos directly to Cloudinary cloud storage
- Store metadata (title, description, upload date)
- Automatic image optimization by Cloudinary
- Edit photo details after upload
- Delete photos with confirmation
- Photo count tracking per album

**Key Components:**
- `PhotoCreateView`: Upload new photo to album
- `PhotoDetailView`: View photo with metadata
- `PhotoUpdateView`: Edit photo details
- `PhotoDeleteView`: Delete photo from album
- Cloudinary integration for image hosting

**Technical Details:**
- Uses CloudinaryField for automatic image handling
- Images stored at CDN for fast global delivery
- Automatic responsive image generation

### 4. User Profiles
**Location**: `accounts/` app → `UserProfile` model

**Features:**
- Extended user profile with bio and avatar
- Profile picture support via URL
- User statistics (album count, photo count)
- Profile editing capability

**Data Structure:**
```
UserProfile
├── user (OneToOne relationship with User)
├── bio (TextField)
├── avatar (URLField)
├── created_at (DateTimeField)
└── updated_at (DateTimeField)
```

### 5. Role-Based Access Control
**Implemented Via:**
- Django's built-in User model
- Custom permission checks using UserPassesTestMixin
- Owner verification on all CRUD operations

**Access Rules:**
- Unauthenticated users: See login page
- Authenticated users: Can only see/edit their own content
- Superusers: Full access via Django admin

---

## Database Design

### Entity Relationship Diagram

```
User (Django Built-in)
├── albums (ForeignKey)
├── photos (ForeignKey)
└── profile (OneToOne) ──→ UserProfile

Album
├── owner (ForeignKey → User)
├── photos (ForeignKey reverse)
└── Constraints: Unique(owner, name)

Photo
├── album (ForeignKey → Album)
├── owner (ForeignKey → User)
└── image (CloudinaryField)

UserProfile
└── user (OneToOne → User)
```

### Database Tables

#### 1. auth_user (Django Built-in)
| Field | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| username | CharField | Unique username |
| email | EmailField | User email |
| password | CharField | Hashed password |
| first_name | CharField | User's first name |
| last_name | CharField | User's last name |
| is_active | Boolean | Account active status |
| is_staff | Boolean | Staff privileges |
| is_superuser | Boolean | Admin privileges |
| date_joined | DateTime | Account creation date |
| last_login | DateTime | Last login timestamp |

#### 2. gallery_album
| Field | Type | Constraints |
|---|---|---|
| id | Integer | Primary key |
| name | CharField(200) | Album name |
| description | TextField | Album description |
| owner_id | Integer | ForeignKey → User |
| created_at | DateTime | Auto-set on creation |
| updated_at | DateTime | Auto-updated |

**Indexes**: `owner_id`, `created_at`
**Unique**: `(owner_id, name)`

#### 3. gallery_photo
| Field | Type | Constraints |
|---|---|---|
| id | Integer | Primary key |
| title | CharField(200) | Photo title |
| description | TextField | Photo description |
| image | CloudinaryField | Cloudinary image URL |
| album_id | Integer | ForeignKey → Album |
| owner_id | Integer | ForeignKey → User |
| uploaded_at | DateTime | Auto-set on creation |
| updated_at | DateTime | Auto-updated |

**Indexes**: `album_id`, `owner_id`, `uploaded_at`

#### 4. accounts_userprofile
| Field | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | OneToOne → User |
| bio | TextField | User biography |
| avatar | URLField | Avatar image URL |
| created_at | DateTime | Auto-set on creation |
| updated_at | DateTime | Auto-updated |

**Relationship**: One UserProfile per User (enforced by OneToOne)

---

## Installation & Setup

### Prerequisites

Before starting development, ensure you have:
- Python 3.11 or higher
- Git for version control
- pip (Python package manager)
- A text editor or IDE (VS Code recommended)
- Cloudinary account (free tier at cloudinary.com)
- PostgreSQL client (psycopg2) or SQLite (included with Python)

### Local Development Setup

#### Step 1: Clone Repository
```bash
git clone <repository-url>
cd cloud-render
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Environment Configuration
Create `.env` file in project root:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

Generate a secure SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Step 5: Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Create test data (optional)
python manage.py shell
```

#### Step 6: Run Development Server
```bash
python manage.py runserver
```

Access at: `http://localhost:8000`

### Initial User Setup

```bash
# Create superuser
python manage.py createsuperuser --username admin --email admin@example.com

# Access admin panel
# Navigate to http://localhost:8000/admin
```

---

## Development Guide

### Running the Development Server

```bash
# Start development server
python manage.py runserver

# Specify custom port
python manage.py runserver 8080

# Make accessible to other machines on network
python manage.py runserver 0.0.0.0:8000
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test gallery

# Run with verbosity
python manage.py test -v 2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Database Migrations

```bash
# Create migration for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations

# Revert to previous migration
python manage.py migrate gallery 0001_initial
```

### Django Admin Interface

Access at: `/admin/`

**Built-in features:**
- User management
- Album management
- Photo management
- Permissions configuration

**Customized via**: `accounts/admin.py` and `gallery/admin.py`

### Creating Fixtures (Sample Data)

```bash
# Dump current database to JSON
python manage.py dumpdata > fixture.json

# Load fixture data
python manage.py loaddata fixture.json
```

### Shell Commands

```bash
# Open interactive Django shell
python manage.py shell

# Example commands:
from django.contrib.auth.models import User
from gallery.models import Album, Photo

# Create user
user = User.objects.create_user('testuser', 'test@example.com', 'password')

# Create album
album = Album.objects.create(name='My Album', owner=user)

# Query albums
albums = Album.objects.filter(owner=user)
```

---

## Deployment Guide

### Pre-Deployment Checklist

- [ ] `DEBUG=False` in production settings
- [ ] Secure `SECRET_KEY` generated and stored in environment
- [ ] `.env` file is in `.gitignore`
- [ ] All static files collected
- [ ] Database migrations applied
- [ ] Cloudinary credentials configured
- [ ] Email service configured (if needed)
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enforced
- [ ] CSRF and XSS protection enabled

### Deployment to Render.com

#### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard: https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure database:
   - **Name**: `photo-album-db`
   - **Database**: `photo_album`
   - **Region**: Select nearest region
   - **Plan**: Free or Standard
4. Copy the Internal Database URL (format: `postgresql://user:pass@host:port/dbname`)

#### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Click "Connect your own" repository
3. Select GitHub repository
4. Choose branch: `main`
5. Click "Connect"

#### Step 3: Configure Web Service

Set these deployment parameters:

| Setting | Value |
|---|---|
| **Name** | photo-album-manager |
| **Environment** | Python 3 |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn recipe_project.wsgi:application --bind 0.0.0.0:$PORT` |
| **Plan** | Free (testing) or Starter (production) |
| **Region** | Same as database |

#### Step 4: Add Environment Variables

In Render dashboard, add these environment variables:

```
SECRET_KEY=<your-generated-secret-key>
DEBUG=False
ALLOWED_HOSTS=photo-album-manager.onrender.com
DATABASE_URL=<your-internal-postgres-url>
CLOUDINARY_CLOUD_NAME=<your-cloudinary-cloud-name>
CLOUDINARY_API_KEY=<your-cloudinary-api-key>
CLOUDINARY_API_SECRET=<your-cloudinary-api-secret>
```

#### Step 5: Deploy

1. Commit and push code to GitHub
2. Render automatically triggers deployment from `build.sh`
3. Monitor deployment in Render dashboard
4. Access application at assigned URL

### Build Script (`build.sh`)

```bash
#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
```

### Post-Deployment Verification

```bash
# Check application health
curl https://your-app-url.onrender.com

# Check admin access
curl https://your-app-url.onrender.com/admin

# Monitor logs
# Via Render dashboard: Logs tab
```

### Production Best Practices

1. **Security**
   - Rotate SECRET_KEY regularly
   - Use strong, unique passwords
   - Enable 2FA on deployment platforms
   - Keep dependencies updated

2. **Performance**
   - Enable caching (Redis recommended)
   - Use CDN for static files (WhiteNoise handles this)
   - Implement database connection pooling
   - Monitor response times

3. **Monitoring**
   - Set up error tracking (Sentry recommended)
   - Monitor database performance
   - Track user activity and security events
   - Regular backup of database

4. **Scaling**
   - Vertical scaling: Increase Render plan
   - Horizontal scaling: Use load balancer
   - Optimize database queries
   - Implement caching strategies

---

## API & Views Documentation

### URL Patterns

#### Accounts App URLs (`accounts/urls.py`)

```
Path: accounts/
├── register/          → RegisterView (GET, POST)
├── login/             → Django's LoginView (GET, POST)
├── logout/            → Django's LogoutView (GET)
├── profile/           → ProfileView (GET)
├── profile/edit/      → ProfileUpdateView (GET, POST)
├── password_reset/    → Django's PasswordResetView
├── password_reset_done/
├── password_reset_confirm/
└── password_reset_complete/
```

#### Gallery App URLs (`gallery/urls.py`)

```
Path: /
├── albums/                    → AlbumListView (GET)
├── albums/create/             → AlbumCreateView (GET, POST)
├── albums/<int:pk>/           → AlbumDetailView (GET)
├── albums/<int:pk>/edit/      → AlbumUpdateView (GET, POST)
├── albums/<int:pk>/delete/    → AlbumDeleteView (GET, POST)
├── photos/<int:pk>/           → PhotoDetailView (GET)
├── photos/<int:pk>/edit/      → PhotoUpdateView (GET, POST)
├── photos/<int:pk>/delete/    → PhotoDeleteView (GET, POST)
└── photos/create/<int:album_pk>/  → PhotoCreateView (GET, POST)
```

### Views Documentation

#### Accounts App Views

**RegisterView**
- URL: `/accounts/register/`
- Method: GET, POST
- Requires Login: No
- Purpose: User registration
- Form: RegisterForm
- Success Redirect: Album list
- Features: Auto-creates UserProfile, auto-login after registration

**ProfileView**
- URL: `/accounts/profile/`
- Method: GET
- Requires Login: Yes
- Purpose: Display user profile and statistics
- Context:
  - `profile_user`: Current user object
  - `user_profile`: UserProfile instance
  - `albums_count`: Number of albums
  - `photos_count`: Number of photos

**ProfileUpdateView**
- URL: `/accounts/profile/edit/`
- Method: GET, POST
- Requires Login: Yes
- Purpose: Update user information
- Form: UserUpdateForm
- Success Redirect: Profile page

#### Gallery App Views

**AlbumListView**
- URL: `/albums/`
- Method: GET
- Requires Login: Yes
- Purpose: List user's albums
- Pagination: 12 albums per page
- Filtering: Only user's own albums
- Context: `albums` list

**AlbumCreateView**
- URL: `/albums/create/`
- Method: GET, POST
- Requires Login: Yes
- Purpose: Create new album
- Form: AlbumForm
- Success Redirect: Album detail page
- Auto-sets owner to logged-in user

**AlbumDetailView**
- URL: `/albums/<id>/`
- Method: GET
- Requires Login: Yes
- Permission: Album owner only
- Purpose: Display album details and photos
- Context:
  - `album`: Album object
  - `photos`: Related photos
  - `photo_form`: PhotoForm for new uploads

**AlbumUpdateView**
- URL: `/albums/<id>/edit/`
- Method: GET, POST
- Requires Login: Yes
- Permission: Album owner only
- Purpose: Edit album details
- Form: AlbumForm

**AlbumDeleteView**
- URL: `/albums/<id>/delete/`
- Method: GET, POST
- Requires Login: Yes
- Permission: Album owner only
- Purpose: Delete album
- Confirmation: Template confirmation required

**PhotoCreateView**
- URL: `/photos/create/<album_id>/`
- Method: GET, POST
- Requires Login: Yes
- Permission: Album owner only
- Purpose: Upload photo to album
- Form: PhotoForm
- Features: Cloudinary integration, automatic image optimization

**PhotoDetailView**
- URL: `/photos/<id>/`
- Method: GET
- Requires Login: Yes
- Permission: Photo owner only
- Purpose: Display photo with metadata
- Context: `photo` object with full details

**PhotoUpdateView**
- URL: `/photos/<id>/edit/`
- Method: GET, POST
- Requires Login: Yes
- Permission: Photo owner only
- Purpose: Edit photo metadata
- Form: PhotoForm
- Updateable: Title, description only (image cannot be changed)

**PhotoDeleteView**
- URL: `/photos/<id>/delete/`
- Method: GET, POST
- Requires Login: Yes
- Permission: Photo owner only
- Purpose: Delete photo
- Confirmation: Template confirmation required

### Form Documentation

#### RegisterForm (accounts/forms.py)
- Fields: username, email, password1, password2
- Validation: Password match, strength, complexity
- Custom validation: Unique username, valid email format

#### UserUpdateForm (accounts/forms.py)
- Fields: username, first_name, last_name, email
- Validation: Unique username (excluding current user)

#### AlbumForm (gallery/forms.py)
- Fields: name, description
- Validation: Max length 200 for name
- Auto-exclude: owner field

#### PhotoForm (gallery/forms.py)
- Fields: title, description, image, album
- Validation: Valid image format, max file size
- Album filtering: Only user's albums shown

---

## Security Considerations

### Authentication & Authorization

**Implemented Security Measures:**
1. **Password Security**
   - Hashed with PBKDF2 + SHA256
   - Minimum 8 characters required
   - Password confirmation validation
   - Password validators check:
     - Similarity to username
     - Common passwords
     - Entirely numeric passwords

2. **Login Security**
   - Session-based authentication
   - Automatic session timeout
   - Secure session cookies (HttpOnly, Secure flags)
   - Failed login attempt tracking (Django built-in)

3. **Permission System**
   - LoginRequiredMixin on all protected views
   - UserPassesTestMixin for ownership verification
   - Object-level permissions enforced in test_func()

### CSRF Protection

**Implementation:**
- `CsrfViewMiddleware` enabled in middleware
- CSRF tokens on all POST forms
- SameSite cookie policy set to 'Lax'

**Usage in templates:**
```html
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### XSS Prevention

**Implemented:**
- Django template auto-escaping enabled
- User input sanitized by Django ORM
- HTML special characters escaped in templates
- JavaScript content-type validation

### SQL Injection Prevention

**Implementation:**
- Django ORM parameterizes all queries
- No raw SQL queries used
- Input validation on all forms
- Database constraints enforced

### HTTPS & Secure Headers

**Production Configuration:**
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {...}
```

### Environment Variable Security

**Best Practices:**
- Never commit `.env` files
- Use `.env.example` as template
- Rotate secrets regularly
- Use secure secret management (AWS Secrets Manager, Hashicorp Vault)

### Data Protection

**Measures:**
1. **At Rest**
   - Database encryption enabled (if using managed database)
   - Sensitive data (passwords) hashed
   - PII not logged unnecessarily

2. **In Transit**
   - All connections use HTTPS in production
   - SSL/TLS 1.2+ enforced
   - HSTS headers enabled

3. **Database Access**
   - Connection pooling with max age
   - SSL required for PostgreSQL connections
   - Least privilege database user

### File Upload Security

**For Cloudinary Integration:**
- File type validation (images only)
- Maximum file size enforcement
- Cloudinary's content security features
- Virus scanning (Cloudinary professional plans)

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: Secret Key not found
**Error Message:** `ImproperlyConfigured: The SECRET_KEY setting must not be empty`

**Solution:**
1. Check `.env` file exists in project root
2. Verify `SECRET_KEY` variable is set
3. Run: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
4. Add the generated key to `.env`

#### Issue: Database connection error
**Error Message:** `django.db.utils.OperationalError: could not connect to server`

**Solution:**
1. Verify PostgreSQL is running (production)
2. Check DATABASE_URL in `.env`
3. For SQLite: Delete `db.sqlite3` and run `python manage.py migrate`
4. Verify credentials if PostgreSQL

#### Issue: Cloudinary images not loading
**Error Message:** `Failed to load resource from Cloudinary`

**Solution:**
1. Verify Cloudinary credentials in `.env`
2. Check CLOUDINARY_CLOUD_NAME spelling
3. Test with: `python test_cloudinary.py`
4. Verify account is active and has storage available

#### Issue: Static files not found in production
**Error Message:** `404 Not Found` for CSS/JavaScript

**Solution:**
1. Collect static files: `python manage.py collectstatic --noinput`
2. Verify STATIC_URL and STATIC_ROOT in settings
3. WhiteNoise should be first in MIDDLEWARE
4. Check Render deployment logs

#### Issue: Migration conflicts
**Error Message:** `Migration ... conflicts with ...`

**Solution:**
```bash
# Show migration status
python manage.py showmigrations

# Revert to stable state
python manage.py migrate gallery 0001_initial

# Recreate migrations
python manage.py makemigrations --merge
```

#### Issue: CSRF token error on form submission
**Error Message:** `Forbidden (403) CSRF verification failed`

**Solution:**
1. Ensure `{% csrf_token %}` in form
2. Check CSRF_TRUSTED_ORIGINS in settings
3. Verify domain in ALLOWED_HOSTS
4. Clear browser cookies and try again

#### Issue: User can see other users' albums
**This should not happen** - Permission check:
1. Verify `UserPassesTestMixin` in views
2. Check `test_func()` compares `album.owner == self.request.user`
3. Verify LoginRequiredMixin on all views

#### Issue: Email not sending (password reset)
**Solution:**
1. Check EMAIL settings in Django settings.py
2. For development: Use console backend
3. For production: Configure SMTP credentials
4. Test with: 
```bash
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

### Debug Mode

**Enable detailed errors locally:**
```python
# In .env
DEBUG=True
```

**Never enable DEBUG in production** - exposes sensitive information

### Checking Application Status

```bash
# Test Django configuration
python manage.py check

# Test email configuration
python manage.py shell
from django.core.mail import get_connection
connection = get_connection()
connection.open()
connection.close()

# Test database connection
python manage.py dbshell

# Test static files
python manage.py collectstatic --dry-run --verbose 2
```

### Accessing Logs

**Local Development:**
- Logs printed to terminal
- Access Django debug toolbar for detailed info

**Production (Render):**
1. Go to Render Dashboard
2. Select your web service
3. Click "Logs" tab
4. View real-time application logs

### Performance Monitoring

**Database Query Count:**
```python
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def my_function():
    from django.db import connection
    # ... perform operations ...
    print(f"Database queries: {len(connection.queries)}")
```

**Response Time:**
```bash
# Install django-debug-toolbar
pip install django-debug-toolbar

# Enable in settings.py for development only
```

---

## Additional Resources

### Documentation Links
- [Django Official Documentation](https://docs.djangoproject.com/)
- [Cloudinary Integration Guide](https://cloudinary.com/documentation)
- [Render Deployment Guide](https://render.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Learning Resources
- Django for Beginners
- Real Python Django Tutorials
- Cloudinary Academy

### Support & Community
- Django Discourse
- Stack Overflow
- GitHub Issues (for this project)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | May 2026 | Initial production release |
| 1.0.1 | TBD | Bug fixes and improvements |

---

## License & Attribution

This project uses the following technologies:
- Django (BSD License)
- Cloudinary (Apache 2.0)
- PostgreSQL (PostgreSQL License)
- Bootstrap (MIT License)

---

**Document Version**: 1.0.0  
**Last Updated**: May 25, 2026  
**Status**: Complete for Production
