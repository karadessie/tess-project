"""DATA MODELS FOR TESS RPOJECT"""

from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

db = SQLAlchemy()

class NewsdataException(Exception):
    """Base class for all other exceptions"""

    def __init__(self, Error):
        self.Error = Error

class Nations(db.Model):
    """Nations"""

    __tablename__ = "nations"

    nation_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    nation_name = db.Column(db.String(64), nullable=False)

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

    def get_nation_by_id(state_region_id):
        nation_id=Nations.query.filter_by(state_region_id).first()
        return nation_id

    def __repr__(self):
         return f"<States & Regions state_region_id={self.state_region_id} name={self.state_region_name}>" 


class Admin_Access(db.Model):
    """Administrative access codes"""

    __tablename__ = "admin_access"

    admin_access_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    admin_access_name = db.Column(db.String(24), nullable=False)
    
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
    
    def get_state_region_by_id(community_id):
        state_region_id=State_Regions.query.filter_by(community_id).first()
        return state_region_id

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

    def __repr__(self):
        return f"<User username={self.username} password={self.password}>"


class Home_Resources(db.Model):
    """Home App Resource Links"""

    __tablename__ = "home_resources"

    home_resource_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    home_resource_name = db.Column(db.String(64), nullable=False)
    home_resource_link = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Home Resource name={self.home_resource_name}>"


class Community_Board_Posts(db.Model):
    """Community Board Posts"""

    __tablename__ = "community_board_posts"

    community_board_post_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'), nullable=False)
    community_board_title = db.Column(db.String(32), nullable=False)
    community_board_post_datetime = db.Column(db.DateTime, nullable=False)
    community_board_post_title = db.Column(db.String(64), nullable=False)
    community_board_post_description = db.Column(db.String(125), nullable=False)

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
    community_event_description = db.Column(db.String(255), nullable=False)

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
