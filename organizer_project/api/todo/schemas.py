from flask_marshmallow import Schema
from marshmallow import fields as f
from flask_marshmallow.sqla import SQLAlchemyAutoSchema


class AddTaskArgsSchema(Schema):
    description = f.String(allow_none=False, required=True)


class TaskResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        from organizer_project.models import Task

        model = Task
        include_pk = True


# class TaskListSchema(Schema):
#     task = f.List(Task)


class TodoListResponseSchema(Schema):
    pass
    # tasks = f.NE(Task)


class UpdateTaskArgsSchema(Schema):
    description = f.String(required=True)
