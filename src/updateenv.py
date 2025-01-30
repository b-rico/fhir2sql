import logging
import os
from .common import set_env

def run():
    logging.info("Running updateenv process.")
    done = False
    while not done:
        key = input("Enter environment variable name to update (or press Enter to finish): ").strip()
        if not key:
            done = True
            break
        value = input(f"Enter new value for {key}: ").strip()
        if value:
            set_env(key, value)
            logging.info(f"Set {key}={value}")
    logging.info("Completed updateenv process.")