from flask_smorest import Blueprint, abort
from .schemas import AddTaskArgsSchema, TaskResponseSchema, UpdateTaskArgsSchema
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
    Task.add_task(description)
    return success_response()


@blp.route("/remove-task/<int:task_id>", methods=["DELETE"], strict_slashes=False)
@blp.doc(description="Deleting client existed task")
def delete_task(task_id: int):
    Task.delete_task(task_id)
    return success_response()


@blp.route("/task-list", methods=["GET"], strict_slashes=False)
@blp.response(200, TaskResponseSchema(many=True))
@blp.doc(description="Getting client task list")
def get_task():
    return Task.get_task_list()


@blp.route("/task/<int:task_id>", methods=["GET"], strict_slashes=False)
@blp.response(200, TaskResponseSchema)
@blp.doc(description="Getting client task list")
def get_task(task_id: int):
    if task := Task.get_task(task_id):
        return task
    else:
        return abort(
            404, errors=str(f"This task was delete {Task.call_date_delete(task_id)}")
        )


@blp.route("/update-task/<int:task_id>", methods=["PATCH"], strict_slashes=False)
@blp.arguments(UpdateTaskArgsSchema, location="json", as_kwargs=True)
@blp.response(200)
@blp.doc(desription="Modify an existing task")
def update_task(task_id: int, description: str):
    Task.update_task(description, task_id)
    return success_response()


@blp.route("/change-done/<int:task_id>", methods=["PATCH"], strict_slashes=False)
@blp.doc(desription="Modify an existing task")
def update_task(task_id: int):
    Task.change_done(task_id)
    return success_response()
