"""DATA MODELS FOR TESS RPOJECT"""

from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions

db = SQLAlchemy()


class Nations(db.Model):
    """Nations"""

    __tablename__ = "nations"

    nation_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    nation_name = db.Column(db.String(255), nullable=False)

    def get_nation_by_id(nation_id):
        user_nation_name=Nations.query.get(nation_id)
        return user_nation_name

    def __repr__(self):     
         return f"<Nations nation_id={self.nation_id} name={self.nation_name}>" 


class State_Regions(db.Model):
    """States or Regions"""

    __tablename__ = "state_regions"

    state_region_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    nation_id = db.Column(db.Integer, db.ForeignKey('nations.nation_id'), nullable=False)
    state_region_name = db.Column(db.String(255), nullable=False)

    def get_state_region_by_id(state_region_id):
        user_state_region=State_Regions.query.get(state_region_id)
        return user_state_region

    def __repr__(self):
         return f"<States & Regions state_region_id={self.state_region_id} name={self.state_region_name}>" 


class Admin_Access(db.Model):
    """Administrative access codes"""

    __tablename__ = "admin_access"

    admin_access_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    admin_access_name = db.Column(db.String(24), nullable=False)

    def get_admin_access_by_id(admin_access_id):
        user_admin_access=Admin_Access.query.get(admin_access_id)
        return user_admin_access
    
    def __repr__(self):
        return f"<Admin Access admin_access_name={self.admin_access_name}>"


class Communities(db.Model):
    """Communities in the database"""

    __tablename__ = "communities"

    community_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    state_region_id = db.Column(db.Integer, db.ForeignKey('state_regions.state_region_id'), nullable=False)
    community_name = db.Column(db.String(255), nullable=False)

    def community_by_id(community_id):
        user_community_name=Communities.query.get(community_id)
        return user_community_name

    def __repr__(self):
        return f"<Community name={self.community_name}>"


class One_Time_Passwords(db.Model):
    """List of one-time-passwords"""

    __tablename__ = "one_time_passwords"

    one_time_password_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'), nullable=False)
    one_time_password_datetime = db.Column(db.DateTime, nullable=False)
    one_time_password = db.Column(db.String(32), nullable=False)

    def get_one_time_password_by_id(one_time_password_id):
        user_one_time_password=One_Time_Passwords.query.get(one_time_password_id)
        return user_one_time_password

    def __repr__(self):
        return f"<One Time Password password={self.one_time_password}>"


class Users(db.Model):
    """Users in the database"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    one_time_password_id = db.Column(db.Integer, db.ForeignKey('one_time_passwords.one_time_password_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(64), nullable=False)

    def get_state_region_nation_id(community_id):
        state_region_id=State_Regions.query.get(community_id)
        national_id=Nations.query.get(state_region_id)
        return state_region_id, national_id

    def __repr__(self):
        return f"<User username={self.username} password={self.password}>"


class Home_Resources(db.Model):
    """Home App Resource Links"""

    __tablename__ = "home_resources"

    home_resource_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'), nullable=False)
    home_resource_name = db.Column(db.String(64), nullable=False)
    home_resource_link = db.Column(db.String(255), nullable=False)

    def get_home_resource_links(user_id):
        home_resource_links = {}
        while Home_Resources.user_id == user_id:
            home_resource_links.append(Home_Resources.home_resource_name, Home_Resources.home_resource_link)
        return home_resource_links

    def __repr__(self):
        return f"<Home Resource name={self.home_resource_name}>"


class Community_Boards(db.Model):
    """Community Board Titles"""

    __tablename__ = "community_boards"

    community_board_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    community_board_title = db.Column(db.String(64), nullable=False)

    def get_community_board(community_board_id):
        user_community_board=Community_Boards.query.get(community_board_id)
        return user_community_board

    def __repr__(self):
        return f"<Community Board title={self.community_board_title}>"


class Community_Board_Posts(db.Model):
    """Community Board Posts"""

    __tablename__ = "community_board_posts"

    community_board_post_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'), nullable=False)
    community_board_id = db.Column(db.Integer, db.ForeignKey('community_boards.community_board_id'), nullable=False)
    community_board_post_datetime = db.Column(db.DateTime, nullable=False)
    community_board_post_title = db.Column(db.String(64), nullable=False)
    community_board_post_description = db.Column(db.String(510), nullable=False)

    def get_community_board_posts(community_id, community_board_post_id):
        user_community_board_posts = {}
        while Community_Board_Posts.community_id == community_id and \
              Community_Board_Posts.community_board_post_id == community_board_post_id:
              user_community_board_posts.append(Community_Board_Posts.community_board_post_title, \
                                                Community_Board_Posts.community_board_post_description)
        return user_community_board_posts

    def __repr__(self):
        return f"<Community Board Posts community_board_post_id={self.community_board_post_id} \
                 community_board_post_title={self.community_board_post_title}>"


class Community_Events(db.Model):
    """Community Events"""

    __tablename__ = "community_events"

    community_event_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'), nullable=False)
    community_event_datetime = db.Column(db.DateTime)
    community_event_title = db.Column(db.String(64), nullable=False)
    community_event_description = db.Column(db.String(500), nullable=False)
        
    def get_community_events(community_id):
        user_community_events= {}
        while Community_Events.community_id == community_id:
              user_community_events.append(Community_Events.community_event_title, \
              Community_Events.community_event_description)
        return user_community_events

    def __repr__(self):
        return f"<Community Events community_event_id={self.commmunity_event_id} \
                  commmunity_event_title={self.community_event_title}>"


class State_Region_Resources(db.Model):
    """State or Region Resource Links"""

    __tablename__ = "state_region_resources"

    state_region_resource_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    state_region_id = db.Column(db.Integer, db.ForeignKey('state_regions.state_region_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    state_region_resource_name = db.Column(db.String(64), nullable=False)
    state_region_resource_link = db.Column(db.String(255), nullable=False)
    
    def get_state_region_resource_links(state_region_id, admin_access_id):
        user_state_region_resource_links = {}
        while State_Region_Resources.state_region_id == state_region_id and \
              State_Region_Resources.admin_access_id == admin_access_id:
              user_state_region_resource_links.append(State_Region_Resources.state_region_resource_name, \
                                               State_Region_Resources.state_region_resource_link)
        return user_state_region_resource_links

    def __repr__(self):            
         return f"<State & Region Resources state_region_resource_id={self.state_region_resource_id} \
                                            state_region_resource_name={self.state_region_resource_name}>" 


class National_Resources(db.Model):
    """National Resource Links"""

    __tablename__ = "national_resources"

    national_resource_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    nation_id = db.Column(db.Integer, db.ForeignKey('nations.nation_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    national_resource_name = db.Column(db.String(64), nullable=False)
    national_resource_link = db.Column(db.String(255), nullable=False)
  
    def get_national_resource_links(national_id, admin_access_id):
        user_national_resource_links = {}
        while National_Resources.national_id == national_id and \
            National_Resources.admin_access_id == admin_access_id:
            user_national_resource_links.append(National_Resources.national_resource_name, \
                                           National_Resources.national_resource_link)
        return user_national_resource_links

    def __repr__(self):      
        return f"<National Resources national_resource_id={self.national_resource_id}\
                  national_resource_name={self.national_resource_name}>" 


class Global_Resources(db.Model):
    """Global Resource Links"""

    __tablename__ = "global_resources"

    global_resource_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    global_resource_name = db.Column(db.String(64), nullable=False)
    global_resource_link = db.Column(db.String(255), nullable=False)
        
    def get_global_resource_links(admin_access_id):
        user_global_resource_links = {}
        while Global_Resources.global_resource_id == admin_access_id:
            user_global_resource_links.append(Global_Resources.global_resource_name, \
                                         Global_Resources.global_resource_link)
        return user_global_resource_links

    def __repr__(self):           
        return f"<Global Resources global_resource_id={self.global_resource_id} \
                  global_resource_name={self.global_resource_name}>" 


    """CONNECT TO DATABASE"""

def connect_to_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://aeuiriruznhytf:f271469a21f44207c4806154efc00666af69e02b5b57c30058c6efdc5bded155@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d1c6vl2nchn4s5"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


    """MAIN"""

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
