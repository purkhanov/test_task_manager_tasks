from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field, StringConstraints


class Status(Enum):
    done = 'Выполнена'
    not_done = 'Не выполнена'


class Priority(Enum):
    low = 'Низкий'
    medium = 'Средний'
    high = 'Высокий'


PRIORITY = Annotated[Priority, Field(default = Priority.low)]
STATUS = Annotated[Status, Field(default = Status.not_done)]
STR_TYPE = Annotated[
    str,
    StringConstraints(strip_whitespace = True),
]


class AddTask(BaseModel):
    title: STR_TYPE
    description: STR_TYPE
    category: STR_TYPE
    due_date: str
    priority: PRIORITY


class Task(AddTask):
    id: int = Field(gt = 0)
    status: STATUS
    priority: PRIORITY


class UpdateTask(AddTask):
    status: STATUS

