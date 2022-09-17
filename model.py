"""Data Models for TESS Project"""
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

from flask_login import UserMixin, login_user, LoginManager, login_required, login_user, current_user

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    """Users in the database"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access_id'), nullable=False)
    one_time_password_id = db.Column(db.Integer, db.ForeignKey('one_time_password_id'), nullable=False)

    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the user_id to satisfy Flask-Login's requirements."""
        return self.user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Users username={self.username} name={self.name}>"
        

class Admin_Access(db.Model):
    """List of administrative access codes"""

    __tablename__ = "admin_access"

    admin_access_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    admin_access = db.Column(db.String(12), nullable=False)
    users = db.relationship('Users', backref=db.backref("Users"))
    community_resource = db.relationship('Community_Resource', backref=db.backref("Community_Resource"))
    state_region_resource = db.relationship('State_Region_Resource', backref=db.backref("State_Region_Resource"))
    national_resource = db.relationship('National_Resource', backref=db.backref("National_Resource"))
    global_resource = db.relationship('Global_Resource', backref=db.backref("Global_Resource"))

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Admin Code admin_access={self.admin_access}>"


class One_Time_Passwords(db.Model):
    """List of temporary one-time-passwords"""

    __tablename__ = "one_time_password"

    one_time_password_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community_id'), nullable=False)
    user = db.relationship('Users', backref=db.backref("Users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<One Time Password password={self.password}>"


class Home_Resource(db.Model):
    """Links for Home App Resources"""

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


class Communities(db.Model):
    """Communities in the database"""

    __tablename__ = "community"

    community_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    state_region_id = db.Column(db.Integer, db.ForeignKey('state_region_id'), nullable=False)
    name = db.Column(db.String(255))
    home_resource = db.relationship('Home_Resource', backref=db.backref("Home_Resource"))
    community_resource = db.relationship('Community_Resource', backref=db.backref("Community_Resource"))
    community_event = db.relationship('Community_Event', backref=db.backref("Community_Event"))
    community_board_post = db.relationship('Community_Board_Post', backref=db.backref("Community_Board_Post"))
    user = db.relationship('Users', backref=db.backref("Users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community name={self.name}>"


class Community_Boards(db.Model):
    """List of Community Board Names"""

    __tablename__ = "community_board"

    community_board_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    community_board_post = db.relationship('Community_Board_Post', backref=db.backref("Community_Board_Post"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Board title={self.title}>"


class Community_Board_Post(db.Model):
    """List of Community Board Posts"""

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
    """List of Community Events"""

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
    """Links for Community Resources"""

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
    """States or Regions in the database"""

    __tablename__ = "state_region"

    state_region_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    community = db.relationship('Communities', backref=db.backref("Communities"))
    state_region_resource = db.relationship('State_Region Resource', backref=db.backref("State_Region_Resource"))

    def __repr__(self):
         """Provide helpful representation when printed."""
         
         return f"<States & Regions state_region_id={self.state_region_id} name={self.name}>" 


class State_Region_Resource(db.Model):
    """Links for State or Region Resources"""

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
    """Nations in the database"""

    __tablename__ = "nation"

    nation_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    state_region = db.relationship('State_Region', backref=db.backref("State_Region"))
    national_resource = db.relationship('National_Resource', backref=db.backref("National_Resource"))

    def __repr__(self):
         """Provide helpful representation when printed."""
                  
         return f"<Nations nation_id={self.nation_id} name={self.name}>" 


class National_Resource(db.Model):
    """Links for National Resources"""

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
    """Links for Global Resources"""

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


def connect_to_db(app):
    """Connect the database to the Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/users"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
