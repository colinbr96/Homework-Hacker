################################################################################
# Imports

import sys
import config


################################################################################
# Globals

VERSION = "Dev"


################################################################################
# Generic Functions

def switch(case, cases: dict):
    cases[case]()


################################################################################
# Primary Functions

def get_action(action_list: list):
    # Printing
    for i, action in enumerate(action_list):
        print("[{}] {}".format(i+1, action))
    print()

    # Validation
    user_in = ""
    while(True):
        user_in = input("> ")
        try:
            user_in = int(user_in)
            assert 1 <= user_in <= len(action_list)
            break
        except (ValueError, AssertionError) as e:
            print("ERROR: {} is not between {}-{}\n".format(user_in,
                                                            1,
                                                            len(action_list)))
    return user_in


def copy_config():
    print("copy_config()")


def main_menu(config_data: dict):
    print("MAIN MENU")
    print(config_data)


def print_first_timer():
    print("Welcome to Homework Manager!\n"
          "It looks like you've never used this program before,\n"
          "or your configuration files could not be found.\n")

    current_actions = [
        "Create a new configuration",
        "Copy an existing configuration",
        "Quit"
    ]
    switch(get_action(current_actions),
           {
               1: config.save_new,
               2: copy_config,
               3: sys.exit
           })


def init():
    config_data = config.load()
    if(len(config_data) == 0):
        print_first_timer()
    else:
        main_menu(config_data)


def print_title():
    title = "Homework Manager (v. {})".format(VERSION)
    print("{}\n{}\n".format(title, "~" * len(title)))


################################################################################
# Main

if __name__ == "__main__":
    print_title()
    init()
