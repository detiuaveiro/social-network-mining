import os
import sys

import Enums.enums as enums
from send import RabbitSend

TASKS_EXCHANGE = "tasks_deliver"
TASKS_ROUTING_KEY_PREFIX = "tasks.twitter"

rabbit_host = os.environ.get("RABBIT_HOST", "mqtt-redesfis.5g.cn.atnog.av.it.pt")
rabbit_port = os.environ.get("RABBIT_PORT", 5672)
rabbit_vhost = os.environ.get("RABBIT_VIRTUALHOST", "PI")
rabbit_username = os.environ.get("RABBIT_USER", "pi_rabbit_admin")
rabbit_pass = os.environ.get("RABBIT_PASS", "yPvawEVxks7MLg3lfr3g")

RABBIT_CONNECTION = RabbitSend(host=rabbit_host, port=rabbit_port, vhost=rabbit_vhost,
                               username=rabbit_username,
                               password=rabbit_pass)

BOT_ID_SESSION_KEY = "bot_id"

current_session = {
    BOT_ID_SESSION_KEY: None,
}


def print_divider():
    print("=" * 30)


def print_current_session():
    print("Currently using the following variables:")
    for k, v in current_session.items():
        print("{}={}".format(k,v))


def cleanup():
    RABBIT_CONNECTION.close()


def setup_current_session():
    while True:
        print("You currently have the BOT ID set to: {0}".format(current_session.get(BOT_ID_SESSION_KEY, None)))
        print("Would you like to change it? (Y/N)")
        option = input("> ").strip().lower()
        if option == "n":
            break
        elif option == "y":
            while True:
                try:
                    new_bot_id = int(input("New Bot ID Value? ").strip())
                    current_session[BOT_ID_SESSION_KEY] = new_bot_id
                    break
                except ValueError:
                    print("The Bot ID must be a number!")
        else:
            print("Incorrect option! Try again")


def follow_users_task():
    # reading the users
    print("Type the Screen Names of the users (type /exit to end)")
    users = []
    while not users:
        user = input("> ").strip()
        if user == "/exit":
            if not users:
                print("You must at least add 1 user!")
            else:
                break
        else:
            users += [user]
    print("User currently has: ")
    print(users)
    print("Do you want to send? (press Enter to confirm, N to cancel)")
    option = input("> ").strip().lower()
    if option == "n":
        print("Canceled")
        return
    print("Sending to bot with ID={}...".format(current_session.get(BOT_ID_SESSION_KEY)))
    payload = {
        "type" : enums.ResponseTypes.FOLLOW_USERS,
        "params" : {
            "type" : "screen_name",
            "data" : users
        }
    }
    RABBIT_CONNECTION.send(
        routing_key="{0}.{1}".format(TASKS_ROUTING_KEY_PREFIX,current_session.get(BOT_ID_SESSION_KEY)),
        message=payload
    )
    print("Sent")


def send_task_loop():
    while True:
        print("Select a task (type /exit to exit):")
        for val in enums.ResponseTypes:
            print("{0} - {0.name}".format(val))
        option = input("> ")
        if option is enums.ResponseTypes.FOLLOW_USERS:
            follow_users_task()
        elif option == "/exit":
            return
        else:
            print("Not implemented/Invalid option, try again!")


print("{0} Twitter Bots Helper Scripts {0}".format('-' * 5))
while True:
    print_divider()
    print_current_session()
    print_divider()
    print("Select an option:")
    print("1 - Setup current session")
    print("2 - Send a Task to a Bot")
    print("0 - Exit")
    option = input("> ").strip()

    if option == "0":
        print("Exiting...")
        cleanup()
        sys.exit(0)
    elif option == "1":
        setup_current_session()
    elif option == "2":
        if current_session.get(BOT_ID_SESSION_KEY, None) is None:
            print("Bot id is none! You need to setup first!")
            continue
        send_task_loop()
    else:
        print("Incorrect option! Try again")
