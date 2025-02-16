import json
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path

def load_cities_from_json(file_path: str) -> list:
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            cities_data = json.load(file)
            return cities_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка при декодировании JSON: {e}")
        
@dataclass
class City:
    name: str
    lat: float
    lon: float
    district: str
    population: int
    subject: str

class CitiesIterator:
    def __init__(self, cities_data: List[Dict], sort_by: str = None, reverse: bool = False):
        
        self.cities_data = cities_data
        self._validate_data()
        self.cities = [self._create_city(city_data) for city_data in cities_data]
        if sort_by is not None:
            self.sort_by(sort_by, reverse)
        self.min_population = 0  

    def _validate_data(self):
        """Проверка наличия всех необходимых полей в данных."""
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
                lat=city_data["coords"]["lat"],
                lon=city_data["coords"]["lon"],
                district=city_data["district"],
                population=city_data["population"],
                subject=city_data["subject"]
            )
        except KeyError as e:
            raise ValueError(f"Ошибка при создании города: отсутствует ключ {e}")
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
    
if __name__ == "__main__":
    cities_data = 

    # Создаем итератор
    cities_iterator = CitiesIterator(cities_data, sort_by="population", reverse=True)

    # Устанавливаем фильтр по населению
    cities_iterator.set_population_filter(min_population=1000000)

    # Итерация по городам
    for city in cities_iterator:
        print(f"{city.name} ({city.population})")