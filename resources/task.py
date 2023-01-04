from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import TaskModel
from schemas import TaskSchema

blp = Blueprint("Tasks", __name__, description="Operations on tasks.")


@blp.route("/task")
class Task(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the task.")
        return {"message": "Task created successfully.", "task": task_data}, 201


@blp.route("/task/<string:task_id>")
class TaskList(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

@blp.route("/user/<string:user_id>/task")
class TasksOnUser(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema(many=True))
    def get(self, user_id):
        task = TaskModel.query.filter_by(user_id=user_id).all()
        return task