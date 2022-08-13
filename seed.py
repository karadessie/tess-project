"""Utility file to seed databases in seed_data/"""

import datetime
from turtle import title
from unicodedata import name
from sqlalchemy import func

from model import Users, Access_Codes, One_Time_Passwords, Community_Boards, Community_Board_Posts, \
                  Home_Resources, Communities, Community_Events, Community_Resources, \
                  Community_Boards, Community_Board_Posts, States_Regions, State_Region_Resources, \
                  Nations, National_Resources, Global_Resources, connect_to_db, db
from server import app


def load_users(users_filename):
    """Load users into database."""

    print("Users")

    for i, row in enumerate(open(users_filename)):
        row = row.rstrip()
        user_id, one_time_password_id, access_codes_id, username, password, name, communities_id = row.split("|")

        user = Users(user_id=user_id,
                     one_time_password_id=one_time_password_id,
                     access_codes_id=access_codes_id,
                     communities_id=communities_id,
                     username=username,
                     password=password,
                     name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_access_codes(access_codes_filename):
    """Load access codes into database."""

    print("Access Codes")

    for i, row in enumerate(open(access_codes_filename)):
        row = row.rstrip()
        access_codes_id, code, name = row.split("|")

        access_code = Access_Codes(access_codes_id=access_codes_id,
                                   code=code,
                                   name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(access_code)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_one_time_passwords(one_time_passwords_filename):
    """Load one time passwords into database."""

    print("One Time Passwords")

    for i, row in enumerate(open(one_time_passwords_filename)):
        row = row.rstrip()
        one_time_password_id, date_time, password = row.split("|")

        one_time_password = One_Time_Passwords(one_time_password_id=one_time_password_id,
                                               date_time=date_time,
                                               password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(one_time_password)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_communities(communities_filename):
    """Load Communities into database."""

    print("Communities")

    for i, row in enumerate(open(communities_filename)):
        row = row.rstrip()
        communities_id, states_regions_id, name = row.split("|")

        community = Communities(communities_id=communities_id,
                                states_regions_id=states_regions_id,
                                name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(community)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


def load_community_boards(community_boards_filename):
    """Load community boards into database."""

    print("Community Boards")

    for i, row in enumerate(open(community_boards_filename)):
        row = row.rstrip()
        community_boards_id, title = row.split("|")

        community_board = Community_Boards(community_boards_id=community_boards_id,
                                           title=title)

        # We need to add to the session or it won't ever be stored
        db.session.add(community_board)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)


def load_community_board_posts(community_board_posts_filename):
    """Load community board posts into database."""

    print("Community Board Posts")

    for i, row in enumerate(open(community_board_posts_filename)):
        row = row.rstrip()
        community_board_posts_id, title, description = row.split("|")

        community_board_post = Community_Board_Posts(community_board_posts_id=community_board_posts_id,
                                                     title=title,
                                                     description=description)

        # We need to add to the session or it won't ever be stored
        db.session.add(community_board_post)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

def load_community_events(community_events_filename):
    """Load community events into database."""

    print("Community Events")

    for i, row in enumerate(open(community_events_filename)):
        row = row.rstrip()
        community_events_id, title, description = row.split("|")

        community_event = Community_Events(community_events_id=community_events_id,
                                           title=title,
                                           description=description)

        # We need to add to the session or it won't ever be stored
        db.session.add(community_event)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)


def load_community_resources(community_resources_filename):
    """Load community resources into database."""

    print("Community Resources")

    for i, row in enumerate(open(community_resources_filename)):
        row = row.rstrip()
        community_resources_id, community_id, access_codes_id, community_links = row.split("|")

        community_resource = Community_Resources(community_resources_id=community_resources_id,
                                                 community_id=community_id,
                                                 access_codes_id=access_codes_id,
                                                 community_links=community_links)

        # We need to add to the session or it won't ever be stored
        db.session.add(community_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)


def load_home_resources(home_resources_filename):
    """Load home resource links into database."""

    print("Home Resources")

    for i, row in enumerate(open(home_resources_filename)):
        row = row.rstrip()
        home_resources_id, communities_id, home_links = row.split("|")

        home_resource = Home_Resources(home_resources_id=home_resources_id,
                                       communities_id=communities_id,
                                       home_links=home_links)

        # We need to add to the session or it won't ever be stored
        db.session.add(home_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)


def load_states_regions(user_filename):
    """Load states and regions into database."""

    print("States & Regions")

    for i, row in enumerate(open(states_regions_filename)):
        row = row.rstrip()
        state_regions_id, nations_id, name = row.split("|")

        state_region = States_Regions(state_regions_id=state_regions_id,
                                      nations_id=nations_id,
                                      name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(state_region)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_state_region_resources(state_region_resources_filename):
    """Load state and regional resource links into database."""

    print("State & Region Resources")

    for i, row in enumerate(open(state_region_resources_filename)):
        row = row.rstrip()
        state_region_resources_id, states_regions_id, access_codes_id, state_region_links = row.split("|")

        state_region_resource = State_Region_Resources(state_region_resources_id=state_region_resources_id,
                                                       states_regions_id=states_regions_id,
                                                       access_codes_id=access_codes_id,
                                                       states_regions_links=state_region_links)

        # We need to add to the session or it won't ever be stored
        db.session.add(state_region_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

def load_nations(nations_filename):
    """Load Nations into database."""

    print("Nations")

    for i, row in enumerate(open(nations_filename)):
        row = row.rstrip()
        nations_id, name = row.split("|")

        nation = Nations(nations_id=nations_id,
                         name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(nation)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_national_resources(national_resources_filename):
    """Load national resource links into database."""

    print("National Resources")

    for i, row in enumerate(open(national_resources_filename)):
        row = row.rstrip()
        national_resources_id, nations_id, access_codes_id, national_links = row.split("|")

        national_resource = National_Resources(national_resources_id=national_resources_id,
                                               nations_id=nations_id,
                                               access_codes_id=access_codes_id,
                                               national_links=national_links)

        # We need to add to the session or it won't ever be stored
        db.session.add(national_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_global_resources(global_resources_filename):
    """Load global resource links into database."""

    print("Global Resources")

    for i, row in enumerate(open(global_resources_filename)):
        row = row.rstrip()
        global_resources_id, access_codes_id, global_links = row.split("|")

        global_resource = Global_Resources(global_resources_id=global_resources_id,
                                           access_codes_id=access_codes_id,
                                           global_links=global_links)

        # We need to add to the session or it won't ever be stored
        db.session.add(global_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Users.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    users_filename = "seed_data/u.users"
    access_codes_filename = "seed_data/u.access_codes"
    one_time_passwords_filename = "seed_data/u.one_time_passwords"
    communities_filename = "seed_data/u.communities"
    community_boards_filename = "seed_data/u.community_boards"
    community_board_posts_filename = "seed_data/u.community_board_posts"
    community_events_filename = "seed_data/u.community_events"
    community_resources_filename = "seed_data/u.community_resources"
    states_regions_filename = "seed_data/u.states_regions"
    state_region_resources_filename = "seed_data/u.state_region_resources"
    nations_filename = "seed_data/u.nations"
    national_resources_filename = "seed_data/u.national_resources"
    global_resources_filename = "seed_data/u.global_resources"
    load_users(users_filename)
    load_access_codes(access_codes_filename)
    load_one_time_passwords(one_time_passwords_filename)
    load_communities(communities_filename)
    load_community_boards(community_boards_filename)
    load_community_board_posts(community_board_posts_filename)
    load_community_events(community_events_filename)
    load_community_resources(community_resources_filename)
    load_states_regions(states_regions_filename)
    load_state_region_resources(state_region_resources_filename)
    load_nations(nations_filename)
    load_national_resources(national_resources_filename)
    load_global_resources(global_resources_filename)
    set_val_user_id()
