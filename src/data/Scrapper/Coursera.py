import pickle
from abc import ABC
# from Scrapper import Scrapper
# from src.data.Storage.Tutor import Tutor
import time
import logging
import getopt
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from Linkedin import get_inputs
import sys

logging.basicConfig(filename='coursera_scraper.log',
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s [%(levelname)s] %(message)s')


class CourseraScarper(object):
    BASE_URL = 'https://www.coursera.org/?authMode=login'
    TIME_DELAY = 1.5

    def __init__(self,
                 email: str,
                 password: str):
        self.email = email
        self.password = password
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(CourseraScarper.BASE_URL)
        time.sleep(CourseraScarper.TIME_DELAY)
        self.__get_cookies()
        self.have_cookies = True if self.driver.get_cookies() else False

    def scrape(self):
        status = self.__authenticate()
        time.sleep(20)
        self.driver.get('https://www.coursera.org/learn/machine-learning/home/week/1')
        self.driver.quit()

    def __get_cookies(self):
        cookies_binary = read_cookies()
        if cookies_binary:
            for cookie in cookies_binary:
                self.driver.add_cookie(cookie)

    def __authenticate(self) -> bool:
        # get the input field for email
        ## /html/body/div[7]/div/div/section/section/div[1]/form/div[1]/div/input
        # get the email input field
        if self.email is None or self.password is None:
            logging.error(
                'Email and password should be passed for authentication!')
            return False
        try:
            email_input = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (By.ID, 'email'))
            )
            email_input.send_keys(self.email)
            # get the password input field
            pass_input = self.driver.find_element(
                by='id',
                value='password'
            )
            pass_input.send_keys(self.password)
            pass_input.submit()
            logging.info('Signed In!')
            if not self.have_cookies:
                save_cookies(self.driver.get_cookies())
            return True
        except Exception as expection:
            logging.error(f'Error during authentication: {str(expection)}')
            return False


def read_cookies():
    coursera_cookies = None
    try:
        with open("coursera_cookies.pkl", "rb") as cookies_file:
            coursera_cookies = pickle.load(cookies_file)
    except FileNotFoundError as E:
        logging.exception(E)
    return coursera_cookies


def save_cookies(coursera_cookies):
    with open("coursera_cookies.pkl", "wb") as cookies_file:
        pickle.dump(coursera_cookies, cookies_file)


if __name__ == '__main__':
    # tutor = Tutor(name='dummy')
    email, password = get_inputs()
    scraper = CourseraScarper(email=email,
                              password=password)
    scraper.scrape()
