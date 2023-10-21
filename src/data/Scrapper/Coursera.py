import os
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
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from src.utils.azure_utils import AzureStorage

logging.basicConfig(filename='./coursera_scraper.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s [%(levelname)s] %(message)s')

logger = logging.getLogger(__name__)


class CourseraScarper(object):
    BASE_URL = 'https://www.coursera.org/?authMode=login'
    TIME_DELAY = 1.5
    HOME_URL = 'https://www.coursera.org'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'

    def __init__(self,
                 email: str,
                 password: str):
        self.email = email
        self.password = password
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={CourseraScarper.USER_AGENT}")
        self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.get(CourseraScarper.BASE_URL)
        time.sleep(CourseraScarper.TIME_DELAY)
        self.__get_cookies()
        self.have_cookies = True if self.driver.get_cookies() else False
        # self.soup = None
        self.lessons: list = []
        self.transcripts: list = []

    def scrape(self, course_name: str, course_link: str):
        status = self.__authenticate()
        time.sleep(20)
        self.driver.get(course_link)
        time.sleep(10)
        # self.soup = BeautifulSoup(self.driver.page_source,'html.parser')
        hrefs = self.__get_weeks_per_course()
        all_lessons = []
        for week_link in tqdm(hrefs, total=len(hrefs)):
            full_url = CourseraScarper.HOME_URL + week_link
            self.driver.get(full_url)
            time.sleep(10)
            # path = r'D:\temo\intelli-service\data\raw\coursera'
            # file_name = week_link.replace('/', '-') + '.html'
            # save_html(path + file_name, self.driver.page_source)
            lessons_links = self.__get_lesson_links_per_week()
            all_lessons.extend(lessons_links)
        self.lessons = all_lessons
        self.__iterate_and_collect_transcripts()
        df = pd.DataFrame({'link': self.lessons, 'transcript': self.transcripts})
        df.to_csv(fr'D:\\temo\\intelli-service\\data\\raw\\{course_name}.csv', mode='w')
        time.sleep(3)
        # self.driver.quit()

    def __del__(self):
        self.driver.quit()

    def __iterate_and_collect_transcripts(self):
        self.transcripts = []
        for link_lesson in tqdm(self.lessons, total=len(self.lessons)):
            full_link = CourseraScarper.HOME_URL + link_lesson
            self.driver.get(full_link)
            time.sleep(5)
            transcript = self.__get_transcripts()
            self.transcripts.append(transcript)

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
            logger.error(
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
            # self.driver.get('https://www.coursera.org/')
            logger.info('Signed In!')
            if not self.have_cookies:
                save_cookies(self.driver.get_cookies())
            return True
        except Exception as expection:
            logger.error(f'Error during authentication: {str(expection)}')
            return False

    def __get_weeks_per_course(self) -> list[str] | None:
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            weeks = soup.find_all(attrs={'class': 'css-y3t86r'})[0].find_all('a')
            hrefs = []
            for week in weeks:
                hrefs.append(week['href'])
            return hrefs
        except Exception as e:
            logger.exception(e)
            return None

    def __get_lesson_links_per_week(self) -> list[str] | None:
        try:
            links = []
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            for section in soup.find_all(attrs={'data-testid': "named-item-list-list"}):
                for lesson in section.find_all('li'):
                    links.append(lesson.a['href'])
            return links
        except Exception as E:
            logger.exception(E)
            return None

    def __get_transcripts(self):
        corpse = """"""
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            for phrase in soup.find_all(attrs={'class': 'phrases'}):
                for statement in phrase.find_all('span'):
                    corpse += statement.text
            return corpse
        except Exception as E:
            logger.exception('No Transcripts here!')
            return None


def read_cookies():
    coursera_cookies = None
    path_to_read = os.getcwd()
    file_to_read = os.path.join(path_to_read, "coursera_cookies.pkl")
    if os.path.exists(file_to_read):
        with open(os.path.join(path_to_read, "coursera_cookies.pkl"), "rb") as cookies_file:
            coursera_cookies = pickle.load(cookies_file)
    return coursera_cookies


def save_html(file_path, html_content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


def save_cookies(coursera_cookies):
    path_to_save = os.getcwd()
    with open(os.path.join(path_to_save, "coursera_cookies.pkl"), "wb") as cookies_file:
        pickle.dump(coursera_cookies, cookies_file)


def read_html(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            # Write HTML content to the file
            html = file.read()
        return html
    return None


def upload_csv_files(files: list[tuple[str, str]]):
    azure_obj = AzureStorage(account_name='graduationwork3664469496',
                             account_key='Vs7mgSGdtSV9S7c+CU8iRoFW74/QbqhHtsQuSudKKdE5sRsiU0k94vjFwOIlxRS79v0EsBxvQP0z+AStsanD+Q==')
    for file_name, path in tqdm(files, total=len(files)):
        azure_obj.store(container_name='tutors',
                        blob_name=f'Andrew NG/raw/text/Coursera/{file_name}',
                        data_to_store_path=path)


if __name__ == '__main__':
    links_file_path = r'D:\temo\intelli-service\src\data\Scrapper\files\coursera-links.csv'
    df = pd.read_csv(links_file_path)
    email, password = get_inputs()
    scraper = CourseraScarper(email, password)

    for index, entry in tqdm(df.iterrows(),total=len(df)):
        scraper.scrape(course_name=entry['course_name'],
                       course_link=entry['link'])

    BASE_PATH = r'D:\temo\intelli-service\data\raw\coursera'
    files = [(file_name, BASE_PATH + '\\' + file_name) for file_name in os.listdir(BASE_PATH)]
    # print(files)
    upload_csv_files(files)
