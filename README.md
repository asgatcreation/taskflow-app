# TaskFlow — Django To-Do App

A production-ready task manager built with Django 5.

🔗 **Live demo:** _coming soon — will update after deployment_

## Features
- User registration, login, and per-user task isolation
- Full CRUD for tasks (create, read, update, delete)
- Priorities (low/medium/high), due dates, overdue highlighting
- Search, status and priority filters, pagination
- Responsive dark UI
- PostgreSQL in production, SQLite locally
- Whitenoise for static files, Gunicorn server
- Deployed on Render

## Tech Stack
Django 5 · PostgreSQL · Gunicorn · Whitenoise · Render

## Local Setup

```bash
git clone https://github.com/asgatcreation/taskflow-app.git
cd taskflow-app
python -m venv venv
venv\Scripts\activate       
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver