"""TESS PROJECT"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Rating


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {username} added.")
    return redirect(f"/users/{new_user.user_id}")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/home/<int:user_id>")
def user_detail(user_id):
    """Show info for home app."""

    user = User.query.options(db.joinedload('users').joinedload('home_app')).get(user_id)
    return render_template("home_app.html", user=user)


@app.route("/community")
def user_list():
    """Show info for community app."""

    users = User.query.all()
    return render_template("community.html", users=users)


@app.route("/state_region")
def user_list():
    """Show infor for stat_region app."""

    users = User.query.all()
    return render_template("state_region.html", users=users)


@app.route("/nation")
def user_list():
    """Show info for nation app."""

    users = User.query.all()
    return render_template("nation.html", users=users)


@app.route("/global")
def user_list():
    """Show info for global app."""

    users = User.query.all()
    return render_template("global.html", users=users)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")