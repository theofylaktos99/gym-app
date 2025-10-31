#!/usr/bin/env bash
# Render.com build script

set -e  # Exit on error

echo "🔨 Building Gym SaaS Application for Render..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations with smart handling
echo "🗄️  Running database migrations..."
export FLASK_APP=run.py

# Create temporary file for migration logs
MIGRATION_LOG=$(mktemp)

# Try to run migrations and capture both output and exit code
set +e  # Temporarily disable exit on error
flask db upgrade > "$MIGRATION_LOG" 2>&1
MIGRATION_EXIT_CODE=$?
set -e  # Re-enable exit on error

cat "$MIGRATION_LOG"  # Show the output

if [ $MIGRATION_EXIT_CODE -ne 0 ]; then
    # Check if the error is about tables already existing
    if grep -q "table.*already exists" "$MIGRATION_LOG"; then
        echo "⚠️  Tables already exist. Stamping database with current migration..."
        flask db stamp head
        echo "✅ Database stamped successfully!"
    else
        echo "❌ Migration failed for an unknown reason!"
        echo "Please check the logs above for details."
        rm -f "$MIGRATION_LOG"
        exit 1
    fi
else
    echo "✅ Migrations applied successfully!"
fi

# Clean up temporary log file
rm -f "$MIGRATION_LOG"

# Seed demo data (only if needed)
if [ "$SEED_DEMO_DATA" = "true" ]; then
    echo "🌱 Seeding demo data..."
    python run.py seed_demo_data || echo "⚠️  Demo data already exists"
fi

echo "✅ Build completed successfully!"
