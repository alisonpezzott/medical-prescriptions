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
