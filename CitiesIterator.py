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
    