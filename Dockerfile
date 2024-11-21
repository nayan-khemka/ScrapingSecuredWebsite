FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all files to the working directory
COPY . .

# Install necessary libraries
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    && pip install flask pandas pytz lxml openpyxl selenium webdriver-manager

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Set environment variable for Chrome
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER=/usr/local/bin/chromedriver

# Start Flask application and run Selenium script
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=8000 & sleep 10 && python scrape.py"]
