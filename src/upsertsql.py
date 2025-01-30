import logging
import os
import json
import pathlib

def run():
    """
    Generates an upsert SQL script for each FHIR JSON file, 
    saved to a single .sql file in OUTPUT_DIR.
    This does NOT execute anything in the DB.
    """
    logging.info("[upsertsql] Generating upsert SQL script.")
    db_type = os.getenv("DB_TYPE", "").lower()
    fhir_in_dir = os.getenv("FHIR_IN_DIR", "").strip()
    output_dir = os.getenv("OUTPUT_DIR", "").strip()
    if not fhir_in_dir or not os.path.isdir(fhir_in_dir):
        logging.error(f"[upsertsql] Invalid FHIR_IN_DIR: {fhir_in_dir}")
        return
    if not output_dir:
        logging.error("[upsertsql] OUTPUT_DIR not set.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "upsert_generated.sql")

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
                raw_str = json.dumps(data).replace("'", "''")  # Escape quotes

                if not resource_id:
                    continue

                # Build the upsert snippet depending on DB
                if db_type == "postgres":
                    stmt = f"""
INSERT INTO {table_name} (id, resource_type, raw_content)
VALUES ('{resource_id}', '{resource_type}', '{raw_str}')
ON CONFLICT (id)
DO UPDATE SET resource_type = EXCLUDED.resource_type,
              raw_content   = EXCLUDED.raw_content;
""".strip()
                    all_sql_statements.append(stmt)

                elif db_type == "oracle":
                    stmt = f"""
MERGE INTO {table_name} t
USING (SELECT '{resource_id}' AS id, '{resource_type}' AS resource_type, '{raw_str}' AS raw_content FROM DUAL) src
ON (t.id = src.id)
WHEN MATCHED THEN
  UPDATE SET t.resource_type = src.resource_type,
             t.raw_content   = src.raw_content
WHEN NOT MATCHED THEN
  INSERT (id, resource_type, raw_content)
  VALUES (src.id, src.resource_type, src.raw_content);
""".strip()
                    all_sql_statements.append(stmt)

                elif db_type in ("mssql", "sqlserver"):
                    stmt = f"""
MERGE {table_name} AS T
USING (SELECT '{resource_id}' AS id, '{resource_type}' AS resource_type, '{raw_str}' AS raw_content) AS S
ON (T.id = S.id)
WHEN MATCHED THEN
  UPDATE SET resource_type = S.resource_type,
             raw_content   = S.raw_content
WHEN NOT MATCHED THEN
  INSERT (id, resource_type, raw_content)
  VALUES (S.id, S.resource_type, S.raw_content);
""".strip()
                    all_sql_statements.append(stmt)
                else:
                    logging.error(f"[upsertsql] Unsupported DB_TYPE: {db_type}")
                    return

            except Exception as e:
                logging.exception(f"[upsertsql] Failed to build statement for {fpath}: {e}")

    # Write all statements to a single file
    if all_sql_statements:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n".join(all_sql_statements))
            out.write("\n")
        logging.info(f"[upsertsql] Generated {len(all_sql_statements)} statements in {output_file}.")
    else:
        logging.info("[upsertsql] No SQL statements generated.")