from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os

def scrape_data():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://localhost:8000/")

    driver.find_element(By.NAME, 'username').send_keys('user')
    driver.find_element(By.NAME, 'password').send_keys('password')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    # Extract city times from the webpage
    new_york_time = driver.find_element(By.ID, 'new_york').text.split(": ")[1]
    london_time = driver.find_element(By.ID, 'london').text.split(": ")[1]
    tokyo_time = driver.find_element(By.ID, 'tokyo').text.split(": ")[1]

    cities = {
        "New York": new_york_time,
        "London": london_time,
        "Tokyo": tokyo_time
    }

    # Convert city time data into a DataFrame
    city_time_df = pd.DataFrame(list(cities.items()), columns=["City", "Current Time"])

    file_path = 'scraped_data.xlsx'
    if not os.path.exists(file_path):
        city_time_df.to_excel(file_path, index=False)
    else:
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay') as writer:
            city_time_df.to_excel(writer, sheet_name='Sheet1', index=False)

    driver.quit()

if __name__ == "__main__":
    scrape_data()
    
