"""THE EARTH SAVE SYSTEM (TESS)"""

from ast import Global
from asyncio.windows_events import NULL
from wsgiref import validate
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, One_Time_Passwords, Home_Resources, Community_Boards, \
     Community_Board_Posts, Community_Events, State_Region_Resources, National_Resources, Global_Resources


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
            username = request.form['username']
            password = request.form['password']
            user = Users.query.filter_by(username=username).first()
            if user:
               password_check = password == user.password
               if password_check:
                    flash('Logged in!')
                    return render_template("welcomepage.html", user=user)
    except Exception:
        flash('Invalid Login Credentials!')
        return redirect('/login')
    else:
        flash('Please register!')
        return redirect('/register')


@app.route('/home', methods=['GET']) 
def home_detail():
    """Display home app page"""

    Home_Resources.get_home_resource_links(Users.user_id)

    return render_template("home.html")


@app.route('/communities', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events"""

    user_community_events = {}
    while Community_Events.community_id == Users.community_id:
              user_community_events.append(Community_Events.community_event_title, \
              Community_Events.community_event_description)
    
    user_community_boards = {}
    while Community_Boards.community_id == Users.community_id:
              user_community_boards.append(Community_Events.community_event_title, \
              Community_Events.community_event_description)

    return render_template("community.html", user_community_events, user_community_boards)


@app.route('/communityboard', methods=['GET'])
def community_board():
    """Display community board and posts"""

    user_community_board_posts = {}
    while Community_Board_Posts.community_id == Users.community_id:
              user_community_board_posts.append(Community_Board_Posts.community_board_post_title, \
              Community_Board_Posts.community_board_post_description)

    return render_template("community_board.html", user_community_board_posts)


@app.route('/state_region', methods=['GET']) 
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news"""
  
    Users.get_state_region_nation_id(Users.community_id)
    State_Region_Resources.get_state_region_resource_links(Users.admin_access_id)

    user_state_region_resources = {}
    while State_Region_Resources.community_id == Users.community_id:
              user_state_region_resources.append(State_Region_Resources.state_region_resource_name, \
              State_Region_Resources.state_region_resource_link)

    return render_template("state_region.html", user_state_region_resources)


@app.route('/nation', methods=['GET'])
def nation_detail():
    """Display national page with resource links daily CO2 and AIQ stats and news"""

    user_national_resources = {}
    while National_Resources.community_id == Users.community_id:
              user_national_resources.append(National_Resources.national_resource_name, \
              National_Resources.national_resource_link)

    return render_template("nation.html", user_national_resources)


@app.route('/global', methods=['GET'])
def global_detail():
    """Display global page with resource links, daily CO2 and AIQ stats and news"""

    user_global_resources = {}
    while Global_Resources.admin_access_id == Users.admin_access_id:
              user_global_resources.append(Global_Resources.global_resource_name, \
              Global_Resources.global_resource_link)

    return render_template("global.html", user_global_resources)


@app.route('/logout')
def logout():
    """Log Out"""

    flash(f"Logged Out!")
    return redirect("/")


"""MAIN"""

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension. Do not debug for demo

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
    