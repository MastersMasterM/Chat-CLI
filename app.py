from member import member
import redis
import json
import datetime

rg = redis.Redis(db=1)
rm = redis.Redis(db=2)
rmes = redis.Redis(db=3)

def main_menu():
    pass

def login():
    user_name = input('Hello & welcome to the cli-chatroom\n please enter your username:')
    if rm.exists(user_name):
        user = json.loads(rm.get(user_name))
        m = member(user['name'],user_name)
        m.group = user['groups']
        print(f"Welcome Back {user['name']}")
    else:
        print("Welcome to the app. It seems you're a new user")
        name = input("Please Enter your fullname:")
        m = member(name,user_name)
        m.to_redis()
    return(m)

def send_message(member:member, g_name=""):
    groups_mem = list(member.group.keys())
    if len(groups_mem) > 0 :
        if g_name == "":
            print("You're a member of the following groups:")
            for x in groups_mem: print(x)
            g_name = input("Please enter the name of the group in which you want to save message:")
        elif g_name != "":
            pass
        text = input("Please enter the text of your message:")
        member.send(text,g_name)
        print("What do you want to do now?\n 1)Back to the main menu\n 2)Sending message again\n 3)Exit")
        op = int(input("Please enter a number:"))
        if op == 1:
            main_menu(member)
        elif op == 2:
            send_message(member)
        elif op == 3:
            exit()
        else:
            print("You've entered wrong input. I will go to the main menu\n")
            main_menu(member)
    else:
        print("\nYou are not the member of any groups. I will go back to the main menu")
        main_menu(member)

def view_group(member:member):
    groups_mem = list(member.group.keys())
    print("You're a member of the following groups:")
    for x in groups_mem: print(x)
    g_name = input("Please enter the name of the group that you want to view:")
    gmessages = json.loads(rg.get(g_name))['message']
    for x in gmessages.values():
        print(f"[{x['sent_at']}] {x['sender']}: {x['text']}")
    print("\n What do you want to do now?\n 1)Send Message to this group\n 2)Back to main menu")
    op = int(input("Please enter a number:"))
    if op == 1:
        send_message(member,g_name)
    else:
        main_menu(member)

def create_group(member:member):
    g_name = input("Please enter the name of the group:")
    if rg.exists(g_name):
        print("The name of the groups should be unique.A group with this name has already exist.")
        create_group(member)
    else:
        desc = input("Please write a description for your group:")
        member.create_group(g_name,desc)
        main_menu(member)

def group_info(g_name):
    ginfo = json.loads(rg.get(g_name))
    print(f"Creator: {ginfo['creator']}\n Description: {ginfo['desc']}\n Created_at: {ginfo['created_at']}")

def join_new_group(member:member):
    allgp = rg.keys('*')
    allgp = [x.decode() for x in allgp]
    memgp = list(member.group.keys())
    res = list(set(allgp) - set(memgp))
    print("Please choose from the following list:\n")
    for x in res: print(x)
    g_name = input("Please enter the group name to get more information:")
    group_info(g_name)
    print("Do you want to join this group or want to get info about other groups")
    op = int(input("Enter a number 1)Yes 2)No :"))
    if op == 1:
        member.join_group(g_name)
        main_menu(member)
    else:
        join_new_group(member)

def left_group(member:member):
    groups_mem = list(member.group.keys())
    print("You're a member of the following groups:")
    for x in groups_mem: print(x)
    g_name = input("Please enter the name of the group that you want to leave:")
    member.leave_group(g_name)
    main_menu(member)

def search_history(member:member):
    allgp = rg.keys('*')
    allgp = [x.decode() for x in allgp]
    print("Available groups are as follows:")
    for x in allgp: print(x)
    g_name = input(f"Please enter the group name:")
    s_name = input(f"Please enter the name of the sender name:")
    datet = input(f"Please enter the date with this format {datetime.datetime.now().replace(microsecond=0).isoformat(sep='-')}:")
    print(rmes.get(f"{g_name}-{s_name}-{datet}"))
    main_menu(member)


def main_menu(member:member):
    print("What would you like to do?\n 1)View Joined Groups Messages\n 2)Send Message\n 3)Join new a group\n 4)Create a group\n 5)Left from one of your group\n 6)Search in All Messages History\n 7)Exit")
    op = int(input("Please enter a number:"))
    if op == 1:
        view_group(member)
    elif op == 2:
        send_message(member)
    elif op == 3:
        join_new_group(member)
    elif op == 4:
        create_group(member)
    elif op == 5:
        left_group(member)
    elif op == 6:
        search_history(member)
    elif op == 7:
        quit()
    else:
        print("\nYou've entered wrong input.")
        main_menu(member)

u = login()
main_menu(u)