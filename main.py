# weather app in python

# import library configparser from Python's configparser module
import argparse
import json
import sys
import os
import style
from configparser import ConfigParser
from urllib import error, parse, request
# from pprint import pp

BASE_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)

# System call
os.system("")


def get_api_key():
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


def read_user_cli_args():
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="Getting weather and temperature information of a city"
    )
    parser.add_argument(
        "city", nargs="+", type=str, help="Enter the city name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="Display the temperature in imperial units",
    )
    return parser.parse_args()


def build_weather_query(city_input, imperial=False):
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url


def get_weather_data(query_url):
    """Makes an API request to a URL and returns the data as a Python object.

    Args:
        query_url (str): URL formatted for OpenWeather's city name endpoint

    Returns:
        dict: Weather information for a specific city
    """

    try:
        # uses urllib.request.urlopen() to make an HTTP GET request
        # to the query_url parameter and saves the result as response
        response = request.urlopen(query_url)
    # catches any error. HTTPError that occurs during the HTTP request.
    # It opens up an except block
    except error.HTTPError as http_error:
        if http_error.code == 401:
            sys.exit("Access denied. Please check your API key.")
        elif http_error.code == 400:
            sys.exit("Can not find weather data for this city.")
        else:
            sys.exit(f"Something went wrong...({http_error.code})")

    # extract data from response
    try:
        data = response.read()
    except json.JSONDecodeError:
        sys.exit("Could not read the server response")
    # returns a call to json.loads() with data as the argument.
    # The function returns a Python object holding the JSON information fetched from query_url
    return json.loads(data)


def display_weather_info(weather_data, imperial=False):
    """Prints formatted weather information about a city.

    Args:
        weather_data (dict): API response from OpenWeather by city name
        imperial (bool): Whether to use imperial units for temperature

    More information at https://openweathermap.org/current#name
    """
    city = weather_data["name"]
    weather_id = weather_data["weather"][0]["id"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)

    weather_symbol, color = select_weather_display_params(weather_id)
    style.change_color(color)
    print(f"\t{weather_symbol}", end=" ")
    print(f"{weather_description.capitalize():^{style.PADDING}}", end=" ")
    style.change_color(style.RESET)
    print(f"({temperature}°{'F' if imperial else 'C'})")


def select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("💥", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.DARK_GRAY)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.GREEN)
    elif weather_id in CLEAR:
        display_params = ("🔆", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", style.WHITE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", style.MAGENTA)
    return display_params


if __name__ == "__main__":
    user_args = read_user_cli_args()
    # print(user_args.city, user_args.imperial)
    query_url = build_weather_query(user_args.city, user_args.imperial)
    # print(query_url)
    weather_data = get_weather_data(query_url)
    # pp(weather_data)
    display_weather_info(weather_data, user_args.imperial)
