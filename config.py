################################################################################
# Imports

import pickle


################################################################################
# Globals

DEFAULT_CONFIG = {
    "courses": [],
    "assignments": []
}

CONFIG_FILENAME = "config.hwmngr"


################################################################################
# Primary Functions

def save_new() -> dict:
    with open(CONFIG_FILENAME, "wb") as handle:
        pickle.dump(DEFAULT_CONFIG, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return DEFAULT_CONFIG


def load() -> dict:
    try:
        with open(CONFIG_FILENAME, "rb") as handle:
            return pickle.load(handle)
    except FileNotFoundError:
        return {}
