from models import db, User
from app import app

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id} | Username: {user.username}")
