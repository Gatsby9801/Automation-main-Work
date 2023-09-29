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



def test_add_asset_on_delivery_screen():
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

    print("OPENING DRIVER'S APP")
    #_____________________________Phone Execution____________________________________
    appium_driver = mobile_driver("Delivery Order: add asset 2/2")
    appium_driver.implicitly_wait(15)
    #login
    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)

    # _____________Scheduling_delivery_Order____________________________
    App_orders.schedule_delivery_order(appium_driver, "AutomationCustomer - New12345", "default-HamroShipTo")

    # ___________________Starting_Shift________________________________________
    App_base.shift_start(appium_driver)

    # ______________________Vehicle_select_____________________________________________
    try:
        App_base.vehicle_select(appium_driver,asset_name)
    except TimeoutException:
        print("Vehicle already selected")

    # _____________________Executing_Delivery_Order________________________________________
    #start delivery order
    App_orders.start_delivery_order(appium_driver, "HamroShipTo")

    #ADDING A NEW ASSET
    print("************Adding new asset**************")
    WebDriverWait(appium_driver,30).until(
        EC.presence_of_element_located(add_new_asset_btn)).click()

    print("Selecting Asset type")
    WebDriverWait(appium_driver, 10).until(
        EC.presence_of_element_located(select_asset_type)).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id= 'default-vehicle']").click()

    print("Selecting Product type")
    appium_driver.find_element(*select_product_type).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Regular Def']").click()

    print("Entering Asset name")
    random_asset_name = random.choice(string.ascii_letters.replace('A', '') + string.ascii_letters) + ''.join(random.choices(string.ascii_letters, k=9))
    appium_driver.find_element(*asset_name_input_field).send_keys(random_asset_name)

    print("Entering Licenseplate number")
    random_licenseplate = random.randint(1,99999)
    appium_driver.find_element(*licenseplate_no_input_field).send_keys(random_licenseplate)

    print("Clicking submit button to Create an Asset")
    appium_driver.find_element(*add_asset_submit_btn).click()
    print("ASSET CREATED")

    #verifying if the asset is added
    print("verifying if the Created asset is shown on the list")
    WebDriverWait(appium_driver,15).until(
        EC.presence_of_element_located(search_asset_input_field)
    ).send_keys(random_asset_name)

    random_asset_name += " "
    WebDriverWait(appium_driver,10).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text='#"+ random_asset_name +"']")))
    print("Asset successfully added as it is displayed on the Asset list")

    App_orders.execute_delivery_order(appium_driver, random_asset_name, "55")

    # ______________________Ending the Shift_________________________
    App_base.shift_end_normal(appium_driver)
    appium_driver.quit()


def test_deliver_assets_with_multiple_products():
    driver = web_driver("Delivery Order: Delivery assets with multiple products 1/2")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)
    # navigating to Create New Asset page
    Customer.navigate_to_customer_asset(driver, 'AutomationCustomer')

    # Checking if the assets already exists, if not then create
    driver.implicitly_wait(5)
    try:
        driver.find_element(By.XPATH, "//div[normalize-space()='VehicleWith2products']")
        driver.find_element(By.XPATH, "//div[normalize-space()='VehicleWith1product']")
        print(" Assets named, VehicleWith2products and VehicleWith1products already exists")

    except NoSuchElementException:
        driver.implicitly_wait(30)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(add_asset_btn)).click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Add New Asset']")))
        # creating new asset with 2 products
        print("Creating new asset with 2 products")
        time.sleep(5)
        random_erp_id = random.randint(1, 99999)
        driver.find_element(By.XPATH, "//input[@name='licensePlateNumber']").send_keys(str(random_erp_id))
        driver.find_element(By.XPATH, "//input[@name='name']").send_keys("VehicleWith2products")
        time.sleep(3)
        # adding 1st product
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3] ").send_keys("regular def")
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='Regular Def']").click()
        time.sleep(3)
        # adding 2nd product
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3] ").send_keys("regular diesel")
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='Regular Diesel']").click()
        time.sleep(3)
        # click create button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(add_asset_btn))
        print("Asset named, VehicleWith2products with two products, Regular Def and Regular Diesel created")
        time.sleep(5)

        # Creating another asset with one product
        print("Creating another asset")
        driver.find_element(*add_asset_btn).click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Add New Asset']")))
        print("navigated to Add Asset page again to create an aset with one product")
        time.sleep(5)
        print("Entering unique ERP ID")
        random_erp_id2 = random.randint(1, 99999)
        driver.find_element(By.XPATH, "//input[@name='licensePlateNumber']").send_keys(str(random_erp_id2))
        print("Entering Asset name: VehicleWith1product")
        driver.find_element(By.XPATH, "//input[@name='name']").send_keys("VehicleWith1product")
        time.sleep(3)
        # adding a product
        print("adding a product from a list: Regular Def")
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3] ").send_keys("regular def")
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='Regular Def']").click()
        print("product added from the list")
        time.sleep(3)
        # click create button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(add_asset_btn))
        print("Asset name, VehicleWith1product with a product, Regular Def created")

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
    print("OPENING DRIVER'S APP")
    #_________________________________Phone Execution__________________________________________________
    appium_driver = mobile_driver("Delivery Order: Delivery assets with multiple products 2/2")
    appium_driver.implicitly_wait(15)

    #Login
    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)

    #_____________Scheduling_delivery_Order____________________________
    App_orders.schedule_delivery_order(appium_driver, "AutomationCustomer - New12345", "default-HamroShipTo")

    #___________________Starting_Shift________________________________________
    App_base.shift_start(appium_driver)

    #_______________Vehicle_select___________________________________________
    App_base.vehicle_select(appium_driver, asset_name)

    #___________________Executing_Delivery_Order________________________________________
    #starting delivery order
    App_orders.start_delivery_order(appium_driver, "HamroShipTo")

    #select assets and volume
    print("Selecting asset")
    WebDriverWait(appium_driver,30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text='#VehicleWith2products ']"))
    ).click() #asset clicked
    print("Selecting product from the asset")
    time.sleep(5)
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Regular Def']").click()
    print("product selected")
    gallon_box = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='compartment-0']"))
    )
    gallon_box.click()
    try:
        WebDriverWait(appium_driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='success-btn']"))
        ).click()
    except TimeoutException:

        print("Entering gallon value")
    gallon_box.send_keys("425")
    print("delivered gallon value entered for NewHamroAssetAutomation: 425")
    time.sleep(3)
    appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit-button']").click()
    print("submit button clicked")

    print("Selecting another product from the same asset")
    WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text='#VehicleWith2products ']"))
    ).click()  # asset clicked
    print("Selecting product from the asset")
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Regular Diesel']").click()
    print("product selected")
    gallon_box2 = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='compartment-1']"))
    )
    gallon_box2.click()
    try:
        WebDriverWait(appium_driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH,"//android.view.ViewGroup[@resource-id='success-btn']"))
        ).click() #clicking continue button if the product doesn't match
    except TimeoutException:
        print("Entering gallon value")
    gallon_box2.send_keys("475")
    print("Delivered gallon value entered: 475")
    appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit-button']").click()
    print("submit button clicked")

    #Verify green tick is on Regular DEF here when the ID for it, is available

    WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located(mark_customer_as_complete_btn)
    ).click()  # Mark customer as complete button
    print("Mark customer as complete button pressed")
    post_ordernote = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='note']"))
    )
    post_ordernote.click()
    post_ordernote.send_keys("Driver's post order automation note")
    print("post order note Entered")
    # submit
    appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit']").click()
    WebDriverWait(appium_driver,30).until(
        EC.presence_of_element_located(today_shift))
    print("Delivery Order executed")

    # ______________________Ending the Shift_________________________
    App_base.shift_end_normal(appium_driver)
    appium_driver.quit()






