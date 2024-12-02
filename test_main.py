import os
import pytest
from unittest.mock import patch
from task_manager import TaskManager
from task import Priority, Task, Status
from main import add_task, show_tasks_by_category, show_all_tasks, search_task, task_done, update_task


TEST_FILE = "test.json"

mock_inputs = iter([
    "Test task",            # Title
    "Test description",     # Description
    "Работа",               # Category
    "2024-12-01",           # Due date
])

def mocked_input(prompt):
    return next(mock_inputs)


mock_search_inputs = iter([
    "task",
    "Работа",
])

def mocked_search_input(prompt):
    return next(mock_search_inputs)


mock_update_inputs = iter([
    "1",                  # Task ID
    "FastAPI",            # Title
    "Studing Fastapi",    # Description
    "Study",              # Category
    "2024-07-30",         # Due date
])

def mocked_update_input(prompt):
    return next(mock_update_inputs)


@pytest.fixture(scope = "session")
def task_manager():
    manager = TaskManager(filename = TEST_FILE)

    yield manager

    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


@patch('builtins.input', side_effect = mocked_input)
@patch('questionary.select')
def test_add_task(mock_select, mock_input, task_manager: TaskManager):
    mock_select.return_value.ask.return_value = Priority.medium
    add_task(task_manager)
    assert len(task_manager.tasks) == 1


def test_get_tasks(task_manager: TaskManager):
    tasks = show_all_tasks(task_manager)
    assert isinstance(tasks, list)
    assert all(isinstance(task, Task) for task in tasks)


def test_get_tasks_by_not_category(task_manager: TaskManager, capfd):
    with patch('builtins.input', return_value = "Study"):
        show_tasks_by_category(task_manager)

    captured = capfd.readouterr()
    assert "Задачи по категории 'Study' не найден" in captured.out


def test_get_task_by_category(task_manager: TaskManager):
    with patch('builtins.input', return_value = "Работа"):
        tasks = show_tasks_by_category(task_manager)
    assert all(task.category == "Работа" for task in tasks)


@patch('builtins.input', side_effect = mocked_search_input)
@patch('questionary.select')
def test_search_tasks(mock_select, mock_input, task_manager: TaskManager):
    mock_select.return_value.ask.return_value = Status.not_done.value
    tasks = search_task(task_manager)
    assert all(isinstance(task, Task) for task in tasks)
    assert all(task.status == Status.not_done for task in tasks)


@patch('builtins.input', side_effect = mocked_update_input)
@patch('questionary.select')
def test_update_task(mock_select, mock_input, task_manager: TaskManager, capfd):
    mock_select.return_value.ask.side_effect = [Priority.high.value, Status.not_done.value]

    update_task(task_manager)
    captured = capfd.readouterr()
    assert "Задача успешно обновлена." in captured.out


def test_task_done(task_manager: TaskManager, capfd):
    with patch('builtins.input', return_value = "1"):
        task_done(task_manager)
    
    captured = capfd.readouterr()
    assert "Задача обновлена.\n" == captured.out


def test_task_done_wrong_id(task_manager: TaskManager, capfd):
    with patch('builtins.input', return_value = "10"):
        task_done(task_manager)
    
    captured = capfd.readouterr()
    assert "По ID 10 задача не найдена" in captured.out


def test_delete_task_by_id(task_manager: TaskManager):
    res = task_manager.delete_task(1)
    assert res == "Задача успешно удалена."


def test_delete_task_by_category(task_manager: TaskManager):
    res = task_manager.delete_task(category = "Работа")
    assert res == "Задача успешно удалена."
