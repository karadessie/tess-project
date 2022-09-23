"""Data Models for TESS Project"""
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

from flask_login import UserMixin

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions

db = SQLAlchemy()


class Nations(db.Model):
    """Nations in the database"""

    __tablename__ = "nation"

    nation_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""
                  
         return f"<Nations nation_id={self.nation_id} name={self.name}>" 


class State_Regions(db.Model):
    """States or Regions in the database"""

    __tablename__ = "state_region"

    state_region_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.nation_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""
 
         return f"<States & Regions state_region_id={self.state_region_id} name={self.name}>" 


class Admin_Access(db.Model):
    """List of administrative access codes"""

    __tablename__ = "admin_access"

    admin_access_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    admin_access_name = db.Column(db.String(12), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Admin Code admin_access={self.admin_access}>"


class Communities(db.Model):
    """Communities in the database"""

    __tablename__ = "community"

    community_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    state_region_id = db.Column(db.Integer, db.ForeignKey('state_region.state_region_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community name={self.name}>"


class One_Time_Passwords(db.Model):
    """List of one-time-passwords"""

    __tablename__ = "one_time_password"

    one_time_password_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<One Time Password password={self.password}>"


class Users(db.Model, UserMixin):
    """Users in the database"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    one_time_password_id = db.Column(db.Integer, db.ForeignKey('one_time_password.one_time_password_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def get_id(self):
        return str(self.alternative_id)
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Users username={self.username} name={self.name}>"


class Home_Resources(db.Model):
    """Links for Home App Resources"""

    __tablename__ = "home_resource"

    home_resource_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Home Resource name={self.name}>"


class Community_Boards(db.Model):
    """List of Community Board Names"""

    __tablename__ = "community_board"

    community_board_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    title = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Board title={self.title}>"


class Community_Board_Posts(db.Model):
    """List of Community Board Posts"""

    __tablename__ = "community_board_post"

    community_board_post_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    community_board_id = db.Column(db.Integer, db.ForeignKey('community_board.community_board_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(510), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Board Posts community_board_post_id={self.community_board_post_id} title={self.title}>"


class Community_Events(db.Model):
    """List of Community Events"""

    __tablename__ = "community_event"

    community_event_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    date_time = db.Column(db.DateTime)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(510), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Community Events community_event_id={self.one_time_password_id} title={self.title}>"


class Community_Resources(db.Model):
    """Links for Community Resources"""

    __tablename__ = "community_resource"

    community_resource_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.community_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""

         return f"<Community Resources community_resource_id={self.community_resource_id} name={self.name}>"


class State_Region_Resources(db.Model):
    """Links for State or Region Resources"""

    __tablename__ = "state_region_resource"

    states_region_resource_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    state_region_id = db.Column(db.Integer, db.ForeignKey('state_region.state_region_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
         """Provide helpful representation when printed."""
                  
         return f"<State & Region Resources state_region_resource_id={self.state_region_resource_id} name={self.name}>" 


class National_Resources(db.Model):
    """Links for National Resources"""

    __tablename__ = "national_resource"

    national_resource_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    nation_id = db.Column(db.Integer, db.ForeignKey('nation.nation_id'), nullable=False)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
             
        return f"<National Resources national_resources_id={self.national_resources_id} name={self.name}>" 


class Global_Resources(db.Model):
    """Links for Global Resources"""

    __tablename__ = "global_resource"

    global_resource_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    admin_access_id = db.Column(db.Integer, db.ForeignKey('admin_access.admin_access_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
                 
        return f"<Global Resources global_resource_id={self.global_resource_id} name={self.name}>" 


def connect_to_db(app):
    """Connect the database to the Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://aeuiriruznhytf:f271469a21f44207c4806154efc00666af69e02b5b57c30058c6efdc5bded155@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d1c6vl2nchn4s5"
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
