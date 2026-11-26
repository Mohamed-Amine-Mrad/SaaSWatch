
import csv
import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from faker import Faker

# Reproducibility
SEED = 42
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

# Project paths
ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = ROOT / "data" / "samples" / "csv"
JSON_DIR = ROOT / "data" / "samples" / "json"

CSV_DIR.mkdir(parents=True, exist_ok=True)
JSON_DIR.mkdir(parents=True, exist_ok=True)

# Dataset configuration
TOTAL_RECORDS = 1000
REFERENCE_TIME = datetime(2026, 11, 26, 12, 0, 0, tzinfo=timezone.utc)
SERVICES = [
    "auth-service",
    "payment-service",
    "user-service",
    "subscription-service",
    "notification-service",
]

ENVIRONMENTS = ["production", "staging", "development"]
LEVELS = ["INFO", "WARNING", "ERROR", "CRITICAL"]

ENDPOINTS = [
    "/api/login",
    "/api/users",
    "/api/payments",
    "/api/subscriptions",
    "/api/notifications",
]

EVENTS = {
    "INFO": [
        "Request processed successfully",
        "User logged in successfully",
        "Subscription created",
        "Payment completed",
    ],
    "WARNING": [
        "High response time detected",
        "Authentication retry limit approaching",
        "Database connection pool nearly full",
    ],
    "ERROR": [
        "Database connection failed",
        "Payment processing failed",
        "Authentication failed",
        "External service unavailable",
    ],
    "CRITICAL": [
        "Database unavailable",
        "Payment gateway failure",
        "Service crashed unexpectedly",
    ],
}

FIELDS = [
    "timestamp",
    "level",
    "service",
    "environment",
    "host",
    "source_ip",
    "method",
    "endpoint",
    "status_code",
    "response_time_ms",
    "message",
    "user_id",
    "request_id",
]


def generate_log(index):
    level = random.choices(
        LEVELS,
        weights=[70, 18, 10, 2],
        k=1
    )[0]

    if level == "INFO":
        status = random.choice([200, 201, 204])
    elif level == "WARNING":
        status = random.choice([200, 429, 503])
    elif level == "ERROR":
        status = random.choice([400, 401, 404, 500, 502])
    else:
        status = random.choice([500, 502, 503])

    timestamp = REFERENCE_TIME - timedelta(
        seconds=random.randint(0, 7 * 24 * 3600)
    )

    return {
        "timestamp": timestamp.isoformat(timespec="milliseconds").replace(
            "+00:00", "Z"
        ),
        "level": level,
        "service": random.choice(SERVICES),
        "environment": random.choices(
            ENVIRONMENTS,
            weights=[75, 15, 10],
            k=1
        )[0],
        "host": f"server-{random.randint(1, 5):02d}",
    "source_ip": fake.ipv4_private(),
        "method": random.choice(["GET", "POST", "PUT", "DELETE"]),
        "endpoint": random.choice(ENDPOINTS),
        "status_code": status,
        "response_time_ms": random.randint(10, 3000),
        "message": random.choice(EVENTS[level]),
        "user_id": f"user_{random.randint(1, 200):03d}",
        "request_id": str(uuid.uuid5(
            uuid.NAMESPACE_DNS,
            f"saaswatch-{SEED}-{index}"
        )),
    }


def generate_valid_datasets():
    records = [
        generate_log(index)
        for index in range(1, TOTAL_RECORDS + 1)
    ]

    csv_path = CSV_DIR / "saas_logs.csv"
    json_path = JSON_DIR / "saas_logs.jsonl"

    # CSV dataset
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    # JSON Lines dataset
    with json_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")

    return records, csv_path, json_path


def generate_malformed_datasets(records):
    # Separate test files; valid datasets remain untouched.
    malformed_csv = CSV_DIR / "saas_logs_malformed.csv"
    malformed_json = JSON_DIR / "saas_logs_malformed.jsonl"

    with malformed_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerow(records[0])

        writer.writerow({
            **records[1],
            "timestamp": "NOT_A_TIMESTAMP",
            "status_code": "INVALID",
        })

        file.write('"broken CSV record\n')

    with malformed_json.open("w", encoding="utf-8") as file:
        file.write(json.dumps(records[0]) + "\n")
        file.write('{"level": "ERROR", "message":\n')
        file.write('"this is not a JSON object"\n')


def main():
    records, csv_path, json_path = generate_valid_datasets()
    generate_malformed_datasets(records)

    print("=" * 50)
    print("SaaSWatch Log Dataset Generation")
    print("=" * 50)
    print(f"Valid records: {len(records)}")
    print(f"CSV: {csv_path}")
    print(f"JSONL: {json_path}")
    print("Malformed CSV and JSONL test files generated.")
    print(f"Random seed: {SEED}")


if __name__ == "__main__":
    main()
