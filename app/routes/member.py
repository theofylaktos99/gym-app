"""Member/Gym routes - Dashboard and member features"""
from flask import Blueprint, render_template, session, redirect, url_for, request
from app import db
from app.models import User, GymArea, WorkoutProgram, Booking
from app.utils.translations import get_translations
from app.utils.decorators import role_required
import random

bp = Blueprint('member', __name__, url_prefix='/member')

@bp.route('/dashboard')
@role_required('member', 'admin', 'staff')
def dashboard():
    """Member dashboard"""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    
    # Get language
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    t = get_translations(lang)
    
    # Get current user
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    # Get gym areas for this tenant
    areas = GymArea.query.filter_by(tenant_id=user.tenant_id).all()
    
    # Get workout programs
    workouts = WorkoutProgram.query.filter_by(tenant_id=user.tenant_id).all()
    
    # Get user bookings
    user_bookings = Booking.query.filter_by(
        user_id=user.id,
        status='confirmed'
    ).order_by(Booking.booking_date.desc(), Booking.start_time.desc()).all()
    
    # Format bookings for template
    formatted_bookings = []
    for booking in user_bookings:
        formatted_bookings.append({
            'id': booking.id,
            'room_name': booking.gym_area.name_en if lang == 'en' else booking.gym_area.name_el,
            'date': booking.booking_date.strftime('%Y-%m-%d'),
            'time': booking.start_time.strftime('%H:%M'),
            'duration': booking.duration_minutes,
            'trainer': booking.trainer_name,
            'price': booking.price
        })
    
    # User stats
    stats = {
        'total_workouts': user.total_workouts,
        'calories_burned': user.calories_burned,
        'streak_days': user.streak_days,
        'membership_level': user.membership_level
    }
    
    # Simulate real-time updates to gym areas
    for area in areas:
        if random.random() < 0.1:  # 10% chance to update
            change = random.randint(-2, 3)
            area.current_users = max(0, min(area.capacity, area.current_users + change))
            
            # Update status based on capacity
            usage_percent = area.current_users / area.capacity if area.capacity > 0 else 0
            if usage_percent >= 1.0:
                area.status = 'Full'
            elif usage_percent >= 0.8:
                area.status = 'Busy'
            elif area.status == 'Maintenance':
                pass  # Keep maintenance status
            elif area.status == 'Class in Session':
                pass  # Keep class status
            else:
                area.status = 'Available'
    
    db.session.commit()
    
    # Format areas for template
    formatted_areas = []
    for area in areas:
        formatted_areas.append({
            'id': area.id,
            'name': {'en': area.name_en, 'el': area.name_el},
            'status': area.status,
            'capacity': area.capacity,
            'current_users': area.current_users,
            'equipment': {'en': area.equipment_en, 'el': area.equipment_el},
            'icon': area.icon,
            'color': area.color,
            'bookable': area.is_bookable,
            'trainers': {'en': area.trainers_en, 'el': area.trainers_el} if area.is_bookable else None,
            'price_per_hour': area.price_per_hour
        })
    
    # Format workouts for template
    formatted_workouts = []
    for workout in workouts:
        formatted_workouts.append({
            'id': workout.id,
            'name': {'en': workout.name_en, 'el': workout.name_el},
            'duration': workout.duration,
            'difficulty': workout.difficulty,
            'calories': workout.calories,
            'exercises': workout.exercises,
            'icon': workout.icon,
            'color': workout.color
        })
    
    return render_template('dashboard.html',
                         areas=formatted_areas,
                         workouts=formatted_workouts,
                         stats=stats,
                         user_bookings=formatted_bookings,
                         t=t,
                         lang=lang)
