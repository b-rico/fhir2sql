import logging
import os
import json
import pathlib

from .common import get_db_connection

def run():
    """
    Reads JSON files from FHIR_IN_DIR subfolders, upserts them into 
    the respective tables (named after the folder).
    """
    logging.info("[upsertdb] Starting upsert process.")
    fhir_in_dir = os.getenv("FHIR_IN_DIR", "").strip()
    if not fhir_in_dir or not os.path.isdir(fhir_in_dir):
        logging.error(f"[upsertdb] FHIR_IN_DIR is invalid: {fhir_in_dir}")
        return

    db_type = os.getenv("DB_TYPE", "").lower()
    conn = None
    try:
        conn = get_db_connection()
        logging.info("[upsertdb] Database connection established.")
        process_folders(db_type, conn, fhir_in_dir)
    except Exception as exc:
        logging.exception(f"[upsertdb] Error during upsert process: {exc}")
    finally:
        if conn:
            conn.close()
            logging.info("[upsertdb] Database connection closed.")

def process_folders(db_type, conn, base_path):
    """
    For each subfolder in FHIR_IN_DIR, read .json files, 
    then upsert them into the matching table name.
    """
    subdirs = [d for d in os.scandir(base_path) if d.is_dir()]

    for sub in subdirs:
        table_name = sub.name.lower()
        logging.info(f"[upsertdb] Processing folder '{table_name}'.")
        json_files = list(pathlib.Path(sub.path).glob("*.json"))
        if not json_files:
            logging.info(f"[upsertdb] No JSON files found in {sub.path}. Skipping.")
            continue

        with conn.cursor() as cur:
            for fpath in json_files:
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    _upsert_record(db_type, cur, table_name, data)
                except Exception as e:
                    logging.exception(f"[upsertdb] Failed to upsert {fpath}: {e}")
            conn.commit()

def _upsert_record(db_type, cursor, table_name, resource_json):
    """
    Upserts a single resource record into the table. 
    Expects columns: id (pk), resource_type, raw_content.
    """
    resource_id = resource_json.get("id", "")
    if not resource_id:
        # If there's no "id" field, skip
        logging.warning(f"[upsertdb] Resource in table {table_name} has no 'id'. Skipped.")
        return

    resource_type = resource_json.get("resourceType", table_name)
    raw_str = json.dumps(resource_json)

    if db_type == "postgres":
        sql = f"""
            INSERT INTO {table_name} (id, resource_type, raw_content)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) 
            DO UPDATE SET 
                resource_type = EXCLUDED.resource_type,
                raw_content   = EXCLUDED.raw_content
        """
        cursor.execute(sql, (resource_id, resource_type, raw_str))

    elif db_type == "oracle":
        # Oracle MERGE
        sql = f"""
            MERGE INTO {table_name} t
            USING (SELECT :id AS id, :rtype AS resource_type, :rcont AS raw_content FROM DUAL) src
            ON (t.id = src.id)
            WHEN MATCHED THEN
                UPDATE SET 
                    t.resource_type = src.resource_type,
                    t.raw_content   = src.raw_content
            WHEN NOT MATCHED THEN
                INSERT (id, resource_type, raw_content)
                VALUES (src.id, src.resource_type, src.raw_content)
        """
        cursor.execute(sql, [resource_id, resource_type, raw_str])

    elif db_type in ("mssql", "sqlserver"):
        # SQL Server MERGE
        sql = f"""
            MERGE {table_name} AS T
            USING (SELECT ? AS id, ? AS resource_type, ? AS raw_content) AS S
            ON (T.id = S.id)
            WHEN MATCHED THEN
                UPDATE SET 
                    resource_type = S.resource_type,
                    raw_content   = S.raw_content
            WHEN NOT MATCHED THEN
                INSERT (id, resource_type, raw_content)
                VALUES (S.id, S.resource_type, S.raw_content);
        """
        cursor.execute(sql, (resource_id, resource_type, raw_str))
    else:
        raise ValueError(f"[upsertdb] Unsupported DB_TYPE for upsert: {db_type}")

    logging.info(f"[upsertdb] Upserted resource '{resource_id}' into '{table_name}'.")