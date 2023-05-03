from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        task = {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": False
    }
        if self.completed_at is not None:
            task["is_complete"] = True

        return task