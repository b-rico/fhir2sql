import os
import logging
from dotenv import load_dotenv

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    import cx_Oracle
except ImportError:
    cx_Oracle = None

try:
    import pyodbc
except ImportError:
    pyodbc = None

def init_logger():
    """
    Initializes logging to write to LOGS_DIR/runs.log and also to console.
    """
    load_dotenv(".env", override=True)
    logs_dir = os.getenv("LOGS_DIR", "").strip()
    if logs_dir and not os.path.exists(logs_dir):
        os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, "runs.log") if logs_dir else "runs.log"

    logging.basicConfig(
        filename=log_file,
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console_handler.setFormatter(console_format)
    logging.getLogger().addHandler(console_handler)

def load_and_check_env_variables():
    """
    Loads .env and checks if required variables are present.
    If missing, prompts the user for the value and updates .env.
    """
    load_dotenv(dotenv_path=".env", override=True)
    required_vars = [
        "FHIR_IN_DIR",
        "OUTPUT_DIR",
        "LOGS_DIR",
        "DB_TYPE",
        "INIT_DB",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]
    updated_any = False
    for var in required_vars:
        val = os.getenv(var, "").strip()
        if not val:
            logging.info(f"Missing environment variable: {var}. Asking user to provide it.")
            new_val = input(f"Please provide a value for {var}: ").strip()
            if new_val:
                set_env(var, new_val)
                updated_any = True

    if updated_any:
        logging.info("Some environment variables were updated. Reloading .env.")
        load_dotenv(dotenv_path=".env", override=True)

def set_env(key, value):
    """
    Updates or appends `key=value` in the .env file.
    """
    env_file = ".env"
    lines = []
    found = False

    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break

    if not found:
        lines.append(f"{key}={value}\n")

    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    logging.info(f"Updated {key} in .env => {value}")

def get_db_connection():
    """
    Creates and returns a DB connection based on DB_TYPE env variable.
    Supported: Postgres (psycopg2), Oracle (cx_Oracle), MSSQL (pyodbc).
    """
    db_type = os.getenv("DB_TYPE", "").lower()
    db_host = os.getenv("DB_HOST", "").strip()
    db_port = os.getenv("DB_PORT", "").strip()
    db_name = os.getenv("DB_NAME", "").strip()
    db_user = os.getenv("DB_USER", "").strip()
    db_pass = os.getenv("DB_PASSWORD", "").strip()

    if db_type == "postgres":
        if not psycopg2:
            raise RuntimeError("psycopg2 is not installed.")
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        return conn
    elif db_type == "oracle":
        if not cx_Oracle:
            raise RuntimeError("cx_Oracle is not installed.")
        dsn_tns = cx_Oracle.makedsn(db_host, db_port, service_name=db_name)
        conn = cx_Oracle.connect(db_user, db_pass, dsn_tns)
        return conn
    elif db_type in ("mssql", "sqlserver"):
        if not pyodbc:
            raise RuntimeError("pyodbc is not installed.")
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={db_host},{db_port};"
            f"DATABASE={db_name};"
            f"UID={db_user};"
            f"PWD={db_pass}"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    else:
        raise ValueError(f"Unsupported DB_TYPE: {db_type}")