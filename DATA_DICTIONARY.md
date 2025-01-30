# Data Dictionary

## Call Outs & Notes

Reserved Words:
	•	Tables like condition or procedure might clash with SQL reserved words. We’ve used _resource suffix to avoid conflicts.

Data Types:
	•	Shown here in a generic SQL form (VARCHAR, TEXT, TIMESTAMP), but actual usage varies by DB (PostgreSQL, Oracle, SQL Server).
	•	For large text fields, use TEXT (Postgres), VARCHAR(MAX) (SQL Server), or CLOB (Oracle).

Foreign Keys:
	•	Each resource table references patient_id or encounter_id if relevant, establishing relationships.

Indexing:
	•	In production, add indexes (e.g., on patient_id, encounter_id, status, or date columns) to optimize queries.

Versioning:
	•	If you need FHIR versioning (resource.meta.versionId), add a version column or store older versions in a history table.

Customization:
	•	Add or remove columns based on the fields you actually need to store from each FHIR resource.
	•	Some implementers store the entire raw JSON in a column (e.g., raw_content) and selectively parse out key fields.


## Table: patient
### Description: 
- Stores patient demographic and identifying information from FHIR Patient resources.

| Column      | Type         | Description                                                                                 |
|-------------|------------- |---------------------------------------------------------------------------------------------|
| patient_id  | VARCHAR(64)  | **Primary key**. FHIR `Patient.id`.                                                         |
| first_name  | VARCHAR(255) | Patient’s first name (from `Patient.name[0].given[0]`).                                     |
| last_name   | VARCHAR(255) | Patient’s last name (from `Patient.name[0].family`).                                        |
| birth_date  | DATE         | Patient’s date of birth (`Patient.birthDate`).                                              |
| gender      | VARCHAR(50)  | Patient’s gender (`Patient.gender`).                                                        |
| address     | TEXT         | Text or JSON representation of `Patient.address[0]`.                                        |
| phone       | VARCHAR(50)  | Patient’s phone number (`Patient.telecom` if phone).                                        |
| member_id   | VARCHAR(64)  | Health plan member ID if different from `Patient.id`.                                       |

## Table: encounter
### Description: 
- Holds encounter data from FHIR Encounter resources, including date/time and type of visit.

| Column       | Type         | Description                                                                                          |
|------------- |------------- |------------------------------------------------------------------------------------------------------|
| encounter_id | VARCHAR(64)  | **Primary key**. FHIR `Encounter.id`.                                                                |
| patient_id   | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                        |
| encounter_dt | TIMESTAMP    | Date/time the encounter took place (`Encounter.period.start` or `.end`).                             |
| encounter_cls| VARCHAR(50)  | Encounter class/type code (`Encounter.class.code` or `Encounter.type[0].coding[0].code`).            |
| status       | VARCHAR(50)  | The encounter’s status (`Encounter.status`).                                                         |
| provider_id  | VARCHAR(64)  | Optional foreign key to `practitioner` or `organization` if you store who performed the service.      |

## Table: condition_resource 
### Description:
- Captures clinical diagnoses from FHIR Condition resources (e.g., SNOMED/ICD-10 codes).

| Column        | Type         | Description                                                                                                       |
|-------------- |------------- |-------------------------------------------------------------------------------------------------------------------|
| condition_id  | VARCHAR(64)  | **Primary key**. FHIR `Condition.id`.                                                                              |
| patient_id    | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                                      |
| encounter_id  | VARCHAR(64)  | Optional foreign key referencing `encounter.encounter_id` (if condition ties to a specific encounter).            |
| code          | VARCHAR(50)  | Condition code (SNOMED, ICD-10, etc.) (`Condition.code.coding[0].code`).                                          |
| description   | VARCHAR(255) | Human-readable display for the code (`Condition.code.coding[0].display`).                                         |
| onset_date    | DATE         | Onset date/time of the condition (`Condition.onsetDateTime`).                                                     |
| verification  | VARCHAR(50)  | Verification status of the condition (`Condition.verificationStatus`).                                            |
| clinical_stat | VARCHAR(50)  | Clinical status (`Condition.clinicalStatus`), e.g. active, resolved.                                              |

## Table:  observation
### Description: 
- Stores lab results, vital signs, or other measurements from FHIR Observation resources.

| Column         | Type         | Description                                                                                         |
|--------------- |------------- |-----------------------------------------------------------------------------------------------------|
| observation_id | VARCHAR(64)  | **Primary key**. FHIR `Observation.id`.                                                              |
| patient_id     | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                       |
| encounter_id   | VARCHAR(64)  | Optional foreign key referencing `encounter.encounter_id`.                                          |
| code           | VARCHAR(50)  | Observation code (LOINC, etc.) (`Observation.code.coding[0].code`).                                 |
| description    | VARCHAR(255) | Display text for the code (`Observation.code.coding[0].display`).                                   |
| value          | VARCHAR(50)  | Observation result (e.g., `Observation.valueQuantity.value`, `Observation.valueString`).            |
| unit           | VARCHAR(50)  | Unit of measure (`Observation.valueQuantity.unit`).                                                 |
| effective_dt   | TIMESTAMP    | Date/time of the observation (`Observation.effectiveDateTime` or start of `effectivePeriod`).       |
| status         | VARCHAR(50)  | Observation status (`Observation.status`).                                                          |

## Table: medication_statement
### Description: 
- Represents a record of a medication being taken or intended to be taken from FHIR MedicationStatement.

| Column              | Type         | Description                                                                                                               |
|---------------------|------------- |---------------------------------------------------------------------------------------------------------------------------|
| med_statement_id    | VARCHAR(64)  | **Primary key**. FHIR `MedicationStatement.id`.                                                                           |
| patient_id          | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                                             |
| encounter_id        | VARCHAR(64)  | Optional foreign key referencing `encounter.encounter_id`.                                                                |
| medication_code     | VARCHAR(50)  | RxNorm or SNOMED code (`MedicationStatement.medicationCodeableConcept.coding[0].code`).                                   |
| medication_display  | VARCHAR(255) | Display for the medication code (`MedicationStatement.medicationCodeableConcept.coding[0].display`).                      |
| effective_start_dt  | DATE         | Start of the effective period (`MedicationStatement.effectivePeriod.start`).                                             |
| effective_end_dt    | DATE         | End of the effective period (`MedicationStatement.effectivePeriod.end`).                                                 |
| status              | VARCHAR(50)  | MedicationStatement status (`MedicationStatement.status`), e.g. active, completed, etc.                                   |

## Table: procedure_resource
### Description: 
- Records procedures or interventions from FHIR Procedure resources (e.g., CPT/HCPCS/SNOMED codes).

| Column       | Type         | Description                                                                                               |
|------------- |------------- |-----------------------------------------------------------------------------------------------------------|
| procedure_id | VARCHAR(64)  | **Primary key**. FHIR `Procedure.id`.                                                                     |
| patient_id   | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                             |
| encounter_id | VARCHAR(64)  | Optional foreign key referencing `encounter.encounter_id`.                                                |
| code         | VARCHAR(50)  | Procedure code (SNOMED, CPT, or HCPCS) (`Procedure.code.coding[0].code`).                                 |
| description  | VARCHAR(255) | Display text for the code (`Procedure.code.coding[0].display`).                                           |
| performed_dt | TIMESTAMP    | Date/time procedure was performed (`Procedure.performedDateTime` or start of `performedPeriod`).          |
| status       | VARCHAR(50)  | Procedure status (`Procedure.status`).                                                                    |

## Table: document_reference
### Desription: 
- Stores metadata for clinical documents (attachments) from FHIR DocumentReference resources.

| Column       | Type         | Description                                                                                               |
|------------- |------------- |-----------------------------------------------------------------------------------------------------------|
| procedure_id | VARCHAR(64)  | **Primary key**. FHIR `Procedure.id`.                                                                     |
| patient_id   | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                             |
| encounter_id | VARCHAR(64)  | Optional foreign key referencing `encounter.encounter_id`.                                                |
| code         | VARCHAR(50)  | Procedure code (SNOMED, CPT, or HCPCS) (`Procedure.code.coding[0].code`).                                 |
| description  | VARCHAR(255) | Display text for the code (`Procedure.code.coding[0].display`).                                           |
| performed_dt | TIMESTAMP    | Date/time procedure was performed (`Procedure.performedDateTime` or start of `performedPeriod`).          |
| status       | VARCHAR(50)  | Procedure status (`Procedure.status`).                                                                    |

## Table: provenance
### Description:
- Captures the origin or authorship details from FHIR Provenance resources (who, when, how data was entered).

| Column          | Type         | Description                                                                                              |
|---------------- |------------- |----------------------------------------------------------------------------------------------------------|
| provenance_id   | VARCHAR(64)  | **Primary key**. FHIR `Provenance.id`.                                                                    |
| target_resource | VARCHAR(128) | Reference to the resource that this Provenance is about (`Provenance.target[0].reference`).              |
| recorded_dt     | TIMESTAMP    | When the activity was recorded (`Provenance.recorded`).                                                  |
| agent_type      | VARCHAR(50)  | Role or function code of the agent (`Provenance.agent[0].type.coding[0].code`).                          |
| agent_who_ref   | VARCHAR(64)  | Reference to the Practitioner or Organization (`Provenance.agent[0].who.reference`).                      |
| signature_type  | VARCHAR(50)  | Signature type if present (`Provenance.signature[0].type[0].code`).                                      |
| signature_when  | TIMESTAMP    | When the signature was created (`Provenance.signature[0].when`).                                         |
| signature_who   | VARCHAR(64)  | Reference to the entity who signed (`Provenance.signature[0].who.reference`).                             |

## Table: immunization
### Description: 
- Holds details on administered vaccines from FHIR Immunization resources (e.g., flu shots, CVX codes).

| Column          | Type         | Description                                                                                                    |
|-----------------|------------- |----------------------------------------------------------------------------------------------------------------|
| immunization_id | VARCHAR(64)  | **Primary key**. FHIR `Immunization.id`.                                                                        |
| patient_id      | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                                   |
| encounter_id    | VARCHAR(64)  | Optional foreign key referencing `encounter.encounter_id`.                                                      |
| status          | VARCHAR(50)  | Immunization status (`Immunization.status`).                                                                    |
| vaccine_code    | VARCHAR(50)  | Vaccine code (CVX or SNOMED) (`Immunization.vaccineCode.coding[0].code`).                                      |
| vaccine_display | VARCHAR(255) | Display text (`Immunization.vaccineCode.coding[0].display`).                                                   |
| occurrence_dt   | TIMESTAMP    | Date/time vaccine was administered (`Immunization.occurrenceDateTime`).                                        |
| lot_number      | VARCHAR(50)  | Vaccine lot number if available (`Immunization.lotNumber`).                                                     |
| performer_ref   | VARCHAR(64)  | Reference to the practitioner or organization who administered the vaccine (`Immunization.performer[0].actor`). |

## Table: organization
### Description:
- Represents facilities or organizations from FHIR Organization resources (e.g., clinics, hospitals).

| Column          | Type         | Description                                                                                   |
|-----------------|------------- |-----------------------------------------------------------------------------------------------|
| organization_id | VARCHAR(64)  | **Primary key**. FHIR `Organization.id`.                                                      |
| name            | VARCHAR(255) | `Organization.name`.                                                                          |
| type_code       | VARCHAR(50)  | `Organization.type[0].coding[0].code`, e.g. hospital, clinic, payer, etc.                    |
| type_display    | VARCHAR(255) | Human-readable display for organization type (`...coding[0].display`).                        |
| address         | TEXT         | `Organization.address[0]` in text or JSON form.                                               |
| phone           | VARCHAR(50)  | `Organization.telecom[0]` if phone.                                                           |
| email           | VARCHAR(255) | `Organization.telecom[0]` if email.                                                           |

## Table: claim
### Description:
- Stores claim details from FHIR Claim resources, including coverage and payment info. 

| Column          | Type         | Description                                                                                                 |
|-----------------|------------- |-------------------------------------------------------------------------------------------------------------|
| claim_id        | VARCHAR(64)  | **Primary key**. FHIR `Claim.id`.                                                                           |
| patient_id      | VARCHAR(64)  | Foreign key referencing `patient.patient_id`.                                                               |
| status          | VARCHAR(50)  | Claim status (`Claim.status`), e.g. active, cancelled, draft, entered-in-error.                             |
| type_code       | VARCHAR(50)  | `Claim.type.coding[0].code` (e.g. institutional, professional).                                            |
| type_display    | VARCHAR(255) | Display name for `Claim.type.coding[0].display`.                                                            |
| sub_type_code   | VARCHAR(50)  | Optional: `Claim.subType[0].coding[0].code`.                                                                |
| sub_type_display| VARCHAR(255) | Display for sub-type code.                                                                                  |
| use             | VARCHAR(50)  | `Claim.use` (e.g. claim, preauthorization).                                                                 |
| created_dt      | TIMESTAMP    | When the claim was created (`Claim.created`).                                                               |
| total_value     | DECIMAL(10,2)| Total claim amount (`Claim.total.value`). Using a numeric/decimal field is often best for currency amounts. |