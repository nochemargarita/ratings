"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """ Show list of users. """

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register")
def register_form():
    """ Directs user to register. """

    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():
    """Complete registration"""

    email = request.form.get("email")
    password = request.form.get("password")

    q = db.session.query(User).filter(User.email == email)
    # print q
    if db.session.query(q.exists()):
        flash('Email is already taken!')
        return redirect('/register')
        
    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect('/')

@app.route("/login")
def login_form():

    return render_template("login_form.html")

@app.route("/login", methods=["POST"])
def login():
    
    email = request.form.get("email")
    password = request.form.get("password")

    user = db.session.query(User).filter(User.email == email,
                                        User.password == password).first()
    if user:
        session['email'] = request.form.get('email')
        flash('You were successfully logged in')
        return redirect('/')

    else:
        flash('You successfully failed!')
        return redirect('/login')

    # flash("works")


    # print user
    # SELECT users.user_id AS users_user_id, users.email AS users_email, users.password AS users_password, users.age AS users_age, users.zipcode AS users_zipcode 
    # FROM users 
    # WHERE users.email = %(email_1)s AND users.password = %(password_1)s

@app.route("/logout")
def logout():
    flash('You successfully logged out! Come back soon!')
    session.pop('email', None)
    print session
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
