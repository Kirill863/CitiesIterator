import json
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path


@dataclass
class City:
    name: str  # Название города
    lat: float  # Широта
    lon: float  # Долгота
    district: str  # Федеральный округ
    population: int  # Население
    subject: str  # Субъект РФ


class CitiesIterator:
    def __init__(self, cities_data: List[Dict], sort_by: str = None, reverse: bool = False):
        self.cities_data = cities_data
        self._validate_data()
        self.cities = [self._create_city(city_data) for city_data in cities_data]
        if sort_by is not None:
            self.sort_by(sort_by, reverse)
        self.min_population = 0  # Минимальный порог населения по умолчанию

    def _validate_data(self):
        required_fields = {"name", "district", "population", "subject", "coords"}
        coords_fields = {"lat", "lon"}

        for city_data in self.cities_data:
            if not required_fields.issubset(city_data.keys()):
                raise ValueError(f"Отсутствуют обязательные поля в данных: {city_data}")
            if not coords_fields.issubset(city_data["coords"].keys()):
                raise ValueError(f"Отсутствуют обязательные поля в 'coords': {city_data}")

    def _create_city(self, city_data: Dict) -> City:
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

    def set_population_filter(self, min_population: int):
        self.min_population = min_population

    def sort_by(self, parameter: str, reverse: bool = False):
        if not hasattr(self.cities[0], parameter):
            raise ValueError(f"Невозможно отсортировать по несуществующему параметру: {parameter}")
        self.cities.sort(key=lambda city: getattr(city, parameter), reverse=reverse)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        while self.index < len(self.cities):
            city = self.cities[self.index]
            self.index += 1
            if city.population >= self.min_population:
                return city
        raise StopIteration


# Функция для загрузки данных из JSON файла
def load_cities_from_json(file_path: str) -> list:
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            cities_data = json.load(file)
            return cities_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка при декодировании JSON: {e}")


# Пример использования
if __name__ == "__main__":
    json_file_path = "cities.json"

    try:
        # Загрузка данных из JSON
        cities_data = load_cities_from_json(json_file_path)

        # Создание итератора городов
        cities_iterator = CitiesIterator(cities_data, sort_by="population", reverse=True)

        # Установка фильтра по населению
        cities_iterator.set_population_filter(min_population=10000)

        # Итерация по городам
        for city in cities_iterator:
            print(f"{city.name} ({city.population})")

    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}")