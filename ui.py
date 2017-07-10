################################################################################
# Imports

import sys
import database


################################################################################
# Globals

PROGRAM_NAME = 'clihw'
VERSION = 'Dev'

COMMAND_LIST = ['database', 'edit', 'help', 'list', 'new']
COMMAND_DESCRIPTION = {
    'database': 'Manage the database file',
    'edit': 'Edit an Assignment',
    'help': 'Print all available commands',
    'list': 'List all Assignments',
    'new': 'Create a new Assignment'
}


################################################################################
# Primary Functions

def print_greeting():
    title = 'CLI Homework Manager (v. {})'.format(VERSION)
    print('{}\n{}'.format(title, '~' * len(title)))
    print_help()


def check_database():
    db_data = database.load()
    if not db_data:
        print('Database file could not be located at ./{}'
              .format(PROGRAM_NAME, database.DB_FILENAME))
        if input('Would you like to create a new one? (y/n) ').lower() == 'y':
            database.save_new()
    else:
        print('Database file located: ./{}'
              .format(database.DB_FILENAME))
        print(db_data)


def prompt_edit():
    pass


def print_help():
    print('SYNOPSIS:\n    {} [command]\n'.format(PROGRAM_NAME))
    print('COMMANDS:')
    for cmd in COMMAND_LIST:
        print('    {} - {}'.format(cmd, COMMAND_DESCRIPTION[cmd]))


def print_list():
    db_data = database.load()
    print(db_data)


def prompt_new():
    pass


def print_unknown(cmd):
    print('{}: Unknown command: '.format(PROGRAM_NAME), end='')
    if type(cmd) == type(""): # str
        print('{}'.format(PROGRAM_NAME, cmd))
    elif type(cmd) == type([]): # list
        print(*cmd, sep=' ')


def parse_args(argv: list):
    if not argv:
        print_greeting()
    elif len(argv) == 1:
        if argv[0] == 'database':
            check_database()
        elif argv[0] == 'edit':
            prompt_edit()
        elif argv[0] == 'help':
            print_help()
        elif argv[0] == 'list':
            print_list()
        elif argv[0] == 'new':
            prompt_new()
        else:
            print_unknown(argv[0])
    else:
        print_unknown(argv)


################################################################################
# Main

if __name__ == '__main__':
    parse_args([x.lower() for x in sys.argv[1:]])
