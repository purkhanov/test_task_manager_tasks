import re
import questionary
from task import Task


def task_template(task: Task) -> str:
    """
    Возвращает строковое представление задачи.

    Args:
        task (Task): Объект задачи.

    Returns:
        str: Отформатированная строка с информацией о задаче.
    """
    return f'''
    ID: {task.id}
    Title: {task.title}
    Description: {task.description}
    Category: {task.category}
    Priority: {task.priority.value}
    Status: {task.status.value}
    Due date: {task.due_date}
    '''


def get_input(prompt: str, current_value: str | None = None) -> str:
    """
    Запрашивает ввод пользователя. Если текущее значение передано и пользователь ничего не вводит,
    возвращается текущее значение.

    Args:
        prompt (str): Сообщение для пользователя.
        current_value (str | None): Текущее значение поля.

    Returns:
        str: Введенное пользователем значение или текущее значение.
    """
    if current_value:
        print(f"{prompt}: {current_value}")

    while True:
        user_input = input(f"{prompt}: ").strip()

        if current_value and user_input == "":
            return current_value

        if user_input == "":
            print(f"{prompt} не может быть пустым")
            continue

        return user_input
    

def get_priority_input() -> str:
    """
    Запрашивает у пользователя выбор приоритета через Questionary.

    Returns:
        str: Выбранный приоритет.
    """
    return questionary.select(
        "Priority:",
        choices=["Низкий", "Средний", "Высокий"]
    ).ask()


def get_status_input() -> str | None:
    """
    Запрашивает у пользователя выбор статуса через Questionary.

    Returns:
        str | None: Выбранный статус или None, если статус не указан.
    """
    status = questionary.select(
        "Статус (по желанию):",
        choices = ["Не указать", "Выполнена", "Не выполнена"],
    ).ask()

    if status == "Не указать":
        return None
    
    return status


def get_validated_date(current_date: str | None = None) -> str:
    """
    Запрашивает ввод даты и проверяет ее формат.

    Args:
        current_date (str | None): Текущее значение даты, если доступно.

    Returns:
        str: Валидированная дата.
    """
    date_pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

    while True:
        due_date = input("Due date (в формате YYYY-MM-DD): ").strip()

        if current_date and due_date == "":
            return current_date

        if not re.match(date_pattern, due_date):
            print("Некорректная дата. Пример: 2024-01-30")
            continue

        return due_date




