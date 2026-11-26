# SaaSWatch Sample Log Datasets

## 1. Overview

This directory contains reproducible sample SaaS logs generated
to test the SaaSWatch ingestion, validation, processing and
analysis pipeline.

The datasets represent five categories of events:
- Web access events
- Application events
- Database events
- Performance events
- Business usage events

## 2. Dataset Files

### CSV datasets
- csv/saas_logs.csv
- csv/saas_logs_malformed.csv

### JSON Lines datasets
- json/saas_logs.jsonl
- json/saas_logs_malformed.jsonl

## 3. Dataset Specifications

| Specification | Value |
|---|---|
| Valid records | 1,000 |
| Random seed | 42 |
| Reference date | 2026-11-26 |
| Time range | 7 days |
| Formats | CSV and JSONL |
| Fields per record | 25 |

## 4. Event Distribution

| Event category | Records |
|---|---:|
| Web access | 250 |
| Application | 250 |
| Database | 200 |
| Performance | 150 |
| Business | 150 |
| Total | 1,000 |

## 5. Log Schema

Each record contains 25 fields.

| Field | Description |
|---|---|
| timestamp | UTC date and time of the event |
| level | INFO, WARNING, ERROR or CRITICAL |
| service | Application or infrastructure service |
| environment | production, staging or development |
| host | Hostname generating the event |
| source_ip | Private source IP address |
| method | HTTP request method |
| endpoint | Requested API endpoint |
| status_code | HTTP response status code |
| response_time_ms | Response time in milliseconds |
| message | Human-readable event description |
| user_id | Associated user identifier |
| request_id | Unique deterministic request identifier |
| event_type | web_access, application, database, performance or business |
| database_operation | SELECT, INSERT, UPDATE or DELETE |
| database_name | Database involved in the event |
| cpu_usage_percent | CPU utilization percentage |
| memory_usage_mb | Memory consumption in MB |
| business_action | Business operation |
| business_value | Monetary value when applicable |
| sql_query | SQL statement associated with a database event |
| query_duration_ms | Simulated SQL execution duration |
| session_id | Identifier shared by login/logout events |
| session_event | Session lifecycle event: login or logout |
| feature_name | Normalized business feature identifier |

Fields that do not apply to a particular event category are left empty.
## 6. Event Categories

### Web access
Contains HTTP methods, API endpoints and HTTP status codes.

### Application
Represents application activity, authentication, payment processing,
subscriptions and application errors.

Includes session identifiers and login/logout lifecycle events
for concurrent user session analysis.

### Database
Represents database operations, database names, SQL statements
and simulated query execution durations.

### Performance
Contains CPU utilization, memory consumption and response-time
measurements.

### Business
Represents business actions such as payments, subscriptions,
registrations and invoice generation.

Includes normalized feature names for business usage analytics.

## 7. Supported Monitoring KPIs

The sample datasets support testing of five principal KPIs:

1. Average HTTP response time per endpoint.
2. HTTP 5xx error rate per service.
3. Slowest SQL queries based on generated execution durations.
4. Simultaneous active user sessions calculated from login/logout events.
5. Most and least used business features.

Note: SQL execution durations and user sessions are simulated test data.
They do not represent measurements from a live production environment.

## 8. Generation

Run the following command from the project root:

    python scripts/generate_logs.py

The generator creates:
- A valid CSV dataset containing 1,000 records.
- A valid JSONL dataset containing 1,000 records.
- A malformed CSV test file.
- A malformed JSONL test file.

## 9. Reproducibility

The generator uses:
- Fixed random seed: 42
- Fixed Faker seed: 42
- Fixed reference timestamp: 2026-11-26 12:00:00 UTC
- Deterministic request identifiers

These settings ensure that repeated executions generate identical
valid CSV and JSONL files.

## 10. Malformed Test Datasets

The malformed CSV fixture includes:
- A valid control record.
- An invalid timestamp.
- An invalid HTTP status code.
- An unterminated quoted CSV record.

The malformed JSONL fixture includes:
- A valid JSON object.
- Invalid JSON syntax.
- A valid JSON string that is not a JSON object.

These files are intended to test parsing, schema validation and
error handling in the ingestion pipeline.

## 11. Validation

The datasets are validated for:
- Record counts.
- 25-field schema consistency.
- CSV and JSONL data consistency.
- Event category distribution.
- Database operation and SQL query consistency.
- SQL query execution duration validity.
- User session pairing and timestamp validity.
- Concurrent session calculation.
- Business action and feature mapping.
- Performance metric validity.
- UTC timestamps and source IP addresses.
- Reproducible output using SHA-256 checksums.
- Malformed CSV and JSONL detection.

## 12. Purpose

These datasets support development and testing of:
- CSV and JSON parsing.
- Data validation.
- Log normalization.
- Error detection and handling.
- Elasticsearch indexing.
- SaaS application monitoring.
- Performance and business usage analysis.
