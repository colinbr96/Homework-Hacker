################################################################################
# Imports

import pickle


################################################################################
# Globals

DEFAULT_DB = {
    'courses': [],
    'assignments': []
}

DB_FILENAME = 'db.hwmngr'


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
