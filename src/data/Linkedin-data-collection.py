import threading
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

from enum import Enum


class DataType(Enum):
    Posts = 0
    Videos = 1
    Images = 2
    Comments = 3
    Articles = 4


logging.basicConfig(filename='linkedin_scraper.log',
                    level=logging.INFO,
                    filemode='w')


class LinkedInScraper(object):
    BASE_URL = 'https://www.linkedin.com/'
    SCROLL_PAUSE_TIME = 1.5

    def __init__(self,
                 email: str,
                 password: str,
                 tutor_linkedin_username: str) -> None:
        # super.__init__(LinkedInScraper)

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(LinkedInScraper.BASE_URL)
        self.email = email
        self.password = password
        self.tutor_linkedin_username = tutor_linkedin_username
        self.content = None
        time.sleep(2)

    def scrape_personal_data(self, data_type: DataType) -> None:
        status = self.__authenticate()
        if status:
            url = LinkedInScraper.BASE_URL + 'in/' + '%s/' % self.tutor_linkedin_username
            # self.driver.get(url)
            choices = {
                DataType.Posts: self.__get_all_posts,
                DataType.Comments: self.__get_all_comments
            }
            if data_type in choices:
                choices[data_type](url, data_type)

            time.sleep(20)
            self.driver.close()
        else:
            logging.error('Can not authenticate!')

    def __get_all_posts(self, url, data_type: DataType):
        full_url = url + 'recent-activity/all/'
        self.driver.get(full_url)
        time.sleep(3)
        logging.info('Start Loading Posts')
        try:
            self.__scroll_and_collect()
            logging.info('Completed loading Posts')
            self.__save_html_file(self.content, data_type)
        except Exception as E:
            logging.exception(E)

    def __get_all_comments(self, url, data_type: DataType):
        full_url = url + 'recent-activity/comments/'
        self.driver.get(full_url)
        time.sleep(2.5)
        logging.info('Loading Comments....')
        try:
            self.__scroll_and_collect()
            logging.info('Completed loading comments successfully!')
            self.__save_html_file(self.content, data_type)
        except Exception as E:
            logging.exception(E)

    def __scroll_and_collect(self):

        self.content = self.driver.page_source
        temp = None
        try:
            while True:
                self.driver.execute_script("window.scrollBy(0,600)")
                time.sleep(2.5)
                temp = self.driver.page_source
                if self.content != temp:
                    self.content = temp
                try:
                    self.driver.execute_script("document.getElementById('ember263').click();")
                    time.sleep(2.5)
                    logging.info('See more button is clicked!')
                except:
                    logging.exception('Can not find the see more button')

        except Exception as E:
            print(E)

    def __save_html_file(self, html_content, data_type: DataType):
        current_time = time.time()
        file_path = None
        if data_type == DataType.Posts:
            file_path = f'./data/raw/linkedIn-{self.tutor_linkedin_username}-posts-{current_time}.html'
        elif data_type == DataType.Comments:
            file_path = f'./data/raw/linkedIn-{self.tutor_linkedin_username}-comments-{current_time}.html'

        logging.info('Start Saving the file......')
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write HTML content to the file
            file.write(html_content)
        logging.info('File stored Successfully!')

    def __search_for_person(self):
        try:
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[5]/header/div/div/div/div[1]/input')
                )
            )
            search_bar.send_keys(self.tutor_linkedin_username)
            search_bar.send_keys(Keys.RETURN)
            logging.info(f'Search Done')
        except:
            logging.error(f'Can not search!')

    def __authenticate(self) -> bool:
        # get the email input field
        if self.email is None or self.password is None:
            logging.error(
                'Email and password should be passed for authentication!')
            return False
        try:
            email_input = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="session_key"]'))
            )
            email_input.send_keys(self.email)
            # get the password input field
            pass_input = self.driver.find_element(
                by='xpath',
                value='//*[@id="session_password"]'
            )
            pass_input.send_keys(self.password)

            # get the button to login
            sign_in_button = self.driver.find_element(
                by='xpath',
                value='//*[@id="main-content"]/section[1]/div/div/form/div[2]/button'
            )
            sign_in_button.click()
            logging.info('Signed In!')
            return True
        except Exception as expection:
            logging.error(f'Error during authentication: {str(expection)}')
            return False


def get_inputs() -> tuple:
    import copy
    email_arg, password_arg = None, None
    try:
        argv = sys.argv[1:]
        opts, _ = getopt.getopt(argv, "e:p:", ["email =", "password ="])
        # lets's check out how getopt parse the arguments
        print(opts)
        for option, value in opts:
            print(option, value)
            if option in ['-e', '--email']:
                email_arg = value.strip()

            elif option in ['-p', '--password']:
                password_arg = value.strip()

        logging.info(f'email: {email_arg}')
        logging.info(f'password: {password_arg}')
    except:
        logging.error('pass the arguments like -e <email> -p <password> or --password <fisrt name> and --email <email>')
    return email_arg, password_arg


if __name__ == '__main__':
    email, password = get_inputs()
    print(email, password)
    scraper = LinkedInScraper(email=email,
                              password=password,
                              tutor_linkedin_username='andrewyng')
    scraper.scrape_personal_data(DataType.Comments)
    print()
