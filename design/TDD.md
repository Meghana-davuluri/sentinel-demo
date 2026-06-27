# Technical Design Doc — Tasks API

A small service for creating and completing tasks, with email notifications.

## 1. Components

- **API layer** (`app/api.py`) — HTTP handlers. Validates input, returns responses.
  It must stay thin: no business logic, no direct DB writes for side effects.
- **Worker** (`app/worker.py`) — does slow work (sending notification emails).
- **Store** (`app/store.py`) — all database reads/writes live here.

## 2. Data model

- A `Task` has: `id`, `title`, `owner_email`, `done`.
- A task has many `Reminder` rows (child rows), linked by `task_id`.

## 3. Notification flow (IMPORTANT)

When a task is completed, the user must be emailed. Sending email is slow and can fail,
so it **must not block the API response**.

**Required design:** the API layer enqueues a notification job onto a **background queue**;
the **worker** consumes the queue and sends the email asynchronously. The API must **never**
call the worker / send email synchronously inside the request handler.

> Rationale: a synchronous email send makes the endpoint slow and couples request latency to
> the email provider's uptime. This was an explicit decision — do not call `worker.send_email`
> directly from the API.

## 4. Deletion

Deleting a `Task` must also remove its `Reminder` child rows (see team rules on cascade deletes).
