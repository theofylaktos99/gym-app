# Migration Guide: From Monolithic to SaaS

This guide explains how the original `gym_app.py` has been transformed into a modern SaaS application.

## 🔄 What Changed?

### Architecture
| Aspect | Original | New SaaS |
|--------|----------|----------|
| **Structure** | Single file (2261 lines) | Modular (22+ files) |
| **Data Storage** | In-memory (lists/dicts) | Database (SQLAlchemy) |
| **Tenancy** | Single gym | Multi-tenant |
| **Authentication** | Simple session | JWT + Sessions |
| **Authorization** | None | Role-based (admin/staff/member) |
| **API** | Inline routes | Separate API blueprint |
| **Deployment** | Manual | Docker + Docker Compose |
| **Configuration** | Hard-coded | Environment variables |
| **Testing** | None | Test framework ready |

### File Mapping

**Original** → **New Location**
- `gym_app.py` (all code) → Split into:
  - `app/__init__.py` - App factory
  - `app/models/__init__.py` - Database models
  - `app/routes/auth.py` - Authentication
  - `app/routes/member.py` - Member dashboard
  - `app/routes/api.py` - API endpoints
  - `app/utils/translations.py` - Translations
  - `app/services/seed_data.py` - Demo data
  - `config/config.py` - Configuration

- `login_html` variable → `app/templates/login.html` + `app/static/css/login.css`
- `dashboard_html` variable → `app/templates/dashboard.html`

## 🗄️ Data Migration

### Original Data Structures

```python
# OLD: In-memory lists/dicts
gym_areas = [...]  # List of dictionaries
room_bookings = []  # List of bookings
member_stats = {...}  # Dictionary
```

### New Database Models

```python
# NEW: SQLAlchemy models
class GymArea(db.Model):
    # Persistent database records with relationships

class Booking(db.Model):
    # Foreign keys to User and GymArea
    
class User(db.Model):
    # Includes member stats as fields
```

### Migration Script (if needed)

If you have custom data from the original app:

```python
# migrate_data.py
from app import create_app, db
from app.models import Tenant, User, GymArea

app = create_app()

with app.app_context():
    # Create tenant
    tenant = Tenant(name="My Gym", subdomain="mygym")
    db.session.add(tenant)
    db.session.commit()
    
    # Migrate gym areas
    for old_area in original_gym_areas:
        area = GymArea(
            tenant_id=tenant.id,
            name_en=old_area['name']['en'],
            name_el=old_area['name']['el'],
            # ... map other fields
        )
        db.session.add(area)
    
    db.session.commit()
```

## 🔐 Authentication Changes

### Original
```python
# Simple session check
if request.form['username'] == '123456' and request.form['password'] == '654321':
    session['logged_in'] = True
```

### New
```python
# Database user with hashed password
user = User.query.filter_by(username=username).first()
if user and user.check_password(password):
    # Creates JWT token or session
    session['user_id'] = user.id
    session['tenant_id'] = user.tenant_id
    session['role'] = user.role
```

### Password Migration
```python
from app.models import User

# For existing users, set hashed passwords
user = User.query.filter_by(username='123456').first()
user.set_password('654321')  # Hashes internally with bcrypt
db.session.commit()
```

## 🌐 API Changes

### Original Endpoints
```python
@app.route('/api/gym-status')
def gym_status():
    return jsonify({'areas': gym_areas})
```

### New RESTful API
```python
@bp.route('/api/gym-status')
def gym_status():
    tenant_id = request.headers.get('X-Tenant-ID')
    areas = GymArea.query.filter_by(tenant_id=tenant_id).all()
    # Returns tenant-specific data
```

**New Header Required**: `X-Tenant-ID` for tenant isolation

## 📦 Deployment Changes

### Original
```bash
python gym_app.py
```

### New Options

**Development**:
```bash
python run.py
```

**Production with Gunicorn**:
```bash
gunicorn --bind 0.0.0.0:5055 run:app
```

**Docker**:
```bash
docker-compose up
```

## ⚙️ Configuration Migration

### Original
```python
app.secret_key = 'underdogs_pro_gym_2025'  # Hard-coded
```

### New
```bash
# .env file
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=postgresql://user:pass@localhost/gym
```

## 🎨 Template Changes

### Original
- HTML embedded in Python strings
- Template rendered with `render_template_string()`

### New
- Separate template files
- Static CSS files
- Better maintainability
```python
# OLD
return render_template_string(login_html, t=t, lang=lang)

# NEW
return render_template('login.html', t=t, lang=lang)
```

## 🔧 Environment Setup

### Original Requirements
```
Flask
pyngrok
```

### New Requirements
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-JWT-Extended==4.6.0
Flask-Bcrypt==1.0.1
Flask-CORS==4.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9  # For PostgreSQL
```

## 📊 Feature Comparison

| Feature | Original | SaaS Version |
|---------|----------|--------------|
| User login | ✅ | ✅ |
| Dashboard | ✅ | ✅ |
| Gym areas | ✅ | ✅ |
| Workouts | ✅ | ✅ |
| Bookings | ✅ | ✅ |
| Multi-language | ✅ | ✅ |
| Real-time updates | ✅ (simulated) | ✅ (database) |
| Multi-tenant | ❌ | ✅ |
| User roles | ❌ | ✅ |
| Database | ❌ | ✅ |
| API | Basic | Full REST |
| Admin panel | ❌ | 🚧 (planned) |
| Payments | ❌ | 🚧 (planned) |
| Analytics | ❌ | 🚧 (planned) |

## 🚀 Migration Steps

1. **Backup** original `gym_app.py` and any custom data
2. **Install** new dependencies: `pip install -r requirements.txt`
3. **Configure** environment: Copy `.env.example` to `.env`
4. **Initialize** database: `flask db upgrade`
5. **Seed** demo data: `python run.py seed_demo_data`
6. **Customize** tenant data in `app/services/seed_data.py`
7. **Test** login with demo credentials
8. **Migrate** custom data if needed (use script above)

## 💡 Benefits of New Architecture

1. **Scalability**: Support unlimited gyms (tenants)
2. **Security**: Password hashing, JWT, role-based access
3. **Maintainability**: Modular code, easy to extend
4. **Professional**: Production-ready with Docker
5. **Flexible**: Switch databases (SQLite → PostgreSQL)
6. **API-First**: Mobile apps can use same backend
7. **Multi-Tenant**: Sell to multiple gym owners
8. **Extensible**: Easy to add features (payments, analytics)

## ⚠️ Breaking Changes

1. **Login**: Must create users in database (not hard-coded)
2. **Bookings**: Persist in database (not session)
3. **Tenant ID**: Required for all multi-tenant operations
4. **Environment**: Need .env file for configuration
5. **Database**: Requires database setup (SQLite or PostgreSQL)

## 🔄 Gradual Migration

You can run both versions simultaneously:

```bash
# Run original version
python gym_app.py  # Port 5055

# Run new version
PORT=5056 python run.py  # Port 5056
```

Then gradually migrate features and users to the new system.

## 📝 Notes

- Original `gym_app.py` is preserved for reference
- Demo data seed creates equivalent data to original
- Credentials remain the same for testing (123456/654321)
- UI design maintained with improvements
- All original features present in new version

## 🆘 Need Help?

- Check [README_SAAS.md](README_SAAS.md) for full documentation
- See [QUICKSTART.md](QUICKSTART.md) for quick setup
- Review seed data in `app/services/seed_data.py`

---

**Recommendation**: Start with SaaS version for new projects. Original version good for learning/demos.
