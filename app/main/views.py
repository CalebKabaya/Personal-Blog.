from . import main
from flask import render_template,request,redirect,url_for,abort
from ..models import  Blog, User
from .forms import UpdateProfile,BlogForm
from .. import db,photos
from flask_login import login_required,current_user




# from ..requests import 
# from .forms import 
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
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)    

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/create_new', methods = ['POST','GET'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_blog_object = Blog(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_blog_object.save_p()
        return redirect(url_for('main.index'))
        
    return render_template('main/blog.html', form = form)