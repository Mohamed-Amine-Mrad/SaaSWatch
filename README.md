
# SaaSWatch
### Web-Based SaaS Log Monitoring and Analysis Platform

## 1. Project Overview

SaaSWatch is a web-based platform designed to collect, process, search, monitor, and analyze application and infrastructure logs.

The platform aims to help technical teams monitor system activity, identify errors, analyze performance, and understand application usage through centralized log management and interactive dashboards.

## 2. Project Objectives

- Centralize logs from different sources.
- Process and structure logs automatically.
- Search and filter log data.
- Monitor application errors and performance.
- Visualize key performance indicators (KPIs).
- Provide a responsive web interface for log management and analysis.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Backend | Python / Flask 3.x |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Search and Analytics | Elasticsearch 8.x |
| Log Processing | Logstash 8.x |
| Data Visualization | Kibana 8.x |
| Metadata Database | MongoDB 7.x |
| Caching | Redis 7.x |
| Containerization | Docker / Docker Compose |
| Log Generation | Python Faker |

## 4. Main Features

- Log file upload and validation.
- Log processing and ingestion.
- Centralized log storage and indexing.
- Log search and filtering.
- Interactive monitoring dashboards.
- Performance and error analysis.
- Upload metadata and search history management.

## 5. Project Structure

```text
SaaSWatch/
├── app/
├── config/
├── data/
├── scripts/
├── tests/
├── docs/
├── .gitignore
└── README.md
```

## 6. Project Status

Initial project setup and directory organization.

## 7. Author

Individual Academic Big Data Mini-Project.

## 8. Infrastructure Architecture

SaaSWatch uses Docker Compose to orchestrate six services:

| Service | Technology | Container | Purpose |
|---|---|---|---|
| Elasticsearch | 8.15.5 | saaswatch-elasticsearch | Log indexing and search |
| Logstash | 8.15.5 | saaswatch-logstash | Log ingestion and processing |
| Kibana | 8.15.5 | saaswatch-kibana | Log visualization |
| MongoDB | 7.0 | saaswatch-mongodb | Metadata storage |
| Redis | 7-alpine | saaswatch-redis | In-memory caching |
| Flask API | Python 3.11 / Flask 3.x | saaswatch-flask | Backend application |

All services communicate through the dedicated Docker bridge network:

`saaswatch_saaswatch-network`

Internal service communication uses Docker Compose service names.

## 9. Network Ports

| Service | Host Port | Container Port | Access |
|---|---:|---:|---|
| Elasticsearch | 9200 | 9200 | Localhost |
| Logstash HTTP Input | 8080 | 8080 | Localhost |
| Logstash Monitoring API | 9600 | 9600 | Localhost |
| Kibana | 5601 | 5601 | Localhost |
| Flask API | 5000 | 5000 | Localhost |
| MongoDB | - | 27017 | Internal network |
| Redis | - | 6379 | Internal network |

The published HTTP ports are bound to 127.0.0.1 and are not directly exposed on external network interfaces.

## 10. Persistent Storage

Docker named volumes preserve important application data:

| Volume | Service | Container Path |
|---|---|---|
| elasticsearch_data | Elasticsearch | /usr/share/elasticsearch/data |
| mongodb_data | MongoDB | /data/db |

Redis currently uses in-memory storage without persistence.

Configuration files are mounted from the repository:

- config/elasticsearch/elasticsearch.yml
- config/logstash/logstash.yml
- config/logstash/pipeline/

## 11. Resource Management

Container memory limits are configured to accommodate the development environment:

| Service | Memory Limit |
|---|---:|
| Elasticsearch | 1200 MB |
| Logstash | 800 MB |
| Kibana | 900 MB |
| MongoDB | 512 MB |
| Redis | 256 MB |
| Flask | 256 MB |

Elasticsearch and Logstash JVM memory settings are configured separately.

## 12. Environment Configuration

Before starting SaaSWatch:

1. Copy the example environment file:

   `cp .env.example .env`

2. Adjust environment values if necessary.

3. Keep `.env` private and never commit it to Git.

The `.env.example` file documents the required environment variables without containing private credentials.

## 13. Installation and Execution

### Start all services

`docker compose up -d`

### Check service status

`docker compose ps`

### Validate configuration

`docker compose config -q`

### View service logs

`docker compose logs -f`

### View logs for a specific service

`docker compose logs -f elasticsearch`

### Stop services safely

`docker compose down`

Named volumes are preserved when using `docker compose down`.

Do not use `docker compose down -v` unless you intentionally want to delete persistent volumes.

## 14. Health Verification

### Elasticsearch

`curl http://localhost:9200`

### Flask API

`curl http://localhost:5000/health`

The Flask health endpoint checks:

- Elasticsearch
- MongoDB
- Redis
- Logstash

A healthy response reports all four dependencies as `up`.

### MongoDB

`docker compose exec mongodb mongosh --quiet --eval "db.adminCommand('ping')"`

### Redis

`docker compose exec redis redis-cli ping`

### Logstash Monitoring API

`curl http://localhost:9600`

## 15. Docker Resource Isolation

SaaSWatch uses its own Docker Compose project, dedicated network, containers and named volumes.

Other Docker projects and unrelated containers, including the MLOps lab environment, are managed independently and should not be stopped or modified by SaaSWatch operations.

## 16. Current Implementation Status

Completed:

- Elasticsearch infrastructure.
- Logstash integration.
- Kibana integration.
- MongoDB service.
- Redis service.
- Flask application container.
- Dependency health monitoring.
- Initial database and log ingestion integration tests.

Future development:

- Backend REST API endpoints.
- API documentation using OpenAPI and Swagger.
- Log search and filtering.
- Log upload and processing.
- Monitoring dashboards and analytics.
