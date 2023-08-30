from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("detach", True)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)
wait = WebDriverWait(driver, 20)

# Provide the path of chromedriver present on your system.
driver = webdriver.Chrome()
driver.set_window_size(1440, 1024)

# Send a get request to the url
driver.get('https://platform.gfk.com/')

time.sleep(15)

driver.find_element("id", "email").send_keys('Allen.huang@elifemall.com.tw')
driver.find_element("id", "password").send_keys('elifemall.9911')
driver.find_element("name", "submit").click()

time.sleep(20)

driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button').click()

driver.find_element(By.XPATH, '//*[@id="newron-header"]/div[2]/div/button').click()
driver.find_element(By.XPATH, '//*[@id="saved-views"]').click()

time.sleep(30)
print("start view page")
print("-----------------------")
# BeautifulSoup get saved view link
links = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
rows = soup.find('table', {'class': 'Table saved-views-table'}).tbody.find_all('tr')
for row in rows:
    columns = row.find_all('td')
    link = columns[0].a['href']
    links.append(link)

# print(links)

for i in range(len(links)):
    print(i)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[i+1])
    driver.get(links[i])
    time.sleep(30)
    driver.find_element(By.XPATH, '//*[@id="newron-content"]/div[1]/div[1]/div[7]/div/header/span[2]/div/span[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="newron-content"]/div[1]/div[1]/div[7]/div/header/span[2]/div[2]/div[1]/div/footer/button[1]').click()





time.sleep(20)
driver.quit()
print("Done")
