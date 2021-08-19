from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from .forms import *
from . import *
from wtforms import ValidationError, validators
from app import db, bcrypt, login_manager
from flask import current_app
from flask_login import (
    UserMixin,
    login_required,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
    send_from_directory,
)
from werkzeug.routing import BuildError
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from utils import *
from flask_bcrypt import generate_password_hash, check_password_hash
from models import *

auth = Blueprint("auth", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        # try:
        uname = form.uname.data
        email = form.email.data
        pwd = form.pwd.data
        fname = form.fname.data
        lname = form.lname.data
        newuser = User(
                uname=uname,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
                fname=fname,
                lname=lname,
            )
        db.session.add(newuser)
        db.session.commit()
        flash(f"Account Succesfully created", "success")
        return redirect(url_for("auth.login"))
        # except InvalidRequestError:
        #     db.session.rollback()
        #     flash(f"Something went wrong!", "danger")
        # except IntegrityError:
        #     db.session.rollback()
        #     flash(f"User already exists!.", "warning")
        # except DataError:
        #     db.session.rollback()
        #     flash(f"Invalid Entry", "warning")
        # except InterfaceError:
        #     db.session.rollback()
        #     flash(f"Error connecting to the database", "danger")
        # except DatabaseError:
        #     db.session.rollback()
        #     flash(f"Error connecting to the database", "danger")
        # except BuildError:
        #     db.session.rollback()
        #     flash(f"An error occured !", "danger")
    return render_template("auth/register.html", form=form)

# lOGIN route
@auth.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    default = 'http://127.0.0.1:5000/auth/login/'

    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                # flash(f"You've been logged in", "success")
                # return redirect(url_for('index')) 
                return redirect(url_for('blog.blog'))
            else:
                flash("Invalid Username or password!", "danger")
        except:
            flash("An Unknown error occured", "danger")

    return render_template("auth/login.html", form=form)


@auth.route("/account/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def account():
    form = UpdateProfile()
    if form.validate_on_submit():
        try:
            if form.profileImg.data:
                picture_file = save_img(form.profileImg.data)
                current_user.image = picture_file

            current_user.uname = form.uname.data
            current_user.email = form.email.data
            current_user.fname = form.fname.data
            current_user.lname = form.lname.data
            current_user.about = form.about.data

            db.session.commit()
            flash("Your profile has been updated", "success")
            return redirect(url_for("auth.account"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    elif request.method == "GET":
        form.uname.data = current_user.uname
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.about.data = current_user.about


    user = User.query.filter_by(uname=current_user.uname).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=30)
    )
    post_count = Post.query.filter_by(author=user).count()
    if not posts:
        flash("Ooops! You don't have any posts yet.", "info")
    image = url_for("static", filename="images/ProfileImages/" + current_user.image)
    return render_template(
        "auth/account.html",
        image=image,
        form=form,
        posts=posts,
        post_count=post_count,
        user=user,
        title="Teksade-Account",
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

