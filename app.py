import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, flash, url_for
from models import db, WeatherData, AlertThreshold
from datetime import datetime
import requests
from flask_mail import Mail, Message
# Load environment variables from the .env file
load_dotenv()
# Flask Application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_data.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Your email password

mail = Mail(app)




# Set configurations using environment variables





# OpenWeatherMap API Configuration
API_KEY = os.getenv('API_KEY')  # your api key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']


def get_weather(city):
    """Fetch weather data for a city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url).json()
        return {
            "city": city,
            "main": response['weather'][0]['main'],
            "temp": round(response['main']['temp'] - 273.15, 2),
            "feels_like": round(response['main']['feels_like'] - 273.15, 2),
            "timestamp": datetime.utcfromtimestamp(response['dt'])
        }
    except (KeyError, requests.exceptions.RequestException):
        return None


def store_weather_data():
    """Store weather data for all cities."""
    with app.app_context():
        db.create_all()
        for city in CITIES:
            weather = get_weather(city)
            if weather:
                weather_entry = WeatherData(
                    city=weather['city'],
                    main=weather['main'],
                    temperature=weather['temp'],
                    feels_like=weather['feels_like'],
                    timestamp=weather['timestamp']
                )
                db.session.add(weather_entry)
        db.session.commit()


def send_email(subject, recipient, body):
    """Send an email notification."""
    msg = Message(
        subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = body
    mail.send(msg)


def check_alerts(city, current_temp):
    """Check if the current temperature exceeds threshold values."""
    threshold = AlertThreshold.query.filter_by(city=city).first()
    if threshold:
        alert_message = None
        if current_temp > threshold.max_temp:
            alert_message = f"ALERT: {city} has breached the maximum temperature threshold of {threshold.max_temp}°C!"
        elif current_temp < threshold.min_temp:
            alert_message = f"ALERT: {city} has breached the minimum temperature threshold of {threshold.min_temp}°C!"

        if alert_message:
            send_email("Weather Alert", threshold.email, alert_message)
            return alert_message
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        max_temp = request.form.get('max_temp')
        min_temp = request.form.get('min_temp')
        email = request.form.get('email')  # Get email from form

        # Check if a threshold already exists for the selected city
        threshold = AlertThreshold.query.filter_by(city=city).first()

        if threshold:
            # Update existing threshold
            threshold.max_temp = float(max_temp)
            threshold.min_temp = float(min_temp)
            threshold.email = email  # Update email
            flash(f'Threshold updated for {city}!', 'success')
        else:
            # Create a new threshold if not found
            threshold = AlertThreshold(
                city=city, max_temp=float(max_temp), min_temp=float(min_temp), email=email
            )
            db.session.add(threshold)
            flash(f'Threshold set for {city}!', 'success')

        db.session.commit()

    # Fetch weather data and alerts
    weather_data = [get_weather(city) for city in CITIES]
    alerts = [check_alerts(data['city'], data['temp'])
              for data in weather_data if check_alerts(data['city'], data['temp'])]

    return render_template('index.html', weather_data=weather_data, alerts=alerts)


@app.route('/summary/<city>')
def summary(city):
    """Generate summary for a specific city."""
    today = datetime.utcnow().date()
    data = WeatherData.query.filter(
        WeatherData.city == city, WeatherData.timestamp >= today).all()

    if not data:
        flash('No data available for summary.', 'warning')
        return redirect('/')

    avg_temp = sum(d.temperature for d in data) / len(data)
    max_temp = max(d.temperature for d in data)
    min_temp = min(d.temperature for d in data)
    dominant_condition = max(set([d.main for d in data]), key=[
                             d.main for d in data].count)

    summary_data = {
        "city": city,
        "avg_temp": round(avg_temp, 2),
        "max_temp": max_temp,
        "min_temp": min_temp,
        "dominant_condition": dominant_condition
    }
    return render_template('summary.html', summary=summary_data)


# Configure the scheduler
scheduler = BackgroundScheduler()
scheduler.start()


def periodic_weather_fetch():
    """Fetch and store weather data every 5 minutes."""
    store_weather_data()
    print("Weather data updated:", datetime.now())


# Schedule weather fetching every 5 minutes
scheduler.add_job(periodic_weather_fetch, 'interval', minutes=5)


def initialize_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()  # Create all tables


def list_tables():
    """List all tables in the database."""
    with app.app_context():  # Ensure we are in the application context
        inspector = inspect(db.engine)  # Create an inspector for the engine
        table_names = inspector.get_table_names()  # Get the list of table names
        print("Tables in the database:", table_names)  # Print the table names


if __name__ == '__main__':
    initialize_db()  # Ensure the database is initialized
       
    app.run(debug=False)
