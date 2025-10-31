# 🚀 Quick Start Guide - Gym SaaS Application

This guide will help you get the new SaaS version of the gym app running quickly.

## 🌐 Cloud Deployment (Easiest!)

### Deploy to Render.com (5 Minutes, Free!)

Get a live link without installing anything locally:

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Blueprint"**
3. Connect this GitHub repo: `theofylaktos99/gym-app`
4. Select branch: `copilot/recreate-saas-application`
5. Click **"Apply"** and wait ~5 minutes

**You'll get a live URL like**: `https://gym-saas-app.onrender.com`

📖 **Full Guide**: See [RENDER_DEPLOY.md](RENDER_DEPLOY.md)

---

## 💻 Local Setup

### Prerequisites
- Python 3.11+
- pip

### Option 1: SQLite (Fastest - No Database Setup Required)

```bash
# 1. Install dependencies
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Migrate==4.0.5 \
    Flask-JWT-Extended==4.6.0 Flask-Bcrypt==1.0.1 Flask-CORS==4.0.0 \
    python-dotenv==1.0.0 Werkzeug==3.0.1

# 2. Initialize the database
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 3. Seed demo data
python3 run.py seed_demo_data

# 4. Run the app
python3 run.py
```

### Option 2: Docker (Recommended for Production)

```bash
# 1. Build and start
docker-compose up -d

# 2. Seed demo data
docker-compose exec web python run.py seed_demo_data

# 3. Access at http://localhost:5055
```

## 🔑 Demo Login

After seeding data, use these credentials:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Member | `123456` | `654321` |
| Staff | `staff` | `staff123` |

## 🌐 Access Points

- **Web Interface**: http://localhost:5055
- **Member Dashboard**: http://localhost:5055/member/dashboard
- **API Docs**: http://localhost:5055/api/*

## 📱 Test the Features

1. **Login** as a member (123456/654321)
2. **View Dashboard** with stats and gym areas
3. **Browse Workouts** in both languages (EN/EL)
4. **Check API** at http://localhost:5055/api/gym-status

## 🛠️ Troubleshooting

### Database Issues
```bash
# Reset database
rm gym_dev.db
flask db upgrade
python3 run.py seed_demo_data
```

### Import Errors
```bash
# Make sure you're in the project root
cd /path/to/gym-app
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Port Already in Use
```bash
# Change port in .env
echo "PORT=5056" >> .env
```

## 📚 Next Steps

1. Read [README_SAAS.md](README_SAAS.md) for full documentation
2. Check [API Documentation](#api-endpoints) below
3. Customize for your gym in `app/services/seed_data.py`

## 🔌 API Endpoints

### Authentication
```bash
# Login
curl -X POST http://localhost:5055/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"123456","password":"654321"}'

# Response includes access_token and refresh_token
```

### Gym Status
```bash
# Get real-time gym area status
curl http://localhost:5055/api/gym-status \
  -H "X-Tenant-ID: <tenant-id>"
```

### Bookings
```bash
# Book a room
curl -X POST http://localhost:5055/api/book-room \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<session-cookie>" \
  -d '{
    "room_id": "<gym-area-id>",
    "time": "14:00",
    "duration": 60,
    "trainer": "Alex Strong",
    "price": 25
  }'
```

## 🎨 Customization

### Change Gym Name
Edit `app/utils/translations.py`:
```python
'gym_name': 'YourGym'  # Change to your gym name
```

### Add New Gym Areas
Edit `app/services/seed_data.py` and re-run:
```bash
python3 run.py seed_demo_data
```

### Configure Email/Payment
Coming soon in admin panel!

## ✅ Verify Installation

Run this test:
```bash
python3 -c "from app import create_app; app = create_app(); print('✅ App initialized successfully!')"
```

## 🆘 Getting Help

- Check [README_SAAS.md](README_SAAS.md) for detailed docs
- Review logs: Check console output for errors
- Database: Use `flask shell` to inspect data

---

**Ready to start? Run:** `python3 run.py` 🚀
