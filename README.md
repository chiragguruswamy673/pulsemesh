# PulseMesh 🚀  
*Kubernetes-native Observability & Event Ingestion Platform*

PulseMesh is a cloud-native platform built to simulate how modern distributed systems ingest events, expose metrics, and persist operational data using scalable infrastructure patterns.

This project demonstrates **real-world DevOps practices** including Kubernetes orchestration, Infrastructure as Code, observability, and NoSQL data modeling.

---

## 🧩 Problem Statement

Modern microservices generate:
- High-volume events
- Operational metrics
- Time-series performance data

PulseMesh is designed to:
- Ingest service-level pulse events
- Expose application metrics for monitoring
- Persist events in a scalable NoSQL datastore
- Run entirely on Kubernetes using production-style patterns

---

## 🏗️ Architecture Overview

**PulseMesh consists of four main layers:**

1. **API Layer**
   - FastAPI-based service for ingesting pulse events
   - Exposes Prometheus-compatible metrics

2. **Observability Layer**
   - Prometheus for metrics scraping
   - Grafana for visualization and dashboards

3. **Data Layer**
   - Apache Cassandra for high-throughput event storage
   - Optimized schema for time-series workloads

4. **Platform Layer**
   - Kubernetes (KIND) for orchestration
   - Terraform for infrastructure management
   - Docker for containerization

---

## 🔧 Tech Stack

### Infrastructure & Orchestration
- **Kubernetes (KIND)** – Local Kubernetes cluster
- **Terraform** – Infrastructure as Code
- **Docker** – Containerization

### Backend
- **Python 3.11**
- **FastAPI**
- **Uvicorn (ASGI Server)**

### Observability
- **Prometheus**
- **Grafana**
- **Prometheus Python Client**

### Data Layer
- **Apache Cassandra**
- **Cassandra Query Language (CQL)**

---
## 🚀 Application Layer (FastAPI)

PulseMesh exposes an API endpoint to ingest pulse events:
```bash
POST /pulse
```

Each request:
- Increments request counters
- Records request latency
- Emits metrics in Prometheus format at /metrics

Sample Metrics Exposed
- pulsemesh_requests_total
- pulsemesh_request_latency_seconds

## 📊 Observability
### Prometheus
- Scrapes application metrics via Kubernetes service discovery
- Collects latency and request rate metrics
### Grafana
Dashboards visualize:
- Requests per second (RPS)
- Request latency percentiles
- Application health indicators

## 🗄️ Cassandra (NoSQL Data Layer)
Apache Cassandra is used to persist pulse events due to its:
- High write throughput
- Horizontal scalability
- Suitability for time-series workloads

### Deployment Details
- Deployed using Kubernetes StatefulSet
- Stable pod identity (cassandra-0)
- Persistent storage for durability
- Cluster-internal service discovery

### Schema Design

Pulse events are partitioned by service name and ordered by event time:
```bash 
CREATE TABLE pulse_events_by_service (
  service_name text,
  event_time timestamp,
  latency_ms double,
  status text,
  metadata map<text, text>,
  PRIMARY KEY (service_name, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);
```

### This design enables:
- Efficient per-service queries
- Time-ordered reads
- High ingestion performance

## 🧠 Key Engineering Concepts Demonstrated
- Stateless vs Stateful Kubernetes workloads
- Kubernetes Services and DNS-based discovery
- Infrastructure as Code with Terraform
- Observability-driven debugging
- Time-series data modeling in NoSQL systems
- Production-style troubleshooting and iteration

## 📌 Use Cases Demonstrated
- Distributed application monitoring
- Event ingestion pipelines
- Platform reliability instrumentation
- Kubernetes-native service design

## 📈 Future Enhancements
- Async FastAPI → Cassandra integration
- Multi-node Cassandra cluster
- Log aggregation via Loki
- Alerting via Prometheus Alertmanager
- CI/CD pipeline integration

