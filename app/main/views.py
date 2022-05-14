from . import main
from . import main
from flask import render_template,request,redirect,url_for,abort
from ..models import  User



# from ..requests import 
# from .forms import 
from ..models import User
# from .. import db,photos

# from flask_login import login_required,current_user

@main.route('/')
def index():


    return render_template('main/index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)    
