"""
Gym SaaS Application Entry Point
Modern multi-tenant gym management system
"""
import os
from app import create_app, db
from app.models import Tenant, User, GymArea, WorkoutProgram, Booking, WorkoutSession

# Create application instance
app = create_app()

# Flask shell context
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Tenant': Tenant,
        'User': User,
        'GymArea': GymArea,
        'WorkoutProgram': WorkoutProgram,
        'Booking': Booking,
        'WorkoutSession': WorkoutSession
    }

# CLI commands
@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def seed_demo_data():
    """Seed database with demo data"""
    from app.services.seed_data import seed_all
    seed_all()
    print("Demo data seeded successfully!")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5055))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
