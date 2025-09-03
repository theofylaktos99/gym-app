# Gym App Documentation

> **Σημείωση:** Αυτό το project προορίζεται μόνο για demo/εκπαιδευτική χρήση. Δεν είναι κατάλληλο για παραγωγική λειτουργία χωρίς περαιτέρω ενίσχυση της ασφάλειας και της υποδομής.

## Overview

This project is a modern, multilingual gym management web application built with Flask and integrated with Ngrok for easy remote access. It features a beautiful dashboard, real-time gym area status, workout programs, and a booking system for gym rooms and trainers. The app supports both English and Greek languages.

---

## Features

- **User Authentication**: Simple login system for gym members.
- **Multilingual UI**: English and Greek translations for all UI elements.
- **Dashboard**: Displays member stats, gym areas, featured workouts, and user bookings.
- **Real-Time Gym Area Status**: Each area shows live status (Available, Busy, Full, Maintenance, Class in Session) and current usage.
- **Workout Programs**: Predefined, multilingual workout routines with details and timer modal.
- **Room Booking System**: Bookable gym areas with time slots, trainer selection, and price calculation. Users can view and cancel their bookings.
- **REST API**: Endpoints for gym status, workouts, bookings, and available slots.
- **Ngrok Integration**: Easily expose the app to the internet for remote access.

---

## File Structure

- `gym_app.py` - Main Flask application with all logic, routes, templates, and API endpoints.
- `requirements.txt` - Python dependencies (Flask, pyngrok, etc.).
- `start_gym_ngrok.bat` - Batch script to start the app with Ngrok on Windows.
- `start_gym_ngrok.ps1` - PowerShell script for the same purpose.
- `README_NGROK.md` - Greek/English guide for Ngrok setup and usage.

---

## How It Works

### 1. User Login
- Users log in with a Member ID and password (default: 123456/654321).
- Language preference is stored in the session.

### 2. Dashboard
- Shows member stats (workouts, calories, streak, membership).
- Lists all gym areas with live status, capacity, and equipment.
- Featured workouts section with routines and timer modal.
- User bookings section for managing room reservations.

### 3. Booking System
- Bookable areas allow users to select a time slot, trainer, and duration.
- Price is calculated based on duration and area.
- Bookings are stored in memory (session and global list).
- Users can cancel bookings via the dashboard.

### 4. API Endpoints
- `/api/gym-status`: Real-time gym area data.
- `/api/start-workout`, `/api/complete-workout`: Log workout sessions.
- `/api/book-room`, `/api/cancel-booking`: Manage room bookings.
- `/api/user-bookings`: Get current user's bookings.
- `/api/available-slots/<room_id>`: Get available time slots for a room.

### 5. Ngrok Integration
- Ngrok is used to expose the local Flask app to the internet.
- Scripts (`.bat`/`.ps1`) automate dependency installation and app launch.
- Public URL is printed in the terminal for sharing.

---

## Technologies Used
- **Python 3**
- **Flask** (web framework)
- **Jinja2** (templating)
- **pyngrok** (Ngrok integration)
- **HTML/CSS/JS** (modern, responsive UI)

---

## Setup & Usage

### 1. Install Dependencies
```sh
pip install -r requirements.txt
```

### 2. Ngrok Setup
- Download Ngrok from [ngrok.com](https://ngrok.com/download) and add to PATH.
- (Optional) Set your Ngrok auth token as an environment variable:
  - Windows: `$env:NGROK_AUTH_TOKEN = "your_token_here"`

### 3. Start the App
- **Windows Batch**: `start_gym_ngrok.bat`
- **PowerShell**: `./start_gym_ngrok.ps1`
- **Manual**: `python gym_app.py`

### 4. Access
- Local: [http://localhost:5055](http://localhost:5055)
- Public (Ngrok): URL shown in terminal after launch

---

## Default Credentials
- **Member ID**: 123456
- **Password**: 654321

---

## Customization
- **Languages**: Add/modify translations in the `translations` dictionary in `gym_app.py`.
- **Gym Areas**: Edit the `gym_areas` list for new areas, trainers, or equipment.
- **Workouts**: Add routines to the `workout_programs` list.
- **Booking Logic**: Extend the booking system for persistent storage (e.g., database).

---

## Security Notes
- This app is for demo/educational use. For production:
  - Use a secure authentication system.
  - Store data in a database, not in memory/session.
  - Use HTTPS and secure session management.

---

## Authors & License
- Created by theofylaktos99 (2025)
- Documentation by GitHub Copilot
- MIT License
