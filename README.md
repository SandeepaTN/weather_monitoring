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
cd weather_monitoring```


###  Create the .env File
In the root directory, create a .env file and add the following environment variables:


SECRET_KEY=my_very_secret_key
MAIL_USERNAME=myemail@example.com
MAIL_PASSWORD=my_secure_password
API_KEY=my_openweathermap_api_key


pip install -r requirements.txt
Access the app at http://127.0.0.1:5000/ in your browser.

Usage
Set Temperature Alerts: Users can set temperature thresholds (max/min) and receive email alerts.
View Weather Data: The main page displays real-time data for selected cities.
Summary Page: Navigate to the summary page to view daily summaries for specific cities.
