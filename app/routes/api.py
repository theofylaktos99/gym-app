"""API routes - RESTful API endpoints"""
from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, GymArea, WorkoutProgram, Booking, WorkoutSession, Tenant
from datetime import datetime, date, time as dt_time
from app.utils.decorators import tenant_required

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/gym-status')
def gym_status():
    """API endpoint for real-time gym data"""
    tenant_id = request.headers.get('X-Tenant-ID') or session.get('tenant_id')
    
    if not tenant_id:
        return jsonify({'success': False, 'message': 'Tenant ID required'}), 400
    
    areas = GymArea.query.filter_by(tenant_id=tenant_id).all()
    
    areas_data = [{
        'id': area.id,
        'name': {'en': area.name_en, 'el': area.name_el},
        'status': area.status,
        'capacity': area.capacity,
        'current_users': area.current_users,
        'usage_percent': (area.current_users / area.capacity * 100) if area.capacity > 0 else 0
    } for area in areas]
    
    return jsonify({
        'areas': areas_data,
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/start-workout', methods=['POST'])
def start_workout():
    """API endpoint to log workout start"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    workout_id = request.json.get('workout_id')
    workout = WorkoutProgram.query.get(workout_id)
    
    if not workout:
        return jsonify({'success': False, 'message': 'Workout not found'}), 404
    
    # Create workout session
    workout_session = WorkoutSession(
        user_id=user_id,
        workout_program_id=workout_id,
        start_time=datetime.utcnow(),
        status='in_progress'
    )
    
    db.session.add(workout_session)
    db.session.commit()
    
    # Store in session for convenience
    session['current_workout_session_id'] = workout_session.id
    
    return jsonify({
        'success': True,
        'message': f"Started workout",
        'session_id': workout_session.id,
        'workout': {
            'id': workout.id,
            'name_en': workout.name_en,
            'name_el': workout.name_el
        }
    })

@bp.route('/complete-workout', methods=['POST'])
def complete_workout():
    """API endpoint to log workout completion"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    session_id = request.json.get('session_id') or session.get('current_workout_session_id')
    
    if not session_id:
        return jsonify({'success': False, 'message': 'No active workout found'}), 400
    
    workout_session = WorkoutSession.query.get(session_id)
    
    if not workout_session or workout_session.user_id != user_id:
        return jsonify({'success': False, 'message': 'Invalid workout session'}), 404
    
    # Complete the session
    workout_session.end_time = datetime.utcnow()
    workout_session.duration_seconds = int((workout_session.end_time - workout_session.start_time).total_seconds())
    workout_session.calories_burned = request.json.get('calories_burned', workout_session.workout_program.calories if workout_session.workout_program else 0)
    workout_session.status = 'completed'
    
    # Update user stats
    user = User.query.get(user_id)
    user.total_workouts += 1
    user.calories_burned += workout_session.calories_burned
    
    db.session.commit()
    
    # Clear from session
    session.pop('current_workout_session_id', None)
    
    return jsonify({
        'success': True,
        'message': 'Workout completed successfully!',
        'stats': {
            'total_workouts': user.total_workouts,
            'calories_burned': user.calories_burned,
            'streak_days': user.streak_days
        }
    })

@bp.route('/book-room', methods=['POST'])
def book_room():
    """API endpoint to book a room"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.json
    
    # Validate required fields
    required_fields = ['room_id', 'time', 'duration', 'price']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    # Parse time
    try:
        booking_time = datetime.strptime(data['time'], '%H:%M').time()
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid time format'}), 400
    
    # Create booking
    booking = Booking(
        user_id=user_id,
        gym_area_id=data['room_id'],
        booking_date=date.today(),
        start_time=booking_time,
        duration_minutes=int(data['duration']),
        trainer_name=data.get('trainer', ''),
        price=float(data['price']),
        status='confirmed'
    )
    
    # Check for conflicts
    conflict = Booking.query.filter_by(
        gym_area_id=booking.gym_area_id,
        booking_date=booking.booking_date,
        start_time=booking.start_time,
        status='confirmed'
    ).first()
    
    if conflict:
        return jsonify({'success': False, 'message': 'Time slot already booked'}), 400
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Room booked successfully!',
        'booking': {
            'id': booking.id,
            'date': booking.booking_date.isoformat(),
            'time': booking.start_time.strftime('%H:%M'),
            'duration': booking.duration_minutes,
            'price': booking.price
        }
    })

@bp.route('/cancel-booking', methods=['POST'])
def cancel_booking():
    """API endpoint to cancel a booking"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    booking_id = request.json.get('booking_id')
    
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404
    
    if booking.user_id != user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Cancel the booking
    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Booking cancelled successfully!'
    })

@bp.route('/user-bookings')
def get_user_bookings():
    """API endpoint to get user's bookings"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    bookings = Booking.query.filter_by(
        user_id=user_id,
        status='confirmed'
    ).order_by(Booking.booking_date.desc(), Booking.start_time.desc()).all()
    
    bookings_data = [{
        'id': booking.id,
        'room_id': booking.gym_area_id,
        'room_name': booking.gym_area.name_en,  # TODO: Make language-aware
        'date': booking.booking_date.isoformat(),
        'time': booking.start_time.strftime('%H:%M'),
        'duration': booking.duration_minutes,
        'trainer': booking.trainer_name,
        'price': booking.price
    } for booking in bookings]
    
    return jsonify({
        'success': True,
        'bookings': bookings_data
    })

@bp.route('/available-slots/<room_id>')
def get_available_slots(room_id):
    """API endpoint to get available time slots for a room"""
    today = date.today()
    
    # Get existing bookings for this room today
    existing_bookings = Booking.query.filter_by(
        gym_area_id=room_id,
        booking_date=today,
        status='confirmed'
    ).all()
    
    booked_times = {booking.start_time.strftime('%H:%M') for booking in existing_bookings}
    
    # Generate available slots
    slots = []
    current_hour = datetime.now().hour
    
    for hour in range(max(current_hour + 1, 8), 22):  # 8 AM to 10 PM
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            slots.append({
                'time': time_str,
                'available': time_str not in booked_times
            })
    
    return jsonify({
        'success': True,
        'slots': slots
    })
