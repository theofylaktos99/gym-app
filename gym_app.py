"""
Gym SaaS Application Entry Point (Render Compatible)
This module provides compatibility for Render's default naming convention.
It re-exports the app from run.py to allow both 'gunicorn run:app' and 'gunicorn gym_app:app'.
"""
from run import app

__all__ = ['app']
