################################################################################
# Imports

import sys
import database
from data_report import DataReport


################################################################################
# Globals

PROGRAM_NAME = 'Homework Hacker'
PROGRAM_CMD = 'hwhack'
VERSION = 'Dev'

COMMAND_LIST = ['database', 'edit', 'help', 'list', 'new']
COMMAND_DESCRIPTION = {
    'database': 'Manage the database file',
    'edit': 'Edit an Assignment',
    'help': 'Print all available commands',
    'list': 'List all Assignments',
    'new': 'Create a new Assignment'
}

PROMPT = '\U0001F4DA  $ '
INDENT = ' ' * 4


################################################################################
# Generic Functions

def safe_input(prompt: str=''):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):  # User aborted
        print()
        sys.exit(0)


################################################################################
# Primary Functions

def print_help(synopsis: bool, end: str = ''):
    result = ''
    if synopsis:
        result += 'SYNOPSIS:\n    {} [command]\n\n'.format(PROGRAM_CMD)
    result += 'COMMANDS:\n'
    for cmd in COMMAND_LIST:
        result += '    {} - {}\n'.format(cmd, COMMAND_DESCRIPTION[cmd])
    result = result[:-1]  # strip last newline
    result += end
    print(result)


def print_greeting(synopsis: bool = True, end: str = ''):
    title = '{} (v. {})'.format(PROGRAM_NAME, VERSION)
    print('{}\n{}'.format(title, '~' * len(title)))
    print_help(synopsis, end)


def check_database(verbose: bool) -> (dict, bool):
    db_data = database.load()

    if not db_data:
        prompted = True
        print('Database file could not be located at {}'
              .format(database.DB_FILENAME))
        if safe_input('Would you like to create a new one? (y/n) ').lower() == 'y':
            database.save_new()
            return (database.DEFAULT_DB, True)
        return ({}, True)

    elif verbose:
        print('Database file located: {}'
              .format(database.DB_FILENAME))
        print(db_data)

    return (db_data, False)


def prompt_edit():
    pass


def print_list():
    db_data = database.load()
    print(DataReport(
        [('Title', 'title'), ('Course', 'course'), ('Due Date', 'due_date')],
        db_data['assignments']).ascii_table())


def prompt_new():
    db_data, prompted = check_database(verbose = False)
    if db_data:
        if prompted:
            print('')
        print('NEW ASSIGNMENT:')
        # Prompt title
        title = safe_input(INDENT + 'Title: ')

        # Prompt course
        course_set = set()
        for assignment in db_data['assignments']:
            course_set.add(assignment['course'])
        course_list = sorted(course_set)

        print(INDENT + 'Course', end='')
        for i, course in enumerate(course_list):
            if i == 0:
                print('')
            print('{}[{}] {}'.format(INDENT * 2, i+1, course))
        course = safe_input('{}: '.format(INDENT if course_list else ''))
        globbed = False
        try:
            index = int(course)
            assert 1 <= index <= len(course_list)
            course = course_list[index-1]
            globbed = True
        except (ValueError, AssertionError) as e:
            pass

        # Prompt due date
        due_date = safe_input(INDENT + 'Due Date: ')

        # Confirm
        if globbed and db_data['settings']['confirmOnGlob']:
            print('\nCONFIRM:\n{0}Title: {1}\n{0}Course: {2}\n{0}Due Date: {3}\n'
                  .format(INDENT, title, course, due_date))
            if safe_input('(y/n) ').lower() != 'y':
                return

        # Save
        db_data['assignments'].append(
            {'title': title, 'course': course, 'due_date': due_date})
        database.save(db_data)


def print_unknown(cmd: str):
    print('{}: Unknown command: '.format(PROGRAM_NAME), end='')
    if type(cmd) == type(""): # str
        print('{}'.format(cmd))
    elif type(cmd) == type([]): # list
        print(*cmd, sep=' ')


def parse_args(argv: [str]):
    if not argv:
        launch_interactive()
    elif len(argv) == 1:
        if argv[0] == 'database':
            check_database(verbose=True)
        elif argv[0] == 'edit':
            prompt_edit()
        elif argv[0] == 'help':
            print_greeting()
        elif argv[0] == 'list':
            print_list()
        elif argv[0] == 'new':
            prompt_new()
        else:
            print_unknown(argv[0])
    else:
        print_unknown(argv)


def launch_interactive():
    print_greeting(False)

    while True:
        user_input = safe_input('\n' + PROMPT)
        parse_args(user_input.split())


################################################################################
# Main

if __name__ == '__main__':
    parse_args([x.lower() for x in sys.argv[1:]])
