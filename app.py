from flask import Flask, request, jsonify
from models import db, User, Train, Booking, Seat
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/railwaydb'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
jwt = JWTManager(app)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),  # In production, hash the password
        role=data.get('role', 'User')  # Set role to 'User' by default
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(status="Account successfully created", status_code=200, user_id=new_user.user_id), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'user_id': user.user_id, 'role': user.role})
        return jsonify(status="Login successful", status_code=200, user_id=user.user_id, access_token=access_token), 200
    else:
        return jsonify(status="Incorrect username/password provided. Please retry", status_code=401), 401
    
API_KEY="1234"

@app.route('/api/trains/create', methods=['POST'])
def add_train():
    if 
    api_key = request.headers.get('x-api-key')
    if api_key == API_KEY:
        data = request.get_json()
        new_train = Train(
            train_name=data['train_name'],
            source=data['source'],
            destination=data['destination'],
            seat_capacity=data['seat_capacity'],
            arrival_time_at_source=data['arrival_time_at_source'],
            arrival_time_at_destination=data['arrival_time_at_destination']
        )

        db.session.add(new_train)
        db.session.commit()

        return jsonify(message="Train added successfully", train_id=new_train.train_id), 200
    else:
        return jsonify(message="Unauthorized access", status_code=401), 401

@app.route('/api/trains/availability', methods=['GET'])
def get_seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return jsonify(message="Source and destination are required", status_code=400), 400

    trains = Train.query.filter_by(source=source, destination=destination).all()
    result = []

    for train in trains:
        booked_seats = db.session.query(db.func.sum(Booking.no_of_seats)).filter_by(train_id=train.train_id).scalar() or 0
        available_seats = train.seat_capacity - booked_seats
        result.append({
            "train_id": train.train_id,
            "train_name": train.train_name,
            "available_seats": available_seats
        })
    
    return jsonify(result), 200

@app.route('/api/trains/<int:train_id>/book', methods=['POST'])
def book_seat(train_id):
    #token = request.headers.get('Authorization')
    #if not token or not token.startswith('Bearer '):
        #return jsonify(message="Missing or invalid token", status_code=401), 401

    # Here you would add a function to verify the token
    # if not verify_token(token[7:]):
    #     return jsonify(message="Invalid token", status_code=401), 401

    data = request.get_json()
    user_id = data['user_id']
    no_of_seats = data['no_of_seats']

    train = Train.query.get(train_id)
    train=Train.query.filter_by(train_id=train_id)[0]
    #train=train_id
    if not train:
        return jsonify(message="Train not found", status_code=404), 404

    booked_seats = db.session.query(db.func.sum(Booking.no_of_seats)).filter_by(train_id=train_id).scalar() or 0
    available_seats = train.seat_capacity - booked_seats

    if no_of_seats > available_seats:
        return jsonify(message="Not enough seats available", status_code=400), 400

    seat_numbers = list(range(booked_seats + 1, booked_seats + no_of_seats + 1))

    new_booking = Booking(
        train_id=train_id,
        user_id=user_id,
        no_of_seats=no_of_seats
    )
    
    db.session.add(new_booking)
    db.session.commit()

    return jsonify(message="Seat booked successfully", booking_id=new_booking.booking_id, seat_numbers=seat_numbers), 200

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify(message="Missing or invalid token", status_code=401), 401

    # Here you would add a function to verify the token
    # if not verify_token(token[7:]):
    #     return jsonify(message="Invalid token", status_code=401), 401

    booking = db.session.query(Booking, Train).join(Train, Booking.train_id == Train.train_id).filter(Booking.booking_id == booking_id).first()
    
    if not booking:
        return jsonify(message="Booking not found", status_code=404), 404

    booking_data, train_data = booking
    seat_numbers = list(range(booking_data.seat_start, booking_data.seat_start + booking_data.no_of_seats))

    response_data = {
        "booking_id": str(booking_data.booking_id),
        "train_id": str(train_data.train_id),
        "train_name": train_data.train_name,
        "user_id": str(booking_data.user_id),
        "no_of_seats": booking_data.no_of_seats,
        "seat_numbers": seat_numbers,
        "arrival_time_at_source": train_data.arrival_time_at_source.strftime('%Y-%m-%d %H:%M:%S'),
        "arrival_time_at_destination": train_data.arrival_time_at_destination.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(response_data), 200


# Other endpoints (Login, Add New Train, Get Seat Availability, Book a Seat, Get Specific Booking Details) would be created similarly

if __name__ == '__main__':
    app.run(debug=True)
