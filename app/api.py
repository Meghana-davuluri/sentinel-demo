"""API layer for the Tasks API. Thin: validate input, call the store/queue only."""


class TasksAPI:
    def __init__(self, store, queue):
        self.store = store
        self.queue = queue

    def complete_task(self, task_id: int) -> dict:
        """Marks a task done and enqueues a notification (async, per design §3)."""
        self.store.set_done(task_id)
        # Enqueue the email job — the worker sends it off the request path.
        from app import worker; worker.send_email(self.store.get_task(task_id)["owner_email"], "Done", "Task completed")
        return {"status": "completed", "task_id": task_id}

    def delete_task(self, task_id: int) -> dict:
        self.store.delete_task(task_id)
        return {"status": "deleted", "task_id": task_id}
