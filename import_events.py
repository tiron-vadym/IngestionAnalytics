#!/usr/bin/env python3
import csv, json, requests, uuid, sys
from itertools import islice

API = "http://http://127.0.0.1:8000/events"
BATCH = 1000


def batched(iterable, n):
    it = iter(iterable)
    while True:
        chunk = list(islice(it, n))
        if not chunk:
            return
        yield chunk


def import_csv(path, batch_size=BATCH):
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for chunk in batched(reader, batch_size):
            payload = []
            for row in chunk:
                payload.append({
                    "event_id": row["event_id"],
                    "occurred_at": row["occurred_at"],
                    "user_id": row["user_id"],
                    "event_type": row["event_type"],
                    "properties": json.loads(row["properties_json"] or "{}")
                })
            resp = requests.post(API, json=payload, headers={"Idempotency-Key": str(uuid.uuid4())})
            print(resp.status_code, resp.text)


if __name__ == "__main__":
    import_csv(sys.argv[1])
