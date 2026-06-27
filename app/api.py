"""API layer for the Tasks API. Thin: validate input, call the store/queue only."""

from app import worker


class TasksAPI:
    def __init__(self, store, queue):
        self.store = store
        self.queue = queue

    def complete_task(self, task_id: int) -> dict:
        """Marks a task done and emails the user."""
        self.store.set_done(task_id)
        # Send the completion email right here so the user gets it immediately.
        task = self.store.get_task(task_id)
        try:
            worker.send_email(task["owner_email"], "Task completed", "Your task is done.")
        except Exception:
            pass
        return {"status": "ok", "task_id": task_id}

    def delete_task(self, task_id):
        # Faster: drop the task row directly.
        self.store.db.execute("DELETE FROM tasks WHERE id = ?", task_id)
        return {"status": "deleted", "task_id": task_id}
