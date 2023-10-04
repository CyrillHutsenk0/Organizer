from flask_smorest import Blueprint, abort
from .schemas import AddTaskArgsSchema, TaskSchema, UpdateTaskArgsSchema, UpdateTaskResponseSchema
from organizer_project.config import TASK_LIST
from organizer_project.models import Task
from ...utils.universal_responses import success_response

blp = Blueprint(
    "todo_list",
    "todo_list",
    url_prefix="/api/todo-list",
    description="Functionality for todo lists",
)


@blp.route("/add-task", methods=["POST"], strict_slashes=False)
@blp.arguments(AddTaskArgsSchema, location="json", as_kwargs=True)
@blp.doc(description="Creating new task")
def add_task(description: str):
    TASK_LIST.append(Task(description=description))
    return success_response()


@blp.route("/remove-task/<int:task_id>", methods=["DELETE"], strict_slashes=False)
@blp.doc(description="Deleting client existed task")
def delete_task(task_id: int):
    try:
        TASK_LIST.pop(task_id)
        return success_response()
    except IndexError:
        return abort(404, errors=[f"Task {task_id} not found"])


@blp.route("/task-list", methods=["GET"], strict_slashes=False)
@blp.response(200, TaskSchema(many=True))
@blp.doc(description="Getting client task list")
def get_task():
    return TASK_LIST


@blp.route("/task/<int:task_id>", methods=["GET"], strict_slashes=False)
@blp.response(200, TaskSchema)
@blp.doc(description="Getting client task list")
def get_task(task_id: int):
    return TASK_LIST[task_id]


@blp.route("/update-task/<int:task_id>", methods=["PATCH"], strict_slashes=False)
@blp.arguments(UpdateTaskArgsSchema, location="json", as_kwargs=True)
@blp.response(200, UpdateTaskResponseSchema)
@blp.doc(desription="Modify an existing task")
def update_task(task_id: int, description: str):
    TASK_LIST[task_id].description = description
    return success_response()

