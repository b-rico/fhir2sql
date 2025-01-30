import logging
import os
from .common import set_env

def run():
    """
    Interactively update environment variables in .env.
    The user is prompted for a VAR name, then a new value.
    Press Enter with no input to finish.
    """
    logging.info("[updateenv] Starting interactive update of environment variables.")
    done = False
    while not done:
        key = input("Enter environment variable name to update (or press Enter to finish): ").strip()
        if not key:
            done = True
            break
        value = input(f"Enter new value for {key}: ").strip()
        if value:
            set_env(key, value)
            logging.info(f"[updateenv] Set {key}={value}")
        else:
            logging.warning("[updateenv] No value provided; skipping update.")

    logging.info("[updateenv] Completed environment variable updates.")