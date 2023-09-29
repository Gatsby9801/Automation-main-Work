import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pytest_Framework.testSetup.mobile_setup import mobile_driver
from Pytest_Framework.pageObjects.app_locators import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from appium import webdriver
import time
import random
import string
from Pytest_Framework.testSetup.data_entry import *
from Pytest_Framework.testSetup.web_setup import web_driver
from Pytest_Framework.pageObjects.app_functions import *
from Pytest_Framework.pageObjects.functions import *


def test_record_transfer_order():
    driver = web_driver("Transfer Order: record fuel transfer")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    #_________________Recording_Fuel_Transfer_______________________
    from_driver = motorist
    from_asset = "automation tank"
    from_fueltype = "regular diesel"
    from_comp = "compartment-1"
    to_driver = motorist
    to_asset = "automation truck"
    to_comp = "compartment-1"
    gallons = "34.89"

    Orders.record_transfer_order(driver, from_driver, from_asset, from_fueltype, from_comp, to_driver, to_asset, to_comp, gallons)

    driver.quit()


def test_schedule_transfer_order():
    driver = web_driver("Transfer Order: schedule transfer order 1/2")
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

    #_________________Schedule Transfer Order______________________

    from_asset = asset_name
    to_asset = "automation tank"
    from_fueltype = "regular diesel"
    from_comp = "compartment-1"
    to_comp =  "compartment-1"
    gallons = "567.89"
    driver_name = driver_name

    Orders.schedule_transfer_order(driver, from_asset, to_asset, from_fueltype, from_comp, to_comp, gallons, driver_name)

    # Create a Delivery Order to skip
    customer_search = "AutomationCustomer"
    customer = "AutomationCustomer - New12345"
    shipto = "HamroShipTo - NewCustomer123 - Kathmandu, Nepal"
    asset = "NewHamroAssetAutomation(HA_01876)"
    gal = gallons
    Orders.create_delivery_order(driver, customer_search, customer, shipto, asset, gal, driver_name)

    '''
    # _________________Schedule 2nd Transfer Order______________________

    from_asset = asset_name
    to_asset = "automation tank"
    from_fueltype = "regular diesel"
    from_comp = "compartment-1"
    to_comp = "compartment-1"
    gallons = "567.89"
    driver_name = driver_name

    Orders.schedule_transfer_order(driver, from_asset, to_asset, from_fueltype, from_comp, to_comp, gallons,
                                   driver_name)
    '''
    driver.quit()

    print("OPENING PHONE APP TO EXECUTE TRANSFER ORDER")

    # __________________Phone Execution__________________________________
    appium_driver = mobile_driver("Transfer Order: schedule transfer order 2/2")
    appium_driver.implicitly_wait(15)
    # login
    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)
    #shift start
    App_base.shift_start(appium_driver)
    #Vehicle_select
    App_base.vehicle_select(appium_driver, asset_name)

    #Execute Transfer order
    WebDriverWait(appium_driver,12).until(
        EC.element_to_be_clickable((MobileBy.XPATH, "//android.widget.TextView[@text='Transfer Order']"))).click()

    #verify asset name, gallon value and note is correct
    WebDriverWait(appium_driver, 12).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text= '"+asset_name+"']")))
    print("Correct Asset is pre selected")
    WebDriverWait(appium_driver, 12).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.EditText[@text='"+gallons+"']")))
    print("gallon value is correct")
    WebDriverWait(appium_driver, 5).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.EditText[@text='Automated transfer order note']")))
    print("Note is correctly displayed")

    #submit
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='submit']").click()

    WebDriverWait(appium_driver, 12).until(
        EC.presence_of_element_located(today_shift))


    # Ending the shift by skipping one order
    print("***********Ending the shift*******************")
    WebDriverWait(appium_driver, 5).until(
        EC.presence_of_element_located(post_shift_activities)
    ).click()

    WebDriverWait(appium_driver, 5).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='success-btn']"))).click()
    appium_driver.find_element(*certify_submitbtn).click()
    print("Entering reason for skipping orders")
    appium_driver.find_element(MobileBy.XPATH, "//android.widget.EditText[@text='Note is Required *']").send_keys("Automated skip note")
    print("Note entered")
    appium_driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='Send back to Dispatch']").click()

    #Verify if shift is completed
    great_text = (MobileBy.XPATH, "//*[@text= 'Great! you do not have any tasks right now to perform']")
    try:
        WebDriverWait(appium_driver, 120).until(EC.presence_of_element_located(great_text))
        print("SHIFT ENDED SUCCESSFULLY")
    except TimeoutException:
        assert False, "Shift was unable to end"

    appium_driver.quit()


















