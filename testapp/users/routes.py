from flask import Blueprint,url_for,redirect,render_template,flash,request,abort
from testapp.users.forms import (registration_form,login_form,updateform,
                                 Requestresetform,Resetpasswordform,AnnouncementForm)
from flask_login import current_user,login_required,login_user,logout_user
from testapp.models import User,Post,Announcement
from testapp import db,bcrypt
from testapp.users.utils import save_picture,send_reset_email

users = Blueprint('users',__name__)


@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = registration_form()
    if form.validate_on_submit():
        hashed_passwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_passwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! your now you able to login','success')
        return redirect(url_for('main.home'))
    return render_template('register.html',title="Register",form=form)

@users.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = login_form()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page)if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Failed. recheck your email and password",'danger')
    return render_template('login.html',title="Login",form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account",methods=['POST','GET'])
@login_required
def account():
    form=updateform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file        
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated successfully','success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    
    image_file= url_for('static',filename='pictures/'+ current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page=request.args.get("page",1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
            .paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts=posts,user=user)

@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=Requestresetform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been send containing instructions to reset your password")
        return redirect('login')
    return render_template("reset_request.html",title="Reset password",form=form)
    
@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.verify_reset_token(token)
    if user is None:
        flash("This is an Invaid or expired token",'warning')
        return redirect(url_for('users.reset_request'))
    form=Resetpasswordform()
    if form.validate_on_submit():
        hashed_passwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_passwd
        db.session.commit()
        flash(f'Your password has been Updated! your now you able to login','success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html",title="Reset password",form=form)

@users.route("/admin",methods=['GET','POST'])
@login_required
def admin_page():
    def get_options():
        opt=Announcement.query.filter_by()
        option=0
        for i in opt:
            option+=1
        return option
    option=get_options()
    image_file= url_for('static',filename='pictures/'+ current_user.image_file)
    if current_user.username=='admin':
        return render_template('admin.html',title='Admin',image_file=image_file,option=option)
    else:
        flash("Please login with valid credentials to Access Admin Page")
        logout_user()
    return redirect(url_for('users.login'))

@users.route('/announcements')
def annonucements():
    posts=Announcement.query.order_by(Announcement.date_post.desc()).paginate()
    return render_template('announcement.html',title='Announcement',posts=posts)    


@users.route("/announcement/update",methods=["GET","POST"])
@login_required
def update_Announcement():
    form = AnnouncementForm()
    if current_user.username !="admin":
        abort(403)
    if form.validate_on_submit():
        Announce=Announcement(announce=form.announce.data)
        db.session.add(Announce)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('announce.html',title="New Announcement",form=form)

@users.route("/announcement/delete",methods=["POST","GET"])
@login_required
def delete_announcement():
    if current_user.username!="admin":
        abort(403)
    if request.method == 'POST':
        announcement_id = request.form.get('selectid')
        del_announcement=Announcement.query.get_or_404(announcement_id)
        db.session.delete(del_announcement)
        db.session.commit()
        flash("Your Announcement has been deleted","success")
        return redirect(url_for("main.home"))