FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all files to the working directory
COPY . .

# Install necessary libraries
RUN pip install flask pandas pytz lxml openpyxl selenium webdriver-manager

# Install Chrome and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Start Flask application and run Selenium script
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=8000 & sleep 10 && python scrape.py"]
