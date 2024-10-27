
# Weather Monitoring Application

A Flask-based web application that fetches weather data for multiple cities, stores it in a database, and sends email alerts based on user-defined temperature thresholds. Users can view daily weather summaries and set alert thresholds.

## Features

- Fetch and store real-time weather data for multiple cities.
- Send email notifications for temperature threshold alerts.
- View daily weather summaries for specific cities.

## Tech Stack

- Flask  
- Flask-SQLAlchemy  
- Flask-Mail  
- APScheduler  
- SQLite (for the database)  
- OpenWeatherMap API  
- HTML/CSS for frontend  

---

## Setup Instructions

### Prerequisites

Ensure you have the following installed on your system:

- **Python** (version 3.6 or higher)  
- **Pip** (Python package installer)  
- **Git** (optional, for cloning the repository)

---

### 1. Clone the Repository

```bash
git clone https://github.com/SandeepaTN/weather_monitoring.git
cd weather_monitoring
```

---

### 2. Create the `.env` File

In the root directory, create a `.env` file and add the following environment variables:

```
SECRET_KEY=my_very_secret_key
MAIL_USERNAME=myemail@example.com
MAIL_PASSWORD=my_secure_password
API_KEY=my_openweathermap_api_key
```

> Replace the placeholder values with your actual credentials.

---

### 3. Install Required Dependencies

Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

---

### 4. Run the Application

To start the application, use:

```bash
python app.py
```

Open the application in your browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

---

## Usage

1. **Set Temperature Alerts**: Users can set temperature thresholds (max/min) and receive email alerts.
2. **View Weather Data**: The main page displays real-time data for selected cities.
3. **Summary Page**: Navigate to the summary page to view daily summaries for specific cities.

---

## Project Structure

```
.
├── app.py                  # Main Flask application file
├── .env                    # Environment variables for sensitive data
├── requirements.txt        # List of dependencies
├── models.py               # Database models for SQLAlchemy
├── templates/              # HTML templates
│   ├── index.html          # Main page template
│   └── summary.html        # Summary page template
└── static/                 # Static files (CSS)
    └── styles.css          # CSS styles
```

---

