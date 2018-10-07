import os
import secrets
from Unholify import app, db
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
#from Unholify.forms import RegistrationFormParty, RegistrationFormSponser, LoginForm, SelectForm,UpdateAccountFormParty,UpdateAccountFormSponsor, ChatBoxText, RequestForm, InviteForm
#from Unholify.models import PartyUser, SponsorUser, User, Conversing, Conversation
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
