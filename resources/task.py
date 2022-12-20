from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TaskModel
from schemas import TaskSchema

blp = Blueprint("Tasks", __name__, description="Operations on tasks.")


@blp.route("/task")
class Task(MethodView):
    @blp.arguments(TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            print(SQLAlchemyError)
            abort(500, message="An error occurred while creating the task.")
        return {"message": "Task created successfully.", "task": task_data}, 201


@blp.route("/task/<string:task_id>")
class TaskList(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

@blp.route("/user/<string:user_id>/task")
class TasksOnUser(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, user_id):
        task = TaskModel.query.get_or_404(user_id)
        return task