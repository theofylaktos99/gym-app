# Gym App

🎉 **NEW: SaaS Version Available!** This project has been transformed into a modern multi-tenant SaaS application. See [README_SAAS.md](README_SAAS.md) for the new architecture.

## Quick Links

- **🚀 Deploy to Render**: [RENDER_DEPLOY.md](RENDER_DEPLOY.md) - Get a live link in 5 minutes!
- **📖 New SaaS Version**: [README_SAAS.md](README_SAAS.md) - Multi-tenant, database-backed, production-ready
- **⚡ Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Get running locally in 5 minutes
- **🏗️ Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - System design and structure
- **📖 Original Version**: See below for the original monolithic version

---

## Original Gym App (Legacy)

A modern, multilingual gym management web application built with Flask and Ngrok integration. This project is intended for demo/educational use only.

### Note on Versions

This repository contains two versions:

1. **New SaaS Version** (Recommended):
   - Multi-tenant architecture
   - Database-backed (PostgreSQL/SQLite)
   - Role-based access control
   - RESTful API
   - Docker support
   - **See [README_SAAS.md](README_SAAS.md)**

2. **Original Version** (This file):
   - Single-file Flask app (`gym_app.py`)
   - In-memory storage
   - Simple demo application

---

## Original Features
- User authentication (demo credentials)
- Multilingual UI (English & Greek)
- Dashboard with member stats, gym areas, and featured workouts
- Real-time gym area status
- Room booking system with trainers and time slots
- REST API endpoints for gym data and bookings
- Ngrok integration for remote access

## Quick Start
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Ngrok setup:**
   - Download from [ngrok.com](https://ngrok.com/download) and add to PATH
   - (Optional) Set your Ngrok auth token as environment variable
3. **Run the app:**
   - Windows Batch: `start_gym_ngrok.bat`
   - PowerShell: `./start_gym_ngrok.ps1`
   - Manual: `python gym_app.py`
4. **Access:**
   - Local: [http://localhost:5055](http://localhost:5055)
   - Public: Ngrok URL shown in terminal

## Demo Credentials
- **Member ID:** 123456
- **Password:** 654321

## File Structure
- `gym_app.py` — Main Flask app
- `requirements.txt` — Python dependencies
- `start_gym_ngrok.bat` / `start_gym_ngrok.ps1` — Startup scripts
- `README_NGROK.md` — Ngrok setup guide (GR/EN)
- `DOCUMENTATION.md` — Full documentation
- `CODE_REVIEW.md` / `DEV_REVIEW.md` — Reviews (GR/EN)

## License
MIT License

---
> **Note:** This project is for demo/educational purposes only. Not suitable for production use without further security and infrastructure improvements.
