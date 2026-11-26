
# SaaSWatch Sample Log Datasets

## Overview

This directory contains representative SaaS application logs generated for testing the SaaSWatch ingestion pipeline.

## Dataset Files

### CSV
- csv/saas_logs.csv
- csv/saas_logs_malformed.csv

### JSON Lines
- json/saas_logs.jsonl
- json/saas_logs_malformed.jsonl

## Dataset Specifications

- Valid records: 1,000
- Random seed: 42
- Reference date: 2026-11-26
- Time range: 7 days
- Formats: CSV and JSONL

## Log Fields

- timestamp
- level
- service
- environment
- host
- source_ip
- method
- endpoint
- status_code
- response_time_ms
- message
- user_id
- request_id

## Generation

Run from the project root:

    python scripts/generate_logs.py

The generator creates both valid datasets and separate malformed test datasets.

The fixed random seed and reference timestamp ensure reproducible output.

## Purpose

These datasets are used to test:
- CSV parsing
- JSON parsing
- Data validation
- Log normalization
- Elasticsearch indexing
