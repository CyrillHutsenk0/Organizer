# Organizer
___
This is the first large-scale project in which I, as a beackend developer, create a program for the organization of my affairs
## To-do List
___
It's a simple to-do list app.
Thanks to this project, I learned
work with databases, learned how to use 
the text exchange of data JSON, will learn 
routing, API. First I will describe
the principle of action, and then 
I will tell you about the code itself

## Item 1 How to run

1. The program is launched through **app.py**
2. The database is used PostgreSQL
3. Create an .inv file to add your personal details

## Item 2 API
___
**POST** 
___
the route allows you to create a Task.

```python
@blp.route("/add-task", methods=["POST"], strict_slashes=False)

```
*Full path = http://your_URL/api/todo-list/add-task* 
___
**DELETE** 
___
route is the deletion route, the 
principle is simple and clear, but we do not 
delete the Task automatically. Instead, we make
a note and do not return the table with the GET request

```python
@blp.route("/remove-task/<int:task_id>", methods=["DELETE"], strict_slashes=False)

```
*Full path = http://your_URL/api/todo-list/remove-task/<int:task_id>* 
___
**GET** 
___
route is GET. I have two of them,
the first returns a list of all rows in the table.
The second returns the table by a certain id

1. Get task list, *Full path = http://your_URL/api/todo-list/task-list* 

```python
@blp.route("/task-list", methods=["GET"], strict_slashes=False)
```

2. Get task, *Full path = http://your_URL/api/todo-list/task-list* 
```python
@blp.route("/task/<int:task_id>", methods=["GET"], strict_slashes=False)
```
___
**PATCH** 
___
route is an update, it also has two types

1. Updates the description value
```python
@blp.route("/update-task/<int:task_id>", methods=["PATCH"], strict_slashes=False)
```
*Full path = http://your_URL/api/todo-list/update-task/<int:task_id>* 

2. Updates the is_done value
```python
@blp.route("/change-done/<int:task_id>", methods=["PATCH"], strict_slashes=False)
```

## Item 2 DATABASE
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
This class also has its own functions
```python
    def add_task(cls, description: str)

    def delete_task(cls, task_id: int)

    def get_task_list(cls)
    
    def get_task(cls, task_id: int)
    
    def update_task(cls, description: str, task_id: int)
    
    def change_done(cls, task_id: int)
    
    def call_date_delete(cls, task_id: int)
```