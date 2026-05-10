import requests
import json

# Our specified User-Agent
USER_AGENT = 'FCC-Student-App'
HEADERS = {'User-Agent': USER_AGENT}

# The locations we want to fetch weather for
LOCATIONS = {
    "Fresno, CA": {"lat": 36.73, "lon": -119.78},
    "New York, NY": {"lat": 40.71, "lon": -74.00},
}

print(f"Hello, Thing One here! Let's fetch some weather data for {len(LOCATIONS)} locations.\n")


for city_name, coords in LOCATIONS.items():
    lat = coords["lat"]
    lon = coords["lon"]
    print(f"--- Fetching weather for {city_name} (Lat: {lat}, Lon: {lon}) ---")

    try:
        # Step 1: Get 'points' data to find observation stations URL
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        print(f"Requesting NWS 'points' URL: {points_url}")
        points_response = requests.get(points_url, headers=HEADERS)
        points_response.raise_for_status()
        points_data = points_response.json()

        observation_stations_url = points_data['properties']['observationStations']
        print(f"Found observation stations URL: {observation_stations_url}")

        # Step 2: Get the list of observation stations
        print(f"Requesting NWS observation stations list URL: {observation_stations_url}")
        stations_response = requests.get(observation_stations_url, headers=HEADERS)
        stations_response.raise_for_status()
        stations_data = stations_response.json()

        if not stations_data['features']:
            print(f"No observation stations found for {city_name}.")
            continue

        # For simplicity, we'll just pick the first station in the list
        first_station_id = stations_data['features'][0]['properties']['stationIdentifier']
        print(f"Using observation station: {first_station_id}")

        # Step 3: Fetch the latest observation for that station
        latest_observation_url = f"https://api.weather.gov/stations/{first_station_id}/observations/latest"
        print(f"Requesting NWS latest observation URL: {latest_observation_url}")
        observation_response = requests.get(latest_observation_url, headers=HEADERS)
        observation_response.raise_for_status()
        latest_observation_data = observation_response.json()

        # Step 4: Print the raw JSON
        print(f"\nRAW JSON for {city_name}'s latest observation:")
        # Using json.dumps with indent makes the JSON much more readable
        print(json.dumps(latest_observation_data, indent=2))

    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error occurred for {city_name}: {e}")
        if e.response: # If there's a response body, print it
            print(f"Response content: {e.response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Connection error occurred for {city_name}: {e}")
    except requests.exceptions.Timeout as e:
        print(f"ERROR: Request timed out for {city_name}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: An unexpected request error occurred for {city_name}: {e}")
    except (KeyError, IndexError) as e:
        print(f"ERROR: Missing expected key or index in JSON response for {city_name}: {e}")
        # Optionally print the full data that caused the error for debugging
        # print(f"Problematic points_data: {json.dumps(points_data, indent=2)}")
        # print(f"Problematic stations_data: {json.dumps(stations_data, indent=2)}")
    print("\n" + "=" * 80 + "\n") # Big separator for clarity between cities

print("All done! Hope you learned something cool about APIs today!")
