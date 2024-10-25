from flask_sqlalchemy import SQLAlchemy
from application.database import db


# Model for Admin
class Admin(db.Model):
    __tablename__ = "Admin"
    roll = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "roll":self.roll,
            "username":self.username,
            "email":self.email
        }


# Model for User
class User(db.Model):
    __tablename__ = "User"
    roll = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tickets_booked = db.Column(db.Integer, nullable=False, default=0)
    booked = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "roll":self.roll,
            "username":self.username,
            "email":self.email,
            "tickets_booked":self.tickets_booked,
            "booked":self.booked,
        }


# Model for Theater
class Theater(db.Model):
    __tablename__ = "Theater"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theater_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='theater', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "roll":self.roll,
            "theater_name": self.theater_name,
            "location":self.location,
            "capacity":self.capacity
        }


# Model for Show
class Show(db.Model):
    __tablename__ = "Show"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String(120), nullable=False)
    theater_id =  db.Column(db.Integer,db.ForeignKey(Theater.roll, ondelete='CASCADE'))
    tags = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(120), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return{
            "roll": self.roll,
            "show_name":self.show_name,
            "theater_id":self.theater_id,
            "tags":self.tags,
            "time":self.time,
            "rating":self.rating,
            "price":self.price,
            "poster":self.poster,
            "seats_booked":self.seats_booked
        }


# Model for Booking
class Booking(db.Model):
    __tablename__ = "Booking"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_id = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey(User.roll, ondelete='CASCADE'))
    tickets_booked = db.Column(db.Integer,nullable=False)
    total_price = db.Column(db.Integer,nullable=False)
    booking_user = db.relationship('User', foreign_keys=[user_id], backref='bookings')

    def to_dict(self):
        return{
            "roll":self.roll,
            "show_id":self.show_id,
            "user_id":self.user_id,
            "tickets_booked":self.tickets_booked,
            "total_price":self.total_price
        }


# Model for Admin Token 
class AdminToken(db.Model):
    __tablename__ = "AdminToken"
    admin = db.Column(db.Integer, db.ForeignKey(Admin.roll), primary_key=True, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)


# Model for User Token
class UserToken(db.Model):
    __tablename__ = "UserToken"
    user = db.Column(db.Integer, db.ForeignKey(User.roll), primary_key=True, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)