# Configuration Flow Diagrams - Visual Guide

## 1. HOW DJANGO LOADS CONFIGURATION

```
┌─────────────────────────────────────────────────────────┐
│                  Django Startup                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
         ┌─────────────────┐
         │  settings.py    │
         │  runs first     │
         └────────┬────────┘
                  │
                  ▼
    ┌──────────────────────────────┐
    │  from dotenv import load_dotenv
    │  load_dotenv()               │ ← Reads .env file into environment
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │  os.getenv('CLOUDINARY_CLOUD_NAME')│
    │  os.getenv('DATABASE_URL')       │ ← Get values from .env
    │  os.getenv('SECRET_KEY')         │
    │  ... etc                         │
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │  Django ready with values from   │
    │  .env file                       │
    └──────────────────────────────────┘
```

## 2. DATABASE SELECTION LOGIC

```
                    ┌────────────────────┐
                    │  Django Starts     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Check for          │
                    │ DATABASE_URL in    │
                    │ environment vars   │
                    └────────┬───────────┘
                             │
               ┌─────────────┴─────────────┐
               │                           │
         ┌─────▼──────┐            ┌─────▼──────┐
         │ DATABASE_URL│           │No DATABASE │
         │ EXISTS?     │           │   _URL     │
         │ (set)       │           │ (not set)  │
         └─────┬──────┘            └─────┬──────┘
               │                         │
               ▼                         ▼
         ┌──────────────┐         ┌──────────────┐
         │ Use          │         │ Use          │
         │ PostgreSQL   │         │ SQLite       │
         │ (Render)     │         │ (Local)      │
         └──────┬───────┘         └──────┬───────┘
                │                        │
                ▼                        ▼
        ┌──────────────────┐    ┌──────────────────┐
        │ photos stored at │    │ photos stored in │
        │ dpg-d8a4...      │    │ db.sqlite3       │
        │ (Production)     │    │ (Development)    │
        └──────────────────┘    └──────────────────┘

CURRENT SITUATION (LOCAL):
  DATABASE_URL is set in .env, but points to production
  → Django tries to connect to production database
  → Connection fails (can't reach production from local)
  
SOLUTION FOR LOCAL DEVELOPMENT:
  Comment out DATABASE_URL in .env
  → Django uses SQLite (db.sqlite3)
  → Works perfectly locally
  
PRODUCTION (RENDER):
  Render sets DATABASE_URL environment variable
  → Django uses PostgreSQL
  → Photos stored in production database
```

## 3. IMAGE UPLOAD FLOW

```
┌─────────────────────────────────────────────────────────────┐
│                    User Uploads Photo                       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────┐
    │  Browser: <input type="file">
    │  Sends file to server       │
    └────────────┬────────────────┘
                 │
                 ▼
    ┌──────────────────────────────┐
    │  Django View receives file:  │
    │  PhotoCreateView.form_valid()│
    └────────────┬─────────────────┘
                 │
                 ▼
    ┌──────────────────────────────┐
    │  PhotoForm validates:        │
    │  - Title (required)          │
    │  - Description (optional)    │
    │  - Image (required)          │
    │  - Album (hidden input)      │
    │  - Owner (set by view)       │
    └────────────┬─────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  Django checks STORAGES config:  │
    │  Which storage backend to use?   │
    └────────────┬──────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────────┐
    │  STORAGES['default'] =               │
    │  'cloudinary_storage.             │
    │   storage.MediaCloudinaryStorage'    │
    │  → Use Cloudinary (NOT local disk)   │
    └────────────┬───────────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────────┐
    │  File sent to Cloudinary:            │
    │  - Uses CLOUDINARY_CLOUD_NAME        │
    │  - Uses CLOUDINARY_API_KEY           │
    │  - Uses CLOUDINARY_API_SECRET        │
    │  Cloudinary URL generated            │
    └────────────┬───────────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────────┐
    │  Photo record saved to database:     │
    │  {                                   │
    │    title: "My Photo",                │
    │    image_url: "https://res.cloudinary│
    │             .com/dubp5jwpw/image...", │
    │    album: Album.id,                  │
    │    owner: User.id                    │
    │  }                                   │
    └────────────┬───────────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────────┐
    │  Browser redirects to Album Detail   │
    │  Page loads and displays photos      │
    └──────────────────────────────────────┘
```

## 4. CLOUDINARY CONFIGURATION

```
┌──────────────────────────────────────────────────────┐
│             .env file (your local config)           │
├──────────────────────────────────────────────────────┤
│ CLOUDINARY_CLOUD_NAME=dubp5jwpw                     │
│ CLOUDINARY_API_KEY=478641119815689                  │
│ CLOUDINARY_API_SECRET=wevkD7yA-IzxNwmWRSHO5...     │
└────────────┬─────────────────────────────────────────┘
             │ (load_dotenv() reads)
             │
             ▼
┌──────────────────────────────────────────────────────┐
│          settings.py (Django config)                │
├──────────────────────────────────────────────────────┤
│ CLOUDINARY_STORAGE = {                               │
│     'CLOUDINARY_CLOUD_NAME': os.getenv('...'),      │
│     'CLOUDINARY_API_KEY': os.getenv('...'),         │
│     'CLOUDINARY_API_SECRET': os.getenv('...')       │
│ }                                                    │
│                                                      │
│ STORAGES = {                                         │
│     "default": {                                     │
│         "BACKEND":                                   │
│         "cloudinary_storage.storage.               │
│          MediaCloudinaryStorage"                     │
│     }                                                │
│ }                                                    │
│                                                      │
│ cloudinary.config(                                   │
│     cloud_name='...',                                │
│     api_key='...',                                   │
│     api_secret='...'                                 │
│ )                                                    │
└────────────┬─────────────────────────────────────────┘
             │ (Django uses this config)
             │
             ▼
┌──────────────────────────────────────────────────────┐
│          Photo Model (gallery/models.py)            │
├──────────────────────────────────────────────────────┤
│ class Photo(models.Model):                           │
│     image = CloudinaryField('image')                 │
│     # ↑ This field uses STORAGES['default']         │
│     # ↑ Which is MediaCloudinaryStorage             │
│     # ↑ Which uses the Cloudinary config            │
└────────────┬─────────────────────────────────────────┘
             │ (When saving Photo)
             │
             ▼
┌──────────────────────────────────────────────────────┐
│     Image Upload to Cloudinary Cloud                │
├──────────────────────────────────────────────────────┤
│ POST https://api.cloudinary.com/v1_1/upload         │
│ Headers:                                             │
│   - cloud_name: dubp5jwpw                           │
│   - api_key: 478641119815689                        │
│   - api_secret: wevkD7yA-...                        │
│ Data:                                                │
│   - file: <image data>                              │
└────────────┬─────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────┐
│           Image stored on Cloudinary CDN            │
├──────────────────────────────────────────────────────┤
│ Accessible at:                                       │
│ https://res.cloudinary.com/dubp5jwpw/image/upload   │
│ /v123456/photo_name.jpg                             │
│                                                      │
│ Benefits:                                            │
│  ✓ Global access (fast everywhere)                   │
│  ✓ Automatic backups                                 │
│  ✓ Never lost if server resets                       │
│  ✓ Can use on any server                             │
└──────────────────────────────────────────────────────┘
```

## 5. LOCAL VS PRODUCTION ENVIRONMENTS

```
LOCAL DEVELOPMENT (Your Computer)
┌─────────────────────────────────────────────────────┐
│                                                     │
│  .env file                                          │
│  ├─ SECRET_KEY=...                                  │
│  ├─ DEBUG=True                  ✓ Good for dev     │
│  ├─ DATABASE_URL=(commented out)                    │
│  ├─ CLOUDINARY_CLOUD_NAME=...   ✓ (shared)        │
│  ├─ CLOUDINARY_API_KEY=...      ✓ (shared)        │
│  └─ CLOUDINARY_API_SECRET=...   ✓ (shared)        │
│                                                     │
│  Database: SQLite (db.sqlite3)  ✓ Simple, local    │
│  Images: Cloudinary             ✓ Same as production
│  Server: http://127.0.0.1:8000  ✓ Local            │
│                                                     │
└─────────────────────────────────────────────────────┘
                        VS
PRODUCTION (Render Server)
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Environment Variables (set on Render)              │
│  ├─ SECRET_KEY=...                                  │
│  ├─ DEBUG=False                 ✓ Hide errors      │
│  ├─ DATABASE_URL=postgresql://  ✓ PostgreSQL       │
│  ├─ CLOUDINARY_CLOUD_NAME=...   ✓ (same)          │
│  ├─ CLOUDINARY_API_KEY=...      ✓ (same)          │
│  └─ CLOUDINARY_API_SECRET=...   ✓ (same)          │
│                                                     │
│  Database: PostgreSQL (Render)  ✓ Powerful         │
│  Images: Cloudinary             ✓ (same)           │
│  Server: cloud-render-...onrender.com              │
│                                                     │
└─────────────────────────────────────────────────────┘

KEY DIFFERENCE:
  Local: DATABASE_URL not set → SQLite
  Render: DATABASE_URL set → PostgreSQL
  
  Cloudinary & images are IDENTICAL in both!
```

## 6. SETTINGS.PY PRIORITY ORDER

```
When Django needs a setting value:

Step 1: Check environment variables (.env values)
        ├─ Found? → Use it
        └─ Not found? → Go to Step 2

Step 2: Check for default value in code
        ├─ Found? → Use it
        └─ Not found? → Error!

Example for Cloudinary:
  os.getenv('CLOUDINARY_CLOUD_NAME', '')
           ↑ Check .env first
                               ↑ Use empty string if not found

Example for DEBUG:
  os.getenv('DEBUG', 'False') == 'True'
           ↑ Check .env first (default is 'False')
  - If .env has DEBUG=True → Result: True
  - If .env has DEBUG=False → Result: False
  - If .env missing DEBUG → Uses 'False' → Result: False
```

## 7. PHOTO DISPLAY FLOW

```
User Requests Album Detail Page
    ↓
Django Template loads album data
    ├─ Album name
    ├─ Album description
    ├─ Photo list: album.photos.all()
    └─ For each photo:
        ├─ photo.title
        ├─ photo.description
        └─ photo.image.url  ← Cloudinary URL
    
Browser receives HTML
    ↓
For each photo, HTML has:
    <img src="https://res.cloudinary.com/dubp5jwpw/image/upload/...">
    
Browser requests image from Cloudinary
    ↓
Cloudinary CDN responds with image
    ↓
Image displays in browser ✓
```

---

## SUMMARY FLOW

```
User uploads photo
    ↓
Form → Django → Cloudinary
    ↓
Photo URL stored in database
    ↓
User views album
    ↓
Django queries database
    ↓
Gets photo URLs from Cloudinary
    ↓
Renders HTML with <img src="...">
    ↓
Browser displays photo ✓
```
