#!/usr/bin/env python
"""
Comprehensive Configuration Verification Script
Tests: Environment variables, Database, and Cloudinary setup
"""
import os
import sys
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')

import django
django.setup()

from django.conf import settings
import cloudinary.api

print("=" * 70)
print("CONFIGURATION VERIFICATION REPORT")
print("=" * 70)

# ============================================================================
# 1. ENVIRONMENT VARIABLES CHECK
# ============================================================================
print("\n1. ENVIRONMENT VARIABLES (.env FILE)")
print("-" * 70)

env_vars = {
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'DEBUG': os.getenv('DEBUG'),
    'DATABASE_URL': os.getenv('DATABASE_URL'),
    'USE_CLOUDINARY': os.getenv('USE_CLOUDINARY'),
    'CLOUDINARY_CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'CLOUDINARY_API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'CLOUDINARY_API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS'),
}

for key, value in env_vars.items():
    if value:
        # Mask sensitive values
        if key in ['SECRET_KEY', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET', 'DATABASE_URL']:
            display_value = f"{str(value)[:20]}..." if len(str(value)) > 20 else value
        else:
            display_value = value
        print(f"✓ {key}: {display_value}")
    else:
        print(f"✗ {key}: NOT SET")

# ============================================================================
# 2. DJANGO SETTINGS CHECK
# ============================================================================
print("\n2. DJANGO SETTINGS (settings.py)")
print("-" * 70)

print(f"✓ DEBUG: {settings.DEBUG}")
print(f"✓ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"✓ SECRET_KEY exists: {bool(settings.SECRET_KEY)}")

# ============================================================================
# 3. DATABASE CONFIGURATION CHECK
# ============================================================================
print("\n3. DATABASE CONFIGURATION")
print("-" * 70)

db_config = settings.DATABASES['default']
print(f"✓ Database ENGINE: {db_config['ENGINE']}")

if 'NAME' in db_config:
    print(f"✓ Database NAME: {db_config['NAME']}")
if 'HOST' in db_config:
    print(f"✓ Database HOST: {db_config['HOST']}")
if 'USER' in db_config:
    print(f"✓ Database USER: {db_config['USER']}")

# ============================================================================
# 4. STORAGE CONFIGURATION CHECK
# ============================================================================
print("\n4. STORAGE CONFIGURATION")
print("-" * 70)

print(f"✓ Default Storage Backend: {settings.STORAGES['default']['BACKEND']}")
print(f"✓ Using Cloudinary Storage: {settings.STORAGES['default']['BACKEND'] == 'cloudinary_storage.storage.MediaCloudinaryStorage'}")

# ============================================================================
# 5. CLOUDINARY CONFIGURATION CHECK
# ============================================================================
print("\n5. CLOUDINARY CONFIGURATION")
print("-" * 70)

cloudinary_settings = settings.CLOUDINARY_STORAGE
print(f"✓ CLOUDINARY_CLOUD_NAME: {cloudinary_settings['CLOUDINARY_CLOUD_NAME']}")
print(f"✓ CLOUDINARY_API_KEY exists: {bool(cloudinary_settings['CLOUDINARY_API_KEY'])}")
print(f"✓ CLOUDINARY_API_SECRET exists: {bool(cloudinary_settings['CLOUDINARY_API_SECRET'])}")

# ============================================================================
# 6. DATABASE CONNECTION TEST
# ============================================================================
print("\n6. DATABASE CONNECTION TEST")
print("-" * 70)

try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✓ Database connection: SUCCESS")
    print(f"✓ Database type: {db_config['ENGINE'].split('.')[-1]}")
except Exception as e:
    print(f"✗ Database connection FAILED: {str(e)}")
    print("  This may be normal if DATABASE_URL points to production (Render)")

# ============================================================================
# 7. CLOUDINARY CONNECTION TEST
# ============================================================================
print("\n7. CLOUDINARY CONNECTION TEST")
print("-" * 70)

try:
    # Try to get account info from Cloudinary
    account_info = cloudinary.api.ping()
    if account_info.get('status') == 'ok':
        print("✓ Cloudinary connection: SUCCESS")
        print(f"✓ Response: {account_info}")
    else:
        print(f"✗ Cloudinary connection: UNEXPECTED RESPONSE")
        print(f"  Response: {account_info}")
except Exception as e:
    print(f"✗ Cloudinary connection FAILED: {str(e)}")
    print("  Check if CLOUDINARY credentials are valid")

# ============================================================================
# 8. MODEL CHECK - Photo Upload Configuration
# ============================================================================
print("\n8. PHOTO MODEL CONFIGURATION")
print("-" * 70)

try:
    from gallery.models import Photo
    
    # Get field types
    image_field = Photo._meta.get_field('image')
    print(f"✓ Photo.image field type: {type(image_field).__name__}")
    print(f"✓ Storage backend for Photo.image: {image_field.storage.__class__.__name__}")
    
except Exception as e:
    print(f"✗ Error checking Photo model: {str(e)}")

# ============================================================================
# 9. SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

checks = {
    'Environment variables loaded': bool(os.getenv('CLOUDINARY_CLOUD_NAME')),
    'Cloudinary configured': bool(settings.CLOUDINARY_STORAGE['CLOUDINARY_CLOUD_NAME']),
    'Using Cloudinary storage': settings.STORAGES['default']['BACKEND'] == 'cloudinary_storage.storage.MediaCloudinaryStorage',
    'DEBUG mode': settings.DEBUG,
    'ALLOWED_HOSTS set': bool(settings.ALLOWED_HOSTS),
}

passed = sum(1 for v in checks.values() if v)
total = len(checks)

print(f"\nPassed: {passed}/{total} checks\n")

for check, result in checks.items():
    status = "✓" if result else "✗"
    print(f"{status} {check}")

if passed == total:
    print("\n✓ ALL CHECKS PASSED - Configuration looks good!")
else:
    print(f"\n⚠ {total - passed} check(s) failed - Review the configuration")

print("\n" + "=" * 70)
