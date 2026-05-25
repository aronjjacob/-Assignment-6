# Course Submission - Photo Album Management System

## Project Information

### Project Title
**Photo Album Management System**

### Project Description
A production-ready Django web application for managing photo albums with secure user authentication, cloud-based image storage, and role-based access control. The application demonstrates enterprise-level Django development practices and is fully deployed on Render.com.

---

## Submission Details

### 1. Live Application URL
**Production URL:** `https://cloud-render-demo.onrender.com`

- The application is deployed on Render.com
- **Database**: PostgreSQL hosted on Render
- **Storage**: Cloudinary (cloud-based image CDN)
- **Server**: Gunicorn with WhiteNoise
- ⚠️ **Important**: Ensure the Render instance is active during the grading period
- **Login Credentials** (for testing):
  - Username: `admin`
  - Password: `admin123`

### 2. Source Code Repository
**GitHub Repository:** `https://github.com/diangchristian/IT383-Assignment6`

**Repository Contents:**
- ✅ Complete project source code
- ✅ Comprehensive README.md with setup and deployment instructions
- ✅ requirements.txt with all dependencies
- ✅ Environment configuration examples (.env.example)
- ✅ Render deployment configuration (render.yaml, Procfile)
- ✅ Database migrations
- ✅ Static files and templates

**Repository Structure:**
```
IT383-Assignment6/
├── accounts/              # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── migrations/
├── gallery/              # Photo album app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── migrations/
├── recipe_project/       # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/            # HTML templates
│   ├── base/base.html
│   ├── index.html
│   ├── accounts/         # Auth templates
│   └── gallery/          # Gallery templates
├── README.md             # Complete documentation
├── requirements.txt      # Python dependencies
├── Procfile             # Gunicorn configuration for Render
├── render.yaml          # Render deployment config
├── manage.py            # Django management script
└── db.sqlite3          # SQLite (development only)
```

---

## Project Documentation

### Quick Start

#### Local Development Setup
```bash
# 1. Clone repository
git clone https://github.com/diangchristian/IT383-Assignment6.git
cd IT383-Assignment6

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables (.env)
DEBUG=True
SECRET_KEY=your-secret-key-here
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Start development server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Django | 6.0.5 |
| Language | Python | 3.11+ |
| Database | PostgreSQL | (Production) |
| Database | SQLite | (Development) |
| Storage | Cloudinary | 1.44.2 |
| Server | Gunicorn | 26.0.0 |
| Static Files | WhiteNoise | 6.12.0 |
| ORM | Django ORM | Built-in |

### Key Features Implemented

#### 1. User Authentication & Authorization
- User registration with validation
- Secure login/logout with session management
- Password reset via email
- Profile management
- Role-based access control (users can only access their own content)

#### 2. Album Management
- Create albums with name and description
- Edit album details
- Delete albums (with confirmation)
- View all user albums
- Album listing with pagination

#### 3. Photo Management
- Upload photos to albums
- View photos in album detail
- Delete photos
- Auto-optimization via Cloudinary
- Image display with proper sizing

#### 4. User Interface
- Responsive design (mobile-friendly)
- Modern minimal design with black, green, white color scheme
- Glass-morphism navigation
- Card-based layouts
- Smooth animations and transitions
- Font Awesome icons integration

#### 5. Security Features
- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS prevention
- Secure password hashing (PBKDF2)
- Environment-based configuration
- Secure headers (Content-Security-Policy, etc.)
- HTTPS in production

### Database Models

#### User Model (Django Built-in)
- Extended with profile information
- Email verification support
- Password reset tokens

#### Album Model
```python
- name (CharField)
- description (TextField)
- user (ForeignKey to User)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

#### Photo Model
```python
- image (CloudinaryField)
- album (ForeignKey to Album)
- caption (TextField, optional)
- uploaded_at (DateTimeField)
```

### Deployment on Render.com

#### Prerequisites
- GitHub account with repository
- Render.com account
- Cloudinary account
- PostgreSQL database connection string

#### Deployment Steps

1. **Connect Repository to Render**
   - Go to render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `main` branch

2. **Configure Environment Variables**
   In Render Dashboard → Environment:
   ```
   DEBUG=False
   SECRET_KEY=[Your secret key]
   DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
   CLOUDINARY_CLOUD_NAME=[Your cloud name]
   CLOUDINARY_API_KEY=[Your API key]
   CLOUDINARY_API_SECRET=[Your API secret]
   ALLOWED_HOSTS=cloud-render-demo.onrender.com
   ```

3. **Build & Deploy Configuration**
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn recipe_project.wsgi:application`
   - Instance Type: Free or Paid (as needed)

4. **Database Setup**
   - Create PostgreSQL database on Render
   - Add DATABASE_URL to environment variables
   - Run migrations automatically on deploy

5. **Static Files**
   - WhiteNoise handles static file serving
   - Cloudinary handles image storage
   - No additional CDN configuration needed

#### Monitoring Deployment
- Render Dashboard shows deployment status
- View logs for debugging
- Can manually trigger redeploys
- Application stays active during grading period

### System Features

#### User Management
- Registration form with validation
- Login with email/username
- Password recovery via email
- Profile editing
- User dashboard

#### Album Management
- List all user albums
- Create new album
- Edit album info
- Delete album
- View album details with all photos

#### Photo Management
- Upload photos to albums
- View photos in grid
- Download original images
- Delete individual photos
- Auto-optimization on Cloudinary

#### Admin Interface
- Django admin for staff management
- User management
- Album/Photo moderation
- Database backup options

### File Structure

**Templates:**
- `base/base.html` - Master template with navigation, styling
- `index.html` - Home page (with gallery showcase for logged-in users)
- `accounts/login.html` - Login form
- `accounts/register.html` - Registration form
- `accounts/profile.html` - User profile display
- `accounts/profile_edit.html` - Edit profile
- `accounts/password_reset.html` - Password reset initiation
- `gallery/album_list.html` - List all albums
- `gallery/album_detail.html` - View album with photos
- `gallery/album_form.html` - Create/edit album
- `gallery/photo_form.html` - Upload photo form

**Static Files:**
- CSS embedded in templates (no separate CSS files needed)
- Font Awesome icons (CDN)
- Google Fonts (CDN)

**Python Packages:**
See `requirements.txt` for complete list (19 packages total)

---

## Testing the Application

### Test User Account
- **Username**: `admin`
- **Password**: `admin123`
- Can login at: `https://cloud-render-demo.onrender.com/accounts/login/`

### Test Features
1. **Home Page**: View dashboard and featured albums
2. **Create Album**: Add new albums with titles and descriptions
3. **Upload Photos**: Add photos to albums from your device
4. **Edit/Delete**: Modify or remove albums and photos
5. **Profile**: Update user profile information
6. **Password Reset**: Test forgot password functionality

### Browser Compatibility
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## Technical Implementation Details

### Django Configuration
- **Settings Module**: `recipe_project/settings.py`
- **URL Routing**: Separate apps with modular URL configs
- **Middleware**: Security middleware, session, CSRF protection
- **Template Engine**: Django template language
- **Database**: dj-database-url for environment-based config

### Security Considerations
- ✅ HTTPS enforced in production
- ✅ Secure cookie settings
- ✅ CSRF tokens on all forms
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Authentication required for sensitive operations
- ✅ User data isolation (users can't access other users' content)

### Performance Optimizations
- Database query optimization
- Template caching
- Static file compression with WhiteNoise
- Cloudinary image optimization (automatic resizing, compression)
- Pagination for album/photo lists

---

## Submission Checklist

- ✅ **Live URL**: https://cloud-render-demo.onrender.com
- ✅ **Repository**: https://github.com/diangchristian/IT383-Assignment6
- ✅ **README.md**: Comprehensive with setup and deployment instructions
- ✅ **requirements.txt**: All dependencies listed
- ✅ **Deployment Config**: Procfile and render.yaml configured
- ✅ **Environment Setup**: .env.example provided
- ✅ **Project Documentation**: This submission document
- ✅ **Render Instance**: Active during grading period
- ✅ **Database Migrations**: All applied on deployment
- ✅ **Static Files**: WhiteNoise + Cloudinary configured

---

## Support & Troubleshooting

### Common Issues

**Application won't load:**
- Check Render Dashboard for deployment errors
- Verify DATABASE_URL environment variable
- Check Cloudinary credentials

**Images not displaying:**
- Verify Cloudinary API credentials
- Check image upload permissions
- Ensure Cloudinary account is active

**Database errors:**
- Verify PostgreSQL connection string
- Run migrations: `python manage.py migrate`
- Check database user permissions

**Render deployment fails:**
- Check build logs in Render Dashboard
- Verify all environment variables are set
- Ensure requirements.txt is up-to-date

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Render.com Deployment Guide](https://render.com/docs)
- [Cloudinary Integration](https://cloudinary.com/documentation)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## Submission Format

**Upload to Course Portal:**
1. Create a single document (PDF or DOCX) containing:
   - This entire submission document
   - Live Application URL
   - GitHub Repository Link
   - Brief overview of features implemented

2. Ensure the document includes:
   - Project title and description
   - All three required links (live URL, repository, documentation)
   - Setup instructions
   - Testing credentials
   - Deployment information

3. Keep Render instance active during grading period

---

**Project Submitted**: May 25, 2026
**GitHub Repository**: https://github.com/diangchristian/IT383-Assignment6
**Live Application**: https://cloud-render-demo.onrender.com
