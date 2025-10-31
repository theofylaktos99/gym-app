"""
Database Models for Gym SaaS Application
Multi-tenant architecture with support for multiple gym owners
"""
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class Tenant(db.Model):
    """Gym/Tenant - each gym owner gets a tenant"""
    __tablename__ = 'tenants'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    subdomain = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    
    # Subscription info
    subscription_plan = db.Column(db.String(50), default='trial')  # trial, basic, premium, enterprise
    subscription_status = db.Column(db.String(20), default='active')  # active, suspended, cancelled
    subscription_start = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_end = db.Column(db.DateTime)
    
    # Settings (JSON field for flexible configuration)
    settings = db.Column(db.JSON, default={})
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='tenant', lazy='dynamic', cascade='all, delete-orphan')
    gym_areas = db.relationship('GymArea', backref='tenant', lazy='dynamic', cascade='all, delete-orphan')
    workout_programs = db.relationship('WorkoutProgram', backref='tenant', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Tenant {self.name}>'

class User(db.Model):
    """Users - gym owners, staff, and members"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    
    # Basic info
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200))
    password_hash = db.Column(db.String(255), nullable=False)
    member_id = db.Column(db.String(50))  # For gym members
    
    # User type
    role = db.Column(db.String(20), nullable=False)  # admin, staff, member
    
    # Profile info
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    photo_url = db.Column(db.String(500))
    
    # Member stats (for members)
    total_workouts = db.Column(db.Integer, default=0)
    calories_burned = db.Column(db.Integer, default=0)
    streak_days = db.Column(db.Integer, default=0)
    membership_level = db.Column(db.String(50), default='Basic')
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    language_preference = db.Column(db.String(5), default='en')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    # Unique constraint: username must be unique within a tenant
    __table_args__ = (
        db.UniqueConstraint('tenant_id', 'username', name='_tenant_username_uc'),
        db.UniqueConstraint('tenant_id', 'email', name='_tenant_email_uc'),
    )
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class GymArea(db.Model):
    """Gym Areas - different workout zones"""
    __tablename__ = 'gym_areas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    
    # Area info
    name_en = db.Column(db.String(200), nullable=False)
    name_el = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text)
    description_el = db.Column(db.Text)
    
    # Capacity and status
    capacity = db.Column(db.Integer, nullable=False)
    current_users = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='Available')  # Available, Busy, Full, Maintenance, Class in Session
    
    # Visual
    icon = db.Column(db.String(10), default='💪')
    color = db.Column(db.String(20), default='#8B0000')
    
    # Equipment (JSON array)
    equipment_en = db.Column(db.JSON, default=[])
    equipment_el = db.Column(db.JSON, default=[])
    
    # Booking settings
    is_bookable = db.Column(db.Boolean, default=False)
    price_per_hour = db.Column(db.Float, default=0)
    
    # Trainers (JSON array)
    trainers_en = db.Column(db.JSON, default=[])
    trainers_el = db.Column(db.JSON, default=[])
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='gym_area', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<GymArea {self.name_en}>'

class WorkoutProgram(db.Model):
    """Workout Programs - predefined workout routines"""
    __tablename__ = 'workout_programs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'), nullable=False)
    
    # Program info
    name_en = db.Column(db.String(200), nullable=False)
    name_el = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text)
    description_el = db.Column(db.Text)
    
    # Details
    duration = db.Column(db.String(50))  # e.g., "45 min"
    difficulty = db.Column(db.String(50))  # Beginner, Intermediate, Advanced
    calories = db.Column(db.Integer)
    
    # Visual
    icon = db.Column(db.String(10), default='💪')
    color = db.Column(db.String(20), default='#8B0000')
    
    # Exercises (JSON array with multilingual support)
    exercises = db.Column(db.JSON, default=[])
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<WorkoutProgram {self.name_en}>'

class Booking(db.Model):
    """Bookings - room/trainer reservations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    gym_area_id = db.Column(db.String(36), db.ForeignKey('gym_areas.id'), nullable=False)
    
    # Booking details
    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    trainer_name = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled, completed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.id}>'

class WorkoutSession(db.Model):
    """Workout Sessions - track member workouts"""
    __tablename__ = 'workout_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    workout_program_id = db.Column(db.String(36), db.ForeignKey('workout_programs.id'))
    
    # Session details
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    
    # Status
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='workout_sessions')
    workout_program = db.relationship('WorkoutProgram', backref='sessions')
    
    def __repr__(self):
        return f'<WorkoutSession {self.id}>'
