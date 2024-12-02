import json
from task import Task, AddTask, UpdateTask, Status


# Путь к файлу с задачами по умолчанию
DATA_PATH = "./data.json"


class TaskManager:
    """
    Класс для управления задачами. 
    Позволяет добавлять, обновлять, удалять и искать задачи, а также сохранять их в файл.
    """

    def __init__(self, filename: str = DATA_PATH) -> None:
        """
        Инициализация менеджера задач.

        :param filename: Путь к файлу с данными задач.
        """
        self.filename: str = filename
        self.tasks: list[Task] = self.__load_tasks()

    
    def __load_tasks(self) -> list[Task]:
        """
        Загрузка задач из JSON-файла.

        :return: Список объектов Task.
        """
        try:
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
            
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден. Создан пустой список задач.")
            return []
        
        except json.JSONDecodeError:
            print(f"Ошибка чтения данных из файла {self.filename}. Проверьте формат JSON.")
            return []
    

    def _save_tasks(self) -> None:
        """
        Сохранение текущих задач в JSON-файл.
        """
        with open(self.filename, 'w', encoding = 'utf-8') as file:
            json.dump(
                [task.model_dump(mode = 'json') for task in self.tasks],
                file,
                indent = 2,
                ensure_ascii = False,
            )


    def add_task(self, data: AddTask) -> str:
        """
        Добавление новой задачи.

        :param data: Данные для добавления задачи.
        :return: Сообщение о результате операции.
        """
        task_id = max([task.id for task in self.tasks], default = 0) + 1
        data_dict = data.model_dump()
        task = Task(
            id = task_id,
            **data_dict,
            status  = Status.not_done,
        )
        self.tasks.append(task)
        self._save_tasks()

        return "Задача успешно добавлена."


    def delete_task(self, task_id: int = None, category: str = None) -> str:
        """
        Удаление задачи по ID или категории.

        :param task_id: ID задачи для удаления.
        :param category: Категория задач для удаления.
        :return: Сообщение о результате операции.
        """
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
        
        self._save_tasks()
        return "Задача успешно удалена."


    def get_by_category(self, category: str) -> list[Task]:
        """
        Получение задач по категории.

        :param category: Категория для поиска.
        :return: Список задач указанной категории.
        """
        return [task for task in self.tasks if task.category.lower() == category.lower()]
    

    def get_by_id(self, task_id: str) -> Task | None:
        """
        Получение задачи по ID.

        :param task_id: ID задачи.
        :return: Объект Task или None, если задача не найдена.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    
    def update_task(self, task_id: int, update_data: UpdateTask) -> str:
        """
        Обновление задачи по ID.

        :param task_id: ID задачи для обновления.
        :param update_data: Данные для обновления задачи.
        :return: Сообщение о результате операции.
        """
        for task in self.tasks:
            if task.id == task_id:
                updated_task = Task(id=task_id,**update_data.model_dump())
                self.tasks[self.tasks.index(task)] = updated_task
                self._save_tasks()
                return "Задача успешно обновлена."
        return "Задача не найдена."
    

    def mark_as_completed(self, task_id: int) -> str | None:
        """
        Пометить задачу как выполненную.

        :param task_id: ID задачи.
        :return: Сообщение о результате операции или None, если задача не найдена.
        """
        for task in self.tasks:
            if task.id == task_id:
                task.status = Status.done
                self._save_tasks()
                return "Задача обновлена."
        return None

    
    def search_tasks(
            self, keyword: str = None, category: str = None, status: str = None
    ) -> list[Task]:
        """
        Поиск задач по ключевым словам, категории или статусу.

        :param keyword: Ключевое слово для поиска в названии или описании.
        :param category: Категория для фильтрации.
        :param status: Статус для фильтрации.
        :return: Список задач, соответствующих критериям поиска.
        """
        result = self.tasks

        if keyword:
            kw = keyword.lower()
            result = [task for task in result if kw in task.title.lower() or kw in task.description.lower()]

        if category:
            c = category.lower()
            result = [task for task in result if task.category.lower() == c]

        if status:
            result = [task for task in result if task.status.value.lower() == status.lower()]

        return result

