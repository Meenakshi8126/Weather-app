import requests
import json
import argparse
import os
from jinja2 import Template
import datetime

# Import the AWS SDK for Python (boto3)
import boto3

# Define arguments
parser = argparse.ArgumentParser(description="Generate HTML page from weather data")
parser.add_argument("--folder", type=str, default="weather_data", help="The source folder to read the data from")
parser.add_argument("--output", type=str, default="weather.html", help="The output file name for the HTML page")
parser.add_argument("--bucket", type=str, default="your-bucket-name", help="The name of the AWS S3 bucket")
args = parser.parse_args()

# Define constants
TEMPLATE = """
<html>
<head>
    <title>Weather Data</title>
</head>
<body>
    <h1>Weather Data</h1>
    <table border="1">
        <tr>
            <th>City</th>
            <th>Country</th>
            <th>Temperature (C)</th>
            <th>Weather Description</th>
        </tr>
        <tr>
            <td>{{ data.city }}</td>
            <td>{{ data.country }}</td>
            <td>{{ data.temperature }}</td>
            <td>{{ data.weather_description }}</td>
        </tr>
    </table>
</body>
</html>
"""

def retrieve_weather_data():
    # OpenWeatherMap API endpoint and API key
    api_endpoint = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "a94674834395ff8b8aa7cddee69ef429"  # Replace API KEY with your actual API key

    # Parameters for the API request (coordinates of Prague)
    params = {
        "q": "Prague,CZ",  # City name and country code
        "appid": api_key,  # API key
        "units": "metric"  # Units for temperature (metric for Celsius)
    }

    # Send GET request to OpenWeatherMap API
    response = requests.get(api_endpoint, params=params)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        return data
    else:
        # Handle the error
        print("Failed to retrieve weather data. Status code:", response.status_code)
        return None

# Retrieve weather data
weather_data = retrieve_weather_data()

if weather_data:
    # Render the template with the data
    template = Template(TEMPLATE)
    html = template.render(data=weather_data)

    # Write HTML to a file
    with open(args.output, "w") as f:
        f.write(html)

    # Initialize the AWS S3 client
    s3 = boto3.client('s3')

    # Upload the HTML file to the specified S3 bucket
    with open(args.output, "rb") as f:
        s3.upload_fileobj(f, args.bucket, args.output)

    print(f"HTML page '{args.output}' uploaded to AWS S3 bucket '{args.bucket}'.")
else:
    print("Weather data retrieval failed. HTML page not generated.")

