# IRCTC_WorkIndia

Railway Management System
This is a simple railway management system built using Python and Flask, designed to handle train operations, user registration, and seat booking.

## Features
User Registration
User Login
Admin Access for Train Management
Adding New Trains
Checking Seat Availability
Booking Seats
Retrieving Booking Details
Tech Stack
Python Flask for the backend server
MySQL database for data storage
Flask-SQLAlchemy for database management
Flask-Migrate for database migrations
Flask-JWT-Extended for authentication

##Installation
Clone the repository:

git clone https://github.com/yourusername/railway-management-system.git
Install the required dependencies:

pip install -r requirements.txt
Set up your MySQL database and configure the database URI in app.py:

python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/railwaydb'
Create the necessary database tables:

flask db init
flask db migrate
flask db upgrade
Run the Flask application:

flask run

## Usage
Register a user by making a POST request to /api/signup with username, password, and email in the request body.

Log in with your credentials by making a POST request to /api/login.

Admin users can add new trains by making a POST request to /api/trains/create with the appropriate API key.

Check seat availability between two stations by making a GET request to /api/trains/availability?source=SOURCE&destination=DESTINATION.

Book a seat on a particular train by making a POST request to /api/trains/{train_id}/book with the Authorization header containing a valid token.

Get specific booking details by making a GET request to /api/bookings/{booking_id} with the Authorization header containing a valid token.
