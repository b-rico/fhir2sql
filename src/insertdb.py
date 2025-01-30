import logging
import os
import json
import pathlib

from .common import get_db_connection

def run():
    """
    Reads JSON files from FHIR_IN_DIR and inserts them into 
    the respective tables. If duplicates exist, we skip or log an error.
    """
    logging.info("[insertdb] Starting insert process.")
    fhir_in_dir = os.getenv("FHIR_IN_DIR", "").strip()
    if not fhir_in_dir or not os.path.isdir(fhir_in_dir):
        logging.error(f"[insertdb] FHIR_IN_DIR is invalid: {fhir_in_dir}")
        return

    db_type = os.getenv("DB_TYPE", "").lower()
    conn = None
    try:
        conn = get_db_connection()
        logging.info("[insertdb] Database connection established.")
        process_folders(db_type, conn, fhir_in_dir)
    except Exception as exc:
        logging.exception(f"[insertdb] Error during insert process: {exc}")
    finally:
        if conn:
            conn.close()
            logging.info("[insertdb] Database connection closed.")

def process_folders(db_type, conn, base_path):
    subdirs = [d for d in os.scandir(base_path) if d.is_dir()]

    for sub in subdirs:
        table_name = sub.name.lower()
        logging.info(f"[insertdb] Processing folder '{table_name}'.")
        json_files = list(pathlib.Path(sub.path).glob("*.json"))
        if not json_files:
            logging.info(f"[insertdb] No JSON files in {sub.path}. Skipping.")
            continue

        with conn.cursor() as cur:
            for fpath in json_files:
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    _insert_record(db_type, cur, table_name, data)
                except Exception as e:
                    logging.exception(f"[insertdb] Failed to insert {fpath}: {e}")
            conn.commit()

def _insert_record(db_type, cursor, table_name, resource_json):
    resource_id = resource_json.get("id", "")
    if not resource_id:
        logging.warning(f"[insertdb] Resource in table {table_name} has no 'id'. Skipped.")
        return

    resource_type = resource_json.get("resourceType", table_name)
    raw_str = json.dumps(resource_json)

    if db_type == "postgres":
        # Attempt a simple insert, ignoring duplicates with ON CONFLICT DO NOTHING.
        sql = f"""
            INSERT INTO {table_name} (id, resource_type, raw_content)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """
        cursor.execute(sql, (resource_id, resource_type, raw_str))

    elif db_type == "oracle":
        # Attempt to insert; if duplicate, log error. We can catch the exception.
        sql = f"""
            INSERT INTO {table_name} (id, resource_type, raw_content)
            VALUES (:id, :rtype, :rcont)
        """
        try:
            cursor.execute(sql, [resource_id, resource_type, raw_str])
        except Exception as ex:
            logging.warning(f"[insertdb] Oracle insert duplicate for ID={resource_id} in {table_name}: {ex}")

    elif db_type in ("mssql", "sqlserver"):
        # Attempt insert, catch duplicates
        sql = f"""
            INSERT INTO {table_name} (id, resource_type, raw_content)
            VALUES (?, ?, ?)
        """
        try:
            cursor.execute(sql, (resource_id, resource_type, raw_str))
        except Exception as ex:
            logging.warning(f"[insertdb] SQL Server insert duplicate for ID={resource_id} in {table_name}: {ex}")
    else:
        raise ValueError(f"[insertdb] Unsupported DB_TYPE: {db_type}")

    logging.info(f"[insertdb] Inserted resource '{resource_id}' into '{table_name}'.")