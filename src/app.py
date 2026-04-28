import json
import logging
import os
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("prescriptions.log", encoding="utf-8"),
    ],
)

PATIENTS = [
    "Ana Silva",
    "Bruno Costa",
    "Carlos Souza",
    "Daniela Lima",
    "Eduardo Santos",
    "Fernanda Oliveira",
    "Gabriel Pereira",
    "Helena Rocha",
    "Igor Almeida",
    "Julia Ferreira",
    "Lucas Martins",
    "Mariana Ribeiro",
    "Nathan Carvalho",
    "Priscila Gomes",
    "Rafael Nascimento",
    "Sofia Araújo",
    "Thiago Barbosa",
    "Valentina Mendes",
    "Wesley Correia",
    "Yasmin Cardoso",
]

MEDICATIONS = [
    "Amoxicillin",
    "Ibuprofen",
    "Metformin",
    "Atorvastatin",
    "Lisinopril",
    "Omeprazole",
    "Losartan",
    "Amlodipine",
    "Simvastatin",
    "Levothyroxine",
    "Azithromycin",
    "Prednisone",
    "Metoprolol",
    "Furosemide",
    "Pantoprazole",
    "Ciprofloxacin",
    "Clonazepam",
    "Dipyrone",
    "Paracetamol",
    "Diclofenac",
]

DOSES = ["5mg", "10mg", "20mg", "50mg", "100mg", "250mg", "500mg", "1g"]

FREQUENCIES = [
    "Once daily",
    "Twice daily",
    "Every 8 hours",
    "Every 12 hours",
    "As needed",
]

INTERVAL_SECONDS = 10


def generate_prescription():
    num_meds = random.randint(1, 3)
    selected_meds = random.sample(MEDICATIONS, num_meds)
    return {
        "prescription_id": str(uuid.uuid4()),
        "issue_date": datetime.now(timezone.utc).isoformat(),
        "patient": {
            "name": random.choice(PATIENTS),
            "id": random.randint(100, 999),
        },
        "medications": [
            {
                "name": med,
                "dosage": random.choice(DOSES),
                "frequency": random.choice(FREQUENCIES),
            }
            for med in selected_meds
        ],
    }


LOCAL_DIR = Path("medical_prescriptions")


def upload_prescription(blob_service_client, container_name, prescription_data):
    prescrition_id = prescription_data["prescription_id"]
    file_name = (
        f"prescription_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{prescrition_id}.json"
    )
    json_content = json.dumps(prescription_data, indent=2)

    # Upload to blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name
    )
    blob_client.upload_blob(json_content, overwrite=True)

    # Save locally
    LOCAL_DIR.mkdir(exist_ok=True)
    (LOCAL_DIR / file_name).write_text(json_content, encoding="utf-8")

    return file_name


def main():
    connection_string = os.getenv("CONNECTION_STRING")
    container_name = os.getenv("BLOB_CONTAINER", "medical-prescription")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Ensure container exists
    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()
        logging.info(f"Container '{container_name}' created.")

    logging.info(
        f"Generating prescriptions every {INTERVAL_SECONDS}s. Press Ctrl+C to stop."
    )

    while True:
        prescription = generate_prescription()
        file_name = upload_prescription(
            blob_service_client, container_name, prescription
        )
        logging.info(f"Uploaded {file_name}")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
