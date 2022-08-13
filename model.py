"""Models and database functions for Tess project."""

from ast import Global
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
    communities_id = db.Column(db.Integer, db.ForeignKey('communities_id'), nullable=False)
    access_codes_id = db.Column(db.Integer, db.ForeignKey('access_codes_id'), nullable=False)
    one_time_password_id = db.Column(db.Integer, db.ForeignKey('one_time_passwords_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} username={self.username}>"


class Access_Codes(db.Model):
    """List of codes for authorized access."""

    __tablename__ = "access_codes"

    access_codes_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    code = db.Column(db.String(12), nullable=False)
    children = db.relationship('Users', 'Community_Resources,','State_Region_Resources', 
                               'National_Resources', 'Global_Resources')
    

    def __repr__(self):
        """Provide helpful representation when printed."""


class One_Time_Passwords(db.Model):
    """List of temporary one time passwords."""

    __tablename__ = "one_time_passwords"

    one_time_passwords_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    children = db.relationship('Users')
    

    def __repr__(self):
        """Provide helpful representation when printed."""


class Home_Resources(db.Model):
    """Links for Home App Resources."""

    __tablename__ = "home_resources"

    home_resources_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""


class Communities(db.Model):
    """Communities in Tess system."""

    __tablename__ = "communities"

    communities_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    name = db.Column(db.String(255))
    state_regions_id = db.Column(db.Integer, db.ForeignKey('state_regions_id'), nullable=False)
    children = db.Relationship('Home_Resources', 'Community_Resources', 'Users', 'Community Evens', \
                               'Community_Board_Posts')


    def __repr__(self):
        """Provide helpful representation when printed."""


class Community_Boards(db.Model):
    """List of Community Boards."""

    __tablename__ = "community_boards"

    community_boards_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    children = db.Relationship('Community_Board_Posts')


    def __repr__(self):
        """Provide helpful representation when printed."""


class Community_Board_Posts(db.Model):
    """List of Community Board Posts."""

    __tablename__ = "community_board_posts"

    community_board_posts_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    communities_id = db.Column(db.Integer, db.ForeignKey('communities_id'), nullable=False)
    community_boards_id = db.Column(db.Integer, db.ForeignKey('community_boards_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""


class Community_Events(db.Model):
    """List of Community Events."""

    __tablename__ = "community_events"

    community_events_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    date_time = db.Column(db.DateTime)
    communities_id = db.Column(db.Integer, db.ForeignKey('communities_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    

    def __repr__(self):
        """Provide helpful representation when printed."""


class Community_Resources(db.Model):
    """Links for Community Resources."""

    __tablename__ = "community_resources"

    community_resources_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    communities_id = db.Column(db.Integer, db.ForeignKey('communities_id'), nullable=False)
    access_codes_id = db.Column(db.Integer, db.ForeignKey('access_codes_id'), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""

class States_Regions(db.Model):
    """States and Regions in TESS system."""

    __tablename__ = "states_regions"

    state_regions_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nations_id = db.Column(db.Integer, db.ForeignKey('nations_id'), nullable=False)
    children = db.Relationship('Communities', 'State_Region_Resources')


    def __repr__(self):
         """Provide helpful representation when printed."""


class State_Region_Resources(db.Model):
    """Links for State and Region Resources."""

    __tablename__ = "states_regions_resources"

    states_regions_resources_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    states_regions_id = db.Column(db.Integer, db.ForeignKey('states_regions_id'), nullable=False)
    access_codes_id = db.Column(db.Integer, db.ForeignKey('access_codes_id'), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""


class Nations(db.Model):
    """Nations in Tess system."""

    __tablename__ = "nations"

    nations_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    children = db.Relationship('States_Regions', 'National_Resources')

    def __repr__(self):
         """Provide helpful representation when printed."""


class National_Resources(db.Model):
    """Links for National Resources."""

    __tablename__ = "national_resources"

    national_resources_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    nations_id = db.Column(db.Integer, db.ForeignKey('nations_id'), nullable=False)
    access_codes_id = db.Column(db.Integer, db.ForeignKey('access_codes_id'), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""


class Global_Resources(db.Model):
    """Links for Global Resources."""

    __tablename__ = "global_resources"

    global_resources_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    access_codes_id = db.Column(db.Integer, db.ForeignKey('access_codes_id'), nullable=False)
    links = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

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
