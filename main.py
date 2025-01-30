#!/usr/bin/env python3
import argparse
import logging
import sys

# Local module imports
from src import common
from src import upsertdb
from src import insertdb
from src import truncdb
from src import upsertsql
from src import insertsql
from src import updateenv

def main():
    """
    Parses command-line options and delegates to the appropriate script.
    """
    parser = argparse.ArgumentParser(prog="fhir2sql", add_help=False)
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    parser.add_argument("-upsertdb", action="store_true", help="Upsert data into the database.")
    parser.add_argument("-insertdb", action="store_true", help="Insert data into the database (no updates).")
    parser.add_argument("-truncdb", action="store_true", help="Truncate & load data into the database.")
    parser.add_argument("-upsertsql", action="store_true", help="Generate upsert SQL script (does not run).")
    parser.add_argument("-insertsql", action="store_true", help="Generate insert-only SQL script (does not run).")
    parser.add_argument("-updateenv", action="store_true", help="Interactively update environment variables in .env.")

    args = parser.parse_args()

    # Initialize logging and environment checks
    common.init_logger()
    common.load_and_check_env_variables()

    if args.upsertdb:
        logging.info("User invoked -upsertdb")
        upsertdb.run()
    elif args.insertdb:
        logging.info("User invoked -insertdb")
        insertdb.run()
    elif args.truncdb:
        logging.info("User invoked -truncdb")
        truncdb.run()
    elif args.upsertsql:
        logging.info("User invoked -upsertsql")
        upsertsql.run()
    elif args.insertsql:
        logging.info("User invoked -insertsql")
        insertsql.run()
    elif args.updateenv:
        logging.info("User invoked -updateenv")
        updateenv.run()
    else:
        logging.info("No valid command was provided.")
        parser.print_help()

if __name__ == "__main__":
    main()