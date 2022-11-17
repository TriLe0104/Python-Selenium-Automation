from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import pickle
import pwinput

"""
Implement WebDriverWait instead of time.sleep
"""
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get('https://ccintegration.dozuki.com/')

"""
Login with user input ID+Pass 
Link to customer guide page
"""


def login(user_id, user_pw, customer):
    successful_url = 'https://ccintegration.dozuki.com/login'

    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except FileNotFoundError:
        id_box = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[4]/div/div[1]/div[2]/div/div/div[2]/div[1]/form[1]/div[1]/input'
        )
        id_box.send_keys(user_id)

        pass_box = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[4]/div/div[1]/div[2]/div/div/div[2]/div[1]/form[1]/div[2]/input'
        )
        pass_box.send_keys(user_pw)

        login_button = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[4]/div/div[1]/div[2]/div/div/div[2]/div[1]/form[1]/button'
        )
        login_button.click()
        time.sleep(3)

    if driver.current_url != successful_url:
        print("Login Successful")
        driver.get('https://ccintegration.dozuki.com/')
        time.sleep(2)
        select_guide(customer)


"""
Find cell elements and grab the guide links
Save cookies so don't have to login again
"""


def select_guide(customer_name):
    driver.get(customer_name)
    time.sleep(2)
    guide_list = []
    guide_id = []
    links = driver.find_elements(
        By.CLASS_NAME,
        'cell'
    )
    time.sleep(1)
    for link in links:
        guide_list.append(link.find_element(By.TAG_NAME, 'a').get_attribute('href'))

    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    for k, guide in enumerate(guide_list):
        print(str(k+1) + ". Guides ID:" + guide + "Found!")
        guide_id.append(re.search(r"-?\d+", guide[::-1]).group(0)[::-1])

    edit_guide(guide_id)


"""
Opening guides, and loading cookie
"""


def edit_guide(guide_id):
    for k, id in enumerate(guide_id):
        print("")
        print("Opening guide: " + id)
        title = ""
        driver.get('https://ccintegration.dozuki.com/Guide/intro/' + id)

        guide_step = driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[4]/div/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[1]/div[1]/a'
        )
        guide_step.click()

        time.sleep(1)

        while title != "Testing ;')" or title != "Add a title":
            guide_title = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span/a/span'
            )
            next_button = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[4]/div/div[1]/div[4]/div/div[7]/p[3]/a'
            )
            title = guide_title.get_attribute("title")
            print(title)

            """Title Update"""
            if title == "Testing" or title == "":
                print("PAGE FOUND!")
                step_title = driver.find_element(
                    By.CLASS_NAME,
                    'stepTitleValue'
                )
                driver.execute_script("arguments[0].innerText = 'Working yayyyy'", step_title)

                step_line = driver.find_elements(
                    By.CSS_SELECTOR,
                    "[id*='line']"
                )
                """Update Steps"""
                for line in step_line:
                    driver.execute_script("arguments[0].innerText = 'Teehee'", line)

                print("Guide " + id + " Updated, " + str(k+1) + " of " + str(len(guide_id)) + " Completed!")
                break

                """Upload Pic
                upload_pic = driver.FindElement(
                    By.XPATH,
                    '/html/body/div[15]/div[1]/div'
                )
                upload_pic.click()
                time.sleep(3)

                upload_pic.send_keys('https://i.kym-cdn.com/entries/icons/original/000/034/772/Untitled-1.png')
                """

            next_button.click()
            time.sleep(1)
            guide_title = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span/a/span'
            )
            title = guide_title.get_attribute("title")


        time.sleep(10)


def main():
    """
    customer_input = input("Guides to edit: ")

    login(id_input, pw_input, customer_input)
    """
    time.sleep(2)
    id_input = input("ID: ")
    pw_input = pwinput.pwinput()

    login(id_input, pw_input, "https://ccintegration.dozuki.com/c/Varian_%28Testing%29")


if __name__ == "__main__":
    main()
time.sleep(5000)
