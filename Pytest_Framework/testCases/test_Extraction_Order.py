import pytest
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pytest_Framework.testSetup.mobile_setup import mobile_driver
from Pytest_Framework.pageObjects.app_functions import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import string
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Pytest_Framework.testSetup.web_setup import web_driver
from Pytest_Framework.pageObjects.functions import *
from Pytest_Framework.pageObjects.locators import *
from Pytest_Framework.testSetup.data_entry import *


def test_create_and_execute_extraction_order():
    driver = web_driver("Extraction Order: create_and_execute_extraction_order 1/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)
    #Feature flag on for extraction order
    Base.Feature_flag_check(driver, "extraction_order_feature")

    # Creating a driver
    driver.get("https://client." + server + ".fleetpanda.com/self_customer/drivers")

    driver_name = ''.join(random.choices(string.ascii_letters, k=10))
    erp_id = str(random.randint(1, 99999))
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    email = random_part + "@example.com"
    driver_number = ''.join(random.choice(string.digits[2:]) for _ in range(10))

    Self_customer.create_driver(driver, driver_name, erp_id, email, driver_number)

    # Creating new Vehicle asset
    print("Navigating to self_customer/assets to create a new vehicle asset")
    driver.get("https://client." + server + ".fleetpanda.com/self_customer/assets")

    asset_name = random.choice(string.ascii_letters.replace('A', '') + string.ascii_letters) + ''.join(random.choices(string.ascii_letters, k=9))
    unique_id = str(random.randint(1, 99999))
    Self_customer.create_vehicle_asset(driver, "Tank Wagon", asset_name, unique_id)
    driver.get(base_url)

    # Create Extraction Order
    customer_search = "automation"
    customer = "AutomationCustomer - New12345"
    shipto = "HamroShipTo - NewCustomer123 - Kathmandu, Nepal"
    asset = "NewHamroAssetAutomation(HA_01876)"
    gallons = str(random.randint(1,999))

    Orders.create_extraction_order(driver, customer_search, customer, shipto, asset, gallons, driver_name)

    driver.quit()

    print("OPENING DRIVER'S APP TO EXECUTE EXTRACTION ORDER")


    #______________________Phone Execution_________________________________
    appium_driver = mobile_driver("Extraction Order: create_and_execute_extraction_order 2/3")
    appium_driver.implicitly_wait(15)
    # login
    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)
    # shift start
    App_base.shift_start(appium_driver)
    # Vehicle_select
    App_base.vehicle_select(appium_driver, asset_name)

    # Starting and executing extraction order
    WebDriverWait(appium_driver, 15).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text='E']"))) # E icon verification
    App_orders.start_extraction_order(appium_driver, "HamroShipTo")
    App_orders.execute_extraction_order(appium_driver, "NewHamroAssetAutomation", gallons)

    #Shift End
    App_base.shift_end_normal(appium_driver)
    appium_driver.quit()
    print("VERIFYING ON WEB APP")

    #_____________________Web execution to verify_________________________
    driver = web_driver("Extraction Order: create_and_execute_extraction_order 3/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    print("Searching for the Extraction Order")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(search_box))
    driver.find_element(*search_box).clear()
    driver.find_element(*search_box).send_keys("extraction unverified " + driver_name)
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Extraction']"))).click()
        driver.implicitly_wait(10)
        # Modal header with Extraction Order text
        driver.find_element(By.XPATH, "//header[@class='panda-modal__header dod-modal__header']//div[text()='Extraction Order']")
        #veridy extracted gallon value
        driver.find_element(By.XPATH, "//span[@class= 'edit-reconcilation'][text()='"+gallons+"']")
        driver.find_element(By.XPATH, "//div[normalize-space()='Extracted Gal']") #table header
        print("Extraction order contains correct labels and gallons")

    except TimeoutException:
        assert False, "The Extraction order executed from the Driver's app is not visible on the OrderWells."

    driver.quit()





