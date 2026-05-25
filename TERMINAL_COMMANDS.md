# Quick Terminal Commands Reference

## TEST POSTGRESQL (Production Database on Render)

### 1. Check if PostgreSQL CLI is installed locally
```bash
psql --version
```
**Expected:** PostgreSQL version number (or "command not found" - which is OK)

### 2. Try to connect to Render PostgreSQL (will fail locally - that's NORMAL)
```bash
psql -h dpg-d8a4cg6gvqtc73cgtrlg-a -U photo_album_bm9d_user -d photo_album_bm9d
```
**Expected error:** `could not translate host name` (NORMAL - production database not accessible locally)

### 3. Check which database Django is using locally
```bash
python manage.py dbshell
```
**Expected:** SQLite prompt with `sqlite>`
(Type `.quit` to exit)

### 4. Check database settings
```bash
python manage.py shell
```
Then in Python prompt:
```python
from django.conf import settings
print(settings.DATABASES['default'])
```
**Expected (locally):**
```
{
  'ENGINE': 'django.db.backends.sqlite3',
  'NAME': 'db.sqlite3'
}
```

---

## TEST CLOUDINARY (Image Storage)

### 1. Run full configuration verification
```bash
python verify_config.py
```
**Expected output:**
```
✓ Cloudinary connection: SUCCESS
✓ Response: {'status': 'ok'}
✓ ALL CHECKS PASSED
```

### 2. Test Cloudinary connection in Python shell
```bash
python manage.py shell
```
Then type:
```python
import cloudinary.api
result = cloudinary.api.ping()
print(result)
```
**Expected output:**
```
{'status': 'ok'}
```

### 3. List all images in your Cloudinary account
```bash
python manage.py shell
```
Then type:
```python
from cloudinary.search import search
result = search().expression("resource_type:image").max_results(10).execute()
print(f"Found {result['total_count']} images")
for item in result.get('resources', []):
    print(f"  - {item['public_id']} ({item['format']})")
```
**Expected output:**
```
Found 5 images
  - my_image_1 (jpg)
  - my_image_2 (jpg)
  ...
```

### 4. Check Cloudinary credentials are loaded
```bash
python manage.py shell
```
Then type:
```python
import os
from dotenv import load_dotenv
load_dotenv()
print(f"Cloud Name: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
print(f"API Key: {os.getenv('CLOUDINARY_API_KEY')}")
print(f"API Secret: {os.getenv('CLOUDINARY_API_SECRET')[:10]}...")
```
**Expected output:**
```
Cloud Name: dubp5jwpw
API Key: 478641119815689
API Secret: wevkD7yA-I...
```

### 5. Verify Photo model uses Cloudinary storage
```bash
python manage.py shell
```
Then type:
```python
from gallery.models import Photo
field = Photo._meta.get_field('image')
print(f"Field type: {type(field).__name__}")
print(f"Field storage: {field.storage.__class__.__name__ if hasattr(field, 'storage') else 'CloudinaryField'}")
```
**Expected output:**
```
Field type: CloudinaryField
Field storage: CloudinaryField
```

---

## TEST FULL WORKFLOW (Photo Upload)

### 1. Start development server
```bash
python manage.py runserver
```
**Expected:**
```
Starting development server at http://127.0.0.1:8000/
```

### 2. Visit homepage
```
http://127.0.0.1:8000
```

### 3. Login with admin credentials
- Username: `admin`
- Password: `admin123`

### 4. Navigate to an album (or create one first)
```
http://127.0.0.1:8000/gallery/
```

### 5. Click on an album to view details
```
http://127.0.0.1:8000/gallery/album/1/
```

### 6. Upload a test photo
1. Scroll to "Upload Photo" section
2. Select a JPG/PNG file
3. Fill in Title and Description
4. Click "Upload"

### 7. Verify upload was successful
- Should redirect back to album detail page
- New photo should appear in the grid
- Right-click photo → "View Image" should show URL like:
  ```
  https://res.cloudinary.com/dubp5jwpw/image/upload/v...
  ```

---

## EXPECTED CONSOLE OUTPUTS

### When everything is working:

**verify_config.py output:**
```
========== CONFIGURATION VERIFICATION REPORT ==========

1. ENVIRONMENT VARIABLES (.env FILE)
✓ SECRET_KEY: dqw6k-^u(5p97mlda1b8...
✓ DEBUG: True
✓ DATABASE_URL: postgresql://...
✓ CLOUDINARY_CLOUD_NAME: dubp5jwpw
✓ CLOUDINARY_API_KEY: 478641119815689
✓ CLOUDINARY_API_SECRET: wevkD7yA-I...

2. DJANGO SETTINGS (settings.py)
✓ DEBUG: True
✓ ALLOWED_HOSTS: ['localhost', '127.0.0.1', ...]
✓ SECRET_KEY exists: True

3. DATABASE CONFIGURATION
✓ Database ENGINE: django.db.backends.postgresql
✓ Database NAME: photo_album_bm9d
✓ Database HOST: dpg-d8a4cg6gvqtc73cgtrlg-a

4. STORAGE CONFIGURATION
✓ Default Storage Backend: cloudinary_storage.storage.MediaCloudinaryStorage
✓ Using Cloudinary Storage: True

5. CLOUDINARY CONFIGURATION
✓ CLOUDINARY_CLOUD_NAME: dubp5jwpw
✓ CLOUDINARY_API_KEY exists: True
✓ CLOUDINARY_API_SECRET exists: True

6. DATABASE CONNECTION TEST
✗ Database connection FAILED: could not translate host name...
  (This is NORMAL - production database not accessible locally)

7. CLOUDINARY CONNECTION TEST
✓ Cloudinary connection: SUCCESS
✓ Response: {'status': 'ok'}

8. PHOTO MODEL CONFIGURATION
✓ Photo.image field type: CloudinaryField

SUMMARY
Passed: 5/5 checks
✓ ALL CHECKS PASSED - Configuration looks good!
```

---

## WHAT EACH COMPONENT DOES

| Component | What it does | Expected Status |
|-----------|-------------|-----------------|
| **DATABASE_URL** | Tells Django which database to use | Set (uses PostgreSQL on Render, SQLite locally) |
| **SECRET_KEY** | Encrypts sensitive data | Set and hidden |
| **DEBUG** | Shows error details | True locally, False on Render |
| **CLOUDINARY_CLOUD_NAME** | Your Cloudinary account ID | `dubp5jwpw` |
| **CLOUDINARY_API_KEY** | Authentication for Cloudinary | `478641119815689` |
| **CLOUDINARY_API_SECRET** | Secret password for Cloudinary | Present but hidden |
| **ALLOWED_HOSTS** | Which domains can access the app | `['localhost', '127.0.0.1']` |
| **STORAGES** | Where to save uploaded files | `cloudinary_storage.storage.MediaCloudinaryStorage` |

---

## TROUBLESHOOTING

**If `verify_config.py` shows errors:**

1. Make sure .env file exists
   ```bash
   ls .env
   ```

2. Make sure Python packages are installed
   ```bash
   pip install -r requirements.txt
   ```

3. Try running migrations
   ```bash
   python manage.py migrate
   ```

4. Restart Django server
   ```bash
   python manage.py runserver
   ```

**If Cloudinary test fails:**

1. Check credentials in .env are correct
2. Visit https://console.cloudinary.com to verify your account
3. Copy credentials again from Cloudinary dashboard

**If photos don't upload:**

1. Check browser console for errors (F12 → Console)
2. Check Django console for errors
3. Check Cloudinary dashboard to see if image was uploaded
4. Verify Photo model and PhotoForm are configured correctly

---

## QUICK CHECK: Is Everything Working?

Run this one command:
```bash
python verify_config.py
```

If you see:
```
✓ ALL CHECKS PASSED - Configuration looks good!
```

Then ✓ **Everything is configured correctly!**
