# System Architecture - Gym SaaS Application

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Gym SaaS Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │  Tenant 1   │  │  Tenant 2   │  │  Tenant N   │              │
│  │  (Gym A)    │  │  (Gym B)    │  │  (Gym N)    │              │
│  └────────────┘  └────────────┘  └────────────┘               │
│         │                │                │                      │
│         └────────────────┴────────────────┘                      │
│                          │                                       │
│                ┌─────────▼─────────┐                            │
│                │  Multi-Tenant     │                            │
│                │  Application      │                            │
│                └─────────┬─────────┘                            │
│                          │                                       │
│         ┌────────────────┼────────────────┐                    │
│         │                │                │                    │
│    ┌────▼────┐    ┌──────▼─────┐   ┌────▼────┐              │
│    │   Web   │    │    API     │   │  Admin  │              │
│    │Interface│    │ (REST/JWT) │   │  Panel  │              │
│    └─────────┘    └────────────┘   └─────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                          │
                ┌─────────▼─────────┐
                │    Database       │
                │  (Multi-Tenant)   │
                │  PostgreSQL/SQLite│
                └───────────────────┘
```

## 🏗️ Application Structure

```
gym-app/
├── 📱 app/                          # Main application package
│   ├── __init__.py                  # App factory, extensions init
│   │
│   ├── 🗄️ models/                   # Data models (SQLAlchemy)
│   │   └── __init__.py              # Tenant, User, GymArea, etc.
│   │
│   ├── 🛣️ routes/                   # Blueprint routes
│   │   ├── __init__.py
│   │   ├── auth.py                  # Login, logout, JWT
│   │   ├── member.py                # Member dashboard
│   │   ├── admin.py                 # Gym owner admin panel
│   │   ├── gym.py                   # Gym area management
│   │   ├── booking.py               # Booking management
│   │   └── api.py                   # RESTful API endpoints
│   │
│   ├── 🔧 services/                 # Business logic
│   │   ├── __init__.py
│   │   └── seed_data.py             # Demo data seeding
│   │
│   ├── 🛠️ utils/                    # Utilities
│   │   ├── __init__.py
│   │   ├── translations.py          # i18n translations
│   │   └── decorators.py            # Auth decorators
│   │
│   ├── 🎨 templates/                # HTML templates (Jinja2)
│   │   ├── login.html
│   │   └── dashboard.html
│   │
│   └── 📦 static/                   # Static assets
│       ├── css/
│       │   └── login.css
│       ├── js/
│       └── images/
│
├── ⚙️ config/                       # Configuration
│   ├── __init__.py
│   └── config.py                    # Dev, Prod, Test configs
│
├── 🔄 migrations/                   # Database migrations
│   └── versions/
│
├── 🧪 tests/                        # Test suite
│
├── 🐳 Docker files
│   ├── Dockerfile                   # Container definition
│   └── docker-compose.yml           # Multi-container setup
│
├── 📄 Configuration files
│   ├── .env.example                 # Environment template
│   ├── .gitignore                   # Git ignore rules
│   ├── requirements.txt             # Python dependencies
│   └── setup.sh                     # Quick setup script
│
├── 🚀 Entry points
│   ├── run.py                       # Application runner
│   └── gym_app.py                   # Original monolithic (legacy)
│
└── 📚 Documentation
    ├── README.md                    # Main readme
    ├── README_SAAS.md               # SaaS documentation
    ├── QUICKSTART.md                # Quick start guide
    ├── MIGRATION_GUIDE.md           # Migration guide
    └── ARCHITECTURE.md              # This file
```

## 🔄 Request Flow

### Web Interface Flow
```
User Browser
     │
     ▼
┌─────────────┐
│ Login Page  │ (/auth/login)
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  Session    │ (Flask session + DB validation)
│  Created    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  Dashboard  │ (/member/dashboard)
│  (Tenant    │ ← Queries tenant-specific data
│   Scoped)   │
└─────────────┘
```

### API Flow
```
Mobile/Web Client
     │
     ▼
┌─────────────┐
│ POST /api/  │ {username, password}
│ auth/login  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  JWT Token  │ {access_token, refresh_token}
│  Generated  │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ API Request │ Headers: {Authorization: Bearer <token>}
│ with Token  │          {X-Tenant-ID: <tenant-id>}
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   Tenant    │ Data filtered by tenant_id
│   Scoped    │
│   Response  │
└─────────────┘
```

## 🗄️ Database Schema

```
┌──────────────────┐
│    Tenants       │
├──────────────────┤
│ id (PK)          │◄───────┐
│ name             │        │
│ subdomain        │        │
│ subscription_*   │        │
│ settings         │        │
└──────────────────┘        │
                            │
                            │ tenant_id (FK)
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│     Users      │  │   GymAreas     │  │WorkoutPrograms │
├────────────────┤  ├────────────────┤  ├────────────────┤
│ id (PK)        │  │ id (PK)        │  │ id (PK)        │
│ tenant_id (FK) │  │ tenant_id (FK) │  │ tenant_id (FK) │
│ username       │  │ name_en        │  │ name_en        │
│ password_hash  │  │ name_el        │  │ name_el        │
│ role           │  │ capacity       │  │ difficulty     │
│ email          │  │ current_users  │  │ exercises      │
│ member_id      │  │ is_bookable    │  │ ...            │
│ stats          │  │ ...            │  └────────────────┘
│ ...            │  └────────┬───────┘
└────────┬───────┘           │
         │                   │
         │                   │
         │           ┌───────▼────────┐
         │           │   Bookings     │
         │           ├────────────────┤
         └──────────►│ id (PK)        │
                     │ user_id (FK)   │
                     │ gym_area_id(FK)│
                     │ booking_date   │
                     │ start_time     │
                     │ duration       │
                     │ price          │
                     │ status         │
                     └────────────────┘

         ┌────────────────┐
         │WorkoutSessions │
         ├────────────────┤
         │ id (PK)        │
         │ user_id (FK)   │
         │ program_id(FK) │
         │ start_time     │
         │ end_time       │
         │ calories       │
         │ status         │
         └────────────────┘
```

## 🔐 Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                  │
├─────────────────────────────────────────┤
│                                          │
│  1. Input Validation                     │
│     ├── Form validation                  │
│     ├── SQL injection protection (ORM)   │
│     └── XSS protection (Jinja2)          │
│                                          │
│  2. Authentication                       │
│     ├── Password hashing (bcrypt)        │
│     ├── JWT tokens (API)                 │
│     └── Session-based (Web)              │
│                                          │
│  3. Authorization                        │
│     ├── Role-based access control        │
│     ├── Tenant isolation                 │
│     └── Resource ownership checks        │
│                                          │
│  4. Transport Security                   │
│     ├── HTTPS (production)               │
│     ├── Secure cookies                   │
│     └── CORS configuration               │
│                                          │
│  5. Environment Security                 │
│     ├── Secret keys in .env              │
│     ├── No hard-coded credentials        │
│     └── Separate dev/prod configs        │
│                                          │
└─────────────────────────────────────────┘
```

## 🌐 Multi-Tenancy Model

### Tenant Isolation
```
Request arrives
     │
     ▼
Extract Tenant ID
  (Header or Session)
     │
     ▼
┌────────────────┐
│ Query Filter:  │
│ WHERE          │
│ tenant_id = ?  │
└────────────────┘
     │
     ▼
Return only
tenant's data
```

### Tenant Identification
1. **Web Interface**: Session-based (`session['tenant_id']`)
2. **API**: Header-based (`X-Tenant-ID`)
3. **Subdomain**: Future support (`gym1.yourgym.com`)

## 📡 API Architecture

### RESTful Endpoints
```
Authentication
├── POST   /api/auth/login       # Login, get JWT
├── POST   /api/auth/refresh     # Refresh token
└── POST   /api/auth/logout      # Logout

Gym Management
├── GET    /api/gym-status        # Real-time status
└── GET    /api/available-slots/:id  # Time slots

Workouts
├── POST   /api/start-workout    # Start session
└── POST   /api/complete-workout # Complete session

Bookings
├── POST   /api/book-room        # Create booking
├── GET    /api/user-bookings    # List bookings
└── POST   /api/cancel-booking   # Cancel booking
```

### Response Format
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... },
  "timestamp": "2025-01-01T00:00:00Z"
}
```

## 🚀 Deployment Architecture

### Development
```
┌──────────────┐
│  Developer   │
│   Machine    │
├──────────────┤
│  SQLite DB   │
│  Flask Dev   │
│  Server      │
└──────────────┘
```

### Production (Docker)
```
┌─────────────────────────────────────┐
│         Docker Host                  │
├─────────────────────────────────────┤
│                                      │
│  ┌──────────────┐  ┌─────────────┐ │
│  │   Nginx      │  │  PostgreSQL  │ │
│  │   (Reverse   │  │  (Database)  │ │
│  │    Proxy)    │  └─────────────┘ │
│  └──────┬───────┘                   │
│         │                            │
│  ┌──────▼───────┐                   │
│  │  Gunicorn    │                   │
│  │  (4 workers) │                   │
│  │              │                   │
│  │  Flask App   │                   │
│  └──────────────┘                   │
│                                      │
└─────────────────────────────────────┘
```

## 📊 Data Flow Example: Booking a Room

```
1. User clicks "Book Room" in dashboard
   │
   ▼
2. Frontend sends POST /api/book-room
   {
     "room_id": "uuid",
     "time": "14:00",
     "duration": 60,
     "trainer": "Alex",
     "price": 25
   }
   │
   ▼
3. Backend validates:
   - User authenticated? (session/JWT)
   - Tenant ID present?
   - Room exists in tenant?
   - Time slot available?
   │
   ▼
4. Create Booking record:
   booking = Booking(
     user_id=user.id,
     gym_area_id=room_id,
     ...
   )
   │
   ▼
5. Check conflicts:
   existing = Booking.query.filter_by(
     gym_area_id=room_id,
     date=today,
     time=time,
     status='confirmed'
   ).first()
   │
   ▼
6. If no conflict:
   db.session.add(booking)
   db.session.commit()
   │
   ▼
7. Return success response:
   {
     "success": true,
     "booking": {...}
   }
```

## 🔄 Technology Stack

```
Frontend
├── HTML5
├── CSS3 (Mobile-responsive)
└── JavaScript (Vanilla)

Backend
├── Python 3.11+
├── Flask 3.0
├── SQLAlchemy (ORM)
├── Flask-Migrate (Migrations)
├── Flask-JWT-Extended (Auth)
└── Flask-Bcrypt (Passwords)

Database
├── PostgreSQL (Production)
└── SQLite (Development)

Deployment
├── Docker
├── Docker Compose
├── Gunicorn
└── Nginx (reverse proxy)

Development Tools
├── Flask CLI
├── Python dotenv
└── Git
```

## 📈 Scalability Considerations

### Horizontal Scaling
- Stateless application (JWT tokens)
- Database connection pooling
- Load balancer ready (multiple Gunicorn workers)

### Vertical Scaling
- Database indexing on tenant_id
- Query optimization
- Caching layer (future: Redis)

### Multi-Region
- Database replication (future)
- CDN for static assets (future)
- Geographic tenant routing (future)

---

For implementation details, see [README_SAAS.md](README_SAAS.md)
