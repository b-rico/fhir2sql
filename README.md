# FHIR2SQL

A minimal Python-based pipeline that ingests FHIR resource files (including CDex) and loads them into a relational database. This is an MVP project demonstrating how to organize scripts for **upserting**, **inserting**, **truncating** tables, and generating **SQL scripts** from FHIR JSON data. It also includes a utility to **update environment variables** via the command line.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [Command-Line Flags](#command-line-flags)
  - [Examples](#examples)
- [Database Schema](#database-schema)
- [Logs](#logs)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## Overview

`FHIR2SQL` organizes your Python code to:

1. **Ingest JSON files** from a directory structure mirroring FHIR resource types (e.g. `patient`, `organization`, `observation`, etc.).
2. **Load data into a relational database** (PostgreSQL, Oracle, or MS SQL Server).
3. Provide **SQL script generators** for offline execution.
4. Support a **configurable** environment via `.env`.
5. Write **logs** to a specified directory.

This MVP helps you quickly set up an end-to-end pipeline for FHIR data ingestion. It’s intended for demonstration and not production-ready out of the box.

---

## Features

- **Multi-Database Support**  
  - Easily switch between PostgreSQL, Oracle, or MSSQL by changing `DB_TYPE`.
- **Multiple Loading Modes**  
  - **Upsert** (insert or update existing rows), **Insert** (no updates), **Truncate & Insert** (clear tables, then insert).
- **Auto-Generated SQL**  
  - Create standalone SQL scripts for Upsert or Insert without executing them in the DB.
- **Environment Management**  
  - Prompt to fill missing variables on the fly.  
  - Update `.env` interactively.
- **Logging**  
  - Writes logs to a `runs.log` file, plus console output for real-time status.

---

## Directory Structure

.
├─ .env               # Your main environment variables file
├─ .env.example       # Sample environment variables template
├─ main.py            # Entry point script
├─ src/
│  ├─ init.py
│  ├─ common.py       # Shared logic: DB connection, logging setup, env loading
│  ├─ upsertdb.py     # Logic for upserting JSON data
│  ├─ insertdb.py     # Logic for inserting JSON data
│  ├─ truncdb.py      # Logic for truncating & loading JSON data
│  ├─ upsertsql.py    # Generates upsert SQL
│  ├─ insertsql.py    # Generates insert SQL
│  └─ updateenv.py    # Interactively updates .env variables
└─ requirements.txt    # Python dependencies (optional)

- **`fhir_in/`** (not shown above)  
  A suggested directory for your actual FHIR JSON files. Subfolders like `patient/`, `observation/`, etc. should store `.json` files.

---

## Requirements

- **Python 3.8+**  
- **pip** or another package manager for Python libraries
- One or more DB driver libraries, depending on the target:
  - `psycopg2` (for PostgreSQL)
  - `cx_Oracle` (for Oracle)
  - `pyodbc` (for MS SQL Server)
- **`python-dotenv`** for environment variable management

Install via:

```bash
pip install python-dotenv psycopg2 cx_Oracle pyodbc
```

## Environment Variables

In your .env file set:

```ini
# Script Variables
FHIR_IN_DIR=                # Path to the input FHIR data directory
OUTPUT_DIR=                 # Path to the output directory
LOGS_DIR=                   # Path to the logs directory
DB_TYPE=                    # Valid values are "postgres", "oracle", or "mssql"
INIT_DB=                    # Valid values are "True" or "False". True will trigger creation of the database schema.

# Database Credentials
DB_HOST=                    # Hostname of the database server
DB_PORT=                    # Port number for the database
DB_NAME=                    # Database name
DB_USER=                    # Database user
DB_PASSWORD=                # Password for the database user
DB_TYPE=                    # "postgres" or "oracle" or "mssql"
```

If any required variables are missing, the script will prompt you for them on the first run and update .env.

## Usage
	1.	Place your FHIR JSON files under FHIR_IN_DIR, with each resource type in its own subfolder (e.g. fhir_in/patient, fhir_in/organization, etc.).
	2.	Customize your .env settings.
	3.	Run with one of the flags below:

### Command-Line Flags

|       Flag        |                                           Action                                              |
|-------------------|-----------------------------------------------------------------------------------------------|
|-upsertdb          |	Reads all JSON files and upserts them into the DB (insert if new, update if existing).      |
|-insertdb          |	Reads JSON files and inserts new rows only. Duplicates are ignored or cause a warning.      |
|-truncdb           |	Truncates existing tables, then loads all JSON data. Useful for a fresh load scenario.      |
|-upsertsql         |	Generates upsert SQL scripts (does not execute). Saved to OUTPUT_DIR/upsert_generated.sql.  |
|-insertsql         |	Generates insert SQL scripts (does not execute). Saved to OUTPUT_DIR/insert_generated.sql.  |
|-updateenv         |	Interactively update environment variables in .env.                                         |

#### Examples

```bash
python main.py -upsertdb
python main.py -insertdb
python main.py -truncdb
python main.py -upsertsql
python main.py -insertsql
python main.py -updateenv
```

## Database Schema

Each resource subfolder is mapped to a table named after the folder. By default, the scripts assume a very simple table structure, for example:

```sql
CREATE TABLE patient (
    patient_id   VARCHAR(64)  PRIMARY KEY,
    first_name   VARCHAR(255),
    last_name    VARCHAR(255),
    birth_date   DATE,
    gender       VARCHAR(50),
    address      TEXT,
    phone        VARCHAR(50),
    member_id    VARCHAR(64)
);
```

You must create these tables in advance or modify the scripts to run DDL automatically (e.g. if you extend the INIT_DB logic).

See [Data Dictionary](DATA_DICTIONARY.md)

## Logs

	•	Logs are written to a file named runs.log in the directory specified by LOGS_DIR.
	•	The output is also mirrored to console so you can follow progress in real time.

Example snippet from runs.log:

```bash
2025-01-30 10:15:42 [INFO] Database connection established.
2025-01-30 10:15:42 [INFO] Upserting resource 'example-patient-1' into 'patient'.
2025-01-30 10:15:43 [INFO] Successfully completed upsertdb process.
```

## License

Coopyright © Berto J. Rico, 2025
This project is licensed under [Apache v2.0 2004](LICENSE)

## Disclaimer

     __
    /  \
   /    \
   \    /
    \  /
     \/
   
    ---
   |   |
    ---

This repository is an MVP / reference. It does not address production concerns such as:
**Security (e.g., encryption, secure credential management)**
**High availability or scalability**
**Compliance with standards like HIPAA or GDPR when handling patient data**

!!! Use caution and adapt to your organizational requirements before deploying in a production environment. !!!
     __
    /  \
   /    \
   \    /
    \  /
     \/
   
    ---
   |   |
    ---