"""THE EARTH SAVE SYSTEM (TESS)"""

from asyncio.windows_events import NULL
from unicodedata import name
from unittest import result
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, One_Time_Passwords, Home_Resources, Communities, Community_Boards, \
     Community_Board_Posts, Community_Events, State_Regions, State_Region_Resources, National_Resources, \
     Nations, Global_Resources


"""NEWS & CLIMATE APIS"""

"""guardian_url = GUARDIAN_URL
climatiq_url = CLIMATIQ_URL

from theguardian import theguardian_content

news_content = theguardian_content.Content(api='test', url=GUARDIAN_URL)

news_content_response = news_content.get_content_response()
print(news_content_response)"""


"""from Climatiq:

curl --request GET 
    --url 'https://beta3.api.climatiq.io/search?query=category&region' 
    --header 'Authorization: Bearer CLIMATIQ_API_KEY'
"""

"""CREATE APP"""

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


"""ROUTES/FUNCTIONS"""

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

    try:
        if request.method == 'POST':
            one_time_password = request.form["one_time_password"]
            valid_one_time_password = One_Time_Passwords.query.filter_by(one_time_password=one_time_password).first()
            if one_time_password == valid_one_time_password:
                username = request.form["username"]
                name = request.form["name"]
                password = request.form["new_password"]      
                user = Users(username=username, password=password, name=name)
                db.session.add(user)
                db.session.commit()
                flash(f"{{ name }} registered!")
                return render_template("welcomepage.html")
    except Exception:
           flash(f"Invalid one-time-password!")
           return redirect("/register")
    else:
        flash(f"Please register!")
        return redirect("/register")


@app.route('/login', methods=['GET'])
def display_login():
    """Display Login Form"""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def process_login():
    """Login"""

    try:
        if request.method == 'POST':
            username = request.form["username"]
            password = request.form["password"]
            user = Users.query.filter_by(username=username).first()
            if user:
               password_check = password == user.password
               if password_check:
                    community_id = user.community_id
                    admin_access_id = user.admin_access_id
                    session["username"] = username
                    session["password"] = password
                    session["community_id"] = community_id
                    session["admin_access_id"] = admin_access_id
                    print(username, password, community_id, admin_access_id)
                    flash('Logged in!')
                    return render_template("welcomepage.html")
    except Exception:
        flash('Invalid Login!')
        return redirect('/login')
    else:
        flash('Please register!')
        return redirect('/register')


@app.route("/home", methods=['GET']) 
def home_detail():
    """Display home app page"""
    
    try:
        home_resources = {}
        community_id = session["community_id"]
        for i in Home_Resources.query.filter_by(community_id=community_id).all():
              home_resources[i.home_resource_name] = i.home_resource_link
    except Exception:
        flash('Error!')

    print(home_resources)

    return render_template("home.html", home_resources=home_resources)


@app.route('/community', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events"""

    try:
        user_community_events = {}
        community_id = session["community_id"]
        community_name = Communities.query.filter_by(community_id=community_id).first()
        print(community_id, community_name)
        for i in Community_Events.query.filter_by(community_id=community_id).all():
              user_community_events[i.community_event_title] = i.community_event_link
              print(user_community_events)
    except Exception:
        flash('Error!')
    
    try:
        user_community_boards = {}
        community_id = session["community.id"]
        for i in Community_Boards.query.filter_by(community_id=community_id).all():
              user_community_boards[i.community_board_title] = i.community_board_link
    except Exception:
        flash('Error!')

    return render_template("community.html", user_community_events=user_community_events, \
                            user_community_boards=user_community_boards, community_name=community_name)


@app.route('/communityboard', methods=['GET'])
def community_board():
    """Display community board and posts"""

    try:
        user_community_board_posts = {}
        community_name = session["community_id"]
        for i in Community_Board_Posts.query.filter_by(community_name=community_name).add():
              user_community_board_posts[i.community_board_post_title] = i.community_board_post_description
    except Exception:
        flash('Error!')

    return render_template("community_board.html", user_community_board_posts=user_community_board_posts)


@app.route('/state_region', methods=['GET']) 
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news"""

    try:
        user_state_region_resources = {}
        state_region_name = " "
        state_region_id = session["state_region_id"]
        admin_access_id = session["admin_access_id"]
        state_region_name = State_Regions.query.filter_by(state_region_id=state_region_id).first()
        for i in State_Region_Resources.query.filter_by(state_region_id=state_region_id, \
                                                        admin_access_id=admin_access_id).all():
              user_state_region_resources[i.state_region_resource_name] = i.state_region_resource_link
    except Exception:
        flash('Error!')

    return render_template("state_region.html", user_state_region_resources=user_state_region_resources, \
                            state_region_name=state_region_name)


@app.route('/nation', methods=['GET'])
def nation_detail():
    """Display national page with resource links daily CO2 and AIQ stats and news"""

    try:
        user_national_resources = {}
        nation_name = " "
        admin_access_id = session["admin_access_id"]
        nation_id = session["nation_id"]
        nation_name = Nations.query.filter_by(nation_id=nation_id).first()
        user_nation = National_Resources.query.filter_by(nation_id=nation_id).first()
        for i in National_Resources.query.filter_by(admin_access_id=admin_access_id, nation_id=nation_id).all():
              user_national_resources[i.national_resource_name] = i.national_resource_link
    except Exception:
        flash('Error!')

    return render_template("nation.html", user_national_resources=user_national_resources, nation_name=nation_name)


@app.route('/global', methods=['GET'])
def global_detail():
    """Display global page with resource links, daily CO2 and AIQ stats and news"""

    try:
        user_global_resources = {}
        admin_access_id = session["admin_access_id"]
        for i in Global_Resources.query.filter_by(admin_access_id).all():
              user_global_resources[i.global_resource_name] = i.global_resource_link
    except Exception:
        flash('Error!')

    return render_template("global.html", user_global_resources=user_global_resources)


@app.route('/logout')
def logout():
    """Log Out"""

    if "username" in session:
        del session["username"]
        flash(f"Logged Out!")
    return redirect("/")


"""MAIN"""

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension. Do not debug for demo

    app.debug = False

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
    