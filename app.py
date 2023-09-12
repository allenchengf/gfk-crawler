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
import shutil
from ftplib import FTP
ftp = FTP()


def main():
    correct_path = get_path_by_os()
    current_directory = os.getcwd() + correct_path + "temp"
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')
    prefs = {"download.default_directory": current_directory}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()

    # Send a get request to the url
    driver.get('https://platform.gfk.com/')
    original_window = driver.current_window_handle
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

    loging_ftp()

    for row in rows:
        columns = row.find_all('td')
        link = columns[0].a['href']
        name = columns[0].p.text.strip()
        links.append(link)
        names.append(name)

    logging_message("  Total: " + str(len(links)) + "links")
    logging_message("  Total: " + str(len(names)) + "names")
    logging_message("  Lists: \n" + ', \n'.join(names))

    for i in range(len(links)):
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        # driver.switch_to.new_window('tab')
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
        download_file_rename(names[i], driver, original_window, current_directory)

    close_ftp()
    time.sleep(5)
    remove_temp_file(current_directory, correct_path)
    driver.quit()
    print("Process Done!")


def loging_ftp():
    try:
        ftp.encoding = 'utf-8'
        ftp.connect(os.environ['FTP_SERVER'], 21)
        ftp.login(os.environ['FTP_USER'], os.environ['FTP_PASSWORD'])
        logging_message("  Login FTP")
    except requests.exceptions.RequestException as e:
        logging_message(e)
        print(e)


def close_ftp():
    ftp.close()


def download_file_rename(name, driver, original_window, current_directory):
    correct_path = get_path_by_os()
    lists = os.listdir(current_directory)
    lists.sort(key=lambda fn: os.path.getmtime(current_directory + correct_path + fn))
    latest_file = lists.pop()
    new_file_path = current_directory + correct_path
    new_file_name = name.replace(' ', '_').replace('/', '_').replace('\\', '_').strip() + "_" + time.strftime(
        '%Y%m%d_%H_%M_%S') + '.xlsx'
    original_file = current_directory + correct_path + latest_file
    new_file = new_file_path + new_file_name
    os.chmod(original_file, stat.S_IRWXU)
    os.rename(original_file, new_file)
    logging_message("  Download " + new_file)

    upload_to_ftp(new_file, correct_path)

    # os.remove(new_file)

    driver.close()
    driver.switch_to.window(original_window)


def remove_temp_file(current_directory, correct_path):
    shutil.rmtree(current_directory)
    os.mkdir(current_directory)
    fp = open(current_directory + correct_path + ".gitignore", "w")
    fp.close()


def upload_to_ftp(file_local, correct_path):
    time.sleep(2)
    file_name = file_local.split(correct_path)[-1]
    bufsize = 1024
    fp = open(file_local, 'rb')
    ftp.storbinary('STOR %s' % os.environ['FTP_PATH'] + "/" + file_name, fp, bufsize)
    logging_message("  Upload " + file_name)
    ftp.set_debuglevel(0)
    fp.close()


def get_path_by_os():
    os_name = platform.system()
    if os_name == 'Windows':
        return '\\'
    else:
        return '/'


def logging_message(message):
    print(message)
    logging.basicConfig(level=logging.INFO, filename='accesslog ' + time.strftime('%Y%m%d_%H_%M_%S') + '.log',
                        filemode='a', format='%(asctime)s %(levelname)s: %(message)s')
    logging.info(message)


if __name__ == '__main__':
    main()
