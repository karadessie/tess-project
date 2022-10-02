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

    if request.method == 'POST':
        one_time_password = request.form["one_time_password"]
        valid_one_time_password = One_Time_Passwords.query.filter_by(one_time_password=one_time_password).first
        if one_time_password == valid_one_time_password:
            username = request.form["username"]
            name = request.form["name"]
            password = request.form["new_password"]
            flash(f"{{ name }} registered!")
        else:
           flash(f"Invalid password!")
           return redirect("/register")
    else:
        flash(f"Please register!")
        return redirect("/register")
    

    user = Users(username=username, password=password, name=name)
    db.session.add(user)
    db.session.commit()
    flash(f"{name} added")
    return render_template("welcomepage.html")


@app.route('/login', methods=['GET'])
def display_login():
    """Display Login Form"""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def process_login():
    """Login"""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usersignin = [username, password]
        userdata = Users.query.filter_by(username=username, password=password)
        if usersignin == userdata:
            user_id = Users.query.filter_by(username)
            community_id = Users.query.filter_by(user_id)
            admin_access_id = Users.query.filter_by(user_id)
            user_name = Users.query.filter_by(user_id)
            user=(user_id, username, password, admin_access_id, community_id, user_name)
            db.session.add(user)
            db.session.commit()
            flash('Logged in!')
            return redirect('/')
        else:
            flash('Please log in!')
            return redirect('/login')


@app.route('/home', methods=['GET']) 
def home_detail():
    """Display home app page"""

    Home_Resources.get_home_resource_links(session.user_id)

    return render_template("home.html")


@app.route('/communities', methods=['GET'])
def community_detail():
    """Display community page with community boards, daily CO2 and AIQ stats, news, and events"""

    Community_Events.get_community_events(session.community_id)
    Community_Boards.get_community_boards(session.community_id)

    return render_template("community.html")


@app.route('/communityboard', methods=['GET'])
def community_board():
    """Display community board and posts"""

    Community_Board_Posts.get_community_board_posts(session.community_id)

    return render_template("community_board.html")


@app.route('/state_region', methods=['GET']) 
def state_region_detail():
    """Display state/region page with resource links, daily CO2 and AIQ stats, and news"""

    
    Users.get_state_region_nation_id(session.community_id)
    State_Region_Resources.get_state_region_resource_links(session.admin_access_id)

    return render_template("state_region.html")


@app.route('/nation', methods=['GET'])
def nation_detail():
    """Display national page with resource links daily CO2 and AIQ stats and news"""

    
    Users.get_state_region_nation_id(session.community_id)
    National_Resources.get_national_resource_links(session.admin_access_id)

    return render_template("nation.html")


@app.route('/global', methods=['GET'])
def global_detail():
    """Display global page with resource links, daily CO2 and AIQ stats and news"""

    Global_Resources.get_global_resource_links(session.admin_access_id)

    return render_template("global.html")


@app.route('/logout')
def logout(user_id):
    """Log Out"""

    if username:
        try:
            username = Users.query.get(user_id)
            db.session.delete(username)       
            flash("Logged out!")
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return redirect("/")


"""MAIN"""

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension. Do not debug for demo

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
    