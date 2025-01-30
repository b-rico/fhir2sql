-- PostgreSQL CREATE TABLE statements

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

CREATE TABLE encounter (
    encounter_id   VARCHAR(64)  PRIMARY KEY,
    patient_id     VARCHAR(64)  NOT NULL,
    encounter_dt   TIMESTAMP,
    encounter_cls  VARCHAR(50),
    status         VARCHAR(50),
    provider_id    VARCHAR(64),
    FOREIGN KEY (patient_id) REFERENCES patient (patient_id)
);

CREATE TABLE condition_resource (
    condition_id    VARCHAR(64)  PRIMARY KEY,
    patient_id      VARCHAR(64)  NOT NULL,
    encounter_id    VARCHAR(64),
    code            VARCHAR(50),
    description     VARCHAR(255),
    onset_date      DATE,
    verification    VARCHAR(50),
    clinical_stat   VARCHAR(50),
    FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE observation (
    observation_id  VARCHAR(64)  PRIMARY KEY,
    patient_id      VARCHAR(64)  NOT NULL,
    encounter_id    VARCHAR(64),
    code            VARCHAR(50),
    description     VARCHAR(255),
    value           VARCHAR(50),
    unit            VARCHAR(50),
    effective_dt    TIMESTAMP,
    status          VARCHAR(50),
    FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE medication_statement (
    med_statement_id   VARCHAR(64)  PRIMARY KEY,
    patient_id         VARCHAR(64)  NOT NULL,
    encounter_id       VARCHAR(64),
    medication_code    VARCHAR(50),
    medication_display VARCHAR(255),
    effective_start_dt DATE,
    effective_end_dt   DATE,
    status             VARCHAR(50),
    FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE procedure_resource (
    procedure_id   VARCHAR(64)  PRIMARY KEY,
    patient_id     VARCHAR(64)  NOT NULL,
    encounter_id   VARCHAR(64),
    code           VARCHAR(50),
    description    VARCHAR(255),
    performed_dt   TIMESTAMP,
    status         VARCHAR(50),
    FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE document_reference (
    docref_id        VARCHAR(64)  PRIMARY KEY,
    patient_id       VARCHAR(64),
    encounter_id     VARCHAR(64),
    type_code        VARCHAR(50),
    type_display     VARCHAR(255),
    content_url      TEXT,
    content_format   VARCHAR(50),
    created_dt       TIMESTAMP,
    doc_status       VARCHAR(50),
    description      TEXT,
    FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE provenance (
    provenance_id    VARCHAR(64)  PRIMARY KEY,
    target_resource  VARCHAR(128),
    recorded_dt      TIMESTAMP,
    agent_type       VARCHAR(50),
    agent_who_ref    VARCHAR(64),
    signature_type   VARCHAR(50),
    signature_when   TIMESTAMP,
    signature_who    VARCHAR(64)
    -- In practice, you might store references to practitioner/organization if needed
);

CREATE TABLE immunization (
    immunization_id   VARCHAR(64)  PRIMARY KEY,
    patient_id        VARCHAR(64)  NOT NULL,
    encounter_id      VARCHAR(64),
    status            VARCHAR(50),
    vaccine_code      VARCHAR(50),
    vaccine_display   VARCHAR(255),
    occurrence_dt     TIMESTAMP,
    lot_number        VARCHAR(50),
    performer_ref     VARCHAR(64),
    FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE practitioner (
    practitioner_id   VARCHAR(64)  PRIMARY KEY,
    npi               VARCHAR(20),
    first_name        VARCHAR(255),
    last_name         VARCHAR(255),
    phone             VARCHAR(50),
    email             VARCHAR(255),
    address           TEXT,
    specialty_code    VARCHAR(50),
    specialty_display VARCHAR(255)
);

CREATE TABLE organization (
    organization_id   VARCHAR(64)  PRIMARY KEY,
    name              VARCHAR(255),
    type_code         VARCHAR(50),
    type_display      VARCHAR(255),
    address           TEXT,
    phone             VARCHAR(50),
    email             VARCHAR(255)
);