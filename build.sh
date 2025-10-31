#!/usr/bin/env bash
# Render.com build script

set -e  # Exit on error

echo "🔨 Building Gym SaaS Application for Render..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
export FLASK_APP=run.py
flask db upgrade || echo "⚠️  Migration failed or no migrations needed"

# Seed demo data (only if needed)
if [ "$SEED_DEMO_DATA" = "true" ]; then
    echo "🌱 Seeding demo data..."
    python run.py seed_demo_data || echo "⚠️  Demo data already exists"
fi

echo "✅ Build completed successfully!"
