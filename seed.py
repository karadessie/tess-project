"""Utility file to seed database"""

from sqlalchemy import func

from model import Home_Resources, National_Resources, State_Region_Resources, State_Regions, Users, Admin_Access, One_Time_Passwords, Community_Boards, \
                  Communities, Community_Events, Community_Board_Posts, State_Regions, State_Region_Resources, \
                  Nations, Global_Resources, connect_to_db, db
from server import app


def load_nations():
    """Load Nations into database."""

    print("Nations")

    for i, row in enumerate(open(nation_filename)):
        row = row.rstrip()
        nation_id, nation_name = row.split("|")

        nation = Nations(nation_id=nation_id,
                         nation_name=nation_name)
        db.session.add(nation)


def load_states_regions():
    """Load states and regions into database."""

    print("States & Regions")

    for i, row in enumerate(open(state_region_filename)):
        row = row.rstrip()
        state_region_id, nation_id, state_region_name = row.split("|")

        state_region = State_Regions(state_region_id=state_region_id,
                                     nation_id=nation_id,
                                     state_region_name=state_region_name)
        db.session.add(state_region)

    db.session.commit()


def load_access_codes():
    """Load admin codes into database."""

    print("Admin_Access")

    for i, row in enumerate(open(admin_access_filename)):
        row = row.rstrip()
        admin_access_id, admin_access_name = row.split("|")

        admin_access = Admin_Access(admin_access_id=admin_access_id,
                                    admin_access_name=admin_access_name)
        db.session.add(admin_access)

    db.session.commit()


def load_communities():
    """Load Communities into database."""

    print("Communities")

    for i, row in enumerate(open(community_filename)):
        row = row.rstrip()
        community_id, state_region_id, community_name = row.split("|")

        community = Communities(community_id=community_id,
                                state_region_id=state_region_id,
                                community_name=community_name)
        db.session.add(community)

    db.session.commit()


def load_one_time_passwords():
    """Load one time passwords into database."""

    print("One_Time_Passwords")

    for i, row in enumerate(open(one_time_passwords_filename)):
        row = row.rstrip()
        one_time_password_id, admin_access_id, community_id, one_time_password_datetime, one_time_password = row.split("|")

        add_one_time_password = One_Time_Passwords(one_time_password_id=one_time_password_id,
                                                   admin_access_id=admin_access_id,
                                                   community_id=community_id,
                                                   one_time_password_datetime=one_time_password_datetime,
                                                   one_time_password=one_time_password)
        db.session.add(add_one_time_password)

    db.session.commit()


def load_users():
    """Load users into database."""

    print("Users")

    for i, row in enumerate(open(user_filename)):
        row = row.rstrip()
        user_id, one_time_password_id, admin_access_id, community_id, username, password, user_name = row.split("|")

        user = Users(user_id=user_id,
                     one_time_password_id=one_time_password_id,
                     admin_access_id=admin_access_id,
                     community_id=community_id,
                     username=username,
                     password=password,
                     user_name=user_name)
        db.session.add(user)

    db.session.commit()


def load_home_resources():
    """Load home resource links into database."""

    print("Home Resources")

    for i, row in enumerate(open(home_resource_filename)):
        row = row.rstrip()
        home_resource_id, community_id, home_resource_name, home_resource_link = row.split("|")

        home_resource = Home_Resources(home_resource_id=home_resource_id,
                                       community_id=community_id,
                                       home_resource_name=home_resource_name,
                                       home_resource_link=home_resource_link)
        db.session.add(home_resource)

    db.session.commit()


def load_community_boards():
    """Load community boards into database."""

    print("Community_Boards")

    for i, row in enumerate(open(community_board_filename)):
        row = row.rstrip()
        community_board_id, community_board_title = row.split("|")

        community_board = Community_Boards(community_board_id=community_board_id,
                                           community_board_title=community_board_title)
        db.session.add(community_board)

    db.session.commit()


def load_community_board_posts():
    """Load community board posts into database."""

    print("Community Board Posts")

    for i, row in enumerate(open(community_board_post_filename)):
        row = row.rstrip()
        community_board_post_id, community_id, community_board_id, community_board_post_datetime, \
                                                          community_board_post_title, \
                                                          community_board_post_description = row.split("|")

        community_board_posts = Community_Board_Posts(community_board_post_id=community_board_post_id,
                                                      community_id=community_id,
                                                      community_board_id=community_board_id,
                                                      community_board_post_datetime=community_board_post_datetime,
                                                      community_board_post_title=community_board_post_title,
                                                      community_board_post_description=community_board_post_description)
        db.session.add(community_board_posts)

    db.session.commit()


def load_community_events():
    """Load community events into database."""

    print("Community Events")

    for i, row in enumerate(open(community_event_filename)):
        row = row.rstrip()
        community_event_id, community_id, community_event_datetime, community_event_title, community_event_description = row.split("|")

        community_event = Community_Events(community_event_id=community_event_id,
                                           community_id=community_id,
                                           community_event_datetime=community_event_datetime,
                                           community_event_title=community_event_title,
                                           community_event_description=community_event_description)
        db.session.add(community_event)

    db.session.commit()


def load_state_region_resources():
    """Load state and regional resource links into database."""

    print("State & Region Resources")

    for i, row in enumerate(open(state_region_resource_filename)):
        row = row.rstrip()
        state_region_resource_id, state_region_id, admin_access_id, state_region_resource_name, \
        state_region_resource_link = row.split("|")

        state_region_resource = State_Region_Resources(state_region_resource_id=state_region_resource_id,
                                                       state_region_id=state_region_id,
                                                       admin_access_id=admin_access_id,
                                                       state_region_resource_name=state_region_resource_name,
                                                       state_region_resource_link=state_region_resource_link)
        db.session.add(state_region_resource)

    db.session.commit()


def load_national_resources():
    """Load national resource links into database."""

    print("National Resources")

    for i, row in enumerate(open(national_resource_filename)):
        row = row.rstrip()
        national_resource_id, nation_id, admin_access_id, national_resource_name, national_resource_link = row.split("|")

        national_resource = National_Resources(national_resource_id=national_resource_id,
                                               nation_id=nation_id,
                                               admin_access_id=admin_access_id,
                                               national_resource_name=national_resource_name,
                                               national_resource_link=national_resource_link)
        db.session.add(national_resource)

    db.session.commit()


def load_global_resources():
    """Load global resource links into database."""

    print("Global Resources")

    for i, row in enumerate(open(global_resource_filename)):
        row = row.rstrip()
        global_resource_id, admin_access_id, global_resource_name, global_resource_link = row.split("|")

        global_resource = Global_Resources(global_resource_id=global_resource_id,
                                           admin_access_id=admin_access_id,
                                           global_resource_name=global_resource_name,
                                           global_resource_link=global_resource_link)
        db.session.add(global_resource)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Users.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('Users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    user_filename = "seed_data/user.txt"
    admin_access_filename = "seed_data/admin_access.txt"
    one_time_passwords_filename = "seed_data/one_time_password.txt"
    community_filename = "seed_data/community.txt"
    community_board_filename = "seed_data/community_board.txt"
    community_board_post_filename = "seed_data/community_board_post.txt"
    community_event_filename = "seed_data/community_event.txt"
    home_resource_filename = "seed_data/home_resource.txt"
    state_region_filename = "seed_data/state_region.txt"
    state_region_resource_filename = "seed_data/state_region_resource.txt"
    nation_filename = "seed_data/nation.txt"
    national_resource_filename = "seed_data/national_resource.txt"
    global_resource_filename = "seed_data/global_resource.txt"
    load_nations(nation_filename)
    load_states_regions(state_region_filename)
    load_access_codes(admin_access_filename)
    load_communities(community_filename)
    load_one_time_passwords(one_time_passwords_filename)
    load_users(user_filename)
    load_home_resources(home_resource_filename)
    load_community_boards(community_board_filename)
    load_community_board_posts(community_board_post_filename)
    load_community_events(community_event_filename)
    load_state_region_resources(state_region_resource_filename)
    load_national_resources(national_resource_filename)
    load_global_resources(global_resource_filename)
