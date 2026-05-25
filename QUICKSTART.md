# Quick Start & Deployment Checklist

## 📋 Pre-Deployment Checklist

### Local Development Setup
- [ ] Python 3.11+ installed
- [ ] Clone/download repository
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Update `.env` with your settings
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Run tests: `python manage.py test`
- [ ] Start dev server: `python manage.py runserver`

### Feature Testing (Local)
- [ ] User registration works
- [ ] User login works
- [ ] Profile viewing works
- [ ] Create album works
- [ ] Upload photo to album works
- [ ] Edit photo works
- [ ] Delete photo works
- [ ] Delete album works
- [ ] Cloudinary integration works
- [ ] Email sending works (if configured)
- [ ] Password reset works
- [ ] Admin panel accessible

### Production Preparation
- [ ] Generate SECRET_KEY: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- [ ] Verify `.env` is in `.gitignore`
- [ ] Verify `.env.example` has no secrets
- [ ] Test build script: `bash build.sh`
- [ ] Test static files collection
- [ ] Verify all dependencies in requirements.txt
- [ ] Review DEPLOYMENT.md guide
- [ ] Sign up for Render.com account
- [ ] Sign up for Cloudinary account (if not done)
- [ ] Get Cloudinary credentials

## 🚀 Render Deployment Steps

### Step 1: Prepare Repository
```bash
# Ensure clean repository
git status

# Add all changes
git add .

# Commit
git commit -m "Production-ready photo album app v1.0"

# Push to GitHub
git push origin main
```
- [ ] Code pushed to GitHub

### Step 2: Create PostgreSQL Database
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `photo-album-db`
   - Database: `photo_album`
   - Region: (choose nearest)
   - Plan: Free (testing) or standard (production)
4. Click "Create Database"
5. Wait for database to initialize (2-5 minutes)
6. Copy the Internal Database URL

- [ ] PostgreSQL database created
- [ ] Database URL copied

### Step 3: Create Web Service
1. Click "New +" → "Web Service"
2. Click "Connect your own"
3. Select your GitHub repository
4. Choose branch: `main`
5. Click "Connect"

- [ ] GitHub repository connected

### Step 4: Configure Web Service
1. Set **Name**: `photo-album-manager` (or your preference)
2. Set **Environment**: Python
3. Set **Region**: Same as database
4. Set **Build Command**: `./build.sh`
5. Set **Start Command**: `gunicorn recipe_project.wsgi:application --bind 0.0.0.0:$PORT`
6. Set **Plan**: Free (testing) or standard (production)

- [ ] Web service configured

### Step 5: Add Environment Variables
Click "Environment" and add these variables:

```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgresql://...internal...
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

- [ ] SECRET_KEY added
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS set
- [ ] DATABASE_URL added
- [ ] Cloudinary credentials added
- [ ] Email configuration added (optional)

### Step 6: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete (5-10 minutes)
3. Check logs for any errors

- [ ] Web service created
- [ ] Deployment completed successfully
- [ ] No errors in logs

### Step 7: Post-Deployment Setup
1. Visit your app: `https://your-app.onrender.com`
2. Go to app Shell in Render dashboard
3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
4. Test the application

- [ ] App accessible at public URL
- [ ] Superuser account created
- [ ] Home page loads
- [ ] Registration works
- [ ] Login works
- [ ] Can create albums
- [ ] Can upload photos

### Step 8: Final Testing
1. Register a test account
2. Create an album
3. Upload a photo
4. Edit the photo
5. Delete the photo
6. Delete the album
7. Test password reset (if email configured)
8. Visit admin panel

- [ ] Registration successful
- [ ] Album creation works
- [ ] Photo upload works
- [ ] Photo edit works
- [ ] Photo delete works
- [ ] Album delete works
- [ ] Admin panel accessible

## 🔧 Common Issues & Solutions

### Issue: Build fails
**Solution:**
- Check Render logs for specific error
- Verify `build.sh` is executable
- Ensure all dependencies are in requirements.txt
- Check Python version is 3.11+

### Issue: Database connection error
**Solution:**
- Verify DATABASE_URL format: `postgresql://user:password@host:5432/db`
- Check PostgreSQL database is running
- Verify ALLOWED_HOSTS includes your domain
- Test connection string locally

### Issue: Static files not loading
**Solution:**
```bash
# Redeploy and trigger static file collection
python manage.py collectstatic --clear --noinput
```

### Issue: Images not uploading
**Solution:**
- Verify CLOUDINARY_CLOUD_NAME is correct
- Check CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET
- Verify Cloudinary account is active
- Check storage limits in Cloudinary dashboard

### Issue: Email not working
**Solution:**
- Verify EMAIL_HOST_USER is correct
- Use Gmail App Password (not regular password)
- Enable 2FA on Google account
- Check EMAIL_PORT is 587

### Issue: Permission denied errors
**Solution:**
- Verify user is authenticated
- Check user owns the album/photo
- Review UserPassesTestMixin logic

## 📱 Testing the Application

### User Flow Test
1. **Visit homepage** → See welcome page
2. **Click "Sign Up"** → Register account
3. **Login** → Access albums page
4. **Create Album** → Give it a name
5. **Add Photo** → Select image file
6. **Edit Photo** → Update title
7. **Delete Photo** → Remove from album
8. **Delete Album** → Remove entire album
9. **View Profile** → See account info
10. **Logout** → Exit application

### Admin Testing
1. **Visit `/admin`**
2. **Login with superuser**
3. **View Users**
4. **View Albums**
5. **View Photos**
6. **Edit an Album**
7. **Delete a Photo from admin**

## 📞 Support Resources

### Documentation
- [README.md](README.md) - Complete overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [API.md](API.md) - Endpoint reference
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - What was built

### External Resources
- [Django Docs](https://docs.djangoproject.com/)
- [Render Docs](https://render.com/docs)
- [Cloudinary Docs](https://cloudinary.com/documentation)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## 🎯 Success Criteria

✅ Application successfully deployed when:
- Web service is running on Render
- Database is connected
- Users can register
- Users can login
- Photos can be uploaded to Cloudinary
- Photos can be viewed/edited/deleted
- Admin panel is accessible
- No errors in logs

## 📊 Performance Tips

### For Better Performance
- Use database indexes (already configured)
- Enable Cloudinary CDN (automatic)
- Use WhiteNoise for static files (configured)
- Consider Redis cache layer (future enhancement)

### Monitoring
- Check Render metrics dashboard
- Monitor error rates
- Track response times
- Review Cloudinary storage usage

## 🔐 Security Checklist

- [ ] SECRET_KEY is strong and unique
- [ ] DEBUG is False in production
- [ ] DATABASE_URL uses secure connection
- [ ] HTTPS enabled on Render (automatic)
- [ ] Sensitive data in environment variables only
- [ ] Cloudinary credentials secured
- [ ] Email password not in code
- [ ] Regular security updates applied

## 🚀 Ready to Deploy?

If all checklist items are completed, your application is ready for production!

**Next Steps:**
1. Push to GitHub
2. Create PostgreSQL on Render
3. Create Web Service on Render
4. Add environment variables
5. Deploy and test
6. Share with users!

---

**Questions?** Refer to the documentation files or check Render support.

**Last Updated:** May 25, 2026
**Status:** Ready for Production
