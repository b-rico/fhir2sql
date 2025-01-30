import logging
import os
import json
import pathlib

from .common import get_db_connection

def run():
    """
    Truncates each known resource table, then inserts all records from FHIR_IN_DIR.
    """
    logging.info("[truncdb] Starting truncate & load process.")
    fhir_in_dir = os.getenv("FHIR_IN_DIR", "").strip()
    if not fhir_in_dir or not os.path.isdir(fhir_in_dir):
        logging.error(f"[truncdb] FHIR_IN_DIR is invalid: {fhir_in_dir}")
        return

    db_type = os.getenv("DB_TYPE", "").lower()
    conn = None
    try:
        conn = get_db_connection()
        logging.info("[truncdb] Database connection established.")
        all_subdirs = [d for d in os.scandir(fhir_in_dir) if d.is_dir()]
        table_names = [sub.name.lower() for sub in all_subdirs]

        # Truncate each table
        with conn.cursor() as cur:
            for tname in table_names:
                _truncate_table(db_type, cur, tname)
            conn.commit()

        # Insert all data
        for sub in all_subdirs:
            _insert_folder(db_type, conn, sub.name.lower(), sub.path)

    except Exception as exc:
        logging.exception(f"[truncdb] Error during trunc & load process: {exc}")
    finally:
        if conn:
            conn.close()
            logging.info("[truncdb] Database connection closed.")

def _truncate_table(db_type, cursor, table_name):
    if db_type == "postgres":
        sql = f"TRUNCATE TABLE {table_name} RESTART IDENTITY"
    elif db_type == "oracle":
        sql = f"TRUNCATE TABLE {table_name}"
    elif db_type in ("mssql", "sqlserver"):
        sql = f"TRUNCATE TABLE {table_name}"
    else:
        raise ValueError(f"[truncdb] Unsupported DB_TYPE for truncate: {db_type}")
    cursor.execute(sql)
    logging.info(f"[truncdb] Truncated table '{table_name}'.")

def _insert_folder(db_type, conn, table_name, folder_path):
    logging.info(f"[truncdb] Inserting from {folder_path} into {table_name}.")
    json_files = list(pathlib.Path(folder_path).glob("*.json"))
    if not json_files:
        logging.info(f"[truncdb] No JSON files in {folder_path}. Skipping.")
        return

    with conn.cursor() as cur:
        for fpath in json_files:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                resource_id = data.get("id", "")
                resource_type = data.get("resourceType", table_name)
                raw_str = json.dumps(data)

                if db_type == "postgres":
                    sql = f"INSERT INTO {table_name} (id, resource_type, raw_content) VALUES (%s, %s, %s)"
                    cur.execute(sql, (resource_id, resource_type, raw_str))
                elif db_type == "oracle":
                    sql = f"INSERT INTO {table_name} (id, resource_type, raw_content) VALUES (:id, :rtype, :rcont)"
                    cur.execute(sql, [resource_id, resource_type, raw_str])
                elif db_type in ("mssql", "sqlserver"):
                    sql = f"INSERT INTO {table_name} (id, resource_type, raw_content) VALUES (?, ?, ?)"
                    cur.execute(sql, (resource_id, resource_type, raw_str))
                else:
                    raise ValueError(f"[truncdb] Unsupported DB_TYPE for insert after trunc: {db_type}")

                logging.info(f"[truncdb] Inserted {resource_id} into {table_name}.")
            except Exception as e:
                logging.exception(f"[truncdb] Error inserting file {fpath}: {e}")

        conn.commit()