from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options=Options()
options.add_experimental_option("detach",True)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(),options=Options))  # Optional argument, if not specified will search path.
# print(driver.title)
# search_bar = driver.find_element_by_name("q")
# search_bar.clear()
# search_bar.send_keys("getting started with python")
# search_bar.send_keys(Keys.RETURN)
# print(driver.current_url)
# driver.close()
#//*[@id="c-ph-right-nav"]/ul/li[3]/a
#/html/body/div[10]/div/div/section/section/div[1]/form/button
path=""
#link of one of the courses as test
url = "https://www.coursera.org/lecture/machine-learning/applications-of-machine-learning-IjrpM?authMode=login"
# driver = webdriver.Chrome(path)
driver.get(url)
email="****"
password="****"
# driver.add_cookie("XHEryuQAYnZChHSwoOTUVJO0X-1s0_LCJaSK9TRpyM74_o_Lutl5SwgxCnd7H45H4JGxWfyiuU20uF-YAU_Wnw.DrFYW5lN56dlbjsk7mDQGA.D5qqPJ58Lwvj10BF5080xTtmEi_mVuoehO4QvHAzN5FuH7lMtAYAQAJa-x7OiFpgM90HMKJQENcx85U_6xLO_HcM-SW0MIRzlsvkYj6gUJaYiXvAIGI6slcZDB11K9pUZjA0sALo8EEx2ALKM5xnC5lN8JscyUtRJJIMCcCnH26SJ_JVW7-jB3tnr9uAQvsQ6xb9lQkOjgthLrC_bedOkubKt20CGex_FD7CbP_TwMtZD20yBXfjUj0Z5gluiXCAHxBhsi-_UQb7Z8KsceEO3ZAwIvn-ZtFHPl_7KqMyzBdlYzXSof9tzvMXyDwgfitc_SBjortoB1YSoFfP31HBTz_51eMwQGZmJne3qcKhuwTYLYWo2TRBXVKM9kA-YDML0STPFIDBKLRvcmEhJ1vsK8_UiM4pc2alD9S0sMakcDZrBpoHLykjjx3Xa_fYDEj8")
# driver.find_element_by_id("c-ph-right-nav-button c-ph-log-in isLohpRebrand").click
driver.find_element_by_id("email").send_keys(email)
driver.find_element_by_name("password").send_keys(password)
# driver.find_element_by_id("button").click

# transcript = driver.find_elements(By.CLASS_NAME, 'rc-Transcript')
# for row in transcript:
#     time = row.find_element(By.CLASS_NAME, 'rc-TranscriptTime')
#     text = row.find_element(By.CLASS_NAME, 'rc-TranscriptLine')
#     print(time.text, text.text)

driver.quit()
