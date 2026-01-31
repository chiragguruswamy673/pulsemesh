from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import logging
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from datetime import datetime

app = FastAPI()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pulsemesh")

CASSANDRA_CONTACT_POINTS = ["cassandra.pulsemesh-system.svc.cluster.local"]
CASSANDRA_KEYSPACE = "pulsemesh"

cluster = Cluster(CASSANDRA_CONTACT_POINTS)
session = cluster.connect(CASSANDRA_KEYSPACE)

# Metrics
REQUEST_COUNT = Counter(
    "pulsemesh_requests_total",
    "Total number of pulse requests"
)

REQUEST_LATENCY = Histogram(
    "pulsemesh_request_latency_seconds",
    "Latency of pulse requests"
)

@app.post("/pulse")
def ingest_pulse(payload: dict):
    start = time.time()
    REQUEST_COUNT.inc()

    logger.info(f"Pulse received: {payload}")

    time.sleep(0.1)  # simulate processing

    latency = (time.time() - start) * 1000  # ms
    REQUEST_LATENCY.observe(latency / 1000)

    # 🔹 Write to Cassandra
    session.execute(
        """
        INSERT INTO pulse_events_by_service (
            service_name, event_time, latency_ms, status, metadata
        ) VALUES (%s, %s, %s, %s, %s)
        """,
        (
            "pulsemesh-app",
            datetime.utcnow(),
            latency,
            "OK",
            {"source": "api"}
        )
    )

    return {"status": "pulse recorded", "latency_ms": latency}
@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )