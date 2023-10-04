from flask_marshmallow import Schema
from marshmallow import fields as f, validates_schema, ValidationError, validates

from organizer_project.models import Task


class AddTaskArgsSchema(Schema):
    description = f.String(allow_none=False, required=True)


class TaskSchema(Schema):
    id_ = f.Integer(required=True)
    description = f.String(required=True)


# class TaskListSchema(Schema):
#     task = f.List(Task)


class TodoListResponseSchema(Schema):
    pass
    # tasks = f.NE(Task)


class UpdateTaskArgsSchema(Schema):
    description = f.String(required=True)


class UpdateTaskResponseSchema(Schema):
    description = f.String(required=True)
