"""THE EARTH SAVE SYSTEM (TESS) PROJECT"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
"""from flask_debugtoolbar import DebugToolbarExtension"""

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
        one_time_password = request.form["one_time_password"]
        name = request.form["name"]
        new_password = request.form["password"]
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
    """Process login. Store user data in session."""

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

    user = User(username=username, password=password, admin_access=admin_access, community_id=community_id, name=name)
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

    user_id = User.query.options(db.joinedload('user').joinedload('community')).get(user_id)
    return render_template("home.html", user_id=user_id)


@app.route('/community', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events."""

    community_id = Community.query.get()
    return render_template("community.html", community_id=community_id)


@app.route('/state_region', methods=['GET'])
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news."""

    state_region_id = State_Region.query.get('state_id')
    return render_template("state_region.html", state_region_id=state_region_id)


@app.route('/nation', methods=['GET'])
def nation_detail():
    """Display national page with resource links daily CO2 and AIQ stats, and news."""

    nation_id = Nation.query.get('nation_id')
    return render_template("nation.html", nation_id=nation_id)


@app.route('/global', methods=['GET'])
def global_detail():
    """Display global page with resource links, daily CO2 and AIQ stats, and news."""

    global_resource_id = Global_Resource.query.one()
    return render_template("global.html", global_resource_id=global_resource_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    """DebugToolbarExtension(app)"""

    app.run(host="0.0.0.0")