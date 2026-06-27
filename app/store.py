"""Database access for the Tasks API. All DB reads/writes live here."""


class Store:
    def __init__(self, db):
        self.db = db

    def get_task(self, task_id: int) -> dict:
        return self.db.query_one("SELECT * FROM tasks WHERE id = ?", task_id)

    def set_done(self, task_id: int) -> None:
        self.db.execute("UPDATE tasks SET done = 1 WHERE id = ?", task_id)

    def delete_task(self, task_id: int) -> None:
        # Prod has no ON DELETE CASCADE — remove child Reminder rows first.
        self.db.execute("DELETE FROM reminders WHERE task_id = ?", task_id)
        self.db.execute("DELETE FROM tasks WHERE id = ?", task_id)
