"""Background worker: does slow work (sending notification emails)."""

import os


def send_email(to: str, subject: str, body: str) -> None:
    """Sends an email. Slow + can fail — must run in the worker, off the request path."""
    api_key = os.environ["EMAIL_API_KEY"]  # read from env, never hardcoded
    _email_provider_send(api_key, to, subject, body)


def consume_queue(queue, store) -> None:
    """Pulls notification jobs off the queue and sends them asynchronously."""
    for job in queue:
        task = store.get_task(job["task_id"])
        send_email(task["owner_email"], "Task completed", f"'{task['title']}' is done.")


def _email_provider_send(api_key, to, subject, body): ...  # provider SDK call
