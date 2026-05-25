# Troubleshooting Guide - Fix Photo Not Showing Issue

## SYMPTOM: Photos Don't Display After Upload

If you upload a photo but it doesn't show up in the album, follow this guide:

---

## STEP 1: Check If the Form Accepted the Upload

**What to look for:**
- After clicking "Upload", did the page redirect back to the album?
- Did you see a success message?

**If NO - Form rejected the upload:**

### 1A: Check Browser Console for JavaScript Errors
1. Press `F12` to open Developer Tools
2. Click "Console" tab
3. Look for red error messages
4. Try uploading again and watch console
5. Screenshot any errors

### 1B: Check if Image File is Valid
- Make sure the file is JPG, PNG, or GIF
- File must be less than 10MB
- Try a different image

### 1C: Check if Form Field is Required
Try uploading without all fields:
- Title: Required ✓
- Description: Optional
- Image: Required ✓
- Album: Hidden (set automatically)

**If form still rejects:**
```bash
python manage.py shell
```
```python
from gallery.forms import PhotoForm
form = PhotoForm()
print(form.fields.keys())  # Should show: title, description, image
```

---

## STEP 2: Check If Photo Was Saved to Database

**Open Python shell:**
```bash
python manage.py shell
```

**Run these commands:**
```python
from gallery.models import Photo
from django.contrib.auth.models import User

# How many photos exist?
print(f"Total photos: {Photo.objects.count()}")

# Get the most recent photo
photo = Photo.objects.latest('created_at')
print(f"Latest photo: {photo.title}")
print(f"Album: {photo.album.name}")
print(f"Owner: {photo.owner.username}")
print(f"Image URL: {photo.image.url if photo.image else 'NO IMAGE'}")

# Check if image field is empty
if not photo.image:
    print("⚠ WARNING: Photo record has no image!")
else:
    print(f"✓ Image is set: {photo.image}")
```

**If you see "NO IMAGE":**
- The form accepted the upload but didn't save the image
- Go to Step 3

**If you see a URL:**
- The image is saved, go to Step 4

---

## STEP 3: Check If Image Was Uploaded to Cloudinary

### 3A: View Recent Uploads
```bash
python manage.py shell
```
```python
from cloudinary.search import search

# Get recent uploads
result = search().expression("resource_type:image").max_results(10).execute()
print(f"Total images in Cloudinary: {result['total_count']}")
print("\nRecent images:")
for item in result.get('resources', []):
    print(f"  - {item['public_id']}")
    print(f"    URL: {item['secure_url']}")
    print(f"    Uploaded: {item['created_at']}")
```

**If you see your image:**
- Image is in Cloudinary ✓
- Problem is with database reference
- Go to Step 4

**If you don't see your image:**
- Cloudinary didn't receive it
- Check Django console for upload errors
- Go to Step 5

### 3B: Check Django Console for Cloudinary Errors
Look for messages like:
```
ERROR: Cloudinary upload failed
ERROR: API authentication failed
ERROR: File too large
```

---

## STEP 4: Check If Photo Displays in Template

**Navigate to album detail page:**
```
http://127.0.0.1:8000/gallery/album/1/
```

**Right-click on the album:**
- "View Page Source"
- Search for: `res.cloudinary.com`

**If you find Cloudinary URL:**
- Image is in HTML ✓
- Problem is with image rendering
- Check browser console (F12 → Console)

**If you don't find it:**
- Template isn't rendering photos
- Go to Step 6

---

## STEP 5: Test Cloudinary Connection

### 5A: Verify Credentials
```bash
python manage.py shell
```
```python
import os
from dotenv import load_dotenv
load_dotenv()

print("Cloudinary credentials from .env:")
print(f"  CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
print(f"  API_KEY: {os.getenv('CLOUDINARY_API_KEY')}")
print(f"  API_SECRET: {os.getenv('CLOUDINARY_API_SECRET')[:10]}...")
```

**If any are empty:**
1. Edit `.env` file
2. Add missing values from Cloudinary dashboard
3. Save `.env`
4. Restart Django server

### 5B: Test Cloudinary Connection
```bash
python manage.py shell
```
```python
import cloudinary.api

try:
    result = cloudinary.api.ping()
    print(f"✓ Cloudinary connection: {result}")
except Exception as e:
    print(f"✗ Cloudinary error: {e}")
```

**If you see error:**
- Cloudinary credentials are wrong
- Go back and verify credentials

### 5C: Test Image Upload Directly
```bash
python manage.py shell
```
```python
from cloudinary.uploader import upload

try:
    # Upload a test image
    result = upload(
        "https://res.cloudinary.com/demo/image/upload/sample.jpg",
        public_id="test_image_123"
    )
    print(f"✓ Upload successful!")
    print(f"  URL: {result['secure_url']}")
except Exception as e:
    print(f"✗ Upload failed: {e}")
```

---

## STEP 6: Check Template Configuration

**Check album_detail.html:**
```bash
grep -n "photo.image" templates/gallery/album_detail.html
```

**Should show something like:**
```html
<img src="{{ photo.image.url }}" alt="{{ photo.title }}">
```

**If not found:**
- Template isn't configured to show images
- Template needs update

### 6A: Verify Template Has Image Display
Run this to find the exact line:
```bash
python manage.py shell
```
```python
with open('templates/gallery/album_detail.html', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if 'photo.image' in line:
            print(f"Line {i}: {line.strip()}")
```

**If you see:**
```
<img src="{{ photo.image.url }}" ...
```
Good ✓

**If you see:**
```
<img src="{{ photo.image }}
```
Wrong - needs `.url`

**If nothing found:**
Image display code is missing - template needs update

---

## STEP 7: Check Photo Model

```bash
python manage.py shell
```
```python
from gallery.models import Photo

# Check field type
field = Photo._meta.get_field('image')
print(f"Field type: {type(field).__name__}")
print(f"Field: {field}")

# Get a photo and check its image
photo = Photo.objects.latest('created_at')
print(f"\nPhoto: {photo.title}")
print(f"Image object: {photo.image}")
print(f"Image URL method exists: {hasattr(photo.image, 'url')}")

if hasattr(photo.image, 'url'):
    print(f"Image URL: {photo.image.url}")
else:
    print(f"⚠ Image field doesn't have .url attribute!")
```

---

## COMPLETE DIAGNOSTIC - RUN THIS FIRST

```bash
python verify_config.py
```

This checks everything automatically. Look for:
- ✓ All checks should pass
- ✗ Any failures point to problems

---

## COMMON FIXES

### Fix 1: .env File Not Reloaded
**Problem:** Changed .env but changes don't take effect

**Solution:**
```bash
# Restart Django server
python manage.py runserver
```

### Fix 2: Cloudinary Credentials Wrong
**Problem:** API key doesn't work

**Solution:**
1. Go to https://console.cloudinary.com
2. Copy correct credentials
3. Update `.env` file
4. Restart Django server

### Fix 3: Image Not Uploading to Cloudinary
**Problem:** Form accepts but image doesn't appear in Cloudinary

**Solution:**
```bash
# Check if file size is issue
ls -lh path/to/your/image.jpg  # Must be under 10MB

# Check if format is supported
file path/to/your/image.jpg    # Should be JPEG, PNG, or GIF
```

### Fix 4: Photo Record Created But No Image URL
**Problem:** Photo exists in database but image.url is empty

**Solution:**
```bash
# Check photo in database
python manage.py shell
```
```python
from gallery.models import Photo
photo = Photo.objects.latest('created_at')
print(photo.image)  # What is this?
```

If empty:
1. Delete the photo
2. Re-upload it
3. Make sure to select a file

### Fix 5: Storage Backend Not Configured
**Problem:** Photos saved to local /media/ instead of Cloudinary

**Solution:** Check settings.py
```python
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }
}
```

This MUST say `MediaCloudinaryStorage`, not `FileSystemStorage`

---

## IF ALL ELSE FAILS

### Complete Reset
```bash
# 1. Stop Django server (Ctrl+C)

# 2. Clear database
rm db.sqlite3

# 3. Run migrations to create fresh database
python manage.py migrate

# 4. Create new superuser
python manage.py createsuperuser

# 5. Restart server
python manage.py runserver
```

### Then test:
1. Login
2. Create album
3. Upload photo
4. Check if photo appears

### If still not working:

**Collect all info and check:**
```bash
# 1. Configuration
python verify_config.py > config_report.txt

# 2. Database
python manage.py shell <<EOF
from gallery.models import Photo
print(Photo.objects.all())
EOF

# 3. Cloudinary
python manage.py shell <<EOF
import cloudinary.api
print(cloudinary.api.ping())
EOF
```

Share the output with debugging info.

---

## QUICK REFERENCE

| Issue | Solution |
|-------|----------|
| Form rejects upload | Check image format (JPG/PNG), file size < 10MB |
| Photo saved but no URL | Cloudinary didn't receive it, check credentials |
| Photo saved but doesn't display | Check template has `photo.image.url` |
| Template shows but image won't load | Check browser console (F12), check image URL directly |
| Credentials seem wrong | Verify on https://console.cloudinary.com |
| Changes don't take effect | Restart Django server: `python manage.py runserver` |

---

## WHEN TO USE EACH COMMAND

| Situation | Command |
|-----------|---------|
| Unsure what's wrong | `python verify_config.py` |
| Check database | `python manage.py shell` then query models |
| Check Cloudinary | `python manage.py shell` then use cloudinary.api |
| Check template | Use browser F12 and view page source |
| Debug form | Check browser console and Django terminal output |
| Test upload | Use web interface: http://127.0.0.1:8000 |

---

## DEBUGGING CHECKLIST

- [ ] Ran `python verify_config.py` and all passed?
- [ ] Checked browser console (F12) for errors?
- [ ] Checked Django terminal for error messages?
- [ ] Verified photo exists in database?
- [ ] Verified photo exists in Cloudinary?
- [ ] Verified template has `photo.image.url`?
- [ ] Tried uploading a different image?
- [ ] Restarted Django server?
- [ ] Restarted browser (hard refresh: Ctrl+Shift+R)?

---

## SUCCESS INDICATORS

✓ Everything working when you see:
- Form accepts upload without errors
- Page redirects to album detail
- Photo appears in grid with image
- Right-click image → "View Image" shows Cloudinary URL
- Image displays properly
