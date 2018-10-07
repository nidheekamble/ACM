from Unholify import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), unique=True)
    password= db.Column(db.String(150), nullable=False)
    stress_level= db.Column(db.Integer,unique=False,nullable=True)
    type= db.Column(db.String(1), nullable=True)
    #aboveUser= db.relationship("AboveUser", uselist=False, back_populates="user")

    def __repr__(self):
        return f"User('{self.email}','{self.type}','{self.stress_level}')"

class AboveUser(db.Model):

    id = db.Column(db.Integer, primary_key=True )
    above_type=db.Column(db.String(20), unique= False , nullable= False)
    above_friend=db.Column(db.String(120), unique=False)
    above_family=db.Column(db.String(120), unique=False)
    above_colleague=db.Column(db.String(120), unique=False)
    above_drunktimes=db.Column(db.Integer,unique=False )
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    #user = db.relationship("User", back_populates= "aboveUser" )

    def __repr__(self):
        return f"AboveUser('{self.above_type}','{self.above_friend}','{self.above_family}','{self.above_colleague}','{self.above_drunktimes}')"
