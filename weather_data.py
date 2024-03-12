import requests
import json
import argparse
import os
import datetime

# Define arguments
parser = argparse.ArgumentParser(description="Retrieve weather data")
parser.add_argument("--folder", type=str, default="weather_data", help="The destination folder to store the weather data")
parser.add_argument("--frequency", type=str, choices=["daily", "hourly"], default="daily", help="How often to download the data")
parser.add_argument("--country", type=str, default="Prague", help="The country to extract the data for")
args = parser.parse_args()

# Define constants
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "a94674834395ff8b8aa7cddee69ef429"  # Replace 'YOUR_API_KEY' with your actual API key
BUCKET_NAME = "your-bucket-name"  # Change this to your cloud storage bucket name

# Create the destination folder if it does not exist
if not os.path.exists(args.folder):
    os.makedirs(args.folder)

def retrieve_weather_data():
    # Parameters for the API request (coordinates of Prague)
    params = {
        "q": "Prague,CZ",  # City name and country code
        "appid": API_KEY,  # API key
        "units": "metric"  # Units for temperature (metric for Celsius)
    }

    # Send GET request to OpenWeatherMap API
    response = requests.get(API_ENDPOINT, params=params)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Extract relevant data
        relevant_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "weather_description": data["weather"][0]["description"]
        }

        # Print extracted data
        print("Extracted Weather Data:")
        print(json.dumps(relevant_data, indent=4))

        # Save extracted data to a JSON file
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{args.folder}/weather_data_{timestamp}.json"
        with open(filename, "w") as json_file:
            json.dump(relevant_data, json_file, indent=4)

        print("Weather data saved to 'weather_data.json' file.")
        # Upload the file to AWS S3 bucket using AWS CLI
        os.system(f"aws s3 cp {filename} s3://{AWS_BUCKET_NAME}/{args.folder}/")
        # Delete the local file
        os.remove(filename)
        print("Weather data uploaded to AWS S3 bucket.")
    else:
        # Handle the error
        print("Failed to retrieve weather data. Status code:", response.status_code)

# Retrieve weather data
retrieve_weather_data()