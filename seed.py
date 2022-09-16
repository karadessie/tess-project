"""Utility file to seed databases in seed_data"""

from sqlalchemy import func

from model import Users, Admin_Access, One_Time_Passwords, Community_Boards, Community_Board_Post, \
                  Home_Resource, Communities, Community_Event, Community_Resource, \
                  Community_Board_Post, State_Region, State_Region_Resource, \
                  Nation, National_Resource, Global_Resource, connect_to_db, db
from server import app


def load_users(users_filename):
    """Load users into database."""

    print("Users")

    for i, row in enumerate(open(user_filename)):
        row = row.rstrip()
        user_id, one_time_password_id, admin_access_id, username, password, name, community_id = row.split("|")

        user = Users(user_id=user_id,
                     one_time_password_id=one_time_password_id,
                     admin_access_id=admin_access_id,
                     community_id=community_id,
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

def load_access_codes(admin_access_filename):
    """Load admin codes into database."""

    print("Admin_Access")

    for i, row in enumerate(open(admin_access_filename)):
        row = row.rstrip()
        admin_access_id, name = row.split("|")

        admin_access = Admin_Access(admin_access_id=admin_access_id,
                                    name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(admin_access)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_one_time_passwords(one_time_passwords_filename):
    """Load one time passwords into database."""

    print("One_Time_Passwords")

    for i, row in enumerate(open(one_time_password_filename)):
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

def load_communities(community_filename):
    """Load Communities into database."""

    print("Communities")

    for i, row in enumerate(open(community_filename)):
        row = row.rstrip()
        community_id, state_region_id, name = row.split("|")

        community = Communities(community_id=community_id,
                                state_region_id=state_region_id,
                                name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(community)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


def load_community_boards(community_board_filename):
    """Load community boards into database."""

    print("Community_Boards")

    for i, row in enumerate(open(community_board_filename)):
        row = row.rstrip()
        community_board_id, title = row.split("|")

        community_board = Community_Boards(community_board_id=community_board_id,
                                           title=title)

        # We need to add to the session or it won't ever be stored
        db.session.add(community_board)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)


def load_community_board_posts(community_board_post_filename):
    """Load community board posts into database."""

    print("Community Board Posts")

    for i, row in enumerate(open(community_board_post_filename)):
        row = row.rstrip()
        community_board_post_id, title, description = row.split("|")

        community_board_post = Community_Board_Post(community_board_post_id=community_board_post_id,
                                                    title=title,
                                                    description=description)

        # We need to add to the session or it won't ever be stored
        db.session.add(community_board_post)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

def load_community_events(community_event_filename):
    """Load community events into database."""

    print("Community Events")

    for i, row in enumerate(open(community_event_filename)):
        row = row.rstrip()
        community_event_id, title, description = row.split("|")

        community_event = Community_Event(community_event_id=community_event_id,
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

    for i, row in enumerate(open(community_resource_filename)):
        row = row.rstrip()
        community_resource_id, community_id, admin_access_id, community_link = row.split("|")

        community_resource = Community_Resource(community_resource_id=community_resource_id,
                                                community_id=community_id,
                                                admin_access_id=admin_access_id,
                                                community_link=community_link)

        # We need to add to the session or it won't ever be stored
        db.session.add(community_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)


def load_home_resources(home_resources_filename):
    """Load home resource links into database."""

    print("Home Resources")

    for i, row in enumerate(open(home_resource_filename)):
        row = row.rstrip()
        home_resource_id, community_id, home_link = row.split("|")

        home_resource = Home_Resource(home_resource_id=home_resource_id,
                                      community_id=community_id,
                                      home_link=home_link)

        # We need to add to the session or it won't ever be stored
        db.session.add(home_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)


def load_states_regions(state_region_filename):
    """Load states and regions into database."""

    print("States & Regions")

    for i, row in enumerate(open(state_region_filename)):
        row = row.rstrip()
        state_region_id, nation_id, name = row.split("|")

        state_region = State_Region(state_region_id=state_region_id,
                                    nation_id=nation_id,
                                    name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(state_region)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_state_region_resources(state_region_resource_filename):
    """Load state and regional resource links into database."""

    print("State & Region Resources")

    for i, row in enumerate(open(state_region_resource_filename)):
        row = row.rstrip()
        state_region_resource_id, states_region_id, admin_access_id, state_region_link = row.split("|")

        state_region_resource = State_Region_Resource(state_region_resource_id=state_region_resource_id,
                                                       states_region_id=states_region_id,
                                                       admin_access_id=admin_access_id,
                                                       states_region_link=state_region_link)

        # We need to add to the session or it won't ever be stored
        db.session.add(state_region_resource)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

def load_nations(nations_filename):
    """Load Nations into database."""

    print("Nations")

    for i, row in enumerate(open(nation_filename)):
        row = row.rstrip()
        nation_id, name = row.split("|")

        nation = Nation(nation_id=nation_id,
                        name=name)

        # We need to add to the session or it won't ever be stored
        db.session.add(nation)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_national_resources(national_resource_filename):
    """Load national resource links into database."""

    print("National Resources")

    for i, row in enumerate(open(national_resource_filename)):
        row = row.rstrip()
        national_resource_id, nation_id, admin_access_id, national_link = row.split("|")

        national_resource = National_Resource(national_resources_id=national_resource_id,
                                               nation_id=nation_id,
                                               access_code_id=admin_access_id,
                                               national_link=national_link)

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
        global_resource_id, admin_access_id, global_link = row.split("|")

        global_resource = Global_Resource(global_resource_id=global_resource_id,
                                          admin_access_id=admin_access_id,
                                          global_link=global_link)

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
    query = "SELECT setval('Users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    user_filename = "seed_data/user.txt"
    admin_access_filename = "seed_data/admin_access.txt"
    one_time_password_filename = "seed_data/one_time_password.txt"
    community_filename = "seed_data/community.txt"
    community_board_filename = "seed_data/community_board.txt"
    community_board_post_filename = "seed_data/community_board_post.txt"
    community_event_filename = "seed_data/community_event.txt"
    home_resource_filename = "seed_data/home_resource.txt"
    community_resource_filename = "seed_data/community_resource.txt"
    state_region_filename = "seed_data/state_region.txt"
    state_region_resource_filename = "seed_data/state_region_resource.txt"
    nation_filename = "seed_data/nation.txt"
    national_resource_filename = "seed_data/national_resource.txt"
    global_resource_filename = "seed_data/global_resource.txt"
    load_users(user_filename)
    load_access_codes(admin_access_filename)
    load_one_time_passwords(one_time_password_filename)
    load_communities(community_filename)
    load_community_boards(community_board_filename)
    load_community_board_posts(community_board_post_filename)
    load_community_events(community_event_filename)
    load_community_resources(community_resource_filename)
    load_states_regions(state_region_filename)
    load_state_region_resources(state_region_resource_filename)
    load_nations(nation_filename)
    load_national_resources(national_resource_filename)
    load_global_resources(global_resource_filename)
    set_val_user_id()
