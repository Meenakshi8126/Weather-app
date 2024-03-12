# Use python:3 as the base image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to /app
COPY requirements.txt /app

# Install the dependencies using pip
RUN pip3 install -r requirements.txt

# Copy the Python scripts to /app
COPY weather_data.py /app
COPY wd.py /app

# Set the environment variables for the arguments
ENV FOLDER weather_data
ENV OUTPUT weather.html

# Run the download_weather.py script as the default command
CMD ["python", "download_weather.py", "--folder", "$FOLDER"]

# Run the generate_weather.py script as an additional command
RUN ["python", "generate_weather.py", "--folder", "$FOLDER", "--output", "$OUTPUT"]
