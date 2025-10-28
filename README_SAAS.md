# Gym SaaS Application

A modern, multi-tenant gym management SaaS application built with Flask. Designed for selling to gym owners with support for multiple gyms, members, staff, and comprehensive management features.

## 🌟 Features

### Multi-Tenancy
- **Multiple Gym Support**: Each gym owner gets their own tenant with isolated data
- **Subscription Management**: Support for trial, basic, premium, and enterprise plans
- **Custom Branding**: Each gym can customize their branding and settings

### User Management
- **Role-Based Access Control**: Admin, Staff, and Member roles
- **Secure Authentication**: JWT tokens for API, sessions for web interface
- **Password Security**: Bcrypt hashing for all passwords

### Gym Management
- **Gym Areas**: Manage different workout zones (strength training, cardio, yoga, etc.)
- **Real-Time Status**: Live capacity tracking and availability
- **Multilingual Support**: Full English and Greek translations

### Workout Programs
- **Predefined Programs**: Ready-to-use workout routines
- **Difficulty Levels**: Beginner, Intermediate, Advanced
- **Exercise Details**: Sets, reps, rest periods in both languages

### Booking System
- **Room Reservations**: Book gym areas and trainers
- **Time Slot Management**: 30-minute slots from 8 AM to 10 PM
- **Trainer Assignment**: Select specific trainers for sessions
- **Pricing**: Hourly rates per area

### Member Features
- **Progress Tracking**: Total workouts, calories burned, streak days
- **Workout Timer**: Built-in timer for workout sessions
- **Booking History**: View and manage reservations
- **Personal Stats**: Membership level, achievements

## 🏗️ Architecture

### Modular Structure
```
gym-app/
├── app/
│   ├── models/           # Database models
│   ├── routes/           # Blueprint routes (auth, member, admin, api, gym, booking)
│   ├── services/         # Business logic and seed data
│   ├── utils/            # Utilities (translations, decorators)
│   ├── templates/        # Jinja2 templates
│   └── static/           # CSS, JS, images
├── config/               # Configuration files
├── migrations/           # Database migrations
└── tests/                # Test suite
```

### Technology Stack
- **Backend**: Flask 3.0 with modular blueprints
- **Database**: PostgreSQL (production), SQLite (development)
- **ORM**: SQLAlchemy with Flask-Migrate
- **Authentication**: Flask-JWT-Extended + Flask-Bcrypt
- **API**: RESTful API with CORS support
- **Frontend**: Responsive HTML/CSS/JS (mobile-friendly)
- **Containerization**: Docker + Docker Compose

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (for production)
- Docker & Docker Compose (optional)

### Installation

#### Option 1: Local Development
```bash
# Clone repository
git clone https://github.com/theofylaktos99/gym-app.git
cd gym-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed demo data
python run.py seed_demo_data

# Run application
python run.py
```

#### Option 2: Docker
```bash
# Build and start containers
docker-compose up -d

# Access container
docker-compose exec web bash

# Seed demo data
python run.py seed_demo_data
```

### Access
- **Local**: http://localhost:5055
- **API**: http://localhost:5055/api/*

### Demo Credentials
- **Admin**: username: `admin`, password: `admin123`
- **Member**: username: `123456`, password: `654321`
- **Staff**: username: `staff`, password: `staff123`

## 📚 API Documentation

### Authentication
- `POST /api/auth/login` - Login with username/password
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout (discard tokens)

### Gym Data
- `GET /api/gym-status` - Get real-time gym area status
- `GET /api/available-slots/<room_id>` - Get available booking slots

### Workouts
- `POST /api/start-workout` - Start a workout session
- `POST /api/complete-workout` - Complete and log workout

### Bookings
- `POST /api/book-room` - Create a booking
- `POST /api/cancel-booking` - Cancel a booking
- `GET /api/user-bookings` - Get user's bookings

## 🔐 Security Features

- Password hashing with bcrypt
- JWT-based API authentication
- Session-based web authentication
- Role-based access control
- Tenant data isolation
- SQL injection protection (SQLAlchemy ORM)
- XSS protection (Jinja2 auto-escaping)
- Environment variable configuration

## 🌍 Internationalization

Full bilingual support:
- **English** (en)
- **Greek** (el - Ελληνικά)

All UI elements, workout programs, and gym areas are available in both languages.

## 📦 Database Models

### Core Models
- **Tenant**: Gym owner/organization
- **User**: Admin, staff, and members
- **GymArea**: Workout zones and facilities
- **WorkoutProgram**: Exercise routines
- **Booking**: Room/trainer reservations
- **WorkoutSession**: Member workout tracking

## 🔧 Configuration

### Environment Variables
```env
FLASK_ENV=development|production|testing
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://user:password@host/database
DEV_DATABASE_URL=sqlite:///gym_dev.db
PORT=5055
```

### Subscription Plans
- **Trial**: 30 days free
- **Basic**: Essential features
- **Premium**: All features + priority support
- **Enterprise**: Custom solutions

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## 📈 Deployment

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use PostgreSQL database
3. Set strong SECRET_KEY and JWT_SECRET_KEY
4. Enable HTTPS/SSL
5. Use Gunicorn or uWSGI
6. Set up reverse proxy (Nginx)
7. Configure monitoring and logging

### Docker Deployment
```bash
# Build for production
docker-compose -f docker-compose.prod.yml up -d
```

## 🔄 Migration from Original App

The monolithic `gym_app.py` has been refactored into a modern SaaS architecture:

**Old Structure** → **New Structure**
- Single file → Modular blueprints
- In-memory storage → Database-backed
- Single gym → Multi-tenant
- Hard-coded data → Dynamic database
- No authentication → JWT + Sessions
- No roles → Role-based access
- Manual deployment → Docker-ready

The original `gym_app.py` is preserved for reference.

## 📝 TODO / Roadmap

- [ ] Complete admin dashboard for gym owners
- [ ] Payment integration (Stripe/PayPal)
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Advanced analytics and reporting
- [ ] Mobile app (React Native)
- [ ] Social features (member profiles, achievements)
- [ ] Class scheduling system
- [ ] Membership package management
- [ ] POS integration for payments
- [ ] Attendance tracking with QR codes
- [ ] Equipment maintenance tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 💡 Support

For support, email support@yourgym.com or create an issue on GitHub.

## 🙏 Acknowledgments

Built with modern web technologies and best practices for SaaS applications.

---

**Note**: This is a comprehensive gym management SaaS platform designed for selling to gym owners. It supports multiple gyms, multi-language, and provides a complete solution for gym operations.
