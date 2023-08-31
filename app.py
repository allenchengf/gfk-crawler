from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import requests

chrome_options = Options()
# chrome_options.add_argument('--headless=new')
# prefs = {"download.default_directory": "Users/allenchen/project"}
# chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("detach", True)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()

# Send a get request to the url
driver.get('https://platform.gfk.com/')
driver.implicitly_wait(90)

try:
    WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.NAME, 'submit')))
    driver.find_element("id", "email").send_keys(os.environ['EMAIL'])
    driver.find_element("id", "password").send_keys(os.environ['PASSWORD'])
    driver.find_element("name", "submit").click()
except requests.exceptions.RequestException as e:
    print(e)

try:
    WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')))
    # close cookie consent
    cookieAlert = driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
    driver.execute_script("arguments[0].click();", cookieAlert)

    userContent = driver.find_element(By.XPATH, '//*[@id="newron-header"]/div[2]/div/button')
    driver.execute_script("arguments[0].click();", userContent)
    #driver.find_element(By.XPATH, '//*[@id="newron-header"]/div[2]/div/button').click()

    saved = driver.find_element(By.XPATH, '//*[@id="saved-views"]')
    driver.execute_script("arguments[0].click();", saved)
    # driver.find_element(By.XPATH, '//*[@id="saved-views"]').click()
except requests.exceptions.RequestException as e:
    print(e)


time.sleep(15)

links = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
rows = soup.find('table', {'class': 'Table saved-views-table'}).tbody.find_all('tr')
for row in rows:
    columns = row.find_all('td')
    link = columns[0].a['href']
    links.append(link)


for i in range(len(links)):
    print(i)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[i+1])
    driver.get(links[i])

    try:
        WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="newron-content"]/div[1]/div[1]/div[8]/div/div[1]')))
        clickDownload = driver.find_element(By.XPATH, '//*[@id="newron-content"]/div[1]/div[1]/div[7]/div/header/span[2]/div/span[1]/button')
        driver.execute_script("arguments[0].click();", clickDownload)

        download = driver.find_element(By.XPATH, '//*[@id="newron-content"]/div[1]/div[1]/div[7]/div/header/span[2]/div[2]/div[1]/div/footer/button[1]')
        driver.execute_script("arguments[0].click();", download)

    except requests.exceptions.RequestException as e:
        print(e)

    time.sleep(10)

time.sleep(5)
driver.quit()
print("Done")
