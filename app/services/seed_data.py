"""
Seed Data Service
Populates database with demo data for development and testing
"""
from app import db
from app.models import Tenant, User, GymArea, WorkoutProgram
from datetime import datetime, timedelta

def seed_all():
    """Seed all demo data"""
    print("Seeding demo data...")
    
    # Clear existing data (be careful in production!)
    db.drop_all()
    db.create_all()
    
    # Create demo tenant
    tenant = create_demo_tenant()
    
    # Create demo users
    create_demo_users(tenant.id)
    
    # Create gym areas
    create_gym_areas(tenant.id)
    
    # Create workout programs
    create_workout_programs(tenant.id)
    
    db.session.commit()
    print("Demo data seeded successfully!")

def create_demo_tenant():
    """Create a demo gym tenant"""
    tenant = Tenant(
        name="Demo Gym",
        subdomain="demo",
        email="demo@yourgym.com",
        phone="+30 210 1234567",
        address="123 Fitness Street, Athens, Greece",
        subscription_plan="premium",
        subscription_status="active",
        subscription_start=datetime.utcnow(),
        subscription_end=datetime.utcnow() + timedelta(days=365),
        settings={
            'timezone': 'Europe/Athens',
            'currency': 'EUR',
            'opening_hours': '06:00-23:00',
            'languages': ['en', 'el']
        }
    )
    db.session.add(tenant)
    db.session.flush()
    return tenant

def create_demo_users(tenant_id):
    """Create demo users"""
    # Admin user
    admin = User(
        tenant_id=tenant_id,
        username='admin',
        email='admin@demo.com',
        first_name='Admin',
        last_name='User',
        role='admin',
        membership_level='Premium'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Member user (original credentials)
    member = User(
        tenant_id=tenant_id,
        username='123456',
        email='member@demo.com',
        member_id='123456',
        first_name='John',
        last_name='Doe',
        role='member',
        total_workouts=147,
        calories_burned=18500,
        streak_days=12,
        membership_level='Premium'
    )
    member.set_password('654321')
    db.session.add(member)
    
    # Staff user
    staff = User(
        tenant_id=tenant_id,
        username='staff',
        email='staff@demo.com',
        first_name='Maria',
        last_name='Trainer',
        role='staff'
    )
    staff.set_password('staff123')
    db.session.add(staff)

def create_gym_areas(tenant_id):
    """Create gym areas"""
    areas = [
        {
            'name_en': 'Strength Training Zone',
            'name_el': 'Ζώνη Προπόνησης Δύναμης',
            'capacity': 25,
            'current_users': 12,
            'status': 'Available',
            'equipment_en': ['Dumbbells', 'Barbells', 'Benches', 'Squat Racks'],
            'equipment_el': ['Αλτήρες', 'Μπάρες', 'Πάγκοι', 'Στάσεις Καθίσματος'],
            'icon': '💪',
            'color': '#8B0000',
            'is_bookable': True,
            'trainers_en': ['Alex Strong', 'Maria Power', 'John Muscle'],
            'trainers_el': ['Αλέξης Δυναμικός', 'Μαρία Δύναμη', 'Γιάννης Μυς'],
            'price_per_hour': 25
        },
        {
            'name_en': 'Cardio Arena',
            'name_el': 'Αρένα Καρδιοπροπόνησης',
            'capacity': 30,
            'current_users': 28,
            'status': 'Busy',
            'equipment_en': ['Treadmills', 'Ellipticals', 'Bikes', 'Rowing Machines'],
            'equipment_el': ['Διάδρομοι Τρεξίματος', 'Ελλειπτικά', 'Ποδήλατα', 'Κωπηλατικά'],
            'icon': '🏃',
            'color': '#FF4500',
            'is_bookable': False
        },
        {
            'name_en': 'Functional Training',
            'name_el': 'Λειτουργική Προπόνηση',
            'capacity': 20,
            'current_users': 8,
            'status': 'Available',
            'equipment_en': ['Battle Ropes', 'Kettlebells', 'TRX', 'Medicine Balls'],
            'equipment_el': ['Σχοινιά Μάχης', 'Κουδούνια', 'TRX', 'Μπάλες Ιατρικής'],
            'icon': '🔥',
            'color': '#FF8C00',
            'is_bookable': True,
            'trainers_en': ['Sofia Fit', 'Mike Cross', 'Anna Athletic'],
            'trainers_el': ['Σοφία Φιτ', 'Μάικ Κρος', 'Άννα Αθλητική'],
            'price_per_hour': 30
        },
        {
            'name_en': 'Yoga & Mindfulness',
            'name_el': 'Γιόγκα & Διαλογισμός',
            'capacity': 15,
            'current_users': 15,
            'status': 'Class in Session',
            'equipment_en': ['Yoga Mats', 'Blocks', 'Straps', 'Meditation Cushions'],
            'equipment_el': ['Στρώματα Γιόγκα', 'Τούβλα', 'Ιμάντες', 'Μαξιλάρια Διαλογισμού'],
            'icon': '🧘',
            'color': '#4B0082',
            'is_bookable': True,
            'trainers_en': ['Elena Zen', 'David Peace', 'Lisa Harmony'],
            'trainers_el': ['Έλενα Ζεν', 'Δαυίδ Ειρήνη', 'Λίζα Αρμονία'],
            'price_per_hour': 20
        },
        {
            'name_en': 'Boxing Arena',
            'name_el': 'Αρένα Πυγμαχίας',
            'capacity': 12,
            'current_users': 3,
            'status': 'Available',
            'equipment_en': ['Heavy Bags', 'Speed Bags', 'Boxing Gloves', 'Pads'],
            'equipment_el': ['Βαριά Σάκια', 'Σάκια Ταχύτητας', 'Γάντια Πυγμαχίας', 'Πάντες'],
            'icon': '🥊',
            'color': '#DC143C',
            'is_bookable': True,
            'trainers_en': ['Rocky Fighter', 'Muhammad Strike', 'Tyson Power'],
            'trainers_el': ['Ρόκι Μαχητής', 'Μουχάμεντ Χτύπημα', 'Τάισον Δύναμη'],
            'price_per_hour': 35
        },
        {
            'name_en': 'Swimming Pool',
            'name_el': 'Πισίνα',
            'capacity': 40,
            'current_users': 0,
            'status': 'Maintenance',
            'equipment_en': ['Olympic Pool', 'Lanes', 'Diving Board', 'Jacuzzi'],
            'equipment_el': ['Ολυμπιακή Πισίνα', 'Διαδρομές', 'Βατήρας', 'Τζακούζι'],
            'icon': '🏊',
            'color': '#191970',
            'is_bookable': False
        },
        {
            'name_en': 'Pilates Studio',
            'name_el': 'Στούντιο Πιλάτες',
            'capacity': 12,
            'current_users': 4,
            'status': 'Available',
            'equipment_en': ['Reformer Machines', 'Pilates Mats', 'Magic Circles', 'Resistance Bands'],
            'equipment_el': ['Μηχανές Reformer', 'Στρώματα Πιλάτες', 'Μαγικοί Κύκλοι', 'Λάστιχα Αντίστασης'],
            'icon': '🤸‍♀️',
            'color': '#8B008B',
            'is_bookable': True,
            'trainers_en': ['Grace Balance', 'Emma Core', 'Sophia Stretch'],
            'trainers_el': ['Γκρέις Ισορροπία', 'Έμμα Κορμός', 'Σοφία Τέντωμα'],
            'price_per_hour': 28
        },
        {
            'name_en': 'Martial Arts Dojo',
            'name_el': 'Ντότζο Πολεμικών Τεχνών',
            'capacity': 16,
            'current_users': 2,
            'status': 'Available',
            'equipment_en': ['Mats', 'Makiwara Boards', 'Wooden Dummies', 'Weapons Rack'],
            'equipment_el': ['Στρώματα', 'Πίνακες Makiwara', 'Ξύλινα Ομοιώματα', 'Στάση Όπλων'],
            'icon': '🥋',
            'color': '#B22222',
            'is_bookable': True,
            'trainers_en': ['Sensei Tanaka', 'Master Lee', 'Sifu Chen'],
            'trainers_el': ['Σενσέι Τανάκα', 'Μάστερ Λι', 'Σίφου Τσεν'],
            'price_per_hour': 40
        }
    ]
    
    for area_data in areas:
        area = GymArea(tenant_id=tenant_id, **area_data)
        db.session.add(area)

def create_workout_programs(tenant_id):
    """Create workout programs"""
    programs = [
        {
            'name_en': 'Beast Mode Strength',
            'name_el': 'Προπόνηση Δύναμης Θηρίου',
            'duration': '45 min',
            'difficulty': 'Advanced',
            'calories': 400,
            'icon': '💪',
            'color': '#8B0000',
            'exercises': [
                {
                    'name': {'en': 'Deadlifts', 'el': 'Νεκρές Αναβάσεις'},
                    'sets': 4,
                    'reps': '6-8',
                    'rest': {'en': '3 min', 'el': '3 λεπτά'}
                },
                {
                    'name': {'en': 'Squats', 'el': 'Καθίσματα'},
                    'sets': 4,
                    'reps': '8-10',
                    'rest': {'en': '2.5 min', 'el': '2.5 λεπτά'}
                },
                {
                    'name': {'en': 'Bench Press', 'el': 'Πιέσεις Πάγκου'},
                    'sets': 4,
                    'reps': '6-8',
                    'rest': {'en': '3 min', 'el': '3 λεπτά'}
                },
                {
                    'name': {'en': 'Pull-ups', 'el': 'Αναρριχήσεις'},
                    'sets': 3,
                    'reps': '8-12',
                    'rest': {'en': '2 min', 'el': '2 λεπτά'}
                },
                {
                    'name': {'en': 'Overhead Press', 'el': 'Πιέσεις από Πάνω'},
                    'sets': 3,
                    'reps': '8-10',
                    'rest': {'en': '2 min', 'el': '2 λεπτά'}
                }
            ]
        },
        {
            'name_en': 'Cardio Burn',
            'name_el': 'Καύση Καρδιοπροπόνησης',
            'duration': '30 min',
            'difficulty': 'Intermediate',
            'calories': 350,
            'icon': '🔥',
            'color': '#FF4500',
            'exercises': [
                {
                    'name': {'en': 'Treadmill Sprint', 'el': 'Σπριντ Διαδρόμου'},
                    'sets': 8,
                    'reps': '30s on/30s off',
                    'rest': {'en': '1 min', 'el': '1 λεπτό'}
                },
                {
                    'name': {'en': 'Burpees', 'el': 'Μπέρπις'},
                    'sets': 3,
                    'reps': '15',
                    'rest': {'en': '1 min', 'el': '1 λεπτό'}
                },
                {
                    'name': {'en': 'Mountain Climbers', 'el': 'Αναρριχητές Βουνού'},
                    'sets': 3,
                    'reps': '30s',
                    'rest': {'en': '30s', 'el': '30 δευτ'}
                },
                {
                    'name': {'en': 'Jump Rope', 'el': 'Σχοινάκι'},
                    'sets': 5,
                    'reps': '1 min',
                    'rest': {'en': '30s', 'el': '30 δευτ'}
                }
            ]
        },
        {
            'name_en': 'Functional Flow',
            'name_el': 'Λειτουργική Ροή',
            'duration': '40 min',
            'difficulty': 'Beginner',
            'calories': 280,
            'icon': '⚡',
            'color': '#FF8C00',
            'exercises': [
                {
                    'name': {'en': 'Bodyweight Squats', 'el': 'Καθίσματα Σώματος'},
                    'sets': 3,
                    'reps': '15',
                    'rest': {'en': '1 min', 'el': '1 λεπτό'}
                },
                {
                    'name': {'en': 'Push-ups', 'el': 'Κάμψεις'},
                    'sets': 3,
                    'reps': '10-15',
                    'rest': {'en': '1 min', 'el': '1 λεπτό'}
                },
                {
                    'name': {'en': 'Lunges', 'el': 'Βηματισμοί'},
                    'sets': 3,
                    'reps': '12 each leg',
                    'rest': {'en': '1 min', 'el': '1 λεπτό'}
                },
                {
                    'name': {'en': 'Plank', 'el': 'Σανίδα'},
                    'sets': 3,
                    'reps': '30-60s',
                    'rest': {'en': '1 min', 'el': '1 λεπτό'}
                },
                {
                    'name': {'en': 'Glute Bridges', 'el': 'Γέφυρες Γλουτών'},
                    'sets': 3,
                    'reps': '15',
                    'rest': {'en': '1 min', 'el': '1 λεπτό'}
                }
            ]
        }
    ]
    
    for program_data in programs:
        program = WorkoutProgram(tenant_id=tenant_id, **program_data)
        db.session.add(program)
