import pytest
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from ..testSetup.mobile_setup import mobile_driver
from ..pageObjects.app_locators import *
from ..pageObjects.app_functions import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import string
import random
from selenium.webdriver.common.action_chains import ActionChains
from ..testSetup.web_setup import Web_Driver
from ..pageObjects.locators import *
from ..testSetup.data_entry import *
from ..pageObjects.functions import *


def test_load_and_delivery_orders():
    driver = Web_Driver("Offline Support Feature: load and delivery orders 1/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    #switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)
    # Turning ON offline mode from Feature flag
    Base.Feature_flag_check(driver, "offline_support_feature")

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
    terminal = "AutomationTerminal"
    product = "Regular Def"
    gallons = str(random.randint(1, 99999))
    supplier = "Suppliers_Automation - supp123"
    bol_supplier = "Suppliers_Automation"  # dependencies on above supplier variable

    # create_loading_order
    Orders.create_load_order(driver, terminal, product, gallons, supplier, driver_name)

#__________________Creating Delivery Order___________________________
    # Create a Delivery Order
    customer_search = "AutomationCustomer"
    customer = "AutomationCustomer - New12345"
    shipto = "HamroShipTo - NewCustomer123 - Kathmandu, Nepal"
    asset = "NewHamroAssetAutomation(HA_01876)"
    gal = gallons
    Orders.create_delivery_order(driver, customer_search, customer, shipto, asset, gal, driver_name)

    driver.quit()
    print("LOADING AND DELIVERY ORDER CREATED FROM THE WEB, NOW EXECUTING FROM DRIVER'S APP OFFLINE")

#_____________________Phone_execution_________________________________________
#Execute_load_and_delivery_orders_when_wifi_off():
    appium_driver = mobile_driver("Offline Support Feature: load and delivery orders 2/3")
    appium_driver.implicitly_wait(15)

    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)

    print("refreshing the app")
    actions = ActionChains(appium_driver)
    actions.w3c_actions.pointer_action.move_to_location(342, 332)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(349, 793)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    #appium_driver.launch_app()
    WebDriverWait(appium_driver,30).until(
        EC.presence_of_element_located(pre_shift_activities)
    )
    time.sleep(6)
    #wifi off
    appium_driver.set_network_connection(0)
    print("WiFi turned OFF")

    #shift start
    print("starting shift")
    WebDriverWait(appium_driver, 30).until(
        EC.element_to_be_clickable(pre_shift_activities))  # Pre-Shift Activities
    appium_driver.implicitly_wait(8)
    while True:
        try:
            appium_driver.find_element(*pre_shift_activities).click()
            print("Pre-Shift Activities clicked")
            time.sleep(5)  # Wait for 5 seconds before attempting again
        except NoSuchElementException:
            break

    appium_driver.implicitly_wait(15)
    WebDriverWait(appium_driver, 7).until(
        EC.presence_of_element_located(start_shiftbtn)).click()  # Starting the shift
    WebDriverWait(appium_driver, 20).until(
        EC.presence_of_element_located(vehicle_search))
    print("shift started")

    #select vehicle
    App_base.vehicle_select(appium_driver, asset_name)

    # _________________Executing load order________________________________
    #start load order
    App_orders.start_load_order(appium_driver, "AutomationTerminal")
    #BOL form fillup
    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Def", gallons)
    App_orders.complete_load_order(appium_driver)


 #______________________Starting and Executing Delivery Order_______________________
    #start delivery order
    App_orders.start_delivery_order(appium_driver, "HamroShipTo")
    App_orders.execute_delivery_order(appium_driver, "NewHamroAssetAutomation", gallons)

    # ______________________Ending the Shift_________________________
    App_base.shift_end_normal(appium_driver)


    # _____________________WIFI ON____________________________

    # subprocess.run(['adb', 'shell', 'svc', 'wifi', 'enable']) #for local android studio emulator
    appium_driver.set_network_connection(6)  # for saucelab Android GoogleAPI Emulator
    print("WiFI turned ON")
    print("Waiting to sync")
    time.sleep(15)
    # Verify if shift is completed
    great_text = (MobileBy.XPATH, "//*[@text= 'Great! you do not have any tasks right now to perform']")
    try:
        WebDriverWait(appium_driver, 120).until(EC.presence_of_element_located(great_text))
        print("Shift synced successfully")
    except TimeoutException:
        assert False, "Failed to sync after turning on the WiFi"

    appium_driver.quit()

    #____________________________Web_verify________________________________________________________
    print("LOADING AND DELIVERY ORDERS SUCCESSFULLY COMPLETED WITH WIFI OFF, NOW VERIFYING FROM THE WEB")
    driver = Web_Driver("Offline Support Feature: load and delivery orders 3/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    #switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)
    
    #verify_offline_load_order_execution
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(search_box)
    )
    element = driver.find_element(By.XPATH, "//div[@ref='eBodyHorizontalScrollViewport']")
    actions = ActionChains(driver)
    for _ in range(15):
        # Simulate pressing and holding the right arrow key to scroll right
        actions.key_down(Keys.ARROW_RIGHT, element).perform()
        # Release the right arrow key
        actions.key_up(Keys.ARROW_RIGHT, element).perform()
    print("scrolled right to search for Load and Delivered value")
    driver.find_element(*search_box).click()
    driver.find_element(*search_box).send_keys("loading unverified " + driver_name)
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='"+gallons+"']"))
        )
    except TimeoutException:
        assert False, "The Load order executed offline from the Driver's app is not visible on the OrderWells."


    #Verify_offline_delivery_order_execution
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(search_box))
    driver.find_element(*search_box).clear()
    driver.find_element(*search_box).send_keys("delivery unverified " + driver_name)
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='"+gallons+"']")))

    except TimeoutException:
        assert False, "The Delivery order executed offline from the Driver's app is not visible on the OrderWells."
        
    driver.quit()


