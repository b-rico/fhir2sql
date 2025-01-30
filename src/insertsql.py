import logging
import os
import json
import pathlib

def run():
    """
    Generates an insert-only SQL script for each FHIR JSON file, 
    saved to a single .sql file in OUTPUT_DIR.
    This does NOT execute anything in the DB.
    """
    logging.info("[insertsql] Generating insert SQL script.")
    db_type = os.getenv("DB_TYPE", "").lower()
    fhir_in_dir = os.getenv("FHIR_IN_DIR", "").strip()
    output_dir = os.getenv("OUTPUT_DIR", "").strip()
    if not fhir_in_dir or not os.path.isdir(fhir_in_dir):
        logging.error(f"[insertsql] Invalid FHIR_IN_DIR: {fhir_in_dir}")
        return
    if not output_dir:
        logging.error("[insertsql] OUTPUT_DIR not set.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "insert_generated.sql")

    all_sql_statements = []
    subdirs = [d for d in os.scandir(fhir_in_dir) if d.is_dir()]
    for sub in subdirs:
        table_name = sub.name.lower()
        json_files = list(pathlib.Path(sub.path).glob("*.json"))
        for fpath in json_files:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                resource_id = data.get("id", "")
                resource_type = data.get("resourceType", table_name)
                raw_str = json.dumps(data).replace("'", "''")

                if not resource_id:
                    continue

                # Build an insert statement
                if db_type in ("postgres", "oracle", "mssql", "sqlserver"):
                    stmt = f"""
INSERT INTO {table_name} (id, resource_type, raw_content)
VALUES ('{resource_id}', '{resource_type}', '{raw_str}');
""".strip()
                    all_sql_statements.append(stmt)
                else:
                    logging.error(f"[insertsql] Unsupported DB_TYPE: {db_type}")
                    return

            except Exception as e:
                logging.exception(f"[insertsql] Failed to build statement for {fpath}: {e}")

    # Write all statements to a single file
    if all_sql_statements:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n".join(all_sql_statements))
            out.write("\n")
        logging.info(f"[insertsql] Generated {len(all_sql_statements)} statements in {output_file}.")
    else:
        logging.info("[insertsql] No SQL statements generated.")