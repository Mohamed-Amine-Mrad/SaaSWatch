import os
import socket

from elasticsearch import Elasticsearch
from pymongo import MongoClient
import redis


def check_dependencies():
    results = {}

    # Elasticsearch
    try:
        es = Elasticsearch(
            os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200"),
            request_timeout=3
        )
        results["elasticsearch"] = (
            "up" if es.ping() else "down"
        )
        es.close()
    except Exception:
        results["elasticsearch"] = "down"

    # MongoDB
    try:
        client = MongoClient(
            os.getenv("MONGODB_URL", "mongodb://mongodb:27017"),
            serverSelectionTimeoutMS=3000
        )
        client.admin.command("ping")
        results["mongodb"] = "up"
        client.close()
    except Exception:
        results["mongodb"] = "down"

    # Redis
    try:
        cache = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379/0"),
            socket_connect_timeout=3
        )
        results["redis"] = "up" if cache.ping() else "down"
        cache.close()
    except Exception:
        results["redis"] = "down"

    # Logstash TCP connectivity
    try:
        with socket.create_connection(
            ("logstash", 8080), timeout=3
        ):
            results["logstash"] = "up"
    except Exception:
        results["logstash"] = "down"

    return results
