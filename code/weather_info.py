from dataclasses import dataclass

@dataclass
class WeatherInfo:
    area : str
    temperature_now : str
    temperature_low : str
    temperature_high : str
    weather_today : str