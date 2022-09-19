"""THE EARTH SAVE SYSTEM (TESS)"""

from ast import Global
from wsgiref import validate
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Admin_Access, One_Time_Passwords, Home_Resources, Communities, \
    Community_Resources, Community_Boards, Community_Board_Post, Community_Event, \
    State_Region, State_Region_Resources, Nation, National_Resources, Global_Resources

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


"""News & Climate APIs

guardian_url = GUARDIAN_URL
climatiq_url = CLIMATIQ_URL

from theguardian import theguardian_content

content = theguardian_content.Content(api='test', url=GUARDIAN_URL)

content_response = content.get_content_response()
print(content_response)
"""

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

"""Flask Login"""

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


@app.route('/')
def welcome():
    """ Display welcomepage"""

    return render_template("welcomepage.html")


@app.route('/register', methods=['GET'])
def add_new_user():
    """Add new user with valid one-time-password"""

    one_time_password = request.form["one_time_password"]
    valid_one_time_password = Users.query.get(one_time_password)

    if one_time_password == valid_one_time_password:
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["new_password"]
    else:
       flash(f"Please enter username & one-time-password")
       return redirect("/register")

    new_user = Users(username=username, password=password, name=name)
    db.session.add(new_user)
    db.session.commit()
    flash(f"{name} added")
    return render_template("welcomepage.html")


@app.route('/login')
def login():
    """Flask Login"""

    if login_required:
        return render_template("login.html")

    login_username = request.form["username"]
    login_password = request.form["password"]
    user = Users.query.one_or_none(username=login_username, password=login_password)
    if user:
        login_user(user)
        db.session.add(user)
        db.session.commit()
        flash(f"Login Successful")
        return render_template("welcomepage.html")
    else:
        flash(f"Login Unsuccessful")
        return render_template("login.html")


@app.route('/home', methods=['GET'])
def home_detail(user_id):
    """Display home app page"""

    community_resources = {}
    home_resources = {}

    user_id = Users.query.get(user_id)
    community_id = Users.query.get(community_id)

    if Users.user_resources:
       for i in Home_Resources:
           home_resources[i] = Home_Resources.query.filter_by(user_id)
           db.session.add(home_resources)
    else:
        for i in community_resources:
            community_resources[i] = Community_Resources.query.filter_by(community_id)
            db.session.add(community_resources)

    db.session.commit()
    return render_template("home.html", user_id=user_id)


@app.route('/community', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events. Access 
       community dbs and news & weather APIs."""

    community_resources = {}
    community_events = {}

    community_id = Users.query.get(community_id)
    for i in community_resources:
        community_resources[i] = Community_Resources.query.filter_by(community_id)
        db.session.add(community_resources)
    for i in community_events:
        community_events[i] = Community_Event.query.filter_by(community_id)

    db.session.add(community_resources, community_events)
    db.session.commit()
    return render_template("community.html")


@app.route('/state_region', methods=['GET'])
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news. Access 
       state_region dbs and news & weather APIs."""

    state_region_resources = {}
    for i in state_region_resources:
        state_region_resources[i] = State_Region_Resources.query.filter_by(state_region_id)
        db.session.add(state_region_resources)
    
    db.session.commit()
    return render_template("state_region.html")


@app.route('/nation', methods=['GET'])
def nation_detail():
    """Display national page with resource links daily CO2 and AIQ stats, and news. Access 
       national dbs and news & weather APIs"""

    national_resources = {}

    for i in national_resources:
        national_resources[i] = National_Resources.query.all(nation_id)
        db.session.add(national_resources)

    db.session.commit()
    return render_template("nation.html")


@app.route('/global', methods=['GET'])
def global_detail():
    """Display global page with resource links, daily CO2 and AIQ stats, and news. Access 
       global_resourc table and news & weather APIs"""

    global_resources= {}
    
    for i in global_resources:
        global_resources[i] = Global_Resources.query.all


    db.session.add(global_resources)
    
    db.session.commit()
    return render_template("global.html")

@app.route('/logout')
def logout():
    logout_user()
    flash("Logged Out")
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")