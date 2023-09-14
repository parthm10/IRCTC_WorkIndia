from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='User')

class Train(db.Model):
    __tablename__ = 'Trains'
    train_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    seat_capacity = db.Column(db.Integer, nullable=False)
    arrival_time_at_source = db.Column(db.Time, nullable=False)
    arrival_time_at_destination = db.Column(db.Time, nullable=False)

class Booking(db.Model):
    __tablename__ = 'Bookings'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.Integer, db.ForeignKey('Trains.train_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    no_of_seats = db.Column(db.Integer, nullable=False)
    seat_numbers = db.Column(db.JSON, nullable=False)

class Seat(db.Model):
    __tablename__ = 'Seats'
    seat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.Integer, db.ForeignKey('Trains.train_id'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Available')
