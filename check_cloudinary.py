#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')
django.setup()

import cloudinary
from dotenv import load_dotenv

load_dotenv()

print("=== Cloudinary Configuration Check ===\n")

cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

print(f"✓ CLOUDINARY_CLOUD_NAME: {cloud_name if cloud_name else 'NOT SET'}")
print(f"✓ CLOUDINARY_API_KEY: {'***' + api_key[-5:] if api_key else 'NOT SET'}")
print(f"✓ CLOUDINARY_API_SECRET: {'***' + api_secret[-5:] if api_secret else 'NOT SET'}")

print(f"\n✓ Cloudinary config cloud_name: {cloudinary.config().cloud_name}")
print(f"✓ Cloudinary config api_key: {cloudinary.config().api_key is not None}")

print("\n=== Database Check ===\n")

from gallery.models import Photo, Album
from django.contrib.auth.models import User

print(f"✓ Total users: {User.objects.count()}")
print(f"✓ Total albums: {Album.objects.count()}")
print(f"✓ Total photos: {Photo.objects.count()}")

if Photo.objects.exists():
    print("\n=== Recent Photos ===\n")
    for photo in Photo.objects.all()[:5]:
        print(f"  - {photo.title}")
        print(f"    Image field value: {photo.image}")
        print(f"    Image URL: {photo.image.url if photo.image else 'NO IMAGE'}")
        print()
