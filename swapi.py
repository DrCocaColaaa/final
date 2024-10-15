import os
import requests


class APIRequester:
    def __init__(self, base_url):
        """Инициализация объекта класса APIRequester."""
        self.base_url = base_url

    def get(self, url):
        """Выполнение GET-запроса с помощью библиотеки requests."""
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None


class SWRequester(APIRequester):
    def __init__(self, base_url="https://swapi.dev/api/"):
        """Инициализация объекта класса SWRequester."""
        super().__init__(base_url)

    def get_sw_categories(self):
        """Получение списка доступных категорий SWAPI."""
        response = self.get(self.base_url)
        if response:
            data = response.json()
            return list(data.keys())
        return []

    def get_sw_info(self, sw_type):
        """Получение информации о конкретной категории SWAPI."""
        url = f"{self.base_url}{sw_type}/"
        response = self.get(url)
        if response:
            return response.text
        return ""


def save_sw_data():
    """
    Создание объекта класса SWRequester, директории data
    и сохранение информации о категориях SWAPI.
    """
    sw_requester = SWRequester()
    categories = sw_requester.get_sw_categories()

    # Создание директории data
    if not os.path.exists("data"):
        os.makedirs("data")

    for category in categories:
        info = sw_requester.get_sw_info(category)
        with open(f"data/{category}.txt", "w", encoding="utf-8") as file:
            file.write(info)


# Вызов функции
save_sw_data()
