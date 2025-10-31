"""
Authentication Routes
Handles login, logout, and session management
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Tenant
from app.utils.decorators import tenant_required
from app.utils.translations import get_translations

bp = Blueprint('auth', __name__, url_prefix='')

@bp.route('/', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    # Get language preference
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    t = get_translations(lang)
    
    # Get tenant from subdomain or header
    tenant_id = request.headers.get('X-Tenant-ID') or session.get('tenant_id')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        language = request.form.get('language', lang)
        
        # Find user
        query = User.query.filter_by(username=username, is_active=True)
        if tenant_id:
            query = query.filter_by(tenant_id=tenant_id)
        user = query.first()
        
        if user and user.check_password(password):
            # Successful login
            session['logged_in'] = True
            session['user_id'] = user.id
            session['tenant_id'] = user.tenant_id
            session['language'] = language
            session['role'] = user.role
            
            # Update last login
            user.last_login = db.func.now()
            user.language_preference = language
            db.session.commit()
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('member.dashboard'))
        else:
            flash(t['invalid_credentials'], 'error')
            return render_template('login.html', error=t['invalid_credentials'], t=t, lang=lang)
    
    return render_template('login.html', t=t, lang=lang)

@bp.route('/api/auth/login', methods=['POST'])
def api_login():
    """API endpoint for login (returns JWT tokens)"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    tenant_id = request.headers.get('X-Tenant-ID')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Missing credentials'}), 400
    
    # Find user
    query = User.query.filter_by(username=username, is_active=True)
    if tenant_id:
        query = query.filter_by(tenant_id=tenant_id)
    user = query.first()
    
    if user and user.check_password(password):
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Update last login
        user.last_login = db.func.now()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'tenant_id': user.tenant_id
            }
        }), 200
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@bp.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': access_token}), 200

@bp.route('/logout')
def logout():
    """Logout handler"""
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def api_logout():
    """API logout (client should discard tokens)"""
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration (for gym members)"""
    lang = request.args.get('lang', session.get('language', 'en'))
    t = get_translations(lang)
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        tenant_id = request.headers.get('X-Tenant-ID') or session.get('tenant_id')
        
        # Validate
        if not all([username, password, tenant_id]):
            flash('Missing required fields', 'error')
            return render_template('register.html', t=t, lang=lang)
        
        # Check if user exists
        existing_user = User.query.filter_by(
            tenant_id=tenant_id,
            username=username
        ).first()
        
        if existing_user:
            flash('Username already exists', 'error')
            return render_template('register.html', t=t, lang=lang)
        
        # Create user
        user = User(
            tenant_id=tenant_id,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='member',
            language_preference=lang
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', t=t, lang=lang)
