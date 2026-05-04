import math
from datetime import UTC, date, datetime, timedelta


def window_start_14d(ts: datetime) -> date:
    epoch = date(1970, 1, 1)
    days = (ts.date() - epoch).days
    return epoch + timedelta(days=(days // 14) * 14)


def compute_window_metrics(events: list[dict]) -> dict[tuple[str, date], dict]:
    buckets: dict[tuple[str, date], dict] = {}
    for ev in events:
        ts = datetime.fromisoformat(ev["timestamp"]).astimezone(UTC)
        ws = window_start_14d(ts)
        key = (ev["id_hash"], ws)
        bucket = buckets.setdefault(key, {"T": 0.0, "E": 0, "V": 0.0})
        bucket["T"] += ev["duration_seconds"] / 60.0
        bucket["E"] += 1
        bucket["V"] += ev["weight"] * ev["duration_seconds"]

    out = {}
    for key, m in buckets.items():
        T = m["T"]
        E = m["E"]
        V = m["V"]
        D = E / T if T > 0 else 0
        out[key] = {
            "T_minutes": T,
            "E_events": E,
            "V_volume": V,
            "D_density": D,
            "V_log": math.log1p(V),
        }
    return out


def compute_ieo(window_metric: dict, baseline: dict) -> dict:
    def z(x, mu, sd):
        return 0.0 if not sd else (x - mu) / sd

    z_t = z(window_metric["T_minutes"], baseline["mean_T"], baseline["sd_T"])
    z_e = z(window_metric["E_events"], baseline["mean_E"], baseline["sd_E"])
    z_v = z(window_metric["V_log"], baseline["mean_V"], baseline["sd_V"])
    z_d_raw = z(window_metric["D_density"], baseline["mean_D"], baseline["sd_D"])
    z_d = max(-3.0, min(3.0, z_d_raw))

    ieo_linear = 0.5 * z_t + 0.3 * z_e + 0.2 * z_v
    ieo_sat = 1 / (1 + math.exp(-1 * (ieo_linear - 1)))
    ieo_final = ieo_sat + 0.1 * z_d

    return {
        "IEO_score": ieo_final,
        "IEO_linear": ieo_linear,
        "IEO_sat": ieo_sat,
        "z_T": z_t,
        "z_E": z_e,
        "z_V": z_v,
        "z_D": z_d,
    }
