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

class User(db.Model):
    """Users in Tess system."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access_id'), nullable=False)
    one_time_password_id = db.Column(db.Integer, db.ForeignKey('one_time_password_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Users username={self.username} name={self.name}>"


class Admin_Access(db.Model):
    """List of codes for authorized access."""

    __tablename__ = "admin_access"

    admin_access_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    admin_access = db.Column(db.String(12), nullable=False)
    children = db.relationship('Users', 'Community_Resource,','State_Region_Resource', 
                               'National_Resource', 'Global_Resource')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Admin Code admin_access={self.admin_access}>"


class One_Time_Password(db.Model):
    """List of temporary one time passwords."""

    __tablename__ = "one_time_password"

    one_time_password_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    child = db.relationship('User')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<One Time Password password={self.password}>"


class Home_Resource(db.Model):
    """Links for Home App Resources."""

    __tablename__ = "home_resource"

    home_resource_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Home Resource name={self.name}>"


class Community(db.Model):
    """Communities in Tess system."""

    __tablename__ = "community"

    community_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    state_region_id = db.Column(db.Integer, db.ForeignKey('state_region_id'), nullable=False)
    name = db.Column(db.String(255))
    children = db.relationship('Home_Resource', 'Community_Resource', 'User', 'Community Event', \
                               'Community_Board_Post')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community name={self.name}>"


class Community_Board(db.Model):
    """List of Community Boards."""

    __tablename__ = "community_board"

    community_board_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    children = db.relationship('Community_Board_Post')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Board title={self.title}>"


class Community_Board_Post(db.Model):
    """List of Community Board Posts."""

    __tablename__ = "community_board_post"

    community_board_post_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    community_board_id = db.Column(db.Integer, db.ForeignKey('community_board_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(510), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Board Posts community_board_post_id={self.community_board_post_id} title={self.title}>"


class Community_Event(db.Model):
    """List of Community Events."""

    __tablename__ = "community_event"

    community_event_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    date_time = db.Column(db.DateTime)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(510), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Events community_event_id={self.one_time_password_id} title={self.title}>"


class Community_Resource(db.Model):
    """Links for Community Resources."""

    __tablename__ = "community_resource"

    community_resource_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""

         return f"<Community Resources community_resource_id={self.community_resource_id} name={self.name}>"

class State_Region(db.Model):
    """States and Regions in TESS system."""

    __tablename__ = "state_region"

    state_region_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    children = db.relationship('Community', 'State_Region_Resource')


    def __repr__(self):
         """Provide helpful representation when printed."""
         
         return f"<States & Regions state_region_id={self.state_region_id} name={self.name}>" 


class State_Region_Resource(db.Model):
    """Links for State and Region Resources."""

    __tablename__ = "state_region_resource"

    states_region_resource_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    states_region_id = db.Column(db.Integer, db.ForeignKey('state_region_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""
                  
         return f"<State & Region Resources state_region_resource_id={self.state_region_resource_id} name={self.name}>" 


class Nation(db.Model):
    """Nations in Tess system."""

    __tablename__ = "nation"

    nation_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    children = db.relationship('States_Regions', 'National_Resources')

    def __repr__(self):
         """Provide helpful representation when printed."""
                  
         return f"<Nations nation_id={self.nation_id} name={self.name}>" 


class National_Resource(db.Model):
    """Links for National Resources."""

    __tablename__ = "national_resource"

    national_resource_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
             
        return f"<National Resources national_resources_id={self.national_resources_id} name={self.name}>" 


class Global_Resource(db.Model):
    """Links for Global Resources."""

    __tablename__ = "global_resource"

    global_resource_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

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
