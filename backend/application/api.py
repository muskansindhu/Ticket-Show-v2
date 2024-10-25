from flask_restful import Resource, request, reqparse
from passlib.hash import pbkdf2_sha256 as passhash
from application.models import Admin, User, AdminToken, UserToken, Show
from application.database import db
from application.access import *
from application.utils import *
from application.validation import NotFoundError, BusinessValidationError, DuplicationError, NotAuthorizedError
import secrets
import requests
import os
from application.config import *

class AdminAPI(Resource):
    def get(self,username):
        admin=getAdminUsername(username)
        if admin:
            return admin.to_dict()
        else:
            raise NotFoundError(404, "Admin Not Found")
    
    def post(self):
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
        return admin.to_dict()

    def put(self):
        auth = request.headers.get("Authorization", "").split()[1]
        token_id = AdminToken.query.filter_by(token=auth).first()
        if not token_id:
            raise NotAuthorizedError(401,"Invalid token or missing token")
        
        admin=Admin.query.filter_by(roll=token_id.admin).first()
        if not admin:
            raise NotFoundError(404, "Admin Not Found")
        
        if "new username" in request.form and request.form["new username"]:
            admin.username=request.form["new username"]

        if "new password" in request.form and request.form["new password"]:
            if len(request.form["new password"]) < 4:
                raise BusinessValidationError(
                    400,"ADMIN002", "Password should be at least 4 charatcers long")
            admin.password=passhash.hash(request.form["new password"])

        if "new email" in request.form and request.form["new email"]:
            admin.email=request.form["email"]

        db.session.commit()
        return getAdminRoll(token_id.admin).to_dict()
    
    def delete(self):
        auth = request.headers.get("Authorization", "").split()[1]
        token_id = AdminToken.query.filter_by(token=auth).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid or missing token")
        
        admin = Admin.query.filter_by(roll=token_id.admin).first()
        if not admin:
            raise NotFoundError(404, "Admin not found")

        resp = requests.get("http://localhost:1234/api/token-jwt", headers=request.headers)
        token = resp.json().get("jwt")
        if not token:
            raise NotAuthorizedError(401, "Invalid or missing token")

        resp = requests.delete("http://localhost:1234/vue/admin", headers={"Authorization": token})

        db.session.delete(admin)
        db.session.commit()
        db.session.delete(token_id)
        db.session.commit()

        return "Successfully Deleted"
        
       


class UserAPI(Resource):
    def get(self,username):
        user=getUserUsername(username)
        if user:
            return user.to_dict()
        else:
            raise NotFoundError(404, "User Not Found")
    
    def post(self):
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
        return user.to_dict()
  

    
    def put(self):
        auth = request.headers.get("Authorization", "").split()[1]
        
        token_id = UserToken.query.filter_by(token=auth).first()
        
        if not token_id:
            raise NotAuthorizedError(401,"Invalid token or missing token")
        
        user=User.query.filter_by(roll=token_id.user).first()
        if not user:
            raise NotFoundError(404, "User not found")
        
        if "new username" in request.form and request.form["new username"]:
            user.username=request.form["new username"]

        if "new password" in request.form and request.form["new password"]:
            if len(request.form["new password"]) < 4:
                raise BusinessValidationError(
                    400,"USER002", "Password should be at least 4 charatcers long")
            user.password = passhash.hash(request.form["new password"])

        if "new email" in request.form and request.form["new email"]:
            user.email=request.form["new email"]

        db.session.commit()
        return getUserRoll(token_id.user).to_dict()
    
    
    def delete(self):
        auth = request.headers.get("Authorization", "").split()[1]
        token_id = UserToken.query.filter_by(token=auth).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid or missing token")
        
        user = User.query.filter_by(roll=token_id.user).first()
        if not user:
            raise NotFoundError(404, "User not found")

        resp = requests.get("http://localhost:1234/api/token-jwt", headers=request.headers)
        token = resp.json().get("jwt")
        if not token:
            raise NotAuthorizedError(401, "Invalid or missing token")

        resp = requests.delete("http://localhost:1234/vue/admin", headers={"Authorization": token})

        db.session.delete(user)
        db.session.commit()
        db.session.delete(token_id)
        db.session.commit()

        return "Successfully Deleted"



class TheaterAPI(Resource):
    
    def get(self,theater_id):
        theater = getTheaterRoll(theater_id)
        if theater:
            return theater.to_dict()
        
        else:
            raise NotFoundError(404, "Theater Not Found")

    def post(self):
        token = request.headers.get("Authorization")
        if not token:
            raise NotAuthorizedError(401, "No Token Provide")
        token_id = AdminToken.query.filter_by(token=token.split()[1]).first()

        if not token_id:
            raise NotAuthorizedError(401, "Invalid Token")
        
        admin = Admin.query.filter_by(roll=token_id.admin).first()

        if not admin:
            raise NotFoundError(404, "Admin Not Found")
        
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
        db.session.commit()

        return theater.to_dict()
    
    def put(self, theater_id):
        token = request.headers.get("Authorization")
        if not token:
            raise NotAuthorizedError(401, "No Token Provide")
        token_id = AdminToken.query.filter_by(token=token.split()[1]).first()

        if not token_id:
            raise NotAuthorizedError(401, "Invalid Token")
        
        admin = Admin.query.filter_by(roll=token_id.admin).first()

        if not admin:
            raise NotFoundError(404, "Admin Not Found")
        
        theater = Theater.query.filter_by(roll=theater_id).first()
        
        theater_name = request.form.get("theater_name")
        if theater_name:
            theater.theater_name=theater_name

        location = request.form.get("location")
        if location:
            theater.location=location

        capacity = request.form.get("capacity")
        if capacity:
            theater.capacity=capacity

        db.session.commit()

        return theater.to_dict()
    
    def delete(self, theater_id):
        auth = request.headers.get("Authorization", "").split()[1]
        token_id = AdminToken.query.filter_by(token=auth).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid or missing token")
       
        theater=Theater.query.filter_by(roll=theater_id).first()

        if not token_id:
            raise NotAuthorizedError(401, "Invalid Token")  
       
        res=requests.get("http://localhost:1234/api/token-jwt", headers=request.headers)

        new_token=res.json()["jwt"]
        headers = {"Authorization": new_token}
        res = requests.delete(f'http://localhost:1234/theater/{theater_id}',headers=headers)

        db.session.delete(theater)
        db.session.commit()

        return "Theater Deleted Successfully"



class ShowAPI(Resource):

     def get(self, theater_id):
        theater = getTheaterRoll(theater_id)
        if not theater:
            raise NotFoundError(404, "Theater Not Found")
        
        shows = getShowsTheater(theater_id)

        return [show.to_dict() for show in shows]
     
     def post(self, theater_id):
        auth_header=request.headers.get("Authorization", None)
        if not auth_header:
            raise NotAuthorizedError(401,"No Token Provided")
        
        token=auth_header.split()[1]
        token_id=AdminToken.query.filter_by(token=token).first()
        if not token_id:
            raise NotAuthorizedError(401,"Invalid Token")
        
        admin = Admin.query.filter_by(roll=token_id.admin).first()
        if not admin:
            raise NotFoundError(404, "Admin not found")
        
        theater=Theater.query.filter_by(roll=theater_id).first()
        if not theater:
            raise NotFoundError(404,"Theater Not Found")
        
        theater_id = theater_id
        show_name = request.form.get("show_name")
        tags = request.form.get("tags")
        time = request.form.get("time")
        rating = request.form.get("rating")
        price = request.form.get("price")
        poster = request.form.get["Poster"]

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
        db.session.commit()

        return new_show.to_dict()
     

     
     def put(self, theater_id, show_id):
        auth_header=request.headers.get("Authorization", None)
        if not auth_header:
            raise NotAuthorizedError(401,"No Token Provided")
        
        token=auth_header.split()[1]
    
        token_id=AdminToken.query.filter_by(token=token).first()
        if not token_id:
            raise NotAuthorizedError(401,"Invalid Token")
        
        admin = Admin.query.filter_by(roll=token_id.admin).first()
        if not admin:
            raise NotFoundError(404, "Admin not found")
        
        theater=Theater.query.filter_by(roll=theater_id).first()
        if not theater:
            raise NotFoundError(404,"Theater Not Found")
        
        show=Show.query.filter_by(roll=show_id).first()
        if not Show:
            raise NotFoundError(404,"Show Not Found")
        
        
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

        db.session.commit()

        return show.to_dict()
     

     
     def delete(self, show_id):
        auth = request.headers.get("Authorization", "").split()[1]
        token_id = AdminToken.query.filter_by(token=auth).first()
        if not token_id:
            raise NotAuthorizedError(401, "Invalid or missing token")
       
        show=Show.query.filter_by(roll=show_id).first()

        if not token_id:
            raise NotAuthorizedError(401, "Invalid Token")  
       
        res=requests.get("http://localhost:1234/api/token-jwt", headers=request.headers)

        new_token=res.json()["jwt"]
        headers = {"Authorization": new_token}
        res = requests.delete(f'http://localhost:1234/show/{show_id}',headers=headers)

        db.session.delete(show)
        db.session.commit()

        return "Show Deleted Successfully"

    

     
    
class BookingAPI(Resource):
    def get(self, user_id):
        user = getUserRoll(user_id)
        if not user:
            raise NotFoundError(404, "User not found")
        booking = getUserBooking(user.roll)

        return [book.to_dict() for book in booking] 
    
    def post(self, show_id, user_id):
        authorization_header = request.headers.get("Authorization", None)
        
        if not authorization_header:
            raise NotAuthorizedError(401, "No Token Provided")

        auth_token = authorization_header.split()[1]
        token = UserToken.query.filter_by(token=auth_token).first()

        if not token:
            raise NotAuthorizedError(401, "Invalid Token")

        user = User.query.filter_by(roll=token.user).first()
        user_id = user.roll
        
        user = User.query.filter_by(roll=user_id).first()
        show = Show.query.filter_by(roll=show_id).first()

        if not user:
            raise BusinessValidationError(400, "BOOK001", "Invalid User ID")
        
        if not show:
            raise BusinessValidationError(400, "BOOK002", "No Show Provided")
        
        tickets_booked = int(request.form.get("tickets_booked"))
        user.tickets_booked = user.tickets_booked + tickets_booked
        user.booked = 1
        total_price =  tickets_booked * show.price
        new_booking = Booking(user_id=user_id, show_id=show_id, tickets_booked=tickets_booked,total_price=total_price)
        db.session.add(new_booking)
        db.session.commit()

        return new_booking.to_dict()



