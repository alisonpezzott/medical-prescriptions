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
- Get data from Azure Storage
- Create a new table prescriptions_exploded and mapping

Run `Query with code`

```kql
// Alter table policy
.alter table prescriptions_exploded policy update
@'[{"Source": "prescriptions_raw", "Query": "prescriptions_raw | mv-expand med = data.medications | project prescription_id = tostring(data.prescription_id), issue_date = todatetime(data.issue_date), patient_name = tostring(data.patient.name), patient_id = toint(data.patient.id), medication_name = tostring(med.name), medication_dosage = tostring(med.dosage), medication_frequency = tostring(med.frequency)", "IsEnabled": true, "IsTransactional": false, "PropagateIngestionProperties": false}]'
```
