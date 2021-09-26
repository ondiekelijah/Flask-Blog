from app import db ,migrate,login_manager,search
from flask_login import UserMixin, AnonymousUserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_sqlalchemy import event
from slugify import slugify
from flask import current_app
from flask_admin.contrib.sqla import ModelView


# from app import db,login_manager

class Permission:
    COMMENT = 0x02
    WRITE= 0x04
    MODERATE= 0x08
    ADMIN = 0x80
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role',lazy=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0    
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit() 

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm    
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm    
    def reset_permissions(self):
        self.permissions = 0    
    def has_permission(self, perm):
        return self.permissions & perm == perm 


    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column("image", db.String(150), default="user-icon.svg")
    uname = db.Column("uname", db.String(10), nullable=False, index=True, unique=True)
    email = db.Column("email", db.String(64), unique=True, nullable=False, index=True)
    pwd = db.Column("pwd", db.String(72), nullable=False, unique=True)
    fname = db.Column("Fname", db.String(20), nullable=False)
    lname = db.Column("Lname", db.String(20), nullable=False)
    about = db.Column(db.Text, nullable=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow) 
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable = False)


    def __init__(self, **kwargs):
    	super(User, self).__init__(**kwargs)
    	if self.role is None:
    		# check if the new user is set up as the admin, and gives them admin permissions
    		if self.email == current_app.config['ADMIN']:
    			self.role = Role.query.filter_by(permissions=0xff).first()
    		if self.role is None:
    			self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
        (self.role.permissions & permissions) == permissions
    def is_administrator(self):
        return self.can(Permission.ADMIN)
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000), nullable=False)
    respondent = db.Column("respondent", db.String(10), nullable=False)
    rimage = db.Column("rimage", db.String(150), default="user-icon.svg")
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id", ondelete="SET NULL"), nullable=True
    )
    post = db.relationship("Post", backref=db.backref("post"), lazy=True)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Comments %r>" % self.comment


class Replies(db.Model):
    __tablename__ = "replies"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.String(100), nullable=False)
    comment_id = db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return "<Replies %r>" % self.message


class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Messages %r>" % self.name
class Images(UserMixin, db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String(150))
    thumbnail=db.Column(db.String(150))
    file_size=db.Column(db.String(150))
    file_width=db.Column(db.String(150))
    file_height=db.Column(db.String(150))

    def __repr__(self):
        return "<Images %r>" % self.filename

class Subscribers(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column("email", db.String(64), unique=True, nullable=False, index=True)

    def __repr__(self):
        return "<Subscribers %r>" % self.email

class Post(db.Model):
    __tablename__ = "posts"
    __searchable__ = ['title','slug','body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    postImage = db.Column("postImage", db.String(150), default="default-blog-img.jpg")
    body = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0)
    count = db.Column(db.Integer, default=0)
    category = db.Column(db.String(30), nullable=False)
    s_category = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("author"), lazy=True)

    def __repr__(self):
        return "<Post %r>" % self.title

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


db.event.listen(Post.title, "set", Post.slugify, retval=False)
