from dataclasses import dataclass

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