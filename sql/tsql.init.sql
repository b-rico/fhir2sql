-- SQL Server CREATE TABLE statements

CREATE TABLE patient (
    patient_id   VARCHAR(64)   NOT NULL PRIMARY KEY,
    first_name   VARCHAR(255),
    last_name    VARCHAR(255),
    birth_date   DATE,
    gender       VARCHAR(50),
    address      VARCHAR(MAX),
    phone        VARCHAR(50),
    member_id    VARCHAR(64)
);

CREATE TABLE encounter (
    encounter_id   VARCHAR(64)   NOT NULL PRIMARY KEY,
    patient_id     VARCHAR(64)   NOT NULL,
    encounter_dt   DATETIME2,
    encounter_cls  VARCHAR(50),
    status         VARCHAR(50),
    provider_id    VARCHAR(64),
    CONSTRAINT fk_encounter_patient
        FOREIGN KEY (patient_id) REFERENCES patient (patient_id)
);

CREATE TABLE condition_resource (
    condition_id    VARCHAR(64)   NOT NULL PRIMARY KEY,
    patient_id      VARCHAR(64)   NOT NULL,
    encounter_id    VARCHAR(64),
    code            VARCHAR(50),
    description     VARCHAR(255),
    onset_date      DATE,
    verification    VARCHAR(50),
    clinical_stat   VARCHAR(50),
    CONSTRAINT fk_condition_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_condition_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE observation (
    observation_id  VARCHAR(64)   NOT NULL PRIMARY KEY,
    patient_id      VARCHAR(64)   NOT NULL,
    encounter_id    VARCHAR(64),
    code            VARCHAR(50),
    description     VARCHAR(255),
    value           VARCHAR(50),
    unit            VARCHAR(50),
    effective_dt    DATETIME2,
    status          VARCHAR(50),
    CONSTRAINT fk_observation_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_observation_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE medication_statement (
    med_statement_id   VARCHAR(64)   NOT NULL PRIMARY KEY,
    patient_id         VARCHAR(64)   NOT NULL,
    encounter_id       VARCHAR(64),
    medication_code    VARCHAR(50),
    medication_display VARCHAR(255),
    effective_start_dt DATE,
    effective_end_dt   DATE,
    status             VARCHAR(50),
    CONSTRAINT fk_medstatement_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_medstatement_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE procedure_resource (
    procedure_id   VARCHAR(64)   NOT NULL PRIMARY KEY,
    patient_id     VARCHAR(64)   NOT NULL,
    encounter_id   VARCHAR(64),
    code           VARCHAR(50),
    description    VARCHAR(255),
    performed_dt   DATETIME2,
    status         VARCHAR(50),
    CONSTRAINT fk_procedure_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_procedure_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE document_reference (
    docref_id       VARCHAR(64)   NOT NULL PRIMARY KEY,
    patient_id      VARCHAR(64),
    encounter_id    VARCHAR(64),
    type_code       VARCHAR(50),
    type_display    VARCHAR(255),
    content_url     VARCHAR(MAX),
    content_format  VARCHAR(50),
    created_dt      DATETIME2,
    doc_status      VARCHAR(50),
    description     VARCHAR(MAX),
    CONSTRAINT fk_documentreference_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_documentreference_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE provenance (
    provenance_id    VARCHAR(64)   NOT NULL PRIMARY KEY,
    target_resource  VARCHAR(128),
    recorded_dt      DATETIME2,
    agent_type       VARCHAR(50),
    agent_who_ref    VARCHAR(64),
    signature_type   VARCHAR(50),
    signature_when   DATETIME2,
    signature_who    VARCHAR(64)
);

CREATE TABLE immunization (
    immunization_id   VARCHAR(64)   NOT NULL PRIMARY KEY,
    patient_id        VARCHAR(64)   NOT NULL,
    encounter_id      VARCHAR(64),
    status            VARCHAR(50),
    vaccine_code      VARCHAR(50),
    vaccine_display   VARCHAR(255),
    occurrence_dt     DATETIME2,
    lot_number        VARCHAR(50),
    performer_ref     VARCHAR(64),
    CONSTRAINT fk_immunization_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_immunization_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE practitioner (
    practitioner_id   VARCHAR(64)   NOT NULL PRIMARY KEY,
    npi               VARCHAR(20),
    first_name        VARCHAR(255),
    last_name         VARCHAR(255),
    phone             VARCHAR(50),
    email             VARCHAR(255),
    address           VARCHAR(MAX),
    specialty_code    VARCHAR(50),
    specialty_display VARCHAR(255)
);

CREATE TABLE organization (
    organization_id   VARCHAR(64)   NOT NULL PRIMARY KEY,
    name              VARCHAR(255),
    type_code         VARCHAR(50),
    type_display      VARCHAR(255),
    address           VARCHAR(MAX),
    phone             VARCHAR(50),
    email             VARCHAR(255)
);