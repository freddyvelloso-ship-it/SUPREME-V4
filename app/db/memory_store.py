from collections import defaultdict
from datetime import date

EVENTS: list[dict] = []
EVENT_HASHES: set[str] = set()
WINDOWS: dict[tuple[str, date], dict] = {}
IEO_LOGS: dict[tuple[str, date], dict] = {}
FLAGS: list[dict] = []

BASELINES = defaultdict(
    lambda: {
        "mean_T": 60.0,
        "sd_T": 30.0,
        "mean_E": 50.0,
        "sd_E": 25.0,
        "mean_V": 30.0,
        "sd_V": 10.0,
        "mean_D": 1.0,
        "sd_D": 0.5,
    }
)
