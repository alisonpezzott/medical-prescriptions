# Medical Prescriptions

Just a demo to ingest data with Microsoft Fabric real-time analytics workload from a blob storage.


## Setup

- Created a storage account in Azure Portal
- Generated connection strings
- Configured at .env (see [.env.example](.env.example))

## Generate prescriptions

Install dependencies:

```powershell
uv sync
```

Start generate medical prescriptions:

```powershell
uv run src/app.py
```

## Fabric Setup

- Create Workspace
- Pin a Fabric Capacity
- Create workspace identity and add role assignment in Storage Account
- Create eventhouse


Run `Query with code`

```kql
// Create table command
.create table ['prescriptions_exploded']  (['prescription_id']:string, ['issue_date']:datetime, ['patient_name']:string, ['patient_id']:int, ['medication_name']:string, ['medication_dosage']:string, ['medication_frequency']:string)
```

```kql
// Create table command
.create table ['prescriptions_raw']  (['payload']:dynamic)
```


```kql
// Alter table policy
.alter table prescriptions_exploded policy update
@'[{"Source": "prescriptions_raw", "Query": "prescriptions_raw | mv-expand med = payload.medications | project prescription_id = tostring(payload.prescription_id), issue_date = todatetime(payload.issue_date), patient_name = tostring(payload.patient.name), patient_id = toint(payload.patient.id), medication_name = tostring(med.name), medication_dosage = tostring(med.dosage), medication_frequency = tostring(med.frequency)", "IsEnabled": true, "IsTransactional": false, "PropagateIngestionProperties": false}]'
```
