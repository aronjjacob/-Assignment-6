# Cloud Render - Photo Gallery Application

A Django photo gallery application with cloud-based image storage using Cloudinary.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Photo Albums**: Create, edit, and delete photo albums
- **Photo Gallery**: Upload and manage photos with Cloudinary storage
- **Minimal Design**: Clean, modern UI with black/green/white color scheme
- **Responsive Layout**: Card-based grid layout that works on all devices

## Tech Stack

- **Backend**: Django 6.0.5
- **Database**: PostgreSQL (production), SQLite (development)
- **Image Storage**: Cloudinary
- **Frontend**: HTML5, CSS3
- **Deployment**: Render

## Quick Start

### Prerequisites
- Python 3.11+
- pip
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/aronjjacob/-Assignment-6.git
cd -Assignment-6
```

2. **Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Open http://127.0.0.1:8000 in your browser
- Login with your superuser credentials

## Configuration

### Cloudinary Setup

1. Create a free account at https://cloudinary.com/
2. Get your Cloud Name, API Key, and API Secret from the dashboard
3. Add these to your `.env` file

### Database

- **Local Development**: Uses SQLite (db.sqlite3) automatically
- **Production (Render)**: Uses PostgreSQL via DATABASE_URL in `.env`

## Project Structure

```
cloud-render/
├── accounts/              # User authentication app
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── gallery/              # Photo gallery app
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── recipe_project/       # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/            # HTML templates
│   ├── base/
│   ├── accounts/
│   └── gallery/
├── manage.py
├── requirements.txt
└── .env                  # Environment variables (not in repo)
```

## Key Features

### Gallery Management
- **Create Albums**: Users can create new albums
- **Upload Photos**: Add photos to albums with title and description
- **Edit/Delete**: Modify or remove photos and albums
- **Cloud Storage**: All images stored securely in Cloudinary

### User Features
- **User Registration**: Create new user accounts
- **User Profiles**: Manage profile information
- **Password Reset**: Recover forgotten passwords
- **Dashboard**: View gallery statistics

## Deployment to Render

1. **Push to GitHub**
```bash
git add .
git commit -m "Your commit message"
git push
```

2. **Create Render service**
   - Go to https://render.com
   - Connect your GitHub repository
   - Set environment variables in Render dashboard
   - Deploy

3. **Update DATABASE_URL in .env**
   - Render will provide a PostgreSQL database URL
   - Add it to your `.env` file for production

## Testing

Test Cloudinary connection:
```bash
python test_cloudinary.py
```

Verify configuration:
```bash
python verify_config.py
```

## Troubleshooting

### Photos not loading
- Check that Cloudinary credentials are correct in `.env`
- Verify CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET are set
- Check that photos are uploaded (check Cloudinary dashboard)

### Database errors
- For local development, make sure DATABASE_URL is commented out in `.env`
- For production, ensure DATABASE_URL from Render is in `.env`

### Static files issues
- Run `python manage.py collectstatic` for production
- Check DEBUG setting (should be True in development, False in production)

## API Endpoints

### Albums
- `GET /gallery/` - List all albums
- `POST /gallery/create/` - Create new album
- `GET /gallery/<id>/` - View album details
- `POST /gallery/<id>/edit/` - Edit album
- `POST /gallery/<id>/delete/` - Delete album

### Photos
- `POST /gallery/<album_id>/photo/create/` - Upload photo
- `GET /gallery/photo/<id>/` - View photo details
- `POST /gallery/photo/<id>/edit/` - Edit photo
- `POST /gallery/photo/<id>/delete/` - Delete photo

### Authentication
- `GET /accounts/register/` - Register new user
- `GET /accounts/login/` - Login
- `GET /accounts/logout/` - Logout
- `GET /accounts/profile/` - View profile
- `POST /accounts/profile/edit/` - Edit profile

## License

This project is open source and available under the MIT License.

## Author

Created by Aron Jacob Masecampo

## Support

For issues or questions, please create an issue on the GitHub repository.
