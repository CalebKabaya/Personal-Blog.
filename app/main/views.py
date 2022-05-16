from . import main
from flask import render_template,request,redirect,url_for,abort,flash
from ..models import  Blog, User,Comment,Subscriber
from .forms import UpdateProfile,BlogForm,CommentForm
from .. import db,photos
from flask_login import login_required,current_user
from app.requests import get_quotes
from ..email import mail_message






# from ..requests import 
# from .forms import 
# from .. import db,photos

# from flask_login import login_required,current_user
@main.route('/')
def index():
    quotes = get_quotes()
    blogs = Blog.query.all()
    technology  = Blog.query.filter_by(category = 'Technology').all() 
    health = Blog.query.filter_by(category = 'Health').all()
    lifestyle= Blog.query.filter_by(category = 'Lifestyle').all()
    food= Blog.query.filter_by(category = 'Food').all()


    return render_template('main/index.html',blogs =blogs,technology =technology, health = health, lifestyle=  lifestyle, food= food,quotes=quotes)
# @main.route('/')
# def index():


#     return render_template('main/index.html')

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
    subscribers = Subscriber.query.all()
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_blog_object = Blog(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_blog_object.save_p()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/welcome_user",subscriber.email,new_blog_object=new_blog_object)
        return redirect(url_for('main.index'))
        
    return render_template('main/blog.html', form = form)

@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        blog_id = blog_id
        new_comment = Comment(comment = comment,blog_id = blog_id)
        new_comment.save_c()
        return redirect(url_for('.comment', blog_id = blog_id))
    return render_template('main/comment.html', form =form,  blog =  blog,all_comments=all_comments) 

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))

@main.route('/blog/<blog_id>/update', methods = ['GET','POST'])
@login_required
def updateblog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.post = form.post.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for('main.blog',id = blog.id)) 
    if request.method == 'GET':
        form.title.data = blog.title
        form.post.data = blog.post
    return render_template('edit.html', form = form)


@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to KalebsBlog","email/welcome_user",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

