import hashlib
import json
from collections.abc import Iterable
from datetime import UTC, datetime

from app.core.config import settings
from app.core.security import pseudonymize_user
from app.services.schemas import EventIn

MEDIA_WEIGHT = {"image": 1.0, "video": 1.5, "preview": 0.5}
SEVERITY_WEIGHT = {1: 0.5, 2: 0.8, 3: 1.0, 4: 1.3, 5: 1.6}


def compute_event_hash(event: dict) -> str:
    key = {
        "id_hash": event["id_hash"],
        "timestamp": event["timestamp"],
        "event_type": event["event_type"],
        "media_type": event["media_type"],
        "severity": event["severity"],
        "source_tool": event["source_tool"],
        "duration_seconds": round(float(event["duration_seconds"]), 1),
    }
    return hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()


def normalize_event(item: EventIn) -> dict:
    id_hash = pseudonymize_user(item.user_identifier, settings.structural_salt)
    payload = {
        "id_hash": id_hash,
        "timestamp": item.timestamp.astimezone(UTC).isoformat(),
        "event_type": item.event_type.value,
        "media_type": item.media_type.value,
        "severity": item.severity,
        "duration_seconds": item.duration_seconds,
        "source_tool": item.source_tool,
    }
    payload["event_hash"] = compute_event_hash(payload)
    payload["weight"] = SEVERITY_WEIGHT[item.severity] * MEDIA_WEIGHT[item.media_type.value]
    return payload


def build_sessions(events: Iterable[dict], gap_seconds: int = 300) -> list[dict]:
    sorted_events = sorted(events, key=lambda e: e["timestamp"])
    sessions: list[dict] = []
    current: list[dict] = []
    last_ts: datetime | None = None

    for ev in sorted_events:
        ts = datetime.fromisoformat(ev["timestamp"])
        if not current:
            current = [ev]
            last_ts = ts
            continue
        assert last_ts is not None
        if (ts - last_ts).total_seconds() > gap_seconds:
            sessions.append(_session_stats(current))
            current = [ev]
        else:
            current.append(ev)
        last_ts = ts

    if current:
        sessions.append(_session_stats(current))
    return sessions


def _session_stats(events: list[dict]) -> dict:
    duration_minutes = sum(e["duration_seconds"] for e in events) / 60.0
    volume = sum(e["weight"] * e["duration_seconds"] for e in events)
    return {
        "id_hash": events[0]["id_hash"],
        "session_start": events[0]["timestamp"],
        "session_end": events[-1]["timestamp"],
        "duration_minutes": duration_minutes,
        "event_count": len(events),
        "total_volume": volume,
    }
