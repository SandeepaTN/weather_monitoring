from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    main = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    feels_like = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class AlertThreshold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    email = db.Column(db.String(120), nullable=False)
