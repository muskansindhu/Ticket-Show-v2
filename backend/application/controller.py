from flask import current_app as app
from application.validation import *
from flask_restful import request
from application.access import *
from application.models import Admin, User, Theater, Show, Booking
from application.config import UPLOAD_FOLDER
from application.cache import cache
from application.api import *
from application.tasks import export_csv, send_report, reminder_email
from application.utils import convert_to_webp
import datetime as dt
from datetime import timedelta
import jwt
import requests
from flask import jsonify, render_template
from application.utils import create_show_analytics
import os

admin_api = AdminAPI()
booking_api = BookingAPI()
user_api = UserAPI()
theater_api = TheaterAPI()
show_api = ShowAPI()

@app.route("/")
def home():
    return "Success", 200


@app.route('/api/token-jwt')
def generate_jwt_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided")

    token = auth_header.split()[1]
    encoded_token = jwt.encode({"token": token}, app.secret_key)

    return {"jwt": encoded_token}


@app.route("/vue/<int:user_id>/bookings")
def BookingUserVueAPI(user_id):
    return booking_api.get(user_id)


@app.route("/vue/admin/login", methods=["POST"])
def AdminLoginVue():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")
    admin = getAdminUsername(username)
    if not admin:
        return {"error": 404, "error_msg": "User not found"}
    if not passhash.verify(password, admin.password):
        return {"error": 401, "error_msg": "Invalid Password"}
    token = AdminToken.query.filter_by(admin=admin.roll).first().token
    encoded_token = jwt.encode({"token": token}, app.secret_key)
    expiry_time = dt.datetime.utcnow() + timedelta(days=30)
    return {"token": encoded_token, "exp": expiry_time}

@app.route("/vue/user/login", methods=["POST"])
def UserLoginVue():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")
    user = getUserUsername(username)
    if not user:
        return {"error": 404, "error_msg": "User not found"}
    if not passhash.verify(password, user.password):
        return {"error": 401, "error_msg": "Invalid Password"}
    token = UserToken.query.filter_by(user=user.roll).first().token
    encoded_token = jwt.encode({"token": token}, app.secret_key)
    expiry_time = dt.datetime.utcnow() + timedelta(days=30)
    return {"token": encoded_token, "exp": expiry_time}


@app.route("/vue/admin/<username>")
def AdminGetVue(username):
    return admin_api.get(username)


@app.route("/vue/admin", methods=["POST","PUT","DELETE"])
def AdminVue():
    if request.method == "PUT":
        response = admin_api.put()
        if isinstance(response, dict):
            return "Successful"
        elif isinstance(response, requests.Response):
            return f"Error: {response.status_code}"
        else:
            return "Unexpected response format"
        
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        roll = request.form.get('roll')

        if not username:
            raise BusinessValidationError(
                400,"ADMIN001", "Username is required"
            )
        
        if not password:
            raise BusinessValidationError(
                400,"ADMIN002", "Password should be at least 4 charatcers long"
            )
        
        if not email:
            raise BusinessValidationError(
                400,"ADMIN003", "Email is required"
            )
        
        if Admin.query.filter_by(username=username).first():
            raise DuplicationError(409, "Username already exist")
        
        admin = Admin(roll=roll,username=username,password=passhash.hash(password), email=email)
        db.session.add(admin)
        db.session.commit()
        admin_token = AdminToken(admin=admin.roll, token=secrets.token_urlsafe(16))
        db.session.add(admin_token)
        db.session.commit()
        cache.clear()
        token = admin_token.token
        encoded = jwt.encode({"token": token}, app.secret_key)
        expiry_time = dt.datetime.utcnow() + timedelta(days=30)
        return {"token": encoded, "exp": expiry_time}
    
    if request.method == "DELETE":
        return admin_api.delete()
    
    
@app.route("/vue/user/<username>")
def UserGetVue(username):
    return user_api.get(username)


@app.route("/vue/user", methods=["POST","PUT","DELETE"])
def UserVue():
    if request.method == "PUT":
        response = user_api.put()
        if isinstance(response, dict):
            return "Successful"
        elif isinstance(response, requests.Response):
            return f"Error: {response.status_code}"
        else:
            return "Unexpected response format"
        
    if request.method == "POST":
        roll = request.form.get('roll')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

    
        if not username:
            raise BusinessValidationError(
                400,"USER001", "Username is required"
            )
        
        if not password:
            raise BusinessValidationError(
                    400,"USER002", "Password should be at least 4 charatcers long")
        
        if not email:
            raise BusinessValidationError(
                400,"USER003", "Email is required"
            )
        
        if User.query.filter_by(username=username).first():
            raise DuplicationError(409, "Username already exist")

        
        user = User(roll=roll,username=username,password=passhash.hash(password), email=email)
        db.session.add(user)
        db.session.commit()
        user_token = UserToken(user=user.roll, token=secrets.token_urlsafe(16))
        db.session.add(user_token)
        db.session.commit()
        cache.clear()
        token = user_token.token
        encoded = jwt.encode({"token": token}, app.secret_key)
        expiry_time = dt.datetime.utcnow() + timedelta(days=30)
        return {"token": encoded, "exp": expiry_time}
    
    if request.method == "DELETE":
        return user_api.delete()
    

@app.route("/vue/theater/<theater_id>")
def TheaterGetVue(theater_id):
    return {"theater": theater_api.get(theater_id)}

@app.route("/vue/theater", methods=["POST","PUT","DELETE"])
def TheaterVue():
    if request.method == "PUT":
        response = theater_api.put()
        if isinstance(response, dict):
            return "Successful"
        elif isinstance(response, requests.Response):
            return f"Error: {response.status_code}"
        else:
            return "Unexpected response format"
        
    if request.method == "POST":
        auth = request.headers.get("Authorization")
        if not auth:
                raise NotAuthorizedError(401, "No Token Provided")
        token = auth.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"]).get("token")
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise NotAuthorizedError(401, "Invalid Token")
        token = AdminToken.query.filter_by(token=decoded_token).first()
        theater_name = request.form.get("theater_name")
        location = request.form.get("location")
        capacity = request.form.get("capacity")

        if not theater_name:
            raise BusinessValidationError(
                400, "THE001", "Theater Name is required")

        if not location:
            raise BusinessValidationError(
                400, "THE002", "Location is required")

        if not capacity:
            raise BusinessValidationError(
                400, "THE003", "Capacity is required")
        
        theater = Theater(theater_name=theater_name, location=location, capacity=capacity)

        db.session.add(theater)
        cache.clear()
        db.session.commit()

        return theater.to_dict()
        


@app.route('/vue/theater/<int:theater_id>', methods=['DELETE'])
def DeleteTheaterVue(theater_id):
    auth = request.headers.get("Authorization")
    if not auth:
        raise NotAuthorizedError(401, "No Token Provided")
    token = auth.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"]).get("token")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise NotAuthorizedError(401, "Invalid Token")
    token = AdminToken.query.filter_by(token=decoded_token).first()

    admin = Admin.query.filter_by(roll=token.admin).first()
    if not admin:
        raise NotFoundError(404, "Admin not found")
        
    theater=Theater.query.filter_by(roll=theater_id).first()
       
    res=requests.get("http://localhost:1234/api/token-jwt", headers=request.headers)

    new_token=res.json()["jwt"]
    headers = {"Authorization": new_token}
    res = requests.delete(f'http://localhost:1234/theater/{theater_id}',headers=headers)

    db.session.delete(theater)
    cache.clear()
    db.session.commit()

    return "Theater Deleted Successfully"

@app.route("/vue/theater/<int:theater_id>/show")
def ShowGetVue(theater_id):
    show=show_api.get(theater_id)
    return jsonify({'show':show, 'status':'success'})

@app.route("/vue/theater/show/<int:show_id>")
def ShowGetVueFromShowID(show_id):
    show = getShowRoll(show_id)
    return show.to_dict()
    
@app.route("/vue/all/theater")
def AllTheaterVue():
    theaters = getAllTheater()
    return jsonify({'theaters':theaters, 'status':'success'})


@app.route("/vue/show", methods=["POST","PUT","DELETE"])
def ShowVue():
    if request.method == "PUT":
        auth = request.headers.get("Authorization")
        if not auth:
                raise NotAuthorizedError(401, "No Token Provided")
        token = auth.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"]).get("token")
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise NotAuthorizedError(401, "Invalid Token")
        token = AdminToken.query.filter_by(token=decoded_token).first()
        
        show_id = request.form.get("show_id")
        
        show=Show.query.filter_by(roll=show_id).first()
        if not show:
            raise NotFoundError(404, "Show Not Found")
         
        try:
            show_name = request.form.get("show_name")
            if show_name:
                show.show_name=show_name

            rating = request.form.get("rating")
            if rating:
                show.rating=rating

            price = request.form.get("price")
            if price:
                show.price=price

            tags = request.form.get("tags")
            if tags:
                show.tags=tags

            time = request.form.get("time")
            if time:
                show.time=time

            cache.clear()
            db.session.commit()

            return jsonify({"message": "Show updated successfully"})
        except Exception as e:
            # Log the exception for debugging
            print(str(e))
            return jsonify({"error": "An error occurred while updating the show"}), 500
    
    if request.method == "POST":
        auth = request.headers.get("Authorization")
        if not auth:
                raise NotAuthorizedError(401, "No Token Provided")
        token = auth.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"]).get("token")
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise NotAuthorizedError(401, "Invalid Token")
        token = AdminToken.query.filter_by(token=decoded_token).first()

        admin = Admin.query.filter_by(roll=token.admin).first()
        if not admin:
            raise NotFoundError(404, "Admin not found")
        
        theater_id = request.form.get("theater_id")
        show_name = request.form.get("show_name")
        tags = request.form.get("tags")
        time = request.form.get("time")
        rating = request.form.get("rating")
        price = request.form.get("price")
        poster = request.files["poster"]

        if not show_name:
            raise BusinessValidationError(400, "SHOW001","Show Name is required")

        if not tags:
            raise BusinessValidationError(400, "SHOW002","Tag is required")
        
        if not time:
            raise BusinessValidationError(400, "SHOW003","Time is required")
        
        if not rating:
            raise BusinessValidationError(400, "SHOW004","Rating is required")
        
        if not price:
            raise BusinessValidationError(400, "SHOW005","Price is required")
        
        if not poster:
            raise BusinessValidationError(400, "SHOW006","Poster is required")
        
        if poster:
            if not allowed_file_img(poster.filename):
                raise BusinessValidationError(400, "SHOW007","Invalid File Type")
            filepath=os.path.join(UPLOAD_FOLDER+"Posters/", show_name +".webp")
            with open (filepath, 'wb') as f:
                f.write(convert_to_webp(poster))
                
        
        new_show = Show(show_name=show_name, tags=tags, time=time, rating=rating, price=price, theater_id=theater_id, poster=filepath)
        db.session.add(new_show)
        cache.clear()
        db.session.commit()

        return new_show.to_dict()
        
    
@app.route('/vue/show/<int:show_id>', methods=['DELETE'])
def DeleteShowVue(show_id):
    auth = request.headers.get("Authorization")
    if not auth:
        raise NotAuthorizedError(401, "No Token Provided")
    token = auth.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"]).get("token")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise NotAuthorizedError(401, "Invalid Token")
    token = AdminToken.query.filter_by(token=decoded_token).first()

    admin = Admin.query.filter_by(roll=token.admin).first()
    if not admin:
        raise NotFoundError(404, "Admin not found")
        
    show=Show.query.filter_by(roll=show_id).first()
       
    res=requests.get("http://localhost:1234/api/token-jwt", headers=request.headers)

    new_token=res.json()["jwt"]
    headers = {"Authorization": new_token}
    res = requests.delete(f'http://localhost:1234/show/{show_id}',headers=headers)

    db.session.delete(show)
    cache.clear()
    db.session.commit()

    return "Show Deleted Successfully"
    

@app.route("/vue/booking", methods=["POST"])
def ShowBookingVue():
        auth = request.headers.get("Authorization")
        if not auth:
                raise NotAuthorizedError(401, "No Token Provided")
        token = auth.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"]).get("token")
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise NotAuthorizedError(401, "Invalid Token")
        token = UserToken.query.filter_by(token=decoded_token).first()

        user = User.query.filter_by(roll=token.user).first()
        user_id=user.roll
        show_id = request.form.get("show_id")
        show = getShowRoll(show_id)
        if not show:
            raise NotFoundError(404, "Show not found")
        tickets_booked = request.form.get("tickets_booked")   
        user.tickets_booked += int(tickets_booked)
        show.seats_booked += int(tickets_booked)
        user.booked = 1

        total_price =  int(tickets_booked) * show.price
        new_booking = Booking(user_id=user_id, show_id=show_id, tickets_booked=tickets_booked,total_price=total_price)
        
        db.session.add(new_booking)
        cache.clear()
        db.session.commit()

        return new_booking.to_dict()


@app.route("/vue/searchShows/<string:term>")
@cache.memoize()
def SearchVueAPIget(term):
    shows = Show.query.filter(Show.show_name.like(f"%{term}%")).all()
    shows = [show.to_dict() for show in shows]
    return {"shows": shows}


@app.route("/vue/analytics/<int:theater_id>")
def analytics(theater_id):
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = AdminToken.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    admin = getAdminRoll(token_id.admin)
    create_show_analytics(theater_id)
    return "Successful"

@app.route("/vue/analytics/export_data/<int:theater_id>")
def export_data(theater_id):
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = AdminToken.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    admin = getAdminRoll(token_id.admin)
    export_csv.delay(admin.username, theater_id)
    return "Mail Sent"
    

@app.route("/vue/rate/<int:show_id>", methods=["PUT"])
def rate_show(show_id):
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = UserToken.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    
    show = Show.query.filter_by(roll=show_id).first()

    rating = request.form.get("rating")
    if rating:
        show.rating=rating

    cache.clear()
    db.session.commit()

    return "Rating Updated"

@app.route("/vue/user/bookings")
def UserBookingVue():
    auth_header = request.headers.get("Authorization").split(" ")[1]
    if not auth_header:
        raise NotAuthorizedError(401, "No token provided.")
    token = jwt.decode(auth_header, app.secret_key, algorithms="HS256").get("token")
    token_id = UserToken.query.filter_by(token=token).first()
    if not token_id:
        raise NotAuthorizedError(401, "Invalid token.")
    
    user = getUserRoll(token_id.user)
    bookingList=[]
    bookings = Booking.query.filter_by(user_id=user.roll).order_by(Booking.roll).all()

    for booking in bookings:
        booking_data={
            "roll": booking.roll,
            "show_id": booking.show_id,
            "tickets_booked": booking.tickets_booked,
            "total_price": booking.total_price
        }
        bookingList.append(booking_data)

    return {"bookings":bookingList}


@app.route("/generate-html-entertainment-report")
def entertainmentReport():
    send_report()
    return "Report Sent"



@app.route("/send-reminder-mail")
def reminderMail():
    reminder_email()
    return "Mail Sent"