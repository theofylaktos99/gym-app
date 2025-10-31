#!/usr/bin/env bash
# Render.com build script

echo "🔨 Building Gym SaaS Application for Render..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations with smart handling
echo "🗄️  Running database migrations..."
export FLASK_APP=run.py

# Try to run migrations and capture both output and exit code
set +e  # Temporarily disable exit on error
flask db upgrade > /tmp/migration.log 2>&1
MIGRATION_EXIT_CODE=$?
cat /tmp/migration.log  # Show the output
set -e  # Re-enable exit on error

if [ $MIGRATION_EXIT_CODE -ne 0 ]; then
    # Check if the error is about tables already existing
    if grep -q "already exists" /tmp/migration.log; then
        echo "⚠️  Tables already exist. Stamping database with current migration..."
        flask db stamp head
        echo "✅ Database stamped successfully!"
    else
        echo "❌ Migration failed for an unknown reason!"
        echo "Please check the logs above for details."
        exit 1
    fi
else
    echo "✅ Migrations applied successfully!"
fi

# Seed demo data (only if needed)
if [ "$SEED_DEMO_DATA" = "true" ]; then
    echo "🌱 Seeding demo data..."
    python run.py seed_demo_data || echo "⚠️  Demo data already exists"
fi

echo "✅ Build completed successfully!"
