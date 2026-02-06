# TaskForge

TaskForge is a lightweight background task processing system built using **FastAPI** and **Redis**. It is designed to handle asynchronous jobs like emails, SMS, or any long-running task without blocking the main API.

Unlike simple queue demos, TaskForge focuses on end-to-end task lifecycle management — from enqueueing tasks via a secured API, processing them using independent worker processes, handling retries and failures, and exposing system metrics for monitoring.

This project focuses on **core backend concepts** such as task queues, workers, retries, rate limiting, metrics, and fault tolerance — keeping the system simple, understandable, and production-oriented.

---

## Why TaskForge?

In real-world backend systems, not every task should be handled inside an API request. Sending emails, notifications, or processing heavy jobs asynchronously improves performance and reliability.

TaskForge demonstrates how such systems work internally, without relying on heavy external tools.

---

## High-Level Architecture

```
Client / API Consumer
        |
        v
FastAPI (Producer Layer)
        |
        v
Redis Queue (Main Queue)
        |
        v
Worker Process
        |
        v
Task Handler (SMS / Email / etc.)
```

Additional flows:

* Failed tasks → Retry Queue (with delay)
* Exhausted retries → Dead Letter Queue (DLQ)
* Metrics & logs stored in Redis

---

## Core Features

* Asynchronous task enqueueing via API
* Independent worker process for task execution
* Retry mechanism with configurable delay
* Dead Letter Queue for failed tasks
* Redis-based rate limiting
* API key authentication
* Centralized task logging
* Metrics endpoint for monitoring

---

## API Endpoints (Overview)

| Endpoint           | Method | Description               |
| ------------------ | ------ | ------------------------- |
| `/enqueue`         | POST   | Enqueue a new task        |
| `/metrics`         | GET    | View system metrics       |
| `/tasks/{task_id}` | GET    | Check task status         |
| `/consume-once`    | POST   | Consume one task manually |
| `/dlq`             | GET    | View Dead Letter Queue    |
| `/dlq`             | DELETE | Clear Dead Letter Queue   |

---

## Worker Design

The worker runs as a **separate process**, independent of the FastAPI server.

Responsibilities:

* Pull tasks from Redis
* Execute the appropriate handler
* Update task status
* Handle retries and failures
* Push failed tasks to DLQ
* Update metrics

This separation mirrors real production systems where workers scale independently from APIs.

---

## Rate Limiting & Security

* API access is protected using an **API key**
* Redis-based rate limiting ensures fair usage
* Prevents abuse and accidental overload

---

## Tech Stack

* **FastAPI** – API layer
* **Redis** – Queue, rate limiting, metrics
* **Python** – Core language
* **Postman** – API testing
* **Git & GitHub** – Version control
* **WSL / Linux** – Redis runtime

---

## Local Setup (Summary)

* Start Redis server
* Run FastAPI using Uvicorn
* Start worker process manually
* Test APIs using Postman

---

## Project Goal

This project is intentionally kept focused and minimal to highlight **backend fundamentals** rather than UI or third-party abstractions.

It serves as a strong foundation for understanding distributed task systems and is suitable for academic evaluation, interviews, and resume projects.
