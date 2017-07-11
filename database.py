################################################################################
# Imports

import json


################################################################################
# Globals

DEFAULT_DB = {
    'assignments': [],
    'settings': {
        'confirmOnGlob': True
    }
}

DB_FILENAME = 'db.hwhkr'


################################################################################
# Primary Functions

def save_new() -> dict:
    with open(DB_FILENAME, 'w') as handle:
        json.dump(DEFAULT_DB, handle)
    return DEFAULT_DB


def save(db_data: dict):
    with open(DB_FILENAME, 'w') as handle:
        json.dump(db_data, handle)


def load() -> dict:
    try:
        with open(DB_FILENAME, 'r') as handle:
            return json.load(handle)
    except FileNotFoundError:
        return {}
