################################################################################
# Imports

import pickle
from collections import namedtuple


################################################################################
# Data Types

Assignment = namedtuple('Assignment', 'title, course, due_date')


################################################################################
# Globals

DEFAULT_DB = {
    'assignments': [],
    'courses': set(),
    'settings': {
        'confirmOnAdd': True
    }
}

DB_FILENAME = 'db.hwhkr'


################################################################################
# Primary Functions

def save_new() -> dict:
    with open(DB_FILENAME, 'wb') as handle:
        pickle.dump(DEFAULT_DB, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return DEFAULT_DB


def save(db_data: dict):
    with open(DB_FILENAME, 'wb') as handle:
        pickle.dump(db_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load() -> dict:
    try:
        with open(DB_FILENAME, 'rb') as handle:
            return pickle.load(handle)
    except FileNotFoundError:
        return {}
