from flask import Blueprint
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from .form import *
from ..utils import *
from ..decorators import admin_required, permission_required

# from .. import app
from flask import current_app
from wtforms import ValidationError, validators
from ..app import db, bcrypt, login_manager
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
from PIL import Image
from flask_bcrypt import generate_password_hash, check_password_hash
from ..models import *
from flask_msearch import Search
from ..app import search

bp = Blueprint("blog", __name__, url_prefix="/blog")

# url = "http://localhost:5000/{url_for('blog.article',post_id=post.id,uname=post.author.uname,slug=post.slug)}"


@bp.route("/", methods=("GET", "POST"), strict_slashes=False)
def blog():
    # All blog posts - order >> descending
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    if not posts:
        flash("No Posts are available", "info")
    # blog posts - order >> trending
    # keyword = request.args.get('sval','')
    # results = Post.query.filter(Post.title.contains(keyword) |
    #         Post.body.contains(keyword))
    trending = (
        Post.query.filter(Post.views >= 1000)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=6)
    )
    return render_template(
        "blog/blog.html", posts=posts, trending=trending, title="Dev Elie | Home"
    )


@bp.route("/search/", strict_slashes=False, methods=("GET", "POST"))
def search():
    keyword = request.args.get("sval", "")
    posts = Post.query

    # posts = Post.query.all()
    # posts = Post.query.msearch(
    #     keyword, fields=["title", "slug", "body"], limit=20
    # ).all()
    # posts = Post.query.filter(Post.title.contains(keyword))
    # posts = Post.query
    # posts = posts.filter_by(Post.title.like('%' + keyword + '%'))
    # posts = posts.order_by(Post.title).all()
    # if request.method == 'POST':
    #     search = request.args.get('sval','')
    # search = search.strip()
    # posts = Post.query.filter(or_(Post.title.like(keyword), Post.slug.ilike(keyword))).all()

    posts = posts.filter(Post.title.like('%' + keyword + '%'))

    posts = posts.order_by(Post.id).all()
    return render_template(
        "blog/search_results.html",
        label="Search Results",
        posts=posts,
        title="Dev Elie | Home",
    )


@bp.route("/Technology/", strict_slashes=False)
def tech():
    form = Search()
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(category="Technology")
        # .filter_by(s_category = 'Technology')
        .paginate(page=page, per_page=10)
    )
    if not posts:
        flash("No Posts are available", "info")
    trending = (
        Post.query.filter(Post.views >= 1000)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=6)
    )

    # blog posts - order >> featured
    return render_template(
        "blog/blog.html",
        posts=posts,
        trending=trending,
        form=form,
        title="Dev Elie | Home",
    )


@bp.route("/Business/", strict_slashes=False)
def bs():
    form = Search()
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter_by(category="Business").paginate(page=page, per_page=10)
    if not posts:
        flash("No Posts are available", "info")
    trending = (
        Post.query.filter(Post.views >= 1000)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=6)
    )
    return render_template(
        "blog/blog.html",
        posts=posts,
        trending=trending,
        form=form,
        title="Dev Elie | Home",
    )


@bp.route(
    "/<int:post_id>/<string:uname>/<string:slug>",
    methods=("GET", "POST"),
    strict_slashes=False,
)
def article(post_id, uname, slug):
    comment_form = CommentPost()
    replies_form = ReplyComment()
    post = Post.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(post_id=post.id).all()
    post.views += 1
    db.session.commit()

    # Comment replies
    # comment_id.get_commentID()

    # comment = Comments.query.filter_by(id=comment_id).first()
    # replies = Replies.query.filter_by(comment_id=comment_id).all()

    url = "http://127.0.0.1:5000/"

    read_time = estimate_reading_time(url)

    if request.method == "POST" and comment_form.validate_on_submit():
        message = comment_form.comment.data
        print(message)
        comment = Comments(
            message=message,
            post_id=post.id,
            respondent=current_user.uname,
            rimage=current_user.image,
        )
        db.session.add(comment)
        post.count += 1
        flash("Comment posted", "success")
        db.session.commit()
    elif request.method == "POST" and replies_form.validate_on_submit():
        message = replies_form.reply.data
        if not current_user.is_authenticated:
            uname = "Anonymous"
        else:
            uname = current_user.uname

            reply = Replies(
                message=message,
                author=uname,
            )
            db.session.add(reply)
            db.session.commit()
            print("Replied")

    return render_template(
        "blog/article.html",
        post=post,
        read_time=read_time,
        form=comment_form,
        form2=replies_form,
        comments=comments,
        title="Dev Elie | Blog",
    )


@bp.route("/add", methods=("GET", "POST"), strict_slashes=False)
@login_required
@admin_required
def new_post():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    form = AddPost()
    if form.validate_on_submit():
        try:
            if form.postImage.data:
                picture_file = upload_img(form.postImage.data)
                title = form.title.data
                postImage = picture_file
                body = form.body.data
                category = form.category.data
                s_category = form.s_category.data
                post = Post(
                    title=title,
                    postImage=postImage,
                    body=body,
                    category=category,
                    s_category=s_category,
                    user_id=current_user.id,
                )
                db.session.add(post)
                db.session.commit()
                flash(f"Post succesfully published", "success")

                return redirect(url_for("blog.blog"))
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

    return render_template(
        "blog/add.html",
        form=form,
        posts=posts,
        title="Dev Elie | Blog",
        legend="Create a new blog article",
    )


@bp.route(
    "/<int:post_id>/<string:slug>/update",
    methods=("GET", "POST"),
    strict_slashes=False,
)
@login_required
@admin_required
def update_article(post_id, slug):
    post = Post.query.filter_by(id=post_id).first()
    if post.author != current_user:
        abort(403)
    form = AddPost()
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.body = form.body.data
            db.session.commit()

            flash("Post succesfully Updated", "success")
            return redirect(url_for("blog.blog"))

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
        form.title.data = post.title
        form.body.data = post.body

    return render_template(
        "blog/add.html",
        form=form,
        post=post,
        title="Dev Elie|Blog-update post",
        legend="Update Post",
    )


@bp.route(
    "/<int:post_id>/<string:slug>/delete",
    methods=("GET", "POST"),
    strict_slashes=False,
)
@login_required
@admin_required
def delete_article(post_id, slug):
    post = Post.query.filter_by(id=post_id).first()
    if post.author != current_user:
        abort(403)

    flash("Post has been deleted succesfully ", "success")
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.blog"))


@bp.route("/user/<string:uname>", methods=("GET", "POST"), strict_slashes=False)
def profile(uname):
    user = User.query.filter_by(uname=uname).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=6)
    )
    if not posts:
        flash("Ooops! You don't have any posts yet.", "info")
    image = url_for("static", filename="images/ProfileImages/" + user.image)
    return render_template(
        "blog/user_profile.html",
        image=image,
        posts=posts,
        user=user,
        title="Dev Elie | Profile",
    )


@bp.route("/subscribe/", methods=("GET", "POST"), strict_slashes=False)
def subscribe():
    form = Subscribe()
    if request.method == "POST":
        if form.validate_on_submit():
            try:

                email = form.email.data
                email = Subscribers(
                    email=email,
                )
                db.session.add(email)
                db.session.commit()
            except InvalidRequestError:
                db.session.rollback()
                flash(f"Something went wrong!", "danger")
            except IntegrityError:
                db.session.rollback()
                flash(f"You are already a member !.", "warning")
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
    return ("", 204)


# Handles javascript image uploads from tinyMCE
@bp.route("/imageuploader", methods=["POST"])
@login_required
@admin_required
def imageuploader():
    file = request.files.get("file")
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split(".")
        # truncate filename (excluding extension) to 30 characters
        fn = fn[:30]
        filename = fn + "." + ext
        if ext in ["jpg", "gif", "png", "jpeg"]:
            try:
                # everything looks good, save file
                img_fullpath = os.path.join(
                    current_app.root_path, "static/images/blog-posts", filename
                )
                file.save(img_fullpath)
                # get the file size to save to db
                file_size = os.stat(img_fullpath).st_size
                size = 160, 160
                # read image into pillow
                im = Image.open(img_fullpath)
                # get image dimension to save to db
                file_width, file_height = im.size
                # convert to thumbnail
                im.thumbnail(size)
                thumbnail = fn + "-thumb.jpg"
                tmb_fullpath = os.path.join(
                    current_app.root_path, "static/images/blog-posts", filename
                )
                # PNG is index while JPG needs RGB
                if not im.mode == "RGB":
                    im = im.convert("RGB")
                # save thumbnail
                im.save(tmb_fullpath, "JPEG")

                # # save to db
                # img = Images(
                #     filename=filename,
                #     thumbnail=thumbnail,
                #     file_size=file_size,
                #     file_width=file_width,
                #     file_height=file_height,
                # )
                # db.session.add(img)
                # db.session.commit()
            except IOError:
                output = make_response(404)
                output.headers["Error"] = "Cannot create thumbnail for " + filename
                return output
            return jsonify({"location": filename})

    # fail, image did not upload
    output = make_response(404)
    output.headers["Error"] = "Filename needs to be JPG, JPEG, GIF or PNG"
    return output
