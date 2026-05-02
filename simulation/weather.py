import requests


def get_coordinates(city):
    """Obtiene las coordenadas de una ciudad usando la API de geocodificación de Open-Meteo."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "es", "format": "json"}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if not data.get("results"):
        return None, None

    result = data["results"][0]
    return result["latitude"], result["longitude"]


def get_weather_params(city):
    """
    Consulta Open-Meteo y devuelve p y f sugeridos según el tiempo actual.
    
    Lógica:
    - Viento fuerte (> 30 km/h) -> reduce p
    - Humedad alta (> 70%) -> aumenta p y f
    - Temperatura alta (> 35°C) -> aumenta f
    """
    lat, lon = get_coordinates(city)
    if lat is None:
        return {"error": f"No se encontró la ciudad: {city}"}

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relativehumidity_2m,windspeed_10m",
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    current = data.get("current", {})
    temperature = current.get("temperature_2m", 20)
    humidity = current.get("relativehumidity_2m", 50)
    wind_speed = current.get("windspeed_10m", 10)

    # Valores base
    p = 0.05
    f = 0.001

    # Ajustes según condiciones meteorológicas
    if wind_speed > 30:
        p *= 0.7  # viento fuerte, los árboles caen

    if humidity > 70:
        p *= 1.3  # humedad alta, árboles crecen mejor
        f *= 1.5  # más probabilidad de tormenta eléctrica

    if temperature > 35:
        f *= 2.0  # temperatura alta, más tormentas

    # Limitar valores entre 0 y 1
    p = round(min(max(p, 0.0), 1.0), 5)
    f = round(min(max(f, 0.0), 1.0), 5)

    return {
        "p": p,
        "f": f,
        "city": city,
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
        }
    }