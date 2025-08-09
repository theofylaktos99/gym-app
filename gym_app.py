from flask import Flask, request, redirect, session, url_for, render_template_string, jsonify
from datetime import datetime, timedelta
from pyngrok import ngrok
import json
import random
import threading
import time
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'underdogs_pro_gym_2025'

# Language translations
translations = {
    'en': {
        'gym_name': 'YourGym',
        'subtitle': 'Premium Fitness Experience',
        'member_id': '👤 Member ID',
        'password': '🔒 Password',
        'enter_gym': 'Enter Gym',
        'invalid_credentials': 'Invalid credentials! Please try again.',
        'welcome_title': 'Welcome to Your Fitness Journey',
        'welcome_subtitle': 'Push your limits, achieve your goals, become legendary.',
        'total_workouts': 'Total Workouts',
        'calories_burned': 'Calories Burned',
        'day_streak': 'Day Streak',
        'membership': 'Membership',
        'gym_areas': 'Gym Areas',
        'featured_workouts': 'Featured Workouts',
        'members': 'members',
        'start_workout': 'Start Workout',
        'workout_timer': 'Workout Timer',
        'logout': 'Logout',
        'language': 'Language',
        'available': 'Available',
        'busy': 'Busy',
        'full': 'Full',
        'maintenance': 'Maintenance',
        'class_in_session': 'Class in Session',
        'beginner': 'Beginner',
        'intermediate': 'Intermediate',
        'advanced': 'Advanced',
        'sets': 'sets',
        'reps': 'reps',
        'rest': 'Rest',
        'exercises': 'exercises',
        'cal': 'cal',
        'start': 'Start',
        'pause': 'Pause',
        'reset': 'Reset',
        'book_room': 'Book Room',
        'room_booking': 'Room Booking',
        'available_slots': 'Available Time Slots',
        'select_time': 'Select Time',
        'book_now': 'Book Now',
        'booking_success': 'Booking successful!',
        'booking_failed': 'Booking failed. Please try again.',
        'your_bookings': 'Your Bookings',
        'cancel_booking': 'Cancel',
        'room_schedule': 'Room Schedule',
        'time_slot': 'Time Slot',
        'duration': 'Duration',
        'trainer': 'Trainer',
        'price': 'Price',
        'minutes': 'min',
        'booked': 'Booked',
        'cancel': 'Cancel'
    },
    'el': {
        'gym_name': 'YourGym',
        'subtitle': 'Εμπειρία Premium Γυμναστικής',
        'member_id': '👤 Κωδικός Μέλους',
        'password': '🔒 Κωδικός Πρόσβασης',
        'enter_gym': 'Είσοδος στο Γυμναστήριο',
        'invalid_credentials': 'Λάθος στοιχεία! Παρακαλώ δοκιμάστε ξανά.',
        'welcome_title': 'Καλώς ήρθατε στο Ταξίδι της Γυμναστικής σας',
        'welcome_subtitle': 'Ξεπεράστε τα όριά σας, πετύχετε τους στόχους σας, γίνετε θρύλοι.',
        'total_workouts': 'Συνολικές Προπονήσεις',
        'calories_burned': 'Θερμίδες που Κάηκαν',
        'day_streak': 'Συνεχόμενες Ημέρες',
        'membership': 'Συνδρομή',
        'gym_areas': 'Χώροι Γυμναστηρίου',
        'featured_workouts': 'Προτεινόμενες Προπονήσεις',
        'members': 'μέλη',
        'start_workout': 'Έναρξη Προπόνησης',
        'workout_timer': 'Χρονόμετρο Προπόνησης',
        'logout': 'Αποσύνδεση',
        'language': 'Γλώσσα',
        'available': 'Διαθέσιμο',
        'busy': 'Πολυσύχναστο',
        'full': 'Γεμάτο',
        'maintenance': 'Συντήρηση',
        'class_in_session': 'Μάθημα σε Εξέλιξη',
        'beginner': 'Αρχάριος',
        'intermediate': 'Μεσαίος',
        'advanced': 'Προχωρημένος',
        'sets': 'σετ',
        'reps': 'επαναλήψεις',
        'rest': 'Ανάπαυση',
        'exercises': 'ασκήσεις',
        'cal': 'θερμ',
        'start': 'Έναρξη',
        'pause': 'Παύση',
        'reset': 'Επαναφορά',
        'book_room': 'Κράτηση Αίθουσας',
        'room_booking': 'Κράτηση Αίθουσας',
        'available_slots': 'Διαθέσιμες Ώρες',
        'select_time': 'Επιλογή Ώρας',
        'book_now': 'Κράτηση Τώρα',
        'booking_success': 'Η κράτηση ολοκληρώθηκε επιτυχώς!',
        'booking_failed': 'Η κράτηση απέτυχε. Παρακαλώ δοκιμάστε ξανά.',
        'your_bookings': 'Οι Κρατήσεις σας',
        'cancel_booking': 'Ακύρωση',
        'room_schedule': 'Πρόγραμμα Αίθουσας',
        'time_slot': 'Ωριαίο Διάστημα',
        'duration': 'Διάρκεια',
        'trainer': 'Γυμναστής',
        'price': 'Τιμή',
        'minutes': 'λεπτά',
        'booked': 'Κρατημένο',
        'cancel': 'Ακύρωση'
    }
}

# Enhanced gym data structure with multilingual support
gym_areas = [
    {
        "id": 1,
        "name": {"en": "Strength Training Zone", "el": "Ζώνη Προπόνησης Δύναμης"},
        "status": "Available",
        "capacity": 25,
        "current_users": 12,
        "equipment": {
            "en": ["Dumbbells", "Barbells", "Benches", "Squat Racks"],
            "el": ["Αλτήρες", "Μπάρες", "Πάγκοι", "Στάσεις Καθίσματος"]
        },
        "icon": "💪",
        "color": "#8B0000",
        "bookable": True,
        "trainers": {
            "en": ["Alex Strong", "Maria Power", "John Muscle"],
            "el": ["Αλέξης Δυναμικός", "Μαρία Δύναμη", "Γιάννης Μυς"]
        },
        "price_per_hour": 25
    },
    {
        "id": 2,
        "name": {"en": "Cardio Arena", "el": "Αρένα Καρδιοπροπόνησης"},
        "status": "Busy",
        "capacity": 30,
        "current_users": 28,
        "equipment": {
            "en": ["Treadmills", "Ellipticals", "Bikes", "Rowing Machines"],
            "el": ["Διάδρομοι Τρεξίματος", "Ελλειπτικά", "Ποδήλατα", "Κωπηλατικά"]
        },
        "icon": "🏃",
        "color": "#FF4500",
        "bookable": False
    },
    {
        "id": 3,
        "name": {"en": "Functional Training", "el": "Λειτουργική Προπόνηση"},
        "status": "Available",
        "capacity": 20,
        "current_users": 8,
        "equipment": {
            "en": ["Battle Ropes", "Kettlebells", "TRX", "Medicine Balls"],
            "el": ["Σχοινιά Μάχης", "Κουδούνια", "TRX", "Μπάλες Ιατρικής"]
        },
        "icon": "🔥",
        "color": "#FF8C00",
        "bookable": True,
        "trainers": {
            "en": ["Sofia Fit", "Mike Cross", "Anna Athletic"],
            "el": ["Σοφία Φιτ", "Μάικ Κρος", "Άννα Αθλητική"]
        },
        "price_per_hour": 30
    },
    {
        "id": 4,
        "name": {"en": "Yoga & Mindfulness", "el": "Γιόγκα & Διαλογισμός"},
        "status": "Class in Session",
        "capacity": 15,
        "current_users": 15,
        "equipment": {
            "en": ["Yoga Mats", "Blocks", "Straps", "Meditation Cushions"],
            "el": ["Στρώματα Γιόγκα", "Τούβλα", "Ιμάντες", "Μαξιλάρια Διαλογισμού"]
        },
        "icon": "🧘",
        "color": "#4B0082",
        "bookable": True,
        "trainers": {
            "en": ["Elena Zen", "David Peace", "Lisa Harmony"],
            "el": ["Έλενα Ζεν", "Δαυίδ Ειρήνη", "Λίζα Αρμονία"]
        },
        "price_per_hour": 20
    },
    {
        "id": 5,
        "name": {"en": "Boxing Arena", "el": "Αρένα Πυγμαχίας"},
        "status": "Available",
        "capacity": 12,
        "current_users": 3,
        "equipment": {
            "en": ["Heavy Bags", "Speed Bags", "Boxing Gloves", "Pads"],
            "el": ["Βαριά Σάκια", "Σάκια Ταχύτητας", "Γάντια Πυγμαχίας", "Πάντες"]
        },
        "icon": "🥊",
        "color": "#DC143C",
        "bookable": True,
        "trainers": {
            "en": ["Rocky Fighter", "Muhammad Strike", "Tyson Power"],
            "el": ["Ρόκι Μαχητής", "Μουχάμεντ Χτύπημα", "Τάισον Δύναμη"]
        },
        "price_per_hour": 35
    },
    {
        "id": 6,
        "name": {"en": "Swimming Pool", "el": "Πισίνα"},
        "status": "Maintenance",
        "capacity": 40,
        "current_users": 0,
        "equipment": {
            "en": ["Olympic Pool", "Lanes", "Diving Board", "Jacuzzi"],
            "el": ["Ολυμπιακή Πισίνα", "Διαδρομές", "Βατήρας", "Τζακούζι"]
        },
        "icon": "🏊",
        "color": "#191970",
        "bookable": False
    },
    {
        "id": 7,
        "name": {"en": "Pilates Studio", "el": "Στούντιο Πιλάτες"},
        "status": "Available",
        "capacity": 12,
        "current_users": 4,
        "equipment": {
            "en": ["Reformer Machines", "Pilates Mats", "Magic Circles", "Resistance Bands"],
            "el": ["Μηχανές Reformer", "Στρώματα Πιλάτες", "Μαγικοί Κύκλοι", "Λάστιχα Αντίστασης"]
        },
        "icon": "🤸‍♀️",
        "color": "#8B008B",
        "bookable": True,
        "trainers": {
            "en": ["Grace Balance", "Emma Core", "Sophia Stretch"],
            "el": ["Γκρέις Ισορροπία", "Έμμα Κορμός", "Σοφία Τέντωμα"]
        },
        "price_per_hour": 28
    },
    {
        "id": 8,
        "name": {"en": "Martial Arts Dojo", "el": "Ντότζο Πολεμικών Τεχνών"},
        "status": "Available",
        "capacity": 16,
        "current_users": 2,
        "equipment": {
            "en": ["Mats", "Makiwara Boards", "Wooden Dummies", "Weapons Rack"],
            "el": ["Στρώματα", "Πίνακες Makiwara", "Ξύλινα Ομοιώματα", "Στάση Όπλων"]
        },
        "icon": "🥋",
        "color": "#B22222",
        "bookable": True,
        "trainers": {
            "en": ["Sensei Tanaka", "Master Lee", "Sifu Chen"],
            "el": ["Σενσέι Τανάκα", "Μάστερ Λι", "Σίφου Τσεν"]
        },
        "price_per_hour": 40
    }
]

# Room booking system data
room_bookings = []  # In a real app, this would be in a database

# Generate time slots for booking
def generate_time_slots():
    """Generate available time slots for today"""
    slots = []
    current_hour = datetime.now().hour
    
    # Generate slots from current hour to 22:00
    for hour in range(max(current_hour + 1, 8), 22):  # Start from 8 AM or next hour
        for minute in [0, 30]:  # 30-minute slots
            time_str = f"{hour:02d}:{minute:02d}"
            slots.append({
                'time': time_str,
                'datetime': datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0),
                'available': True
            })
    
    return slots

# Workout programs with multilingual support
workout_programs = [
    {
        "id": 1,
        "name": {"en": "Beast Mode Strength", "el": "Προπόνηση Δύναμης Θηρίου"},
        "duration": "45 min",
        "difficulty": "Advanced",
        "calories": 400,
        "exercises": [
            {
                "name": {"en": "Deadlifts", "el": "Νεκρές Αναβάσεις"}, 
                "sets": 4, 
                "reps": "6-8", 
                "rest": {"en": "3 min", "el": "3 λεπτά"}
            },
            {
                "name": {"en": "Squats", "el": "Καθίσματα"}, 
                "sets": 4, 
                "reps": "8-10", 
                "rest": {"en": "2.5 min", "el": "2.5 λεπτά"}
            },
            {
                "name": {"en": "Bench Press", "el": "Πιέσεις Πάγκου"}, 
                "sets": 4, 
                "reps": "6-8", 
                "rest": {"en": "3 min", "el": "3 λεπτά"}
            },
            {
                "name": {"en": "Pull-ups", "el": "Αναρριχήσεις"}, 
                "sets": 3, 
                "reps": "8-12", 
                "rest": {"en": "2 min", "el": "2 λεπτά"}
            },
            {
                "name": {"en": "Overhead Press", "el": "Πιέσεις από Πάνω"}, 
                "sets": 3, 
                "reps": "8-10", 
                "rest": {"en": "2 min", "el": "2 λεπτά"}
            }
        ],
        "icon": "💪",
        "color": "#8B0000"
    },
    {
        "id": 2,
        "name": {"en": "Cardio Burn", "el": "Καύση Καρδιοπροπόνησης"},
        "duration": "30 min",
        "difficulty": "Intermediate",
        "calories": 350,
        "exercises": [
            {
                "name": {"en": "Treadmill Sprint", "el": "Σπριντ Διαδρόμου"}, 
                "sets": 8, 
                "reps": "30s on/30s off", 
                "rest": {"en": "1 min", "el": "1 λεπτό"}
            },
            {
                "name": {"en": "Burpees", "el": "Μπέρπις"}, 
                "sets": 3, 
                "reps": "15", 
                "rest": {"en": "1 min", "el": "1 λεπτό"}
            },
            {
                "name": {"en": "Mountain Climbers", "el": "Αναρριχητές Βουνού"}, 
                "sets": 3, 
                "reps": "30s", 
                "rest": {"en": "30s", "el": "30 δευτ"}
            },
            {
                "name": {"en": "Jump Rope", "el": "Σχοινάκι"}, 
                "sets": 5, 
                "reps": "1 min", 
                "rest": {"en": "30s", "el": "30 δευτ"}
            }
        ],
        "icon": "🔥",
        "color": "#FF4500"
    },
    {
        "id": 3,
        "name": {"en": "Functional Flow", "el": "Λειτουργική Ροή"},
        "duration": "40 min",
        "difficulty": "Beginner",
        "calories": 280,
        "exercises": [
            {
                "name": {"en": "Bodyweight Squats", "el": "Καθίσματα Σώματος"}, 
                "sets": 3, 
                "reps": "15", 
                "rest": {"en": "1 min", "el": "1 λεπτό"}
            },
            {
                "name": {"en": "Push-ups", "el": "Κάμψεις"}, 
                "sets": 3, 
                "reps": "10-15", 
                "rest": {"en": "1 min", "el": "1 λεπτό"}
            },
            {
                "name": {"en": "Lunges", "el": "Βηματισμοί"}, 
                "sets": 3, 
                "reps": {"en": "12 each leg", "el": "12 κάθε πόδι"}, 
                "rest": {"en": "1 min", "el": "1 λεπτό"}
            },
            {
                "name": {"en": "Plank", "el": "Σανίδα"}, 
                "sets": 3, 
                "reps": "30-60s", 
                "rest": {"en": "1 min", "el": "1 λεπτό"}
            },
            {
                "name": {"en": "Glute Bridges", "el": "Γέφυρες Γλουτών"}, 
                "sets": 3, 
                "reps": "15", 
                "rest": {"en": "1 min", "el": "1 λεπτό"}
            }
        ],
        "icon": "⚡",
        "color": "#FF8C00"
    }
]

# Member stats
member_stats = {
    "total_workouts": 147,
    "calories_burned": 18500,
    "streak_days": 12,
    "favorite_area": "Strength Training Zone",
    "membership_level": "Premium",
    "join_date": "2024-03-15"
}

login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.gym_name }} - {{ t.subtitle }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }
        .language-selector {
            position: absolute;
            top: 16px;
            right: 16px;
            z-index: 100;
            display: flex;
            gap: 8px;
        }
        .lang-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            text-decoration: none;
            font-size: 0.9rem;
        }
        .lang-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        .lang-btn.active {
            background: rgba(255, 69, 0, 0.8);
            border-color: #ff4500;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
        }
        .bg-animation {
            position: absolute;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><radialGradient id="g" cx="50%" cy="50%" r="50%"><stop offset="0%" style="stop-color:rgba(255,255,255,0.1)"/><stop offset="100%" style="stop-color:rgba(255,255,255,0)"/></radialGradient></defs><circle cx="25" cy="25" r="20" fill="url(%23g)"><animate attributeName="cy" values="25;75;25" dur="3s" repeatCount="indefinite"/></circle><circle cx="75" cy="75" r="15" fill="url(%23g)"><animate attributeName="cx" values="75;25;75" dur="4s" repeatCount="indefinite"/></circle></svg>');
            opacity: 0.3;
            animation: float 6s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        .login-container {
            position: relative;
            z-index: 10;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 16px;
        }
        .login-box {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 18px;
            padding: 32px 18px;
            width: 100%;
            max-width: 370px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.6s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .logo {
            font-size: 2.2rem;
            font-weight: bold;
            color: #fff;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        .subtitle {
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 24px;
            font-size: 1rem;
        }
        .input-group {
            position: relative;
            margin-bottom: 18px;
        }
        .input-group input {
            width: 100%;
            padding: 13px 16px;
            border: none;
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.22);
            color: #fff;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        .input-group input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        .input-group input:focus {
            background: rgba(255, 255, 255, 0.32);
            transform: scale(1.02);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        .login-btn {
            width: 100%;
            padding: 13px;
            border: none;
            border-radius: 50px;
            background: linear-gradient(45deg, #ff4500, #ff6b00, #8B0000);
            color: white;
            font-size: 1.05rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(255, 69, 0, 0.3);
        }
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        .login-btn:active {
            transform: translateY(0);
        }
        .login-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.6s;
        }
        .login-btn:hover::before {
            left: 100%;
        }
        .error {
            color: #ff4500;
            background: rgba(255, 69, 0, 0.1);
            padding: 10px;
            border-radius: 10px;
            margin-top: 15px;
            border: 1px solid rgba(255, 69, 0, 0.3);
            animation: shake 0.5s ease-in-out;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        .gym-icons {
            position: absolute;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
        }
        .gym-icon {
            position: absolute;
            font-size: 2rem;
            opacity: 0.1;
            animation: float-random 8s ease-in-out infinite;
        }
        .gym-icon:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
        .gym-icon:nth-child(2) { top: 60%; right: 15%; animation-delay: 2s; }
        .gym-icon:nth-child(3) { bottom: 30%; left: 20%; animation-delay: 4s; }
        .gym-icon:nth-child(4) { top: 40%; right: 25%; animation-delay: 6s; }
        @keyframes float-random {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            25% { transform: translateY(-15px) rotate(5deg); }
            50% { transform: translateY(-30px) rotate(-5deg); }
            75% { transform: translateY(-15px) rotate(3deg); }
        }
        @media (max-width: 600px) {
            .login-container {
                padding: 0;
                min-height: 100vh;
            }
            .login-box {
                padding: 18px 8px;
                max-width: 98vw;
                border-radius: 12px;
            }
            .logo {
                font-size: 1.5rem;
            }
            .subtitle {
                font-size: 0.95rem;
            }
            .input-group input {
                padding: 10px 12px;
                font-size: 0.95rem;
            }
            .login-btn {
                padding: 10px;
                font-size: 0.95rem;
            }
            .language-selector {
                top: 8px;
                right: 8px;
                gap: 4px;
            }
        }
    </style>
</head>
<body>
    <div class="language-selector">
        <a href="/?lang=en" class="lang-btn {{ 'active' if lang == 'en' else '' }}">English</a>
        <a href="/?lang=el" class="lang-btn {{ 'active' if lang == 'el' else '' }}">Ελληνικά</a>
    </div>
    
    <div class="bg-animation"></div>
    <div class="gym-icons">
        <div class="gym-icon">💪</div>
        <div class="gym-icon">🏋️</div>
        <div class="gym-icon">🏃</div>
        <div class="gym-icon">🥊</div>
    </div>
    
    <div class="login-container">
        <div class="login-box">
            <div class="logo">{{ t.gym_name }}</div>
            <div class="subtitle">{{ t.subtitle }}</div>
            <form method="post">
                <input type="hidden" name="language" value="{{ lang }}">
                <div class="input-group">
                    <input name="username" placeholder="{{ t.member_id }}" required>
                </div>
                <div class="input-group">
                    <input type="password" name="password" placeholder="{{ t.password }}" required>
                </div>
                <button type="submit" class="login-btn">{{ t.enter_gym }}</button>
            </form>
            {% if error %}<div class="error">{{ error }}</div>{% endif %}
        </div>
    </div>
</body>
</html>
"""

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYClOP GYM - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #e0e0e0;
            min-height: 100vh;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 20%, rgba(255, 69, 0, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(139, 0, 0, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 60% 40%, rgba(255, 140, 0, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }
        
        .header {
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(15px);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid rgba(255, 69, 0, 0.3);
            box-shadow: 0 0 20px rgba(255, 69, 0, 0.2);
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #ff4500;
            text-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .language-selector {
            display: flex;
            gap: 10px;
        }
        
        .lang-btn {
            background: rgba(255, 69, 0, 0.1);
            border: 1px solid rgba(255, 69, 0, 0.3);
            color: #e0e0e0;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            text-decoration: none;
            font-size: 0.9rem;
        }
        
        .lang-btn:hover {
            background: rgba(255, 69, 0, 0.2);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
        }
        
        .lang-btn.active {
            background: rgba(255, 69, 0, 0.8);
            border-color: #ff4500;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
        }
        
        .clock {
            font-size: 1.1rem;
            color: #ff8c00;
            text-shadow: 0 0 5px rgba(255, 140, 0, 0.5);
        }
        
        .logout-btn {
            background: linear-gradient(45deg, #8B0000, #B22222);
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            color: white;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(139, 0, 0, 0.3);
        }
        
        .logout-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(139, 0, 0, 0.6);
        }
        
        .main-container {
            padding: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .welcome-section {
            text-align: center;
            margin-bottom: 40px;
            animation: fadeInUp 0.8s ease-out;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .welcome-title {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff4500, #ff8c00, #FFD700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(255, 69, 0, 0.3);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 2px solid rgba(255, 69, 0, 0.2);
            transition: all 0.3s ease;
            animation: slideInLeft 0.6s ease-out;
            box-shadow: 0 0 20px rgba(255, 69, 0, 0.1);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(255, 69, 0, 0.3);
            border-color: rgba(255, 69, 0, 0.5);
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .stat-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .stat-number {
            font-size: 1.8rem;
            font-weight: bold;
            color: #ff4500;
            text-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: rgba(224, 224, 224, 0.8);
        }
        
        .section-title {
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: #ff4500;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 0 10px rgba(255, 69, 0, 0.3);
        }
        
        .areas-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .area-card {
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 25px;
            border: 2px solid rgba(255, 69, 0, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }
        
        .area-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--area-color), #ff4500);
            animation: shimmer 2s ease-in-out infinite;
        }
        
        @keyframes shimmer {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        .area-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 69, 0, 0.2);
            border-color: rgba(255, 69, 0, 0.5);
        }
        
        .area-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .area-name {
            font-size: 1.3rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .area-icon {
            font-size: 1.5rem;
        }
        
        .area-status {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .status-available { background: #228B22; box-shadow: 0 0 10px rgba(34, 139, 34, 0.5); }
        .status-busy { background: #FF8C00; box-shadow: 0 0 10px rgba(255, 140, 0, 0.5); }
        .status-full { background: #8B0000; box-shadow: 0 0 10px rgba(139, 0, 0, 0.5); }
        .status-maintenance { background: #4B0082; box-shadow: 0 0 10px rgba(75, 0, 130, 0.5); }
        .status-class { background: #FF4500; box-shadow: 0 0 10px rgba(255, 69, 0, 0.5); }
        
        .capacity-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin: 15px 0;
            border: 1px solid rgba(255, 69, 0, 0.2);
        }
        
        .capacity-fill {
            height: 100%;
            background: linear-gradient(45deg, var(--area-color), #ff4500);
            border-radius: 10px;
            transition: width 0.5s ease;
            animation: fillBar 1s ease-out;
            box-shadow: 0 0 10px rgba(255, 69, 0, 0.3);
        }
        
        @keyframes fillBar {
            from { width: 0%; }
        }
        
        .capacity-text {
            font-size: 0.9rem;
            color: rgba(224, 224, 224, 0.8);
        }
        
        .equipment-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }
        
        .equipment-tag {
            background: rgba(255, 69, 0, 0.1);
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            border: 1px solid rgba(255, 69, 0, 0.3);
            color: #e0e0e0;
        }
        
        .book-room-btn {
            width: 100%;
            padding: 10px;
            background: linear-gradient(45deg, var(--area-color), rgba(255, 255, 255, 0.2));
            border: none;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .book-room-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        .workouts-section {
            margin-top: 40px;
        }
        
        .workout-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .workout-card {
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 25px;
            border: 2px solid rgba(255, 69, 0, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }
        
        .workout-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 69, 0, 0.2);
            border-color: rgba(255, 69, 0, 0.5);
        }
        
        .workout-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .workout-name {
            font-size: 1.3rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .workout-icon {
            font-size: 1.5rem;
        }
        
        .workout-difficulty {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .difficulty-beginner { background: #228B22; box-shadow: 0 0 10px rgba(34, 139, 34, 0.5); }
        .difficulty-intermediate { background: #FF8C00; box-shadow: 0 0 10px rgba(255, 140, 0, 0.5); }
        .difficulty-advanced { background: #8B0000; box-shadow: 0 0 10px rgba(139, 0, 0, 0.5); }
        
        .workout-stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 0.9rem;
            color: rgba(224, 224, 224, 0.8);
        }
        
        .exercise-list {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .exercise-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 10px;
            border-left: 3px solid var(--workout-color);
        }
        
        .exercise-name {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .exercise-details {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .start-workout-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(45deg, var(--workout-color), rgba(255, 255, 255, 0.2));
            border: none;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 15px;
        }
        
        .start-workout-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
            margin: 5% auto;
            padding: 30px;
            border-radius: 20px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            animation: modalSlideIn 0.3s ease-out;
            border: 2px solid rgba(255, 69, 0, 0.3);
            box-shadow: 0 0 30px rgba(255, 69, 0, 0.2);
        }
        
        @keyframes modalSlideIn {
            from { opacity: 0; transform: translateY(-50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s;
        }
        
        .close:hover { color: #fff; }
        
        .timer-display {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: #ff4500;
            margin: 20px 0;
            text-shadow: 0 0 20px rgba(255, 69, 0, 0.5);
        }
        
        .timer-controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .timer-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .btn-start { background: #228B22; color: white; box-shadow: 0 0 10px rgba(34, 139, 34, 0.5); }
        .btn-pause { background: #FF8C00; color: white; box-shadow: 0 0 10px rgba(255, 140, 0, 0.5); }
        .btn-reset { background: #8B0000; color: white; box-shadow: 0 0 10px rgba(139, 0, 0, 0.5); }
        
        .timer-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        .booking-section {
            margin-bottom: 25px;
        }
        
        .booking-section h3 {
            color: #ff4500;
            margin-bottom: 15px;
            font-size: 1.2rem;
            text-shadow: 0 0 10px rgba(255, 69, 0, 0.3);
        }
        
        .time-slots-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .time-slot {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 10px;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        .time-slot:hover {
            background: rgba(255, 69, 0, 0.3);
            border-color: #ff4500;
            transform: translateY(-2px);
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
        }
        
        .time-slot.selected {
            background: linear-gradient(45deg, #ff4500, #ff8c00);
            border-color: #ff4500;
            box-shadow: 0 5px 15px rgba(255, 69, 0, 0.4);
        }
        
        .time-slot.booked {
            background: rgba(139, 0, 0, 0.3);
            border-color: #8b0000;
            cursor: not-allowed;
            opacity: 0.6;
        }
        
        .booking-select {
            width: 100%;
            padding: 12px;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(255, 69, 0, 0.3);
            border-radius: 10px;
            color: #e0e0e0;
            font-size: 1rem;
            cursor: pointer;
        }
        
        .booking-select:focus {
            outline: none;
            border-color: #ff4500;
            background: rgba(255, 69, 0, 0.1);
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.2);
        }
        
        .booking-select option {
            background: #1a1a1a;
            color: #e0e0e0;
        }
        
        .booking-summary {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }
        
        .summary-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .summary-item:last-child {
            border-bottom: none;
            font-weight: bold;
            color: #ff4500;
            text-shadow: 0 0 10px rgba(255, 69, 0, 0.3);
        }
        
        .book-now-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #228B22, #32CD32);
            border: none;
            border-radius: 25px;
            color: white;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 0 20px rgba(34, 139, 34, 0.3);
        }
        
        .book-now-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(34, 139, 34, 0.4);
        }
        
        .bookings-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .booking-card {
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid rgba(255, 69, 0, 0.2);
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }
        
        .booking-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(255, 69, 0, 0.2);
            border-color: rgba(255, 69, 0, 0.5);
        }
        
        .booking-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .booking-room-name {
            font-size: 1.2rem;
            font-weight: bold;
            color: #ff4500;
            text-shadow: 0 0 10px rgba(255, 69, 0, 0.3);
        }
        
        .booking-details {
            color: rgba(224, 224, 224, 0.8);
            line-height: 1.6;
        }
        
        .cancel-booking-btn {
            background: linear-gradient(45deg, #8B0000, #B22222);
            border: none;
            padding: 8px 15px;
            border-radius: 15px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            box-shadow: 0 0 10px rgba(139, 0, 0, 0.3);
        }
        
        .cancel-booking-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(139, 0, 0, 0.6);
        }
        
        @media (max-width: 900px) {
            .main-container { padding: 8px; }
            .header { flex-direction: column; gap: 10px; padding: 12px; }
            .logo { font-size: 1.2rem; }
            .user-info { flex-direction: column; gap: 8px; }
            .section-title { font-size: 1.2rem; margin-bottom: 12px; }
        }
        @media (max-width: 600px) {
            .main-container { padding: 2px; }
            .header { flex-direction: column; gap: 6px; padding: 8px; }
            .logo { font-size: 1rem; }
            .user-info { flex-direction: column; gap: 4px; }
            .section-title { font-size: 1rem; margin-bottom: 8px; }
            .stats-grid { grid-template-columns: 1fr; gap: 8px; }
            .areas-grid { grid-template-columns: 1fr; gap: 10px; }
            .workout-grid { grid-template-columns: 1fr; gap: 10px; }
            .bookings-grid { grid-template-columns: 1fr; gap: 8px; }
            .stat-card, .area-card, .workout-card, .booking-card { padding: 10px; border-radius: 10px; }
            .welcome-title { font-size: 1.2rem; }
            .area-name, .workout-name { font-size: 1rem; }
            .area-icon, .workout-icon { font-size: 1.2rem; }
            .area-status, .workout-difficulty { font-size: 0.7rem; padding: 3px 8px; }
            .capacity-bar { height: 5px; }
            .equipment-tag { font-size: 0.7rem; padding: 2px 6px; }
            .book-room-btn, .start-workout-btn, .book-now-btn, .cancel-booking-btn { font-size: 0.85rem; padding: 8px; border-radius: 12px; }
            .modal-content { padding: 12px; border-radius: 10px; }
            .timer-display { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">{{ t.gym_name }}</div>
        <div class="user-info">
            <div class="language-selector">
                <a href="/dashboard?lang=en" class="lang-btn {{ 'active' if lang == 'en' else '' }}">EN</a>
                <a href="/dashboard?lang=el" class="lang-btn {{ 'active' if lang == 'el' else '' }}">EL</a>
            </div>
            <div class="clock" id="clock"></div>
            <a href="/logout" class="logout-btn">{{ t.logout }}</a>
        </div>
    </div>
    
    <div class="main-container">
        <div class="welcome-section">
            <h1 class="welcome-title">{{ t.welcome_title }}</h1>
            <p>{{ t.welcome_subtitle }}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🏋️</div>
                <div class="stat-number">{{ stats.total_workouts }}</div>
                <div class="stat-label">{{ t.total_workouts }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-number">{{ stats.calories_burned }}</div>
                <div class="stat-label">{{ t.calories_burned }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚡</div>
                <div class="stat-number">{{ stats.streak_days }}</div>
                <div class="stat-label">{{ t.day_streak }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👑</div>
                <div class="stat-number">{{ stats.membership_level }}</div>
                <div class="stat-label">{{ t.membership }}</div>
            </div>
        </div>
        
        <div class="section-title">
            <span>🏢</span>
            <span>{{ t.gym_areas }}</span>
        </div>
        
        <div class="areas-grid">
            {% for area in areas %}
            <div class="area-card" style="--area-color: {{ area.color }}">
                <div class="area-header">
                    <div class="area-name">
                        <span class="area-icon">{{ area.icon }}</span>
                        <span>{{ area.name[lang] }}</span>
                    </div>
                    <div class="area-status status-{{ area.status.lower().replace(' ', '-') }}">
                        {{ t[area.status.lower().replace(' ', '_')] }}
                    </div>
                </div>
                <div class="capacity-bar">
                    <div class="capacity-fill" style="width: {{ (area.current_users / area.capacity * 100) }}%; --area-color: {{ area.color }}"></div>
                </div>
                <div class="capacity-text">{{ area.current_users }}/{{ area.capacity }} {{ t.members }}</div>
                <div class="equipment-list">
                    {% for equipment in area.equipment[lang] %}
                    <span class="equipment-tag">{{ equipment }}</span>
                    {% endfor %}
                </div>
                {% if area.get('bookable', False) %}
                <button class="book-room-btn" onclick="openBookingModal({{ area.id }})" style="--area-color: {{ area.color }}">
                    {{ t.book_room }}
                </button>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <div class="workouts-section">
            <div class="section-title">
                <span>💪</span>
                <span>{{ t.featured_workouts }}</span>
            </div>
            
            <div class="workout-grid">
                {% for workout in workouts %}
                <div class="workout-card" onclick="startWorkout({{ workout.id }})">
                    <div class="workout-header">
                        <div class="workout-name">
                            <span class="workout-icon">{{ workout.icon }}</span>
                            <span>{{ workout.name[lang] }}</span>
                        </div>
                        <div class="workout-difficulty difficulty-{{ workout.difficulty.lower() }}">
                            {{ t[workout.difficulty.lower()] }}
                        </div>
                    </div>
                    <div class="workout-stats">
                        <span>⏱️ {{ workout.duration }}</span>
                        <span>🔥 {{ workout.calories }} {{ t.cal }}</span>
                        <span>📋 {{ workout.exercises|length }} {{ t.exercises }}</span>
                    </div>
                    <div class="exercise-list">
                        {% for exercise in workout.exercises %}
                        <div class="exercise-item" style="--workout-color: {{ workout.color }}">
                            <div class="exercise-name">{{ exercise.name[lang] }}</div>
                            <div class="exercise-details">{{ exercise.sets }} {{ t.sets }} × {{ exercise.reps }} {{ t.reps }} | {{ t.rest }}: {{ exercise.rest[lang] }}</div>
                        </div>
                        {% endfor %}
                    </div>
                    <button class="start-workout-btn" style="--workout-color: {{ workout.color }}">
                        {{ t.start_workout }}
                    </button>
                </div>            {% endfor %}
        </div>
    </div>
    
    <!-- User Bookings Section -->
    <div class="bookings-section" style="margin-top: 40px;">
        <div class="section-title">
            <span>📅</span>
            <span>{{ t.your_bookings }}</span>
        </div>
        <div id="userBookings" class="bookings-grid">
            {% if user_bookings %}
                {% for booking in user_bookings %}
                <div class="booking-card">
                    <div class="booking-header">
                        <div class="booking-room-name">{{ booking.room_name }}</div>
                        <button class="cancel-booking-btn" onclick="cancelBooking({{ booking.id }})">
                            {{ t.cancel }}
                        </button>
                    </div>
                    <div class="booking-details">
                        <div>📅 {{ booking.date }}</div>
                        <div>⏰ {{ booking.time }} ({{ booking.duration }} {{ t.minutes }})</div>
                        {% if booking.trainer %}
                        <div>👨‍⚕️ {{ booking.trainer }}</div>
                        {% endif %}
                        <div>💰 €{{ booking.price }}</div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <p style="text-align: center; color: rgba(255, 255, 255, 0.6); grid-column: 1 / -1;">
                    {% if lang == 'el' %}Δεν έχετε κρατήσεις ακόμα{% else %}No bookings yet{% endif %}
                </p>
            {% endif %}
        </div>
    </div>
    </div>
    
    <!-- Workout Timer Modal -->
    <div id="workoutModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2 id="modalWorkoutName">{{ t.workout_timer }}</h2>
            <div class="timer-display" id="timerDisplay">00:00</div>
            <div class="timer-controls">
                <button class="timer-btn btn-start" onclick="startTimer()">{{ t.start }}</button>
                <button class="timer-btn btn-pause" onclick="pauseTimer()">{{ t.pause }}</button>
                <button class="timer-btn btn-reset" onclick="resetTimer()">{{ t.reset }}</button>
            </div>
            <div id="currentExercise"></div>
        </div>
    </div>
    
    <!-- Room Booking Modal -->
    <div id="bookingModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeBookingModal()">&times;</span>
            <h2 id="bookingRoomName">{{ t.room_booking }}</h2>
            
            <div class="booking-section">
                <h3>{{ t.available_slots }}</h3>
                <div class="time-slots-grid" id="timeSlotsGrid">
                    <!-- Time slots will be populated by JavaScript -->
                </div>
            </div>
            
            <div class="booking-section" id="trainerSection" style="display: none;">
                <h3>{{ t.trainer }}</h3>
                <select id="trainerSelect" class="booking-select">
                    <option value="">{{ t.select_time }}</option>
                </select>
            </div>
            
            <div class="booking-section" id="durationSection" style="display: none;">
                <h3>{{ t.duration }}</h3>
                <select id="durationSelect" class="booking-select">
                    <option value="60">1 {{ t.minutes }}</option>
                    <option value="90">1.5 {{ t.minutes }}</option>
                    <option value="120">2 {{ t.minutes }}</option>
                </select>
            </div>
            
            <div class="booking-summary" id="bookingSummary" style="display: none;">
                <h3>{{ t.room_schedule }}</h3>
                <div class="summary-item">
                    <span>{{ t.time_slot }}:</span>
                    <span id="selectedTime">-</span>
                </div>
                <div class="summary-item">
                    <span>{{ t.duration }}:</span>
                    <span id="selectedDuration">-</span>
                </div>
                <div class="summary-item">
                    <span>{{ t.trainer }}:</span>
                    <span id="selectedTrainer">-</span>
                </div>
                <div class="summary-item">
                    <span>{{ t.price }}:</span>
                    <span id="totalPrice">-</span>
                </div>
            </div>
            
            <button id="bookNowBtn" class="book-now-btn" onclick="confirmBooking()" style="display: none;">
                {{ t.book_now }}
            </button>
        </div>
    </div>
    
    <script>
        // Clock functionality
        function updateClock() {
            const now = new Date();
            const options = { 
                weekday: 'short', 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric', 
                hour: '2-digit', 
                minute: '2-digit' 
            };
            document.getElementById('clock').textContent = now.toLocaleDateString('en-US', options);
        }
        
        updateClock();
        setInterval(updateClock, 1000);
        
        // Workout timer functionality
        let timerInterval;
        let currentTime = 0;
        let isRunning = false;
        
        function startWorkout(workoutId) {
            const workouts = {{ workouts|tojson }};
            const workout = workouts.find(w => w.id === workoutId);
            const lang = '{{ lang }}';
            
            document.getElementById('modalWorkoutName').textContent = workout.name[lang];
            document.getElementById('workoutModal').style.display = 'block';
            
            // Display current exercise
            const exerciseList = workout.exercises.map((ex, idx) => 
                `<div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px;">
                    <strong>${idx + 1}. ${ex.name[lang]}</strong><br>
                    ${ex.sets} {{ t.sets }} × ${ex.reps} {{ t.reps }} | {{ t.rest }}: ${ex.rest[lang]}
                </div>`
            ).join('');
            document.getElementById('currentExercise').innerHTML = exerciseList;
        }
        
        function closeModal() {
            document.getElementById('workoutModal').style.display = 'none';
            resetTimer();
        }
        
        function startTimer() {
            if (!isRunning) {
                isRunning = true;
                timerInterval = setInterval(() => {
                    currentTime++;
                    updateTimerDisplay();
                }, 1000);
            }
        }
        
        function pauseTimer() {
            isRunning = false;
            clearInterval(timerInterval);
        }
        
        function resetTimer() {
            isRunning = false;
            clearInterval(timerInterval);
            currentTime = 0;
            updateTimerDisplay();
        }
        
        function updateTimerDisplay() {
            const minutes = Math.floor(currentTime / 60);
            const seconds = currentTime % 60;
            document.getElementById('timerDisplay').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('workoutModal');
            if (event.target === modal) {
                closeModal();
            }
        }
        
        // Add floating animation to cards
        document.querySelectorAll('.area-card, .workout-card, .stat-card').forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
        
        // Simulate real-time data updates
        setInterval(() => {
            const capacityFills = document.querySelectorAll('.capacity-fill');
            capacityFills.forEach(fill => {
                const currentWidth = parseInt(fill.style.width);
                const change = Math.random() > 0.5 ? 1 : -1;
                const newWidth = Math.max(0, Math.min(100, currentWidth + change));
                fill.style.width = newWidth + '%';
            });
        }, 30000); // Update every 30 seconds
        
        // Booking system functionality
        let currentBookingRoom = null;
        let selectedTimeSlot = null;
        let userBookings = [];
        
        function openBookingModal(roomId) {
            const areas = {{ areas|tojson }};
            const room = areas.find(r => r.id === roomId);
            const lang = '{{ lang }}';
            
            if (!room || !room.bookable) return;
            
            currentBookingRoom = room;
            document.getElementById('bookingRoomName').textContent = room.name[lang];
            document.getElementById('bookingModal').style.display = 'block';
            
            // Populate trainers
            const trainerSelect = document.getElementById('trainerSelect');
            trainerSelect.innerHTML = '<option value="">{{ t.select_time }}</option>';
            if (room.trainers && room.trainers[lang]) {
                room.trainers[lang].forEach(trainer => {
                    const option = document.createElement('option');
                    option.value = trainer;
                    option.textContent = trainer;
                    trainerSelect.appendChild(option);
                });
                document.getElementById('trainerSection').style.display = 'block';
            }
            
            generateTimeSlots();
        }
        
        function closeBookingModal() {
            document.getElementById('bookingModal').style.display = 'none';
            resetBookingForm();
        }
        
        function generateTimeSlots() {
            const timeSlotsGrid = document.getElementById('timeSlotsGrid');
            timeSlotsGrid.innerHTML = '';
            
            // Generate time slots from current hour to 22:00
            const now = new Date();
            const currentHour = now.getHours();
            
            for (let hour = Math.max(currentHour + 1, 8); hour < 22; hour++) {
                for (let minute of [0, 30]) {
                    const timeString = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
                    const slotElement = document.createElement('div');
                    slotElement.className = 'time-slot';
                    slotElement.textContent = timeString;
                    slotElement.onclick = () => selectTimeSlot(timeString, slotElement);
                    
                    // Check if slot is already booked
                    const isBooked = userBookings.some(booking => 
                        booking.room_id === currentBookingRoom.id && 
                        booking.time === timeString
                    );
                    
                    if (isBooked) {
                        slotElement.classList.add('booked');
                        slotElement.onclick = null;
                    }
                    
                    timeSlotsGrid.appendChild(slotElement);
                }
            }
        }
        
        function selectTimeSlot(time, element) {
            // Remove previous selection
            document.querySelectorAll('.time-slot').forEach(slot => {
                slot.classList.remove('selected');
            });
            
            // Select current slot
            element.classList.add('selected');
            selectedTimeSlot = time;
            
            // Show duration section
            document.getElementById('durationSection').style.display = 'block';
            
            updateBookingSummary();
        }
        
        function updateBookingSummary() {
            if (!selectedTimeSlot || !currentBookingRoom) return;
            
            const duration = document.getElementById('durationSelect').value || '60';
            const trainer = document.getElementById('trainerSelect').value || '{{ t.select_time }}';
            const pricePerHour = currentBookingRoom.price_per_hour || 25;
            const totalPrice = Math.round((parseInt(duration) / 60) * pricePerHour);
            
            document.getElementById('selectedTime').textContent = selectedTimeSlot;
            document.getElementById('selectedDuration').textContent = `${parseInt(duration)} {{ t.minutes }}`;
            document.getElementById('selectedTrainer').textContent = trainer;
            document.getElementById('totalPrice').textContent = `€${totalPrice}`;
            
            document.getElementById('bookingSummary').style.display = 'block';
            document.getElementById('bookNowBtn').style.display = 'block';
        }
        
        // Event listeners for duration and trainer selection
        document.getElementById('durationSelect').addEventListener('change', updateBookingSummary);
        document.getElementById('trainerSelect').addEventListener('change', updateBookingSummary);
        
        function confirmBooking() {
            if (!selectedTimeSlot || !currentBookingRoom) return;
            
            const duration = document.getElementById('durationSelect').value || '60';
            const trainer = document.getElementById('trainerSelect').value;
            const pricePerHour = currentBookingRoom.price_per_hour || 25;
            const totalPrice = Math.round((parseInt(duration) / 60) * pricePerHour);
            const lang = '{{ lang }}';
            
            const booking = {
                id: Date.now(),
                room_id: currentBookingRoom.id,
                room_name: currentBookingRoom.name[lang],
                time: selectedTimeSlot,
                duration: parseInt(duration),
                trainer: trainer,
                price: totalPrice,
                date: new Date().toDateString()
            };
            
            // Send booking to server
            fetch('/api/book-room', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(booking)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    userBookings.push(booking);
                    displayUserBookings();
                    closeBookingModal();
                    alert('{{ t.booking_success }}');
                } else {
                    alert('{{ t.booking_failed }}');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('{{ t.booking_failed }}');
            });
        }
        
        function cancelBooking(bookingId) {
            if (confirm('{{ t.cancel_booking }}?')) {
                fetch('/api/cancel-booking', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ booking_id: bookingId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        userBookings = userBookings.filter(b => b.id !== bookingId);
                        displayUserBookings();
                        alert('{{ t.booking_success }}');
                    } else {
                        alert('{{ t.booking_failed }}');
                    }
                });
            }
        }
        
        function displayUserBookings() {
            const bookingsContainer = document.getElementById('userBookings');
            
            if (userBookings.length === 0) {
                bookingsContainer.innerHTML = '<p style="text-align: center; color: rgba(255, 255, 255, 0.6);">No bookings yet</p>';
                return;
            }
            
            bookingsContainer.innerHTML = userBookings.map(booking => `
                <div class="booking-card">
                    <div class="booking-header">
                        <div class="booking-room-name">${booking.room_name}</div>
                        <button class="cancel-booking-btn" onclick="cancelBooking(${booking.id})">
                            {{ t.cancel }}
                        </button>
                    </div>
                    <div class="booking-details">
                        <div>📅 ${booking.date}</div>
                        <div>⏰ ${booking.time} (${booking.duration} {{ t.minutes }})</div>
                        ${booking.trainer ? `<div>👨‍⚕️ ${booking.trainer}</div>` : ''}
                        <div>💰 €${booking.price}</div>
                    </div>
                </div>
            `).join('');
        }
        
        function resetBookingForm() {
            selectedTimeSlot = null;
            currentBookingRoom = null;
            document.getElementById('durationSection').style.display = 'none';
            document.getElementById('bookingSummary').style.display = 'none';
            document.getElementById('bookNowBtn').style.display = 'none';
            document.getElementById('durationSelect').value = '60';
            document.getElementById('trainerSelect').value = '';
        }
        
        // Load user bookings on page load
        loadUserBookings();
        
        function loadUserBookings() {
            fetch('/api/user-bookings')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        userBookings = data.bookings;
                        displayUserBookings();
                    }
                })
                .catch(error => console.error('Error loading bookings:', error));
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    # Get language from URL parameter or session, default to English
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    t = translations[lang]
    
    if request.method == 'POST':
        # Store language preference from form
        if 'language' in request.form:
            lang = request.form['language']
            session['language'] = lang
            t = translations[lang]
            
        if request.form['username'] == '123456' and request.form['password'] == '654321':
            session['logged_in'] = True
            session['user_id'] = request.form['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(login_html, error=t['invalid_credentials'], t=t, lang=lang)
    
    return render_template_string(login_html, t=t, lang=lang)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Get language from URL parameter or session
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    t = translations[lang]
    
    # Update status translations based on current language
    status_map = {
        'Available': t['available'],
        'Busy': t['busy'], 
        'Full': t['full'],
        'Maintenance': t['maintenance'],
        'Class in Session': t['class_in_session']
    }
    
    # Simulate real-time updates to gym areas
    for area in gym_areas:
        # Randomly update current users (simulate real-time activity)
        if random.random() < 0.1:  # 10% chance to update
            change = random.randint(-2, 3)
            area['current_users'] = max(0, min(area['capacity'], area['current_users'] + change))
            
            # Update status based on capacity
            usage_percent = area['current_users'] / area['capacity']
            if usage_percent >= 1.0:
                area['status'] = 'Full'
            elif usage_percent >= 0.8:
                area['status'] = 'Busy'
            elif area['name']['en'] == 'Swimming Pool' and random.random() < 0.3:
                area['status'] = 'Maintenance'
            elif area['name']['en'] == 'Yoga & Mindfulness' and random.random() < 0.2:
                area['status'] = 'Class in Session'
            else:
                area['status'] = 'Available'
    
    return render_template_string(dashboard_html, 
                                areas=gym_areas, 
                                workouts=workout_programs,
                                stats=member_stats,
                                user_bookings=session.get('user_bookings', []),
                                t=t,
                                lang=lang)

@app.route('/api/gym-status')
def gym_status():
    """API endpoint for real-time gym data"""
    return jsonify({
        'areas': gym_areas,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/start-workout', methods=['POST'])
def start_workout():
    """API endpoint to log workout start"""
    workout_id = request.json.get('workout_id')
    workout = next((w for w in workout_programs if w['id'] == workout_id), None)
    
    if workout:
        # Log workout start (in a real app, this would go to a database)
        session['current_workout'] = {
            'id': workout_id,
            'name': workout['name'],
            'start_time': datetime.now().isoformat(),
            'status': 'in_progress'
        }
        
        return jsonify({
            'success': True,
            'message': f"Started workout: {workout['name']}",
            'workout': workout
        })
    
    return jsonify({'success': False, 'message': 'Workout not found'}), 404

@app.route('/api/complete-workout', methods=['POST'])
def complete_workout():
    """API endpoint to log workout completion"""
    if 'current_workout' in session:
        # Update member stats
        member_stats['total_workouts'] += 1
        member_stats['calories_burned'] += request.json.get('calories_burned', 0);
        
        # Clear current workout
        session.pop('current_workout', None)
        
        return jsonify({
            'success': True,
            'message': 'Workout completed successfully!',
            'stats': member_stats
        })
    
    return jsonify({'success': False, 'message': 'No active workout found'}), 400

@app.route('/api/book-room', methods=['POST'])
def book_room():
    """API endpoint to book a room"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    booking_data = request.json
    user_id = session.get('user_id', '4321')
    
    # Create booking record
    booking = {
        'id': len(room_bookings) + 1,
        'user_id': user_id,
        'room_id': booking_data['room_id'],
        'room_name': booking_data['room_name'],
        'time': booking_data['time'],
        'duration': booking_data['duration'],
        'trainer': booking_data.get('trainer', ''),
        'price': booking_data['price'],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'created_at': datetime.now().isoformat()
    }
    
    # Check for conflicts
    conflict = any(
        existing['room_id'] == booking['room_id'] and 
        existing['date'] == booking['date'] and
        existing['time'] == booking['time']
        for existing in room_bookings
    )
    
    if conflict:
        return jsonify({'success': False, 'message': 'Time slot already booked'}), 400
    
    room_bookings.append(booking)
    
    # Store user bookings in session
    if 'user_bookings' not in session:
        session['user_bookings'] = []
    session['user_bookings'].append(booking)
    
    return jsonify({
        'success': True,
        'message': 'Room booked successfully!',
        'booking': booking
    })

@app.route('/api/cancel-booking', methods=['POST'])
def cancel_booking():
    """API endpoint to cancel a booking"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    booking_id = request.json.get('booking_id')
    user_id = session.get('user_id', '4321')
    
    # Find and remove booking
    global room_bookings
    booking_to_remove = None
    
    for booking in room_bookings:
        if booking['id'] == booking_id and booking['user_id'] == user_id:
            booking_to_remove = booking
            break
    
    if booking_to_remove:
        room_bookings.remove(booking_to_remove)
        
        # Remove from session bookings
        if 'user_bookings' in session:
            session['user_bookings'] = [
                b for b in session['user_bookings'] 
                if b['id'] != booking_id
            ]
        
        return jsonify({
            'success': True,
            'message': 'Booking cancelled successfully!'
        })
    
    return jsonify({'success': False, 'message': 'Booking not found'}), 404

@app.route('/api/user-bookings')
def get_user_bookings():
    """API endpoint to get user's bookings"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    user_id = session.get('user_id', '4321')
    user_bookings = [
        booking for booking in room_bookings 
        if booking['user_id'] == user_id
    ]
    
    return jsonify({
        'success': True,
        'bookings': user_bookings
    })

@app.route('/api/available-slots/<int:room_id>')
def get_available_slots(room_id):
    """API endpoint to get available time slots for a room"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get existing bookings for this room today
    existing_bookings = [
        booking['time'] for booking in room_bookings
        if booking['room_id'] == room_id and booking['date'] == today
    ]
    
    # Generate available slots
    available_slots = generate_time_slots();
    
    # Mark booked slots
    for slot in available_slots:
        if slot['time'] in existing_bookings:
            slot['available'] = False
    
    return jsonify({
        'success': True,
        'slots': available_slots
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def start_ngrok():
    """Start ngrok tunnel"""
    try:
        # Kill any existing ngrok processes
        import subprocess
        try:
            subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                         capture_output=True, check=False)
        except:
            pass
        
        # Set ngrok auth token if available
        ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')
        if ngrok_auth_token:
            ngrok.set_auth_token(ngrok_auth_token)
        
        # Kill any existing tunnels
        try:
            ngrok.kill()
        except:
            pass
        
        # Small delay
        time.sleep(1)
        
        # Create a tunnel
        public_url = ngrok.connect(5055)
        print(f"🌐 Ngrok tunnel created: {public_url}")
        print(f"🌐 Public URL: {public_url}")
        return public_url
        
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        print("🔧 Make sure no other ngrok sessions are running")
        return None

if __name__ == '__main__':
    import os
    use_ngrok = os.getenv('USE_NGROK', '0') == '1'
    if use_ngrok:
        try:
            print("🚀 Starting ngrok tunnel...")
            ngrok_thread = threading.Thread(target=start_ngrok)
            ngrok_thread.daemon = True
            ngrok_thread.start()
            time.sleep(2)
            tunnels = ngrok.get_tunnels()
            if tunnels:
                public_url = tunnels[0].public_url
                print(f"✅ Gym App is now accessible at: {public_url}")
                print(f"✅ Share this URL to access your gym app from anywhere!")
        except Exception as e:
            print(f"❌ Error starting ngrok: {e}")
            print("🔧 Make sure ngrok is installed and configured properly")
    print("🏋️ Starting Gym App locally...")
    app.run(debug=True, host='0.0.0.0', port=5055)
