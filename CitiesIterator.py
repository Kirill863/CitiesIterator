import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class City:
    """Датакласс, представляющий информацию о городе."""
    name: str  # Название города
    lat: float  # Широта
    lon: float  # Долгота
    district: str  # Федеральный округ
    population: int  # Население
    subject: str  # Субъект РФ


class CitiesIterator:
    """
    Класс-итератор для работы со списком городов.
    """

    def __init__(self, cities_data: List[Dict], sort_by: Optional[str] = None, reverse: bool = False):
        """
        Инициализирует итератор городов.

        :param cities_data: Список словарей с данными о городах.
        :param sort_by: Параметр для сортировки (например, 'population', 'name').
        :param reverse: Флаг для обратной сортировки.
        """
        self.cities_data: List[Dict] = cities_data
        self._validate_data()  # Валидация данных
        self.cities: List[City] = [self._create_city(city_data) for city_data in cities_data]
        if sort_by is not None:
            self.sort_by(sort_by, reverse)
        self.min_population: int = 0  # Минимальный порог населения по умолчанию

    def _validate_data(self) -> None:
        """
        Проверяет наличие всех необходимых полей в данных о городах.

        :raises ValueError: Если отсутствуют обязательные поля.
        """
        required_fields = {"name", "district", "population", "subject", "coords"}
        coords_fields = {"lat", "lon"}

        for city_data in self.cities_data:
            if not required_fields.issubset(city_data.keys()):
                raise ValueError(f"Отсутствуют обязательные поля в данных: {city_data}")
            if not coords_fields.issubset(city_data["coords"].keys()):
                raise ValueError(f"Отсутствуют обязательные поля в 'coords': {city_data}")

    def _create_city(self, city_data: Dict) -> City:
        """
        Создает объект City из словаря с данными о городе.

        :param city_data: Словарь с данными о городе.
        :return: Объект City.
        :raises ValueError: Если данные некорректны или отсутствуют ключи.
        """
        try:
            return City(
                name=city_data["name"],
                lat=float(city_data["coords"]["lat"]),  # Преобразование в float
                lon=float(city_data["coords"]["lon"]),  # Преобразование в float
                district=city_data["district"],
                population=city_data["population"],
                subject=city_data["subject"]
            )
        except KeyError as e:
            raise ValueError(f"Ошибка при создании города: отсутствует ключ {e}")
        except ValueError as e:
            raise ValueError(f"Ошибка при преобразовании данных: {e}")

    def set_population_filter(self, min_population: int) -> None:
        """
        Устанавливает минимальный порог населения для фильтрации городов.

        :param min_population: Минимальное население города.
        """
        self.min_population = min_population

    def sort_by(self, parameter: str, reverse: bool = False) -> None:
        """
        Сортирует список городов по указанному параметру.

        :param parameter: Параметр для сортировки (например, 'population', 'name').
        :param reverse: Флаг для обратной сортировки.
        :raises ValueError: Если указанный параметр не существует.
        """
        if not hasattr(self.cities[0], parameter):
            raise ValueError(f"Невозможно отсортировать по несуществующему параметру: {parameter}")
        self.cities.sort(key=lambda city: getattr(city, parameter), reverse=reverse)

    def __iter__(self) -> "CitiesIterator":
        """
        Возвращает итератор.

        :return: Экземпляр самого себя.
        """
        self.index = 0
        return self

    def __next__(self) -> City:
        """
        Возвращает следующий город, удовлетворяющий условиям фильтрации.

        :return: Объект City.
        :raises StopIteration: Если больше нет подходящих городов.
        """
        while self.index < len(self.cities):
            city = self.cities[self.index]
            self.index += 1
            if city.population >= self.min_population:
                return city
        raise StopIteration


def load_cities_from_json(file_path: str) -> List[Dict]:
    """
    Загружает данные о городах из JSON файла.

    :param file_path: Путь к JSON файлу.
    :return: Список словарей с данными о городах.
    :raises FileNotFoundError: Если файл не найден.
    :raises ValueError: Если файл содержит некорректный JSON.
    """
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            cities_data: List[Dict] = json.load(file)
            return cities_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка при декодировании JSON: {e}")


# Пример использования
if __name__ == "__main__":
    json_file_path: str = "cities.json"

    try:
        # Загрузка данных из JSON
        cities_data: List[Dict] = load_cities_from_json(json_file_path)

        # Создание итератора городов
        cities_iterator: CitiesIterator = CitiesIterator(cities_data, sort_by="population", reverse=True)

        # Установка фильтра по населению
        cities_iterator.set_population_filter(min_population=1000000)

        # Итерация по городам
        for city in cities_iterator:
            print(f"{city.name} ({city.population})")

    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}")