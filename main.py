from typing import Callable
from pydantic_core._pydantic_core import ValidationError
from task_manager import TaskManager, AddTask, UpdateTask
from utils import (
    get_priority_input,
    task_template,
    get_input,
    get_status_input,
    get_validated_date
)


APP_DESCRIPTION = '''
Добро пожаловать в Task Manager — удобный инструмент 
для управления вашими задачами. Вы можете добавлять, 
просматривать, изменять, отмечать выполненные задачи и удалять их.

Выберите действие:

1. Просмотр всех задач
2. Просмотр задач по категории
3. Поиск задач
4. Добавить задачу
5. Изменить задачу
6. Отметить задачу как выполненную
7. Удалить задачу
8. Меню
9. Выход или q
'''


def show_all_tasks(manager: TaskManager) -> None:
    """Выводит все задачи пользователя."""
    if not manager.tasks:
        print("Нет задач.")
    else:
        for task in manager.tasks:
            print(task_template(task))
    return manager.tasks


def show_tasks_by_category(manager: TaskManager) -> None:
    """Выводит задачи по указанной категории."""
    category = input("Введите категорию: ").strip()
    tasks = manager.get_by_category(category)

    if not tasks:
        print(f"Задачи по категории '{category}' не найден.\n")
    else:
        for task in tasks:
            print(task_template(task))
    return tasks


def search_task(manager: TaskManager) -> None:
    """Ищет задачи по ключевому слову, категории и статусу."""
    print("Введите ключевое слово")
    keyword = input("Ключевое слово: ").strip()
    category = input("Категория (по желанию): ").strip()
    status = get_status_input()
    
    tasks = manager.search_tasks(keyword, category, status)
    if not tasks:
        print("По вашему запросу задачи не найдены.\n")
        return

    for task in tasks:
        print(task_template(task))
    return tasks


def add_task(manager: TaskManager) -> None:
    """Добавляет новую задачу."""
    title = get_input("Title")
    description = get_input("Description")
    category = get_input("Category")
    due_date = get_validated_date()
    priority = get_priority_input()

    try:
        new_task = AddTask(
            title = title.strip(),
            description = description.strip(),
            category = category.strip(),
            due_date = due_date.strip(),
            priority = priority,
        )
    
        res = manager.add_task(new_task)
        print(res, "\n")
    except ValidationError as ex:
        print(ex)


def update_task(manager: TaskManager) -> None:
    """Обновляет существующую задачу."""
    print("Изменить задачу")
    print("Если не хотите именить полю нажмите 'enter'")

    while True:
        task_id = input("Task ID: ")
        try:
            task_id = int(task_id)
        except ValueError:
            print("Ошибка введите номер задачи")
            continue
        break

    task_to_update = manager.get_by_id(task_id)
    if not task_to_update:
        print(f"По ID {task_id} задача не найдена\n")
        return
    
    title = get_input("title", task_to_update.title)
    description = get_input("Description", task_to_update.description)
    category = get_input("Category", task_to_update.category)
    due_date = get_validated_date(current_date = task_to_update.due_date)
    priority = get_priority_input()
    status = get_status_input() or task_to_update.status

    try:
        updated_task = UpdateTask(
            title = title,
            description = description,
            category = category,
            due_date = due_date,
            priority = priority,
            status = status,
        )

        res = manager.update_task(task_id, updated_task)
        print(res, "\n")
    except ValidationError as ex:
        print(ex)


def task_done(manager: TaskManager) -> None:
    """Помечает задачу как выполненную."""
    while True:
        input_val = input("Task ID: ")
        try:
            task_id = int(input_val)
        except ValueError:
            print("Ошибка введите номер задачи")
            continue

        res = manager.mark_as_completed(task_id)
        if not res:
            print(f"По ID {task_id} задача не найдена\n")
            break
        
        print(res, "\n")
        break


def delete_task(manager: TaskManager) -> None:
    """Удаляет задачу."""
    while True:
        input_val = input("ID задачи: ")
        try:
            task_id = int(input_val)
        except ValueError:
            print("Ошибка введите номер задачи")
            continue
        
        res = manager.delete_task(task_id)
        print(res, "\n")
        break


def main() -> None:
    print(APP_DESCRIPTION)
    manager = TaskManager()

    # Словарь для соответствия ввода пользователя и функций
    funcs: dict[str, Callable[[TaskManager], None]] = {
        "1": show_all_tasks,
        "2": show_tasks_by_category,
        "3": search_task,
        "4": add_task,
        "5": update_task,
        "6": task_done,
        "7": delete_task,
    }

    while True:
        choice = input("Введите номер действия: ")
        
        if choice == '8':
            print(APP_DESCRIPTION)
            continue

        if choice in {"9", "q"}:
            break

        func = funcs.get(choice)
        if not func:
            print("Такого команды нет")
            continue
        
        func(manager)


if __name__ == "__main__":
    main()
