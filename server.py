"""THE EARTH SAVE SYSTEM (TESS)"""

from ast import Global
from wsgiref import validate
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Admin_Access, One_Time_Passwords, Home_Resources, Communities, \
    Community_Resources, Community_Boards, Community_Board_Posts, Community_Events, \
    State_Regions, State_Region_Resources, Nations, National_Resources, Global_Resources

from flask_login import login_user, LoginManager, login_required, logout_user, current_user


"""News & Climate APIs

guardian_url = GUARDIAN_URL
climatiq_url = CLIMATIQ_URL

from theguardian import theguardian_content

news_content = theguardian_content.Content(api='test', url=GUARDIAN_URL)

news_content_response = news_content.get_content_response()
print(news_content_response)


from climatiq:

curl --request GET 
    --url 'https://beta3.api.climatiq.io/search?query=category&region' 
    --header 'Authorization: Bearer CLIMATIQ_API_KEY'
"""

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

"""Flask Login"""

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(alternative_id=user_id).first()

@app.route('/')
def welcome():
    """ Display welcomepage"""

    return render_template("welcomepage.html")


@app.route('/register',  methods=['GET'])
def register():
    """ Display Register Form"""

    return render_template("register.html")


@app.route('/register', methods=['POST'])
def add_new_user():
    """Add new user with valid one-time-password"""

    admin_access = ''
    one_time_password = request.form["one_time_password"]
    valid_one_time_password = One_Time_Passwords.query.get(one_time_password, admin_access)
    admin_access_id = Admin_Access.query.get(admin_access)

    if one_time_password == valid_one_time_password:
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["new_password"]
    else:
       flash(f"Please register")
       return redirect("/register")

    new_user = Users(username=username, password=password, name=name, admin_access_id=admin_access_id)
    db.session.add(new_user)
    db.session.commit()
    flash(f"{name} added")
    return render_template("welcomepage.html")


@app.route('/login', methods=['GET', 'POST'])
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
        flash(f"Please register")
        return redirect("/register")


@app.route('/home', methods=['GET', 'POST'])
def home_detail(user_id):
    """Display home app page"""

    community_resources = {}
    home_resources = {}

    user_id = Users.query.get(user_id)
    community_id = Users.query.get(community_id)
    admin_access_id = Users.query.get(admin_access_id)

    if Users.user_resources:
       for i in Home_Resources:
           home_resources[i] = Home_Resources.query.filter_by(user_id)
           db.session.add(home_resources)
    else:
        for i in community_resources:
            community_resources[i] = Community_Resources.query.filter_by(community_id, admin_access_id)
            db.session.add(community_resources)

    db.session.commit()
    return render_template("home.html")


@app.route('/communities', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events. Access 
       community dbs and news & weather APIs."""

    community_resources = {}
    community_events = {}
    community_name = ' '
    admin_access_id = Users.query.get(admin_access_id)

    community_id = Users.query.get(community_id)
    community_name = Communities.query.get(community_name)

    for i in community_resources:
        community_resources[i] = Community_Resources.query.filter_by(community_id, admin_access_id)
        db.session.add(community_resources)
    for i in community_events:
        community_events[i] = Community_Events.query.filter_by(community_id)

    db.session.add(community_resources, community_events, community_name)
    db.session.commit()
    return render_template("community.html")


@app.route('/communityboard', methods=['GET'])
def community_board():
    """Display community board and posts"""

    community_board_posts = {}
    community_board_name = ' '

    community_id = Users.query.get(community_id)
    community_board_name = Community_Boards.query.get(community_board_name)

    for i in community_board_posts:
        community_board_posts[i] = Community_Board_Posts.query.filter_by(community_id)
        db.session.add(community_board_posts)

    db.session.add(community_board_posts, community_board_name)
    db.session.commit()
    return render_template("community_board.html")


@app.route('/state_region', methods=['GET'])
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news. Access 
       state_region dbs and news & weather APIs."""

    state_region_resources = {}
    state_region_name = ' '
    admin_access_id = Users.query.get(admin_access_id)

    state_region_name = State_Regions.query.get(state_region_name)

    for i in state_region_resources:
        state_region_resources[i] = State_Region_Resources.query.filter_by(state_region_name, admin_access_id)

    db.session.add(state_region_resources, state_region_name)
    db.session.commit()
    return render_template("state_region.html")


@app.route('/nation', methods=['GET'])
def nation_detail():
    """Display national page with resource links daily CO2 and AIQ stats, and news. Access 
       national dbs and news & weather APIs"""

    national_resources = {}
    nation_name = ' '

    nation_name = Nations.query.get(nation_name)
    admin_access_id = Users.query.get(admin_access_id)

    for i in national_resources:
        national_resources = National_Resources.query.all(admin_access_id)

    db.session.add(national_resources, nation_name)
    db.session.commit()
    return render_template("nation.html")


@app.route('/global', methods=['GET'])
def global_detail():
    """Display global page with resource links, daily CO2 and AIQ stats, and news. Access 
       global_resourc table and news & weather APIs"""

    global_resources= {}
    admin_access_id = Users.query.get(admin_access_id)
    
    for i in global_resources:
        global_resources = Global_Resources.query.all(admin_access_id)

    db.session.add(global_resources)
    db.session.commit()
    return render_template("global.html")


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged Out", "error")
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension. Do not debug for demo

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
    