from datetime import date

from fastapi import APIRouter

from app.db.memory_store import BASELINES, EVENTS, EVENT_HASHES, FLAGS, IEO_LOGS, WINDOWS
from app.services.ingestion import normalize_event
from app.services.metrics import compute_ieo, compute_window_metrics
from app.services.schemas import EventsIngestRequest

router = APIRouter()


@router.post("/events/ingest")
def ingest_events(payload: EventsIngestRequest):
    received = len(payload.events)
    stored = 0
    duplicates = 0

    normalized = [normalize_event(ev) for ev in payload.events]
    for ev in normalized:
        if ev["event_hash"] in EVENT_HASHES:
            duplicates += 1
            continue
        EVENT_HASHES.add(ev["event_hash"])
        EVENTS.append(ev)
        stored += 1

    metrics = compute_window_metrics(EVENTS)
    WINDOWS.update(metrics)

    for (id_hash, ws), m in metrics.items():
        ieo = compute_ieo(m, BASELINES[id_hash])
        IEO_LOGS[(id_hash, ws)] = {"window_start": ws, **ieo}

    return {"status": "success", "events_received": received, "events_stored": stored, "duplicates": duplicates}


@router.get("/metrics/{id_hash}")
def get_metrics(id_hash: str, start_date: date | None = None, end_date: date | None = None):
    rows = []
    for (hid, ws), m in WINDOWS.items():
        if hid != id_hash:
            continue
        if start_date and ws < start_date:
            continue
        if end_date and ws > end_date:
            continue
        rows.append({"window_start": ws, **m})
    rows.sort(key=lambda r: r["window_start"])
    return {"id_hash": id_hash, "windows": rows}


@router.get("/ieo/{id_hash}")
def get_ieo(id_hash: str, start_date: date | None = None, end_date: date | None = None):
    rows = []
    for (hid, ws), rec in IEO_LOGS.items():
        if hid != id_hash:
            continue
        if start_date and ws < start_date:
            continue
        if end_date and ws > end_date:
            continue
        rows.append(rec)
    rows.sort(key=lambda r: r["window_start"])
    return {"id_hash": id_hash, "windows": rows}


@router.get("/risk-flags")
def get_risk_flags(start_date: date | None = None, end_date: date | None = None, id_hash: str | None = None):
    rows = []
    for row in FLAGS:
        if id_hash and row["id_hash"] != id_hash:
            continue
        if start_date and row["timestamp"] < start_date:
            continue
        if end_date and row["timestamp"] > end_date:
            continue
        rows.append(row)
    return {"flags": rows}


@router.get("/health")
def health():
    return {
        "status": "ok",
        "database": "memory",
        "queue_analytics_size": 0,
        "queue_dead_letter_size": 0,
    }
