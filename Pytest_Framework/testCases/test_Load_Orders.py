import pytest
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..testSetup.mobile_setup import mobile_driver
from ..pageObjects.app_functions import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import string
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from ..testSetup.web_setup import web_driver
from ..pageObjects.functions import *
from ..pageObjects.locators import *
from ..testSetup.data_entry import *


def test_multiple_bol_and_products():
    driver = web_driver("Load Order: Multiple BOL and Products 1/3")
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

    # Creating new Vehicle asset with 2 compartments
    print("Navigating to self_customer/assets to create a new vehicle asset")
    driver.get("https://client." + server + ".fleetpanda.com/self_customer/assets")

    asset_name = random.choice(string.ascii_letters.replace('A', '') + string.ascii_letters) + ''.join(random.choices(string.ascii_letters, k=9))
    unique_id = str(random.randint(1, 99999))
    Self_customer.create_vehicle_asset_with_2_compartments(driver, "Tank Wagon", asset_name, unique_id)
    driver.quit()


    #____________________________Phone Execution______________________________________
    print("STARTING DRIVER'S APP TO EXECUTE LOAD ORDER")
    appium_driver = mobile_driver("Load Order: Multiple BOL and Products 2/3")
    appium_driver.implicitly_wait(15)
    # Login

    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)

    #__________________________________Schedule a Load order______________________________________
    #variables
    regular_def_volume = random.randint(1, 99999)
    regular_diesel_volume = random.randint(1, 99999)
    regular_def2_volume = random.randint(1, 99999)

    print("Scheduling a Load Order")
    appium_driver.find_element(*side_menu).click()
    appium_driver.find_element(*schedule_load_order).click()

    print("Selecting Terminal")
    appium_driver.find_element(MobileBy.XPATH,"//android.widget.TextView[@text='AutomationTerminal - Term_10210']").click()

    print("Selecting a Product")
    appium_driver.find_element(*product_0).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Regular Def']").click()
    print("Product Selected")

    print("Entering Gross value")
    appium_driver.find_element(*gross_0_input_field).send_keys("825")

    print("Selecting a Supplier")
    appium_driver.find_element(*supplier_0).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Suppliers_Automation']").click()
    print("Supplier selected")

    #Add 2nd Product
    print("Adding 2nd product to schedule Loading Order")
    appium_driver.find_element(*add_more_products).click()


    # scrolling
    print("Scrolling for 2nd product")
    actions = ActionChains(appium_driver)
    actions.w3c_actions.pointer_action.move_to_location(374, 778)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(382, 423)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    print("scrolled")


    print("Selecting a 2nd product")
    appium_driver.find_element(*product_1).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Regular Diesel']").click()
    print("Product selected")

    print("Entering Gross Value")
    appium_driver.find_element(*gross_1_input_field).send_keys("925")
    time.sleep(5)


    print("Selecting a Supplier")
    appium_driver.find_element(*supplier_1).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Suppliers_Automation']").click()
    print("Supplier selected")

    #Add 3rd product
    print("Adding 2nd product to schedule Loading Order")
    appium_driver.find_element(*add_more_products).click()

    #scrolling
    print("Scrolling for 3rd Product")
    actions.w3c_actions.pointer_action.move_to_location(382, 780)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(386, 465)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    print("scrolled")


    print("Selecting a 3rd product")
    appium_driver.find_element(*product_2).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Regular Def']").click()
    print("Product selected")

    print("Entering Gross Value")
    appium_driver.find_element(*gross_2_input_field).send_keys("950")

    print("Selecting a Supplier")
    appium_driver.find_element(*supplier_2).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Suppliers_Automation']").click()
    print("Supplier selected")

    #Submit to schedule a load order
    print("Clicking submit button to schedule a Load Order")
    appium_driver.find_element(*submit_schedule_load_order).click()
    print("submit button clicked to schedule Load Order")

    # ___________________Starting_Shift________________________________________
    App_base.shift_start(appium_driver)

    # _______________Vehicle_select___________________________________________
    App_base.vehicle_select(appium_driver, asset_name)

    #_________________________Start Load Order__________________________________________________________
    App_orders.start_load_order(appium_driver, "AutomationTerminal")

    #BOL form fill up and complete the order
    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Def", volume=str(regular_def_volume))

    print("Adding more products")
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='add-more-product']").click()

    print("scrolling to select product and enter volume")
    actions.w3c_actions.pointer_action.move_to_location(388, 1040)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(390, 606)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    print("scrolled")

    print("Selecting 2nd product")
    appium_driver.find_element(MobileBy.XPATH, "(//android.view.ViewGroup[@resource-id='select-product'])[last()]").click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='Regular Diesel']").click()
    print("Regular Diesel selected")

    print("Entering values in Total net and Total gross")
    appium_driver.find_element(MobileBy.XPATH, "(//*[@resource-id='total-net'])[last()]").send_keys(str(regular_diesel_volume))  # Total net
    appium_driver.find_element(MobileBy.XPATH, "(//android.widget.EditText[@resource-id='total-gross'])[last()]").send_keys(str(regular_diesel_volume))  # Total gross

    appium_driver.find_element(MobileBy.XPATH, "(//*[@resource-id='comp-1'])[last()]").send_keys(str(regular_diesel_volume))  # compartment 1st
    try:
        WebDriverWait(appium_driver,5).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='success-btn']"))
        ).click()
        print("Value entered in 2nd compartment for Regular Diesel")
    except TimeoutException:
        print("Value entered in 2nd compartment for Regular Diesel")

    print("Adding more BOL")
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='add-bol']").click()

    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Def", volume=str(regular_def2_volume))

    #Completing Load Order
    App_orders.complete_load_order(appium_driver)

    # ______________________Ending the Shift_________________________
    App_base.shift_end_normal(appium_driver)
    appium_driver.quit()

    #___________________Verifying on the Web___________________________________________
    print("NOW VERIFYING THE LOADING ORDER WITH MULTIPLE PRODUCTS AND BOL ON THE WEB")
    driver = web_driver("Load Order: Multiple BOL and Products 2/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    scroll_bar = driver.find_element(By.XPATH, "//div[@ref='eBodyHorizontalScrollViewport']")
    actions = ActionChains(driver)
    for _ in range(15):
        # Simulate pressing and holding the right arrow key to scroll right
        actions.key_down(Keys.ARROW_RIGHT, scroll_bar).perform()
        # Release the right arrow key
        actions.key_up(Keys.ARROW_RIGHT, scroll_bar).perform()
    print("Scrolled right to search for Load value")

    # Verifying if the recorded load order is visible in the OrderWells
    volume = regular_diesel_volume + regular_def_volume + regular_def2_volume
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(search_box)
    ).send_keys("loading " + str(volume))

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='" + str(volume) + "']"))
        )
        print("Recorded Load Order is visible on the timeline with correct volume")
    except TimeoutException:
        assert False, "The Load Order recorded from the Driver's app is not visible on the OrderWells."

    driver.quit()


def test_record_load_order_when_shift_is_active_and_not_active():
    driver = web_driver("Load Order: record load order when shift is active and not active 1/2")
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
    driver.quit()

    #______________________________Phone_Execution_____________________________________________________

    #variables
    bol_volume_1 = random.randint(1, 99999)
    bol_volume_2 = random.randint(1, 99999)

    appium_driver = mobile_driver("Load Order: record load order when shift is active and not active 2/2")
    appium_driver.implicitly_wait(15)

    # Login
    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)

    print("Recording load order when SHIFT IS ACTIVE")
    # Scheduling Delivery Order to start shift, if the shift is not started

    App_orders.schedule_delivery_order(
        appium_driver, "AutomationCustomer - New12345", "default-HamroShipTo")
    App_base.shift_start(appium_driver)

     # Vehicle select
    App_base.vehicle_select(appium_driver, asset_name)

    #Recording Load Order
    App_orders.record_load_order(
        appium_driver, "Automation Truck", "Automation Trailer", "Automation Trailer", terminal="AutomationTerminal")

    # ___________________BOL_form_fill_up_&_Complete_Recording_Load_Order________________________________
    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Def", volume=str(bol_volume_1))
    App_orders.complete_load_order(appium_driver)

    print("LOAD ORDER SUCCESSFULLY RECORDED FROM THE PHONE WHEN SHIFT IS ACTIVE")
    print("Now, Ending the shift to record load order when shift is NOT ACTIVE")
    App_base.shift_end(appium_driver)


    #_____________________Recording_Load_Order when Shift is NOT Active_____________________________________________
    App_orders.record_load_order(
        appium_driver, "Automation Truck", "Automation Trailer", "Automation Trailer", terminal="AutomationTerminal" )

    #___________________BOL_form_fill_up_&_Complete_Recording_Load_Order________________________________
    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Def", volume = str(bol_volume_2))
    App_orders.complete_load_order(appium_driver)

    appium_driver.quit()

    print("LOAD ORDER SUCCESSFULLY RECORDED, NOW VERIFYING FROM THE WEB")
    #________________Verifying from the web_____________________________________
    driver = web_driver("Record Load Order: Verify 2/2")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # Application error check
    # Base.refresh_until_no_error(driver)

    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    scroll_bar = driver.find_element(By.XPATH, "//div[@ref='eBodyHorizontalScrollViewport']")
    actions = ActionChains(driver)
    for _ in range(15):
        # Simulate pressing and holding the right arrow key to scroll right
        actions.key_down(Keys.ARROW_RIGHT, scroll_bar).perform()
        # Release the right arrow key
        actions.key_up(Keys.ARROW_RIGHT, scroll_bar).perform()
    print("Scrolled right to search for Load value")

    # Verifying if the recorded load order WHEN SHIFT IS ACTIVE is visible on the OrderWells
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(search_box)
    ).send_keys("loading " + str(bol_volume_1))

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='" + str(bol_volume_1) + "']"))
        )
        print("Recorded Load Order when SHIFT IS ACTIVE is displayed on the OrderWells")
    except TimeoutException:
        assert False, "The Load Order recorded from the Driver's app, WHEN SHIFT IS ACTIVE is not displayed on the OrderWells."

    # Verifying if the recorded load order WHEN SHIFT IS NOT ACTIVE is visible on the OrderWells
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(search_box)
    ).clear()
    driver.find_element(*search_box).send_keys("loading " + str(bol_volume_2))

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='" + str(bol_volume_2) + "']"))
        )
        print("Recorded Load Order when SHIFT IS NOT ACTIVE, is displayed on the OrderWells")
    except TimeoutException:
        assert False, "The Load Order recorded from the Driver's app, WHEN SHIFT IS NOT ACTIVE is not displayed on the OrderWells."

    driver.quit()




































