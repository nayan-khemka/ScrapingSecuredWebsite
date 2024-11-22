from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=service, options=options)

# URL of the login page and the data page
login_url = 'https://www.saucedemo.com/'
data_url = 'https://www.saucedemo.com/inventory.html'

driver.get(login_url)

username_field = driver.find_element(By.ID, 'user-name')
password_field = driver.find_element(By.ID, 'password')

username_field.send_keys('standard_user')
password_field.send_keys('secret_sauce')

# Submit the login form
login_button = driver.find_element(By.ID, 'login-button')
login_button.click()

time.sleep(3)

# Navigate to the data page
driver.get(data_url)

time.sleep(3)

data = driver.find_element(By.TAG_NAME, 'body').text

# Save the extracted data to a file
with open('scraped_data.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Data has been scraped and saved to scraped_data.json")

driver.quit()
