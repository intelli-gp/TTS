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
        time.sleep(2)

    def scrape_personal_data(self, data_type: DataType) -> None:
        status = self.__authenticate()
        if status:
            url = LinkedInScraper.BASE_URL + 'in/' + '%s/' % self.tutor_linkedin_username
            self.driver.get(url)
            choices = {
                DataType.Posts: self.__get_all_posts
            }
            if data_type in choices:
                choices[data_type](url)
            # self.__search_for_person()
            time.sleep(20)
            self.driver.close()
        else:
            logging.error('Can Not load posts!')

    def __get_all_posts(self, url):
        url += 'recent-activity/all/'
        self.driver.get(url)
        time.sleep(3)
        posts = None
        logging.info('Start Loading Posts')
        try:
            self.__scroll_and_collect_posts()
        except Exception as E:
            logging.exception(E)

    # Function to wait for the "See More" button to become visible
    def __wait_for_see_more_button(self):
        try:
            btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div/section/div[2]/div/div/div[2]/div/button'))
            btn.click().perform()
            print("See More button is now visible.")
        except Exception as e:
            print("See More button did not become visible within the timeout:", str(e))

    def __scroll_and_collect_posts(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        first_time = True
        scroll_step = 500
        while True:
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            time.sleep(3)
            self.__wait_for_see_more_button()
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            # Collect and save the HTML content of the posts
        self.posts = self.driver.find_element(By.XPATH,
                                              '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div/section/div[2]/div/div/div[1]/ul')
        if self.posts:
            html_content = self.posts.get_attribute('outerHTML')
            self.__save_html_file(html_content)

    # posts container
    ## /html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div/section/div[2]/div/div/div[1]/ul
    # click
    ## /html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div/section/div[2]/div/div/div[2]/div/button
    def __save_html_file(self, html_content):
        current_time = time.time()
        file_path = f'./data/raw/linkedIn-{self.tutor_linkedin_username}-posts-{current_time}.html'
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write HTML content to the file
            file.write(html_content)

    def __search_for_person(self):
        try:
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[5]/header/div/div/div/div[1]/input')
                )
            )
            search_bar.send_keys(self.tutor_name)
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
    scraper.scrape_personal_data(DataType.Posts)
    print()
