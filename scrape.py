from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from datetime import datetime

def scrape_data():
    print("Starting scrape_data function")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://localhost:8000/")

    print("Opened localhost:8000")

    print("Attempting login...")
    driver.find_element(By.NAME, 'username').send_keys('user')
    driver.find_element(By.NAME, 'password').send_keys('password')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    print("Login form submitted")

    # Verify login by checking for the presence of an element
    try:
        new_york_element = driver.find_element(By.ID, 'new_york')
        london_element = driver.find_element(By.ID, 'london')
        tokyo_element = driver.find_element(By.ID, 'tokyo')
        print("Login successful")
    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()
        return

    # Extract city times from the webpage
    print("Extracting city times")
    new_york_time = new_york_element.text.split(": ")[1]
    london_time = london_element.text.split(": ")[1]
    tokyo_time = tokyo_element.text.split(": ")[1]

    cities = {
        "New York": new_york_time,
        "London": london_time,
        "Tokyo": tokyo_time
    }

    print("City times extracted:", cities)

    # Convert city time data into a DataFrame
    city_time_df = pd.DataFrame(list(cities.items()), columns=["City", "Current Time"])
    print(city_time_df)

#     file_path = 'scraped_data.xlsx'  # Ensure the file is in the root directory
#     if not os.path.exists(file_path):
#         print("File does not exist. Creating new file.")
#         city_time_df.to_excel(file_path, index=False)
#     else:
#         print("Appending to existing file.")
#         with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
#             timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
#             city_time_df.to_excel(writer, sheet_name=f'Time_{timestamp}', index=False)
# def save_to_excel(df, file_path):
#     # Assuming the Excel file is in the same directory as the script
    file_path = os.path.join(os.getcwd(), "scraped_data.xlsx")

    if not os.path.exists(file_path):
        city_time_df.to_excel(file_path, index=False)
    else:
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay') as writer:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            city_time_df.to_excel(writer, sheet_name=f'Sheet_{timestamp}', index=False)

    print("Data saved to Excel", file_path)
    driver.quit()

if __name__ == "__main__":
    print("Starting script")
    scrape_data()
