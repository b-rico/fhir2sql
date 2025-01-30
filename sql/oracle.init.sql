-- Oracle CREATE TABLE statements

CREATE TABLE patient (
    patient_id   VARCHAR2(64)  NOT NULL,
    first_name   VARCHAR2(255),
    last_name    VARCHAR2(255),
    birth_date   DATE,
    gender       VARCHAR2(50),
    address      CLOB,
    phone        VARCHAR2(50),
    member_id    VARCHAR2(64),
    CONSTRAINT pk_patient PRIMARY KEY (patient_id)
);

CREATE TABLE encounter (
    encounter_id   VARCHAR2(64) NOT NULL,
    patient_id     VARCHAR2(64) NOT NULL,
    encounter_dt   TIMESTAMP,
    encounter_cls  VARCHAR2(50),
    status         VARCHAR2(50),
    provider_id    VARCHAR2(64),
    CONSTRAINT pk_encounter PRIMARY KEY (encounter_id),
    CONSTRAINT fk_encounter_patient
        FOREIGN KEY (patient_id) REFERENCES patient (patient_id)
);

CREATE TABLE condition_resource (
    condition_id    VARCHAR2(64) NOT NULL,
    patient_id      VARCHAR2(64) NOT NULL,
    encounter_id    VARCHAR2(64),
    code            VARCHAR2(50),
    description     VARCHAR2(255),
    onset_date      DATE,
    verification    VARCHAR2(50),
    clinical_stat   VARCHAR2(50),
    CONSTRAINT pk_condition_resource PRIMARY KEY (condition_id),
    CONSTRAINT fk_condition_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_condition_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE observation (
    observation_id  VARCHAR2(64) NOT NULL,
    patient_id      VARCHAR2(64) NOT NULL,
    encounter_id    VARCHAR2(64),
    code            VARCHAR2(50),
    description     VARCHAR2(255),
    value           VARCHAR2(50),
    unit            VARCHAR2(50),
    effective_dt    TIMESTAMP,
    status          VARCHAR2(50),
    CONSTRAINT pk_observation PRIMARY KEY (observation_id),
    CONSTRAINT fk_observation_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_observation_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE medication_statement (
    med_statement_id   VARCHAR2(64) NOT NULL,
    patient_id         VARCHAR2(64) NOT NULL,
    encounter_id       VARCHAR2(64),
    medication_code    VARCHAR2(50),
    medication_display VARCHAR2(255),
    effective_start_dt DATE,
    effective_end_dt   DATE,
    status             VARCHAR2(50),
    CONSTRAINT pk_med_statement PRIMARY KEY (med_statement_id),
    CONSTRAINT fk_medstatement_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_medstatement_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE procedure_resource (
    procedure_id   VARCHAR2(64) NOT NULL,
    patient_id     VARCHAR2(64) NOT NULL,
    encounter_id   VARCHAR2(64),
    code           VARCHAR2(50),
    description    VARCHAR2(255),
    performed_dt   TIMESTAMP,
    status         VARCHAR2(50),
    CONSTRAINT pk_procedure_resource PRIMARY KEY (procedure_id),
    CONSTRAINT fk_procedure_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_procedure_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE document_reference (
    docref_id       VARCHAR2(64) NOT NULL,
    patient_id      VARCHAR2(64),
    encounter_id    VARCHAR2(64),
    type_code       VARCHAR2(50),
    type_display    VARCHAR2(255),
    content_url     CLOB,
    content_format  VARCHAR2(50),
    created_dt      TIMESTAMP,
    doc_status      VARCHAR2(50),
    description     CLOB,
    CONSTRAINT pk_document_reference PRIMARY KEY (docref_id),
    CONSTRAINT fk_documentreference_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_documentreference_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE provenance (
    provenance_id    VARCHAR2(64) NOT NULL,
    target_resource  VARCHAR2(128),
    recorded_dt      TIMESTAMP,
    agent_type       VARCHAR2(50),
    agent_who_ref    VARCHAR2(64),
    signature_type   VARCHAR2(50),
    signature_when   TIMESTAMP,
    signature_who    VARCHAR2(64),
    CONSTRAINT pk_provenance PRIMARY KEY (provenance_id)
);

CREATE TABLE immunization (
    immunization_id   VARCHAR2(64) NOT NULL,
    patient_id        VARCHAR2(64) NOT NULL,
    encounter_id      VARCHAR2(64),
    status            VARCHAR2(50),
    vaccine_code      VARCHAR2(50),
    vaccine_display   VARCHAR2(255),
    occurrence_dt     TIMESTAMP,
    lot_number        VARCHAR2(50),
    performer_ref     VARCHAR2(64),
    CONSTRAINT pk_immunization PRIMARY KEY (immunization_id),
    CONSTRAINT fk_immunization_patient
        FOREIGN KEY (patient_id)   REFERENCES patient (patient_id),
    CONSTRAINT fk_immunization_encounter
        FOREIGN KEY (encounter_id) REFERENCES encounter (encounter_id)
);

CREATE TABLE practitioner (
    practitioner_id   VARCHAR2(64) NOT NULL,
    npi               VARCHAR2(20),
    first_name        VARCHAR2(255),
    last_name         VARCHAR2(255),
    phone             VARCHAR2(50),
    email             VARCHAR2(255),
    address           CLOB,
    specialty_code    VARCHAR2(50),
    specialty_display VARCHAR2(255),
    CONSTRAINT pk_practitioner PRIMARY KEY (practitioner_id)
);

CREATE TABLE organization (
    organization_id   VARCHAR2(64) NOT NULL,
    name              VARCHAR2(255),
    type_code         VARCHAR2(50),
    type_display      VARCHAR2(255),
    address           CLOB,
    phone             VARCHAR2(50),
    email             VARCHAR2(255),
    CONSTRAINT pk_organization PRIMARY KEY (organization_id)
);