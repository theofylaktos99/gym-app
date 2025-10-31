# Gym App - Modern SaaS Platform

🎉 **Transformed into a Production-Ready SaaS Application!** This project is now a modern multi-tenant gym management platform with advanced features and professional UI/UX.

## Quick Links

- **🚀 Deploy to Render**: [RENDER_DEPLOY.md](RENDER_DEPLOY.md) - Get a live link in 5 minutes!
- **📖 SaaS Documentation**: [README_SAAS.md](README_SAAS.md) - Complete platform documentation
- **⚡ Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Get running locally in 5 minutes
- **🏗️ Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - System design and structure
- **📋 Migration Guide**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Migration from legacy version
- **📊 Transformation Summary**: [SUMMARY.md](SUMMARY.md) - Complete overview of changes

## 🌟 What's New

This main branch now contains the **modern SaaS architecture** with:

- **Multi-tenant Architecture**: Support for unlimited gym owners
- **MVC Design Pattern**: Clean separation of concerns
- **Database-Backed**: PostgreSQL/SQLite with SQLAlchemy ORM
- **Role-Based Access Control**: Admin, Staff, and Member roles
- **Premium UI/UX**: Modern, responsive design with animations
- **RESTful API**: Complete API for third-party integrations
- **Docker Support**: Containerized deployment
- **Bilingual Support**: Full English and Greek translations
- **Production-Ready**: Secure, scalable, and deployment-ready

## 🚀 Quick Start

### Using Docker (Recommended)
```sh
docker-compose up
```
Visit http://localhost:5055

### Local Development
```sh
# Install dependencies
pip install -r requirements.txt

# Initialize database
python run.py init_db
python run.py seed_demo_data

# Run the application
python run.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 📖 Legacy Version

The original monolithic version (`gym_app.py`) has been preserved in the `old-legacy` branch.

To access the legacy version:
```sh
git checkout old-legacy
```

The legacy version features:
- Single-file Flask app (gym_app.py)
- In-memory storage
- Simple demo application
- Ngrok integration

## License
MIT License

---
> **Note:** This project is for demo/educational purposes only. Not suitable for production use without further security and infrastructure improvements.
