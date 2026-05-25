#!/usr/bin/env bash
# Quick Start Script for Photo Album Manager
# This script sets up the local development environment

set -e

echo "🚀 Photo Album Manager - Quick Start Setup"
echo "=========================================="

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your local settings"
fi

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate
echo "✓ Migrations completed"

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"

# Create superuser
echo ""
echo "👤 Creating superuser account..."
python manage.py createsuperuser

# Done
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the development server: python manage.py runserver"
echo "2. Visit http://127.0.0.1:8000/"
echo "3. Admin panel: http://127.0.0.1:8000/admin/"
echo ""
