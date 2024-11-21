from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from io import StringIO

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

    html_content = driver.page_source
    df = pd.read_html(StringIO(html_content))[0]

    file_path = 'scraped_data.xlsx'
    if not os.path.exists(file_path):
        df.to_excel(file_path, index=False)
    else:
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

    driver.quit()

if __name__ == "__main__":
    scrape_data()
