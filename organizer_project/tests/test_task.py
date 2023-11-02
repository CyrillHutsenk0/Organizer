import string
from random import random

import requests
from organizer_project.config import SERVER_URL
from organizer_project.models import Task

import requests

def test_getting_post():
    response = requests.get(url="http://127.0.0.1:5000/api/todo-list/task-list")
    assert requests.codes["ok"], "Received status code is not equal expected"
