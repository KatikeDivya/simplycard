from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    send_file
)

from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config

import qrcode
import os


# ==========================================
# APPLICATION
# ==========================================

app = Flask(__name__)

app.config.from_object(Config)


# ==========================================
# DATABASE
# ==========================================

db = SQLAlchemy(app)


# ==========================================
# LOGIN
# ==========================================

login_manager = LoginManager()

login_manager.login_view = "login"

login_manager.init_app(app)


# ==========================================
# USER MODEL
# ==========================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    card = db.relationship(
        "Card",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


# ==========================================
# CARD MODEL
# ==========================================

class Card(db.Model):

    __tablename__ = "cards"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    job_title = db.Column(
        db.String(100)
    )

    company = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(150)
    )

    phone = db.Column(
        db.String(30)
    )

    location = db.Column(
        db.String(150)
    )

    website = db.Column(
        db.String(200)
    )

    linkedin = db.Column(
        db.String(200)
    )

    github = db.Column(
        db.String(200)
    )

    instagram = db.Column(
        db.String(200)
    )

    about = db.Column(
        db.Text
    )

    profile_image = db.Column(
        db.String(255)
    )

    views = db.Column(
        db.Integer,
        default=0
    )


# ==========================================
# LOAD USER
# ==========================================

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# ==========================================
# HOME
# ==========================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==========================================
# REGISTER
# ==========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form["name"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]


        existing_user = User.query.filter_by(
            email=email
        ).first()


        if existing_user:

            flash(
                "Email already registered."
            )

            return redirect(
                url_for("register")
            )


        hashed_password = generate_password_hash(
            password
        )


        user = User(
            name=name,
            email=email,
            password=hashed_password
        )


        db.session.add(user)

        db.session.commit()


        flash(
            "Registration successful. Please login."
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# ==========================================
# LOGIN
# ==========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        password = request.form["password"]


        user = User.query.filter_by(
            email=email
        ).first()


        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid email or password."
        )


    return render_template(
        "login.html"
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("index")
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    card = Card.query.filter_by(
        user_id=current_user.id
    ).first()


    return render_template(
        "dashboard.html",
        card=card
    )


# ==========================================
# CREATE CARD
# ==========================================

@app.route(
    "/create-card",
    methods=["GET", "POST"]
)
@login_required
def create_card():

    existing_card = Card.query.filter_by(
        user_id=current_user.id
    ).first()


    if existing_card:

        return redirect(
            url_for("edit_card")
        )


    if request.method == "POST":

        username = request.form["username"].strip().lower()


        existing_username = Card.query.filter_by(
            username=username
        ).first()


        if existing_username:

            flash(
                "Username already exists."
            )

            return redirect(
                url_for("create_card")
            )


        card = Card(

            user_id=current_user.id,

            username=username,

            full_name=request.form["full_name"],

            job_title=request.form["job_title"],

            company=request.form["company"],

            email=request.form["email"],

            phone=request.form["phone"],

            location=request.form["location"],

            website=request.form["website"],

            linkedin=request.form["linkedin"],

            github=request.form["github"],

            instagram=request.form["instagram"],

            about=request.form["about"]
        )


        db.session.add(card)

        db.session.commit()


        flash(
            "Digital card created successfully."
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "create_card.html"
    )


# ==========================================
# EDIT CARD
# ==========================================

@app.route(
    "/edit-card",
    methods=["GET", "POST"]
)
@login_required
def edit_card():

    card = Card.query.filter_by(
        user_id=current_user.id
    ).first()


    if not card:

        return redirect(
            url_for("create_card")
        )


    if request.method == "POST":

        new_username = request.form[
            "username"
        ].strip().lower()


        existing_username = Card.query.filter(
            Card.username == new_username,
            Card.id != card.id
        ).first()


        if existing_username:

            flash(
                "Username already exists."
            )

            return redirect(
                url_for("edit_card")
            )


        card.username = new_username

        card.full_name = request.form["full_name"]

        card.job_title = request.form["job_title"]

        card.company = request.form["company"]

        card.email = request.form["email"]

        card.phone = request.form["phone"]

        card.location = request.form["location"]

        card.website = request.form["website"]

        card.linkedin = request.form["linkedin"]

        card.github = request.form["github"]

        card.instagram = request.form["instagram"]

        card.about = request.form["about"]


        db.session.commit()


        flash(
            "Card updated successfully."
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "create_card.html",
        card=card
    )


# ==========================================
# PUBLIC CARD
# ==========================================

@app.route("/card/<username>")
def public_card(username):

    card = Card.query.filter_by(
        username=username
    ).first()


    if not card:

        abort(404)


    card.views += 1

    db.session.commit()


    return render_template(
        "card.html",
        card=card
    )


# ==========================================
# QR CODE
# ==========================================

@app.route("/qr/<username>")
@login_required
def generate_qr(username):

    card = Card.query.filter_by(
        username=username
    ).first()


    if not card:

        abort(404)


    if card.user_id != current_user.id:

        abort(403)


    card_url = url_for(
        "public_card",
        username=card.username,
        _external=True
    )


    qr = qrcode.make(card_url)


    os.makedirs(
        "uploads",
        exist_ok=True
    )


    filepath = os.path.join(
        "uploads",
        f"{username}_qr.png"
    )


    qr.save(filepath)


    return send_file(
        filepath,
        as_attachment=True,
        download_name=f"{username}_qr.png"
    )


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

with app.app_context():

    db.create_all()


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=False,
        host="0.0.0.0",
        port=5000
    )