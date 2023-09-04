from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os, stat
import requests
import time
import logging
import platform


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    prefs = {"download.default_directory": os.environ['DOWNLOAD_PATH']}
    chrome_options.add_experimental_option("prefs", prefs)
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
        logging_message("Start Process:")

        logging_message("  " + os.environ['EMAIL'] + " login")
        driver.find_element("id", "email").send_keys(os.environ['EMAIL'])
        driver.find_element("id", "password").send_keys(os.environ['PASSWORD'])
        driver.find_element("name", "submit").click()
        logging_message("  Login Success")
    except requests.exceptions.RequestException as e:
        logging_message(e)
        print(e)

    try:
        logging_message("  Into Retailer Overview Page")
        WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-close-btn'
                                                                                       '-container"]/button')))
        # close cookie consent
        cookie_alert = driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button')
        driver.execute_script("arguments[0].click();", cookie_alert)

        user_content = driver.find_element(By.XPATH, '//*[@id="newron-header"]/div[2]/div/button')
        driver.execute_script("arguments[0].click();", user_content)

        saved = driver.find_element(By.XPATH, '//*[@id="saved-views"]')
        driver.execute_script("arguments[0].click();", saved)
    except requests.exceptions.RequestException as e:
        logging_message(e)
        print(e)

    time.sleep(15)
    logging_message("  Into Saved Views Page")
    links = []
    names = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find('table', {'class': 'Table saved-views-table'}).tbody.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        link = columns[0].a['href']
        name = columns[0].p.text.strip()
        links.append(link)
        names.append(name)

    for i in range(len(links)):
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[i+1])
        driver.get(links[i])

        try:
            WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="newron-content'
                                                                                           '"]/div[1]/div[1]/div['
                                                                                           '8]/div/div[1]')))
            click_download = driver.find_element(By.XPATH, '//*[@id="newron-content"]/div[1]/div[1]/div['
                                                           '7]/div/header/span[2]/div/span[1]/button')
            driver.execute_script("arguments[0].click();", click_download)

            download = driver.find_element(By.XPATH, '//*[@id="newron-content"]/div[1]/div[1]/div[7]/div/header/span['
                                                     '2]/div[2]/div[1]/div/footer/button[1]')
            driver.execute_script("arguments[0].click();", download)
            
        except requests.exceptions.RequestException as e:
            logging_message(e)
            print(e)

        time.sleep(10)
        download_file_rename(names[i])

    time.sleep(5)
    driver.quit()
    print("Process Done!")


def download_file_rename(name):
    correct_path = get_path_by_os()
    lists = os.listdir(os.environ['DOWNLOAD_PATH'])
    lists.sort(key=lambda fn: os.path.getmtime(os.environ['DOWNLOAD_PATH'] + correct_path + fn))
    latest_file = lists.pop()
    os.chmod(os.environ['DOWNLOAD_PATH'] + correct_path + latest_file, stat.S_IRWXU)
    os.rename(os.environ['DOWNLOAD_PATH'] + correct_path + latest_file,
              os.environ['DOWNLOAD_PATH'] + correct_path + name + "_" + time.strftime('%Y%m%d_%H_%M_%S') + '.xlsx')
    logging_message("  Download " + os.environ['DOWNLOAD_PATH'] + correct_path
                    + name + "_" + time.strftime('%Y%m%d_%H_%M_%S') + '.xlsx')


def get_path_by_os():
    os_name = platform.system()
    if os_name == 'Windows':
        return '\\'
    else:
        return '/'


def logging_message(message):
    print(message)
    logging.basicConfig(level=logging.INFO, filename='accesslog ' + time.strftime('%Y%m%d_%H_%M_%S') + '.log',
                        filemode='a',format='%(asctime)s %(levelname)s: %(message)s')
    logging.info(message)


if __name__ == '__main__':
    main()
