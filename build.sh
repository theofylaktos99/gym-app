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

# Create temporary file for migration logs and ensure cleanup
MIGRATION_LOG=$(mktemp)
trap 'rm -f "$MIGRATION_LOG"' EXIT

# Try to run migrations and capture both output and exit code
set +e  # Temporarily disable exit on error
flask db upgrade > "$MIGRATION_LOG" 2>&1
MIGRATION_EXIT_CODE=$?
set -e  # Re-enable exit on error

cat "$MIGRATION_LOG"  # Show the output

if [ $MIGRATION_EXIT_CODE -ne 0 ]; then
    # Check if the error is about tables already existing (match SQLite/PostgreSQL format)
    if grep -qE 'table "[^"]*" already exists|table .* already exists' "$MIGRATION_LOG"; then
        echo "⚠️  Tables already exist. Stamping database with current migration..."
        if flask db stamp head; then
            echo "✅ Database stamped successfully!"
        else
            echo "❌ Failed to stamp database!"
            exit 1
        fi
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
