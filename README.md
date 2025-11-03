# Event Ingestion and Analytics Service

A lightweight, asynchronous microservice for collecting user events and generating analytical metrics such as Daily Active Users (DAU).

---

## 🚀 Features

* **Event ingestion** via `POST /events` — accepts batches of JSON events
* **Analytics API** (`GET /stats/dau`) — returns daily active users with filtering and segmentation
* **Async architecture** powered by FastAPI, SQLAlchemy, and PostgreSQL
* **Idempotent requests** — prevents duplicate event ingestion
* **Task queue** using `arq` for background processing
* **Containerized** with Docker Compose

---

## 🧩 Tech Stack

| Layer                   | Tool                   | Purpose                                      |
| ----------------------- | ---------------------- | -------------------------------------------- |
| Web Framework           | **FastAPI**            | Async API and validation                     |
| Database                | **PostgreSQL**         | Reliable event storage with JSONB support    |
| ORM                     | **SQLAlchemy (async)** | Query building and schema management         |
| Task Queue              | **arq**                | Background processing for heavy computations |
| Caching / Rate Limiting | **Redis**              | Rate control and async job backend           |
| Testing                 | **pytest**             | Unit and integration tests                   |
| Deployment              | **Docker Compose**     | Multi-service orchestration                  |

---

## 📦 Project Structure

```
app/
├── api/                # Routers and endpoints
├── db/                 # Models and session management
├── services/           # Business logic and analytics
├── tasks/              # arq background jobs
├── tests/              # pytest tests
└── main.py             # FastAPI entry point
```

---

## ⚙️ Installation

### Prerequisites

* Python 3.11+
* Docker & Docker Compose

### Setup

```bash
git clone https://github.com/tiron-vadym/IngestionAnalytics
cd event-analytics
cp .env.example .env
docker-compose up --build
```

The API will be available at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🧠 Example Usage

### 1. Ingest Events

```bash
POST /events
Content-Type: application/json

[
  {
    "event_id": "uuid",
    "occurred_at": "2025-11-04T12:00:00Z",
    "user_id": 123,
    "event_type": "purchase",
    "properties": {"country": "UA", "amount": 50}
  }
]
```

### 2. Get Daily Active Users

```bash
GET /stats/dau?from=2025-11-01&to=2025-11-04
GET /stats/dau?segment=event_type:purchase
GET /stats/dau?properties=UA
```
