import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import random
import requests
import re
import string
from Pytest_Framework.testSetup.mobile_setup import mobile_driver
from Pytest_Framework.testSetup.web_setup import web_driver
from Pytest_Framework.testSetup.web_setup import Web_Driver
from Pytest_Framework.pageObjects.functions import *
from Pytest_Framework.pageObjects.locators import *
from Pytest_Framework.testSetup.data_entry import *
from Pytest_Framework.pageObjects.app_functions import *

def test_add_shift():
    driver = web_driver("Shift Board: Add Shift")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    print ("Navigating to self_customer/assets to create a new vehicle asset")
    driver.get("https://client."+server+".fleetpanda.com/self_customer/assets")
    Base.refresh_when_application_error(driver)

    #Creating new Vehicle asset
    asset_name_tankwagon = ''.join(random.choices(string.ascii_letters, k=10))
    unique_id = str(random.randint(1, 99999))
    Self_customer.create_vehicle_asset(driver, "Tank Wagon", asset_name_tankwagon, unique_id)

    #Creating new trailer
    asset_name_trailer = ''.join(random.choices(string.ascii_letters, k=10))
    unique_id = str(random.randint(1, 99999))
    Self_customer.create_vehicle_asset(driver, "Trailer", asset_name_trailer, unique_id)

    print("Navigating to self customer to create a new driver")
    driver.get("https://client."+server+".fleetpanda.com/self_customer/drivers")
    Base.refresh_when_application_error(driver)
    #Creating new Driver
    driver_name = ''.join(random.choices(string.ascii_letters, k=10))
    erp_id = str(random.randint(1, 99999))
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    email = random_part + "@example.com"
    driver_number = ''.join(random.choice(string.digits[2:]) for _ in range(10))

    Self_customer.create_driver(driver, driver_name, erp_id, email, driver_number)

    print("Navigating to Shift Board")
    driver.get("https://"+server+".fleetpanda.com/main/shifts/board")

    #Adding Shift on Shift Board page
    Orders.add_shift_on_shift_board(driver, driver_name, asset_name_tankwagon, asset_name_trailer)
    time.sleep(5)

    #Verify Completed status
    print("Searching for the Shift to verify")
    driver.find_element(*search_box_shift_board).send_keys(asset_name_tankwagon)
    WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='"+asset_name_tankwagon+"']"))).click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='order-status-selector']//div[text()='completed']")))
    print("Status is completed for the created shift as expected")
    #Close Shift modal
    time.sleep(3)
    driver.find_element(By.XPATH, "//button[normalize-space()='×']").click()

    #Adding shift with same data
    print("Attempting to Add Shift with the same driver and assets")
    Orders.add_shift_on_shift_board(driver, driver_name, asset_name_tankwagon, asset_name_trailer)

    print("Verifying error toast message")
    WebDriverWait(driver,12).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='toast toast-error']"))
    )
    print("Error Toast message appeared as expected")
    time.sleep(3)

    driver.quit()


def test_accounting_sync():
    driver = Web_Driver("Shift Board: accounting sync 1/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    # Turning On export Feature flags
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(settings_btn)).click()

    feature_flags = driver.find_elements(By.XPATH, "//input[contains(@id, 'export_feature')][@type ='checkbox']")#contains all the export feature flags
    for feature_flag in feature_flags:
        if not feature_flag.is_selected():
            feature_flag.click()
            print("Feature flag " + feature_flag.get_attribute("id") + " turned ON")
        else:
            print("Feature flag " + feature_flag.get_attribute("id") + " is already ON")
    #turning on accounting sync feature
    accounting_sync_feature = driver.find_element(By.ID, "accounting_sync_feature")
    if not accounting_sync_feature.is_selected():
        accounting_sync_feature.click()
        print("Feature flag " + accounting_sync_feature.get_attribute("id") + " turned ON")
    else:
        print("Feature flag " + accounting_sync_feature.get_attribute("id") + " is already ON")


    driver.find_element(By.NAME, "commit").click()
    time.sleep(5)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Dashboard')]")))
    # Returning to main page Dashboard
    driver.find_element(By.XPATH, "//div[contains(text(),'Dashboard')]").click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(dashboard)
    )
    print("Returned to Dashboard")


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

    # ____________________Creating a Load order_________________________
    '''terminal = "AutomationTerminal"
    product = "Regular Def"
    gallons = str(random.randint(1, 99999))
    supplier = "Suppliers_Automation - supp123"
    bol_supplier = "Suppliers_Automation"  # dependencies on above supplier variable

    # create_loading_order
    Orders.create_load_order(driver, terminal, product, gallons, supplier, driver_name)'''

    # __________________Creating Delivery Order___________________________
    # Create a Delivery Order
    gallons = str(random.randint(1, 99999)) #remove this if load order is created
    customer_search = "AutomationCustomer"
    customer = "AutomationCustomer - New12345"
    shipto = "HamroShipTo - NewCustomer123 - Kathmandu, Nepal"
    asset = "NewHamroAssetAutomation(HA_01876)"
    gal = gallons
    Orders.create_delivery_order(driver, customer_search, customer, shipto, asset, gal, driver_name)

    driver.quit()
    print("OPENING DRIVER'S APP")

    # _____________________Phone_execution_________________________________________
    # Execute_load_and_delivery_orders_when_wifi_off():
    appium_driver = mobile_driver("Shift Board: accounting sync 2/3")
    appium_driver.implicitly_wait(15)

    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)

    #shift start
    App_base.shift_start(appium_driver)
    #vehicle select
    App_base.vehicle_select(appium_driver, asset_name)

    # _________________Executing load order________________________________
    '''# start load order
    App_orders.start_load_order(appium_driver, terminal)
    # BOL form fillup
    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Def", gallons)
    App_orders.complete_load_order(appium_driver)'''

    # ______________________Executing Delivery Order_______________________
    # start delivery order
    App_orders.start_delivery_order(appium_driver, "HamroShipTo")

    # select_asset_and_volume
    print("Selecting asset and inserting gallons value for delivery")
    asset = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text='#NewHamroAssetAutomation ']"))
    )
    print("Asset NewHamroAsssetAutomation Regular DEF  selected")
    asset.click()  # selecting the asset/product(def)
    # putting values in compartment
    gallon_box = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='compartment-0']")))
    # gallon_box.click()
    gallon_box.send_keys(gallons)
    print("Delivered gallon value entered for NewHamroAssetAutomation")
    time.sleep(3)
    appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit-button']").click()
    print("submit button pressed")
    mark_customer_as_complete = WebDriverWait(appium_driver, 15).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='mark-customer-complete']"))
    )  # Mark customer as complete button
    mark_customer_as_complete.click()
    print("Mark customer as complete button pressed")

    # test_certify_and_submit
    post_ordernote = WebDriverWait(appium_driver, 15).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='note']"))
    )
    post_ordernote.click()
    post_ordernote.send_keys("Driver's post order automation note")
    print("post order note Entered")
    # submit
    appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit']").click()
    WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located(today_shift))
    print("Delivery order executed")

    # ______________________Ending the Shift_________________________
    App_base.shift_end_normal(appium_driver)

    appium_driver.quit()


    #_______________________Web Execution__________________________________
    driver = web_driver("Shift Board: accounting sync 3/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    print("Navigating to Shift Board")
    driver.get("https://" + server + ".fleetpanda.com/main/shifts/board")

    # change completed status to accounting sync
    #opening completed shift card
    print("Searching for the Shift")
    driver.find_element(*search_box_shift_board).send_keys(asset_name)
    WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='"+asset_name+"']"))).click()

    #changing status
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='order-status-selector']//div[text()='completed']"))).click()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[normalize-space()='accounting_sync_ready']"))).click() #change status
    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='order-status-selector']//div[text()='accounting_sync_ready']"))) #status check
    print("Status changed to Accounting sync ready")

    # Close Shift modal
    time.sleep(3)
    driver.find_element(By.XPATH, "//button[normalize-space()='×']").click()

    #Accounting sync button
    WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Accounting Sync']"))).click()
    #checkmark the shift
    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Press Space to toggle row selection (unchecked)']"))).click()

    WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Go to Review']"))).click()
    WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Export to CSV']"))).click()#download csv button


    #Confirm CSV downloaded
    WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='conformation-wrapper']"))).click()
    print("CSV downloaded confirmed on the web UI")

    print("Searching for the Shift to verify if the status is Accounting Synced")
    driver.find_element(*search_box_shift_board).clear()
    driver.find_element(*search_box_shift_board).send_keys(asset_name)
    time.sleep(5)
    WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='" + asset_name + "']"))).click()

    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='order-status-selector']//div[text()='accounting_synced']")))  # status check
    print("Accounting synced")


    #Verify csv is downloaded by inspecting api response status code
    shift_header = driver.find_element(By.XPATH, "//div[@class='panda-modal__header__title']").text

    match = re.search (r'#(\d+)', shift_header)

    shift_number = match.group(1)
    print("Shift number: " + shift_number)


    # Extract cookies from the current session
    cookies = driver.get_cookies()

    # Look for the API key
    api_key_cookie_name = "fp_access_token"
    api_key = None

    for cookie in cookies:
        if cookie["name"] == api_key_cookie_name:
            api_key = cookie["value"]
            break

    # Check if the API key was found
    if api_key:
        print("API Key:", api_key)
    else:
        print("API Key not found in cookies.")

    api_url = "https://uat.fleetpanda.com/shifts/download_accounting_csvs?shift_ids="+shift_number+""
    fp_access_token = api_key

    print(api_url)
    # headers with the CSRF token
    headers = {
        'Authorization': "Bearer " + fp_access_token + "",
    }

    response = requests.get(api_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        print("API request was successful. Status code:" + str(response.status_code))
    else:
        api_data = response.json()
        print(api_data)
        print(response.text)
        assert False, "API requests failed. Status code:" + str(response.status_code)

    driver.quit()













