from db import db

class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80), unique=True, nullable=False)
    hours_spent = db.Column(db.Date)
    created_at = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=False)

    user = db.relationship("UserModel", back_populates="tasks")#, lazy="dynamic")