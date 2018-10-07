import os
import secrets
from Unholify import app, db
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from Unholify.forms import RegistrationFormAbove,StressForm
from Unholify.models import User, AboveUser
import hashlib #for SHA512
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import Session
from math import sqrt
#from googlemaps import Client as GoogleMaps
from geopy.geocoders import Nominatim
from sqlalchemy import or_ , and_

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form= SelectForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if form.type.data == 'A':
            if form.validate_on_submit():
                pw = (form.password.data)
                s = 0
                for char in pw:
                    a = ord(char) #ASCII
                    s = s+a #sum of ASCIIs acts as the salt
                hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
                user = User( email= form.email.data , password= hashed_password, type= form.type.data )
                db.session.add(user)
                db.session.commit()
                flash(f'Success! Please fill in the remaining details', 'success')
            return redirect(url_for('registerAbove'))

        elif form.type.data == 'B':
            if form.validate_on_submit():
                pw = (form.password.data)
                s = 0
                for char in pw:
                   a = ord(char) #ASCII
                   s = s+a #sum of ASCIIs acts as the salt
                hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
                form2 = StressForm()
                user = User(email=form.email.data, password=hashed_password, type= form.type.data, stress_level=form2.above_stress.data)
                db.session.add(user)
                db.session.commit()
            return redirect(url_for('stress'))
    else: print('halaaaa')
    return render_template('selectForm.html', form2=form2, form=form)

@app.route("/registerAbove", methods=['GET', 'POST'])
def registerAbove():
    form = RegistrationFormAbove()
    if form.validate_on_submit():
        aboveUser=AboveUser(above_type=form.above_type.data,above_friend=form.above_friend.data,above_colleague=form.above_colleague,above_drunktimes=0,user_id=current_user.id)
        db.session.add(aboveUser)
        db.session.commit()
