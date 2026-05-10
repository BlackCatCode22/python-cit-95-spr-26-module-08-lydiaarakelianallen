from pathlib import Path
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Weather Dashboard")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

NWS_HEADERS = {"User-Agent": "FCC-Student-App"}

OPEN_METEO_CODES = {
    0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy Fog",
    51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle",
    61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
    71: "Light Snow", 73: "Snow", 75: "Heavy Snow", 77: "Snow Grains",
    80: "Rain Showers", 81: "Heavy Rain Showers", 82: "Violent Rain Showers",
    85: "Snow Showers", 86: "Heavy Snow Showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ Hail", 99: "Thunderstorm w/ Heavy Hail",
}


async def get_nws_weather(lat: float, lon: float, city_name: str) -> dict:
    async with httpx.AsyncClient(headers=NWS_HEADERS, timeout=15.0) as client:
        points_resp = await client.get(f"https://api.weather.gov/points/{lat},{lon}")
        points_resp.raise_for_status()
        forecast_url = points_resp.json()["properties"]["forecast"]

        forecast_resp = await client.get(forecast_url)
        forecast_resp.raise_for_status()
        period = forecast_resp.json()["properties"]["periods"][0]

    return {
        "city": city_name,
        "temperature": period["temperature"],
        "unit": period["temperatureUnit"],
        "conditions": period["shortForecast"],
        "wind": f"{period['windSpeed']} {period['windDirection']}",
    }


async def get_london_weather() -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=51.5074&longitude=-0.1278"
        "&current=temperature_2m,weather_code"
        "&temperature_unit=fahrenheit"
    )
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        current = resp.json()["current"]

    code = current["weather_code"]
    return {
        "city": "London, UK",
        "temperature": round(current["temperature_2m"]),
        "unit": "F",
        "conditions": OPEN_METEO_CODES.get(code, "Unknown"),
        "wind": "N/A",
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    fresno, new_york, london = None, None, None
    errors = []

    try:
        fresno = await get_nws_weather(36.7378, -119.7871, "Fresno, CA")
    except Exception as e:
        errors.append(f"Fresno: {e}")

    try:
        new_york = await get_nws_weather(40.7128, -74.0060, "New York, NY")
    except Exception as e:
        errors.append(f"New York: {e}")

    try:
        london = await get_london_weather()
    except Exception as e:
        errors.append(f"London: {e}")

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "page_title": "Weather Dashboard",
            "fresno": fresno,
            "new_york": new_york,
            "london": london,
            "errors": errors,
        },
    )
