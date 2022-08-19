"""Models and database functions for Tess project."""

from ast import Global
from turtle import title
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class Users(db.Model):
    """Users in Tess system."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code_id'), nullable=False)
    one_time_password_id = db.Column(db.Integer, db.ForeignKey('one_time_password_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Users username={self.username} name={self.name}>"


class Access_Codes(db.Model):
    """List of codes for authorized access."""

    __tablename__ = "access_codes"

    access_code_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    code = db.Column(db.String(12), nullable=False)
    children = db.relationship('Users', 'Community_Resources,','State_Region_Resources', 
                               'National_Resources', 'Global_Resources')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Code access_code_id={self.access_code_id} code={self.code}>"


class One_Time_Passwords(db.Model):
    """List of temporary one time passwords."""

    __tablename__ = "one_time_passwords"

    one_time_password_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    child = db.relationship('Users')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<One Time Password one_time_password_id={self.one_time_password_id} password={self.password}>"


class Home_Resources(db.Model):
    """Links for Home App Resources."""

    __tablename__ = "home_resources"

    home_resource_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Home Resources home_resource_id={self.home_resource_id} name={self.name}>"


class Communities(db.Model):
    """Communities in Tess system."""

    __tablename__ = "communities"

    community_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    name = db.Column(db.String(255))
    state_region_id = db.Column(db.Integer, db.ForeignKey('state_region_id'), nullable=False)
    children = db.relationship('Home_Resources', 'Community_Resources', 'Users', 'Community Evens', \
                               'Community_Board_Posts')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Communities community_id={self.community_id} name={self.name}>"


class Community_Boards(db.Model):
    """List of Community Boards."""

    __tablename__ = "community_boards"

    community_board_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    children = db.relationship('Community_Board_Posts')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Boards community_board_id={self.community_board_id} title={self.title}>"


class Community_Board_Posts(db.Model):
    """List of Community Board Posts."""

    __tablename__ = "community_board_posts"

    community_board_post_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    community_board_id = db.Column(db.Integer, db.ForeignKey('community_board_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Board Posts community_board_post_id={self.community_board_post_id} title={self.title}>"


class Community_Events(db.Model):
    """List of Community Events."""

    __tablename__ = "community_events"

    community_event_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    date_time = db.Column(db.DateTime)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Events community_event_id={self.one_time_password_id} title={self.title}>"


class Community_Resources(db.Model):
    """Links for Community Resources."""

    __tablename__ = "community_resources"

    community_resource_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""

         return f"<Community Resources community_resource_id={self.community_resource_id} name={self.name}>"

class States_Regions(db.Model):
    """States and Regions in TESS system."""

    __tablename__ = "states_regions"

    state_region_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nations_id = db.Column(db.Integer, db.ForeignKey('nation_id'), nullable=False)
    children = db.relationship('Communities', 'State_Region_Resources')


    def __repr__(self):
         """Provide helpful representation when printed."""
         
         return f"<States & Regions state_region_id={self.state_region_id} name={self.name}>" 


class State_Region_Resources(db.Model):
    """Links for State and Region Resources."""

    __tablename__ = "states_regions_resources"

    states_region_resource_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    states_region_id = db.Column(db.Integer, db.ForeignKey('state_region_id'), nullable=False)
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""
                  
         return f"<State & Region Resources state_region_resource_id={self.state_region_resource_id} name={self.name}>" 


class Nations(db.Model):
    """Nations in Tess system."""

    __tablename__ = "nations"

    nations_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    children = db.relationship('States_Regions', 'National_Resources')

    def __repr__(self):
         """Provide helpful representation when printed."""
                  
         return f"<Nations nation_id={self.nation_id} name={self.name}>" 


class National_Resources(db.Model):
    """Links for National Resources."""

    __tablename__ = "national_resources"

    national_resource_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    nations_id = db.Column(db.Integer, db.ForeignKey('nation_id'), nullable=False)
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
             
        return f"<National Resources national_resources_id={self.national_resources_id} name={self.name}>" 


class Global_Resources(db.Model):
    """Links for Global Resources."""

    __tablename__ = "global_resources"

    global_resource_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
                 
        return f"<Global Resources global_resource_id={self.global_resource_id} name={self.name}>" 

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
