from pathlib import Path
import json
import uuid
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_FILE = ROOT / "xiamen_k12_calendar.ics"

def load_events():
    events = []
    for file in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(file.read_text(encoding="utf-8"))
        for evt in data.get("events", []):
            evt["_academic_year"] = data.get("academic_year", "")
            events.append(evt)
    return events

def ymd(date_str: str) -> str:
    return date_str.replace("-", "")

def next_day(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (dt + timedelta(days=1)).strftime("%Y%m%d")

def build_ics(events):
    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ChatGPT//Xiamen K12 Calendar//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:厦门中小学日历",
        "X-WR-TIMEZONE:Asia/Shanghai"
    ]
    for evt in events:
        summary = evt["summary"].replace(",", r"\,").replace(";", r"\;")
        description = evt.get("description", "").replace(",", r"\,").replace(";", r"\;")
        uid = f"{uuid.uuid4()}@xiamen-k12-calendar"
        start = ymd(evt["start"])
        end_plus_one = next_day(evt["end"])
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"SUMMARY:{summary}",
            f"DTSTART;VALUE=DATE:{start}",
            f"DTEND;VALUE=DATE:{end_plus_one}",
            f"DESCRIPTION:{description}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    events = load_events()
    ics = build_ics(events)
    OUT_FILE.write_text(ics, encoding="utf-8")
    print(f"Generated: {OUT_FILE}")
