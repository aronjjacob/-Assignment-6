#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input --clear

# Run database migrations
python manage.py migrate

# Create superuser if it doesn't exist (optional, for initial deployment)
# Note: In production, create superuser via Django shell or admin panel
echo "Build script completed successfully!"
