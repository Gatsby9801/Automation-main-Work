import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..testSetup.mobile_setup import mobile_driver
from ..pageObjects.app_locators import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from appium import webdriver
import time
import random
import string
from ..testSetup.data_entry import *
from ..testSetup.web_setup import web_driver
from ..pageObjects.app_functions import *
from ..pageObjects.functions import *

def test_add_asset_on_delivery_screen_and_record_a_file():
    driver = web_driver("Delivery Order: add asset 1/2")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)
    # Creating a driver
    driver.get("https://client."+ server +".fleetpanda.com/self_customer/drivers")

    Self_customer.create_driver(driver, driver_name, erp_id, email, driver_number)

    # Creating new Vehicle asset
    print("Navigating to self_customer/assets to create a new vehicle asset")
    driver.get("https://client." + server + ".fleetpanda.com/self_customer/assets")

    
    Self_customer.create_vehicle_asset(driver, "Tank Wagon", asset_name, unique_id)

    #transfer a order

    driver.get("https://"+ server +".fleetpanda.com/")
    Self_customer.record_a_transfer(driver)
    time.sleep(5)
    driver.quit()

    





