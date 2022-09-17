"""THE EARTH SAVE SYSTEM (TESS)"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Admin_Access, One_Time_Passwords, Home_Resource, Communities, \
    Community_Resource, Community_Boards, Community_Board_Post, Community_Event, \
    State_Region, State_Region_Resource, Nation, National_Resource, Global_Resource

"""News & Climate APIs"""

guardian_url = ""
climatiq_url = ""


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Display homepage"""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Display form for user registraion"""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Add new user with valid one-time password. Store user in session."""

    one_time_password = request.form["one_time_password"]
    valid_one_time_password = Users.query.get(one_time_password)

    if valid_one_time_password:
        username = request.form["username"]
        name = request.form["name"]
        password= request.form["new_password"]
    else:
       flash(f"One time password not found.")
       return redirect("/register")

    new_user = Users(username=username, new_password=password, name=name)
    db.session.add(new_user)
    db.session.commit()
    flash(f"{name} added.")
    return redirect(f"/home/")


@app.route('/login', methods=['GET'])
def login_form():
    """Display login form"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Flask Login"""

    db.session.commit()

    flash("Logged in")
    return redirect(f"/home/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/home', methods=['GET'])
def home_detail(user_id):
    """Display home app page"""

    user_id = Users.query.options(db.joinedload('user').joinedload('home_resources')).get(user_id)
    return render_template("home.html", user_id=user_id)


@app.route('/community', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events. Access 
       community dbs and news & weather APIs."""

    community_id = Communities.query.get(community_id)
    return render_template("community.html")


@app.route('/state_region', methods=['GET'])
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news. Access 
       state_region dbs and news & weather APIs."""

    state_region_resource = {}
    state_region_resource = State_Region_Resource.query.all('state_region_id')
    return render_template("state_region.html")


@app.route('/nation', methods=['GET'])
def nation_detail():
    """Display national page with resource links daily CO2 and AIQ stats, and news. Access 
       national dbs and news & weather APIs"""

    nation_id = National_Resource.query.all('nation_id')
    return render_template("nation.html")


@app.route('/global', methods=['GET'])
def global_detail():
    """Display global page with resource links, daily CO2 and AIQ stats, and news. Access 
       global_resourc table and news & weather APIs"""

    return render_template("global.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")