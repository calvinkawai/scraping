from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_elem_by_xpath(driver, xpath, time=10):
    try:
        elem = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return elem
    except Exception as e:
        driver.quit()
        raise e

def wait_for_elems_by_xpath(driver, xpath, time=10):
    try:
        elem = WebDriverWait(driver, time).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return elem
    except Exception as e:
        driver.quit()
        raise e
