CREATE DATABASE RailwayDB;

USE RailwayDB;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255),
    role ENUM('Admin', 'User') DEFAULT 'User'
);

CREATE TABLE Trains (
    train_id INT AUTO_INCREMENT PRIMARY KEY,
    train_name VARCHAR(100),
    source VARCHAR(100),
    destination VARCHAR(100),
    seat_capacity INT,
    arrival_time_at_source TIME,
    arrival_time_at_destination TIME
);

CREATE TABLE Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT,
    user_id INT,
    no_of_seats INT,
    seat_numbers JSON,
    FOREIGN KEY (train_id) REFERENCES Trains(train_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Seats (
    seat_id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT,
    seat_number INT,
    status ENUM('Available', 'Booked') DEFAULT 'Available',
    FOREIGN KEY (train_id) REFERENCES Trains(train_id)
);
