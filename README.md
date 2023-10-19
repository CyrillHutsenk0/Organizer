# Organizer
___
This is the first large-scale project in which I, as a beackend developer, create a program for the organization of my affairs
## To-do List
___
This is a simple to-do list program.
Thanks to this project, I mastered
Flask, Flask-Smorest, Flask-SQLAlchemy,
Flask-Migrate, flask-marshmallow, marshmallow, 
SQLAlchemy. First, I will describe the
principle of operation, and then I 
will talk about the code itself

## Item 1 Flask-Smorest

The routes were recorded in a folder
with a to-do list, and there are also
diagrams there

**The first** route allows you to add changes.

```python
@blp.route("/add-task", methods=["POST"], strict_slashes=False)
@blp.arguments(AddTaskArgsSchema, location="json", as_kwargs=True)
@blp.doc(description="Creating new task")
def add_task(description: str):
    Task.add_task(description)
    return success_response()
```
*Full path = http://your_URL/api/todo-list/add-task* 

The **AddTaskArgsSchema** scheme is very easy, it just de-searializes the description of the change

```python
class AddTaskArgsSchema(Schema):
    description = f.String(allow_none=False, required=True)
```

**Task.add_task()** is a function in the Task class
that creates a new column in the database and fills
in the description field.
P.S.Now, when you encounter *@classmethod*,
remember this function of the Task class

```python
@classmethod
    def add_task(cls, description: str):
        db.session.add(cls(description=description, is_done=False))
        db.session.commit()
```

**The second** route is the deletion route, the 
principle is simple and clear, but we do not 
delete the Task automatically. Instead, we make
a note and do not return the table with the GET request

```python
@blp.route("/remove-task/<int:task_id>", methods=["DELETE"], strict_slashes=False)
@blp.doc(description="Deleting client existed task")
def delete_task(task_id: int):
    Task.delete_task(task_id)
    return success_response()
```
*Full path = http://your_URL/api/todo-list/remove-task/<int:task_id>* 

```python
@classmethod
    def delete_task(cls, task_id: int):
        task = db.get_or_404(cls, task_id)
        # db.session.delete(task)
        task.delete_at = func.now()
        db.session.commit()
```

**The third** route is GET. I have two of them,
the first returns a list of all rows in the table.
The second returns the table by a certain id

1. Get task list, *Full path = http://your_URL/api/todo-list/task-list* 

```python
@blp.route("/task-list", methods=["GET"], strict_slashes=False)
@blp.response(200, TaskResponseSchema(many=True))
@blp.doc(description="Getting client task list")
def get_task():
    return Task.get_task_list()
```
```python
@classmethod
    def get_task_list(cls):
        return db.session.execute(
            db.select(cls).where(cls.delete_at.is_(None)).order_by(cls.id)
        ).scalars()
```
**where(cls.delete_at.is_(None)** performs 
filtering and does not show rows that have been deleted

2. Get task, *Full path = http://your_URL/api/todo-list/task-list* 
```python
@blp.route("/task/<int:task_id>", methods=["GET"], strict_slashes=False)
@blp.response(200, TaskResponseSchema)
@blp.doc(description="Getting client task list")
def get_task(task_id: int):
    if task := Task.get_task(task_id):
        return task
    else:
        return abort(404, errors=str('This task was delete'))
```
A condition is built here, under
which any value of **delete_at** except
**None** will return a 404 error

```python
 @classmethod
    def get_task(cls, task_id: int):
        return db.session.execute(
            db.select(cls).where(cls.delete_at.is_(None), cls.id == task_id)
        ).scalar()
```

The scheme of the GET method contains a 
meta class and simply returns everything it knows
```python
class TaskResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        from organizer_project.models import Task

        model = Task
        include_pk = True
```

**The fourth** route is an update, it also has two types

1. Updates the description value
```python
@blp.route("/update-task/<int:task_id>", methods=["PATCH"], strict_slashes=False)
@blp.arguments(UpdateTaskArgsSchema, location="json", as_kwargs=True)
@blp.response(200)
@blp.doc(desription="Modify an existing task")
def update_task(task_id: int, description: str):
    Task.update_task(description, task_id)
    return success_response()
```
*Full path = http://your_URL/api/todo-list/update-task/<int:task_id>* 

```python
 @classmethod
    def update_task(cls, description: str, task_id: int):
        task = db.get_or_404(cls, task_id)
        task.description = description
        task.update_at = func.now()
        db.session.commit()
```

2. Updates the is_done value
```python
@blp.route("/change-done/<int:task_id>", methods=["PATCH"], strict_slashes=False)
@blp.doc(desription="Modify an existing task")
def update_task(task_id: int):
    Task.change_done(task_id)
    return success_response()
```
```python
@classmethod
    def change_done(cls, task_id: int):
        task = db.get_or_404(cls, task_id)
        is_done = task.is_done
        task.is_done = False if is_done else True
        task.change_done_at = func.now()
        db.session.commit()
```

## Item 2 Flask-SQLAlchemy
Here you can see the Task class itself, 
which is the table in this project

```python
class Task(db.Model):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    change_done_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    delete_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
```
All the class methods were given in point 1, but you can see the full list here
```python
@classmethod
    def add_task(cls, description: str):
        db.session.add(cls(description=description, is_done=False))
        db.session.commit()

    @classmethod
    def delete_task(cls, task_id: int):
        task = db.get_or_404(cls, task_id)
        # db.session.delete(task)
        task.delete_at = func.now()
        db.session.commit()

    @classmethod
    def get_task_list(cls):
        return db.session.execute(
            db.select(cls).where(cls.delete_at.is_(None)).order_by(cls.id)
        ).scalars()

    @classmethod
    def get_task(cls, task_id: int):
        return db.session.execute(
            db.select(cls).where(cls.delete_at.is_(None), cls.id == task_id)
        ).scalar()

    @classmethod
    def update_task(cls, description: str, task_id: int):
        task = db.get_or_404(cls, task_id)
        task.description = description
        task.update_at = func.now()
        db.session.commit()

    @classmethod
    def change_done(cls, task_id: int):
        task = db.get_or_404(cls, task_id)
        is_done = task.is_done
        task.is_done = False if is_done else True
        task.change_done_at = func.now()
        db.session.commit()
```

## Item 3 Schemas
A total of 3 schemes 
are used in the project
1. Add task
2. Get task or task list
3. Update task

+ ```python 
  class AddTaskArgsSchema(Schema):
    description = f.String(allow_none=False, required=True)
  ```
+ ```python 
  class TaskResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        from organizer_project.models import Task
        model = Task
        include_pk = True
  ```
+ ```python 
  class UpdateTaskArgsSchema(Schema):
    description = f.String(required=True)
  ```
