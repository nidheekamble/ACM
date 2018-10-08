import os
import secrets
from Unholify import app, db
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from Unholify.forms import RegistrationFormAbove,StressForm,UpdateAccountFormAboveUser,LoginForm,SelectForm
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
        pw = (form.password.data)
        s = 0
        for char in pw:
            a = ord(char) #ASCII
            s = s+a #sum of ASCIIs acts as the salt
        hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
        user = User( email= form.email.data , password= hashed_password )
        db.session.add(user)
        db.session.commit()
        flash(f'Success! Please fill in the remaining details', 'success')
        #if form.type.data == 'A':
            #flash(f'Success! Please fill in the remaining details', 'success')
        return redirect(url_for('registerAbove'))

        ##return redirect(url_for('login'))
    else: print('halaaaa')
    return render_template('selectForm.html', form=form)

@app.route("/registerAbove", methods=['GET', 'POST'])
def registerAbove():
    form = RegistrationFormAbove()
    if form.validate_on_submit():
        print('TF')
        aboveUser=AboveUser(above_type=form.above_type.data,above_friend=form.above_friend.data,above_family=form.above_family.data,above_colleague=form.above_colleague.data,above_drunktimes=0)
        db.session.add(aboveUser)
        db.session.commit()
        return redirect(url_for('login'))
    else: print('halaaa 1')
    return render_template('registerAbove.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        s = 0
        for char in (form.password.data):
            a = ord(char)
            s = s+a
        now_hash = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
        if (user and (user.password==now_hash)):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('stresslevel'))
        else:
            print('halaaa2')
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print('halaaa2')
    else:
        print('halaaa1')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods= ['POST', 'GET'])
@login_required
def account():

    form = UpdateAccountFormAboveUser()
    aboveUser = AboveUser.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():

        aboveUser.above_type=form.above_type.data
        aboveUser.above_friend=form.above_friend.data
        aboveUser.above_family=form.above_family.data
        aboveUser.above_colleague=form.above_colleague.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':

        form.above_type.data=aboveUser.above_type
        form.above_friend.data=aboveUser.above_friend
        form.above_family.data=aboveUser.above_family
        form.above_colleague.data=aboveUser.above_colleague
    return render_template('UpdateAccountAboveUser.html', title='Account', form=form)

@app.route("/stresslevel",methods=['POST','GET'])
@login_required
def stresslevel():
    form = StressForm()
    if form.validate_on_submit():
        current_user.stress_level=form.above_stress.data
        db.session.commit()
        if current_user.stress_level < 4 :
            return redirect('partyResponsibly')
        else:
            return redirect('stress')
    return render_template('stresslevel.html',title='How are you feeling today',form=form)

@app.route("/severeHelp",methods=['POST','GET'])
@login_required
def severeHelp():
    return render_template('severeHelp.html',title='We are with you')

@app.route("/ModerateHelp",methods=['POST','GET'])
@login_required
def moderateHelp():
    return render_template('moderateHelp.html',title='We are with you')

@app.route("/stress",methods=['POST','GET'])
@login_required
def stress():
    return render_template('stress.html',title='We are with you')

@app.route("/partyResponsibly",methods=['POST','GET'])
@login_required
def partyResponsibly():
    return render_template('congrats.html',title='Yay!')

@app.route("/OneMoreThing",methods=['POST','GET'])
@login_required
def facts():
    return render_template('facts.html',title='Freedom with responsibilities')

@app.route("/TakeMeHome",methods=['POST','GET'])
@login_required
def cab():
    user= User.query.filter_by(id=current_user.id).first()
    aboveUser = AboveUser.query.filter_by(id=user.id).first()
    return render_template('maps.html',title='Take Me Home', aboveUser=aboveUser)
