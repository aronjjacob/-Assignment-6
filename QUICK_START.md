# Quick Start - 5 Minute Setup & Test

## IF YOU JUST WANT TO TEST IF EVERYTHING WORKS

Follow this 5-minute guide:

---

## STEP 1: Start Django Server (30 seconds)

```bash
cd c:\Users\jacob\Downloads\cloud-render
python manage.py runserver
```

**Expected:**
```
Starting development server at http://127.0.0.1:8000/
```

---

## STEP 2: Verify Configuration (1 minute)

In another terminal:

```bash
cd c:\Users\jacob\Downloads\cloud-render
python verify_config.py
```

**Expected:**
```
✓ ALL CHECKS PASSED - Configuration looks good!
```

---

## STEP 3: Test in Browser (2 minutes)

### 3A: Go to homepage
```
http://127.0.0.1:8000
```

### 3B: Login
- Username: `admin`
- Password: `admin123`

### 3C: Create album (if needed)
- Go to Gallery
- Click "New Album"
- Fill in name and description
- Click Create

### 3D: Upload photo
- Go to Gallery → Click an album
- Scroll to "Upload Photo"
- Click "Choose File"
- Select a JPG or PNG image from your computer
- Fill in Title and Description
- Click "Upload"

### 3E: Verify photo displays
- Photo should appear in the gallery grid
- Click on it to view details
- Right-click → "View Image" to see URL
- URL should be: `https://res.cloudinary.com/dubp5jwpw/image/upload/...`

---

## STEP 4: If Photo Doesn't Show (1 minute)

### 4A: Check browser console
- Press F12
- Click "Console" tab
- Look for red errors
- Screenshot and save

### 4B: Check Django terminal
- Look at Django server output
- Look for error messages
- Screenshot and save

### 4C: Run diagnostic
```bash
python verify_config.py
```

---

## EXPECTED SUCCESS INDICATORS

✓ Form accepts upload without errors
✓ Page redirects to album detail
✓ Photo appears in the grid
✓ Image loads and displays
✓ URL shows Cloudinary domain

---

## COMMON ISSUES & QUICK FIXES

| Issue | Fix |
|-------|-----|
| "Could not create photo" | Check image is JPG/PNG, under 10MB |
| Photo uploads but doesn't show | Refresh browser (Ctrl+Shift+R) |
| Can't login | Make sure admin account exists: `python manage.py createsuperuser` |
| Server won't start | Make sure port 8000 is free or use different port: `python manage.py runserver 8001` |
| Getting 404 errors | Make sure migrations ran: `python manage.py migrate` |

---

## IF EVERYTHING WORKS

Congratulations! ✓ Your setup is correct:

- ✓ SQLite database working locally
- ✓ Cloudinary credentials valid
- ✓ Photos uploading to cloud
- ✓ Images displaying properly

You're ready to:
1. Test more features
2. Deploy to Render
3. Push code to GitHub

---

## DETAILED DOCUMENTS

If you need more info:

- **Full verification:** `VERIFICATION_COMPLETE.md`
- **Detailed guide:** `CONFIGURATION_GUIDE.md`
- **Commands:** `TERMINAL_COMMANDS.md`
- **Diagrams:** `CONFIGURATION_DIAGRAMS.md`
- **Problems:** `TROUBLESHOOTING_GUIDE.md`

---

## NEXT STEPS

### To Test More Features
```bash
# While server is running, visit:
http://127.0.0.1:8000/gallery/           # Albums list
http://127.0.0.1:8000/accounts/profile/  # User profile
```

### To Deploy to Render
1. Push code to GitHub
2. Go to render.com
3. Create new web service
4. Connect to GitHub repo
5. Render will deploy automatically

### To Push to GitHub
```bash
git add .
git commit -m "Configure Cloudinary and database setup"
git push
```

---

## THE END

Everything is working! ✓

Just upload a photo and it should display. If not, check the troubleshooting guide.
