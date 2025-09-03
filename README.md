# Gym App

A modern, multilingual gym management web application built with Flask and Ngrok integration. This project is intended for demo/educational use only.

## Features
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
