from application.models import Admin, User, Theater, Show, Booking
from application.cache import cache
from application.config import ALLOWED_EXTENSIONS_IMG


@cache.memoize()
def getAdminUsername(username):
    admin = Admin.query.filter_by(username=username).first()
    return admin

@cache.memoize()
def getUserUsername(username):
    user = User.query.filter_by(username=username).first()
    return user

@cache.memoize()
def getAdminRoll(roll):
    admin = Admin.query.filter_by(roll=roll).first()
    return admin

@cache.memoize()
def getUserRoll(roll):
    user = User.query.filter_by(roll=roll).first()
    return user

@cache.memoize()
def getTheaterRoll(roll):
    theater = Theater.query.filter_by(roll=roll).first()
    return theater


def getShowRoll(roll):
    show = Show.query.filter_by(roll=roll).first()
    return show

@cache.memoize()
def getShowsTheater(theater_id):
    shows = Show.query.filter_by(theater_id=theater_id).order_by(Show.roll).all()
    return shows

@cache.memoize()
def getUserBooking(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.roll).all()
    return bookings

@cache.memoize()
def getBookingRoll(roll):
    bookings = Booking.query.filter_by(roll=roll).first()
    return bookings

@cache.memoize()
def getAllTheater():
    theaters = Theater.query.all()
    theater_list = []

    for theater in theaters:
        theater_data = {
            'roll': theater.roll,
            'theater_name': theater.theater_name,
            'location': theater.location,
            'capacity' : theater.capacity
        }
        theater_list.append(theater_data)

    return theater_list

@cache.memoize()
def getTheaterName(theater_id):
    theater = Theater.query.filter_by(roll=theater_id).first()
    return theater.theater_name

@cache.memoize()
def getTheaterFromTheaterName(theater_name):
    theater = Theater.query.filter_by(theater_name=theater_name).first()
    return theater


@cache.memoize()
def getAllBookings():
    bookings = Booking.query.all()
    return bookings

@cache.memoize()
def getAllAdmin():
    admin = Admin.query.all()
    return admin


@cache.memoize()
def getAllUser():
    user = User.query.all()
    return user

def allowed_file_img(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG