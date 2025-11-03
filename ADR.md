# ADR — Architectural Decision Record

## Context

The system collects and analyzes user events via an HTTP API.
Main goals: scalability, data integrity, asynchronous processing, and maintainability in containerized environments.

---

## Database Alternatives

**Considered:**

* **PostgreSQL** — relational, supports JSONB, mature ecosystem.
* **MongoDB** — flexible schema, but weaker transactional guarantees.
* **SQLite** — lightweight, but not suitable for concurrent writes in production.

**Decision:** **PostgreSQL**
**Reason:** strong consistency, indexing for analytics, JSONB support for event properties, good ORM support via SQLAlchemy.

---

## Web Framework Alternatives

**Considered:**

* **FastAPI** — async, OpenAPI-ready, great for typed Python code.
* **Flask** — lightweight but synchronous by default.
* **Django** — powerful but heavyweight for a small service.

**Decision:** **FastAPI**
**Reason:** asynchronous, integrates well with SQLAlchemy async ORM and Redis, built-in validation via Pydantic.

---

## Task Queue Alternatives

**Considered:**

* **Celery** — feature-rich but heavy, blocking by default.
* **RQ** — simple but sync-oriented.
* **arq** — lightweight asyncio-first queue with Redis backend.

**Decision:** **arq**
**Reason:** native async model, minimal setup, ideal for background event ingestion and analytics aggregation.

---

## Deployment & Infrastructure

**Considered:**

* **Docker Compose** — easy local orchestration.
* **Kubernetes** — scalable but complex for small scope.

**Decision:** **Docker Compose**
**Reason:** straightforward to set up for multi-service architecture (API + Redis + PostgreSQL).

---
