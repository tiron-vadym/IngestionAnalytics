# LEARNED — arq

## Learned During Work

* Asynchronous task queue for Python, built on top of asyncio.
* Simple integration for background jobs and scheduling without Celery’s complexity.
* Supports Redis as the backend for task storage and communication.

## Integrated in Solution

* **Used in:** background processing service to handle event ingestion and analytics asynchronously.

## Pros / Cons / Trade-offs

**Pros**

* Lightweight and easy to set up.
* Natively async (fits well with FastAPI).
* Minimal dependencies.

**Cons**

* Smaller ecosystem compared to Celery.
* Limited advanced features (e.g., task chaining, result backend options).

**When to Use / Avoid**

* Use if you need a simple async task queue with Redis.
* Avoid for complex workflows or multi-broker setups.
