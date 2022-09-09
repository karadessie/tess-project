"""THE EARTH SAVE SYSTEM (TESS)"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session

"""News & Climate APIs"""
guardian_url = ""
climatiq_url = ""

from model import connect_to_db, db, User, Admin_Access, One_Time_Password, Home_Resource, Community, \
    Community_Resource, Community_Board, Community_Board_Post, Community_Event, \
    State_Region, State_Region_Resource, Nation, National_Resource, Global_Resource

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Display homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Display form for new user registraion."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Add new user with valid one-time password. Store user data in session."""

    one_time_password = request.form["one_time_password"]
    valid_one_time_password = User.query.get(one_time_password)

    if valid_one_time_password:
        username = request.form["username"]
        name = request.form["name"]
        password= request.form["new_password"]
    else:
       flash(f"One time password not found.")
       return redirect("/register")

    new_user = User(username=username, new_password=password, admin_access=admin_access, \
                    community_id=community_id, name=name)
    db.session.add(new_user)
    db.session.commit()
    flash(f"{name} added.")
    return redirect(f"/home/{new_user.user_id}")


@app.route('/login', methods=['GET'])
def login_form():
    """Display login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Flask Login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.get(username=username, password=password)

    if not user:
        flash("User not found")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    user = User(user_id=user_id, admin_access=admin_access, community_id=community_id, name=name)
    db.session.add(user)
    db.session.commit()

    flash("Logged in")
    return redirect(f"/home/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/home', methods=['GET'])
def home_detail(user_id):
    """Display home app page with default or customized resource links."""

    user_id = User.query.options(db.joinedload('user').joinedload('home_resources')).get(user_id)
    return render_template("home.html", user_id=user_id)


@app.route('/community', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events. Access 
       community dbs and news & weather APIs."""

    community_id = Community.query.get(community_id)
    return render_template("community.html")


@app.route('/state_region', methods=['GET'])
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news. Access 
       state_region dbs and news & weather APIs."""

    state_region_resource = {}
    state_region_resources = State_Region_Resource.query.all('state_region_id')
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

    # Use the DebugToolbar
    """DebugToolbarExtension(app)"""

    app.run(host="0.0.0.0")