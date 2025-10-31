#!/bin/bash

# Gym SaaS Application - Quick Setup Script
# This script sets up the application for development

set -e  # Exit on error

echo "🏋️ Gym SaaS Application Setup"
echo "=============================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version || {
    echo "❌ Python 3 is not installed"
    exit 1
}

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate || {
    echo "⚠️  Could not activate venv, continuing anyway..."
}

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install Flask==3.0.0 \
    Flask-SQLAlchemy==3.1.1 \
    Flask-Migrate==4.0.5 \
    Flask-JWT-Extended==4.6.0 \
    Flask-Bcrypt==1.0.1 \
    Flask-CORS==4.0.0 \
    python-dotenv==1.0.0 \
    Werkzeug==3.0.1 \
    gunicorn==21.2.0

echo "✅ Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
FLASK_ENV=development
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DEV_DATABASE_URL=sqlite:///gym_dev.db
PORT=5055
EOF
    echo "✅ .env file created with secure keys"
else
    echo "✅ .env file already exists"
fi

# Initialize Flask-Migrate if not already done
if [ ! -d "migrations" ]; then
    echo "🗄️  Initializing database migrations..."
    export FLASK_APP=run.py
    flask db init
    echo "✅ Migrations initialized"
fi

# Create migration
echo "📋 Creating database migration..."
export FLASK_APP=run.py
flask db migrate -m "Initial migration" 2>/dev/null || echo "Migration already exists"

# Run migration
echo "⬆️  Running database migrations..."
flask db upgrade

# Seed demo data
echo "🌱 Seeding demo data..."
python3 run.py seed_demo_data || {
    echo "⚠️  Demo data already exists or error occurred"
}

echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "📌 Demo Credentials:"
echo "   Admin:  username='admin'  password='admin123'"
echo "   Member: username='123456' password='654321'"
echo "   Staff:  username='staff'  password='staff123'"
echo ""
echo "🚀 To start the application:"
echo "   source venv/bin/activate"
echo "   python3 run.py"
echo ""
echo "🌐 Access at: http://localhost:5055"
echo ""
echo "📖 Documentation:"
echo "   - README_SAAS.md - Full documentation"
echo "   - QUICKSTART.md - Quick start guide"
echo "   - MIGRATION_GUIDE.md - Migration from original"
echo ""
