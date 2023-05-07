# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Install necessary dependencies
# RUN apt-get update && \
#     apt-get install -yq \
#     wget \
#     gnupg \
#     unzip \
#     libglib2.0-0 \
#     libnss3 \
#     libgconf-2-4 \
#     libfontconfig1 \
#     libxrender1 \
#     libxtst6 \
#     libxi6 \
#     libxss1 \
#     xvfb \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
#     apt-get update && \
#     apt-get install -yq google-chrome-stable && \
#     rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run the command to start the scraper
CMD ["python", "project/scraper.py"]

