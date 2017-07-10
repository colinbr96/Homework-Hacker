################################################################################
# Imports

import sys
import database


################################################################################
# Globals

PROGRAM_NAME = 'hwhack'
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
# Generic Functions

def safe_input(prompt: str=''):
    try:
        return input(prompt)
    except EOFError: # User aborted
        sys.exit()


################################################################################
# Primary Functions

def print_greeting():
    title = 'Homework Hacker (v. {})'.format(VERSION)
    print('{}\n{}'.format(title, '~' * len(title)))
    print_help()


def check_database(verbose: bool) -> dict:
    db_data = database.load()

    if not db_data:
        print('Database file could not be located at ./{}'
              .format(database.DB_FILENAME))
        if safe_input('Would you like to create a new one? (y/n) ').lower() == 'y':
            database.save_new()
            return database.DEFAULT_DB
        return {}

    elif verbose:
        print('Database file located: ./{}'
              .format(database.DB_FILENAME))
        print(db_data)

    return db_data


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
    db_data = check_database(verbose=False)
    if db_data:
        print('NEW ASSIGNMENT:')
        # Prompt title
        title = safe_input('    Title: ')

        # Prompt course
        print('    Course', end='')
        course_list = sorted(db_data['courses'])
        for i, course in enumerate(course_list):
            if i == 0:
                print('')
            print('        [{}] {}'.format(i+1, course))
        course = safe_input('{}: '.format('    ' if course_list else ''))
        try:
            index = int(course)
            assert 1 <= index <= len(course_list)
            course = course_list[index-1]

        except (ValueError, AssertionError) as e:
            pass

        # Prompt due date
        due_date = safe_input('    Due Date: ')

        # Confirm
        if db_data['settings']['confirmOnAdd']:
            print('\nCONFIRM:\n    Title: {}\n    Course: {}\n    Due Date: {}\n'
                  .format(title, course, due_date))
            if safe_input('(y/n) ').lower() != 'y':
                return

        # Save
        db_data['assignments'].append(database.Assignment(title, course, due_date))
        db_data['courses'].add(course)
        database.save(db_data)


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
            check_database(verbose=True)
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
