import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pytest_Framework.testSetup.mobile_setup import mobile_driver
from Pytest_Framework.pageObjects.app_functions import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import string
from Pytest_Framework.testSetup.web_setup import web_driver
from Pytest_Framework.pageObjects.functions import *
from Pytest_Framework.pageObjects.locators import *
from Pytest_Framework.testSetup.data_entry import *


def test_blend_feature():
    driver = web_driver("Blend Feature: Create resources and orders 1/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)
    # Turning ON Splash blend feature from Feature flag
    Base.Feature_flag_check(driver, "splash_blend_feature")

    # Checking if BlendTerminal exists, if not create one
    driver.get("https://client." + server + ".fleetpanda.com/self_customer/terminals")
    #Base.refresh_when_application_error(driver)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Display Name']")))
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='BlendTerminal']")))
        print("BlendTerminal already exists")
    except TimeoutException:
        Self_customer.create_terminal(
            driver, "BlendTerminal", "blend_123", "Suppliers_Automation", "carrierName / 009988")

    # Checking if Asset with Blend product exists, if not then create a new one
    Customer.navigate_to_customer_asset(driver, "AutomationCustomer")
    try:
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='BlendAsset']")))
        print("Blend Product already exists")

    except TimeoutException:
        # Creating a Blend product
        driver.get("https://client." + server + ".fleetpanda.com/self_customer/products")
        Self_customer.create_blend_product(driver, "Regular Blend")

        # Navigating to Create New Asset page with blend product
        Customer.navigate_to_customer_asset(driver, 'AutomationCustomer')
        # Creating a customer asset with blend product
        Customer.create_customer_asset(driver, "BlendAsset", "HamroShipTo", "Regular Blend")

    #Creating a driver
    driver.get("https://client."+server+".fleetpanda.com/self_customer/drivers")

    driver_name= ''.join(random.choices(string.ascii_letters, k=10))
    erp_id= str(random.randint(1,99999))
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



    print("****************Creating linked Load and Delivery orders******************")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Create Order')]")))
    CreateOrder = driver.find_element(By.XPATH, "//a[contains(text(),'Create Order')]")
    CreateOrder.click()


    # Selecting a Customer from the list
    driver.find_element(By.ID, "customerSelect").click()
    driver.find_element(By.ID, "customerSelect").send_keys("automation")
    driver.find_element(By.XPATH, "//li[normalize-space()='AutomationCustomer - New12345']").click()

    # selecting Shipto from the list
    select = Select(driver.find_element(By.ID, "branchSelect"))
    select.select_by_visible_text("HamroShipTo - NewCustomer123 - Kathmandu, Nepal")
    # clicking create order button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(delivery_create_order_btn)).click()
    # Searching for asset
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(delivery_asset_search_box)).send_keys("blendasset")

    # putting values to product input box
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'BlendAsset')]/parent::node()/parent::node()//input[@name ='asset_volume']").send_keys("1000")
    # Selecting a driver
    driver.find_element(By.XPATH, "//span[contains(text(),'Select Driver')]").click()
    driver.find_element(By.XPATH, "//*[contains(@class,'select2-search__field')]").send_keys(driver_name)
    driver.find_element(By.XPATH, "//*[contains(@class,'select2-search__field')]").send_keys(Keys.ENTER)
    print("Driver selected: " + driver_name)
    # Delivery instruction
    Delivery_instruction = driver.find_element(By.XPATH, "//*[contains(@name,'delivery_instructions')]")
    Delivery_instruction.clear()
    Delivery_instruction.send_keys("Automated text for the driver")
    print("Delivery instruction Entered")

    #LOAD ORDER
    driver.find_element(By.XPATH, "//div[@class='skip-action']//small").click()#toggle button
    #selecting terminal
    print("Selecting Terminal")
    driver.find_element(By.XPATH, "//div[@class='select-terminal-wrapper']//span[@role='textbox']").click()
    driver.find_element(By.XPATH, "//input[@role='textbox']").send_keys("automation")
    driver.find_element(By.XPATH, "//li[normalize-space()='AutomationTerminal']").click() #terminal selected
    print("Terminal Selected")

    print("Unselecting Regular Diesel to select Regular Def only")
    driver.find_element(By.XPATH, "//input[@data-basicproduct-name='Regular Diesel']").click()
    #loading instruction 1
    driver.find_element(By.XPATH, "//textarea[@name='loading_instruction_1']").send_keys("Loading Instruction 1")
    #add terminal/load order button
    driver.find_element(By.XPATH, "//button[@class='add-terminal-btn']").click()

    print("Selecting 2nd terminal")
    driver.find_element(By.XPATH, "(//div[@class='select-terminal-wrapper']//span[@role='textbox'])[2]").click()
    driver.find_element(By.XPATH, "//input[@role='textbox']").send_keys("automation")
    driver.find_element(By.XPATH, "//li[normalize-space()='AutomationTerminal']").click()  # terminal selected
    print("2nd Terminal Selected")

    print("Unselecting Regular Def to select Regular Diesel only")
    driver.find_element(By.XPATH, "(//input[@data-basicproduct-name='Regular Def'])[2]").click()
    # loading instruction 2
    driver.find_element(By.XPATH, "//textarea[@name='loading_instruction_2']").send_keys("Loading Instruction 2")

    # submit button to create the order
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[contains(text(),'Create Orders')]").click()

    # Verify order created
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Order Wells']")))
    print("DELIVERY ORDER CREATED")
    driver.quit()

    #______________________PHONE EXECUTION_______________________________
    print("NOW BOOTING DRIVER'S APP TO COMPLETE THE BLEND ORDER")
    appium_driver = mobile_driver("Blend Feature: Mobile execution 2/3")
    appium_driver.implicitly_wait(15)
    # login
    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)

    # ___________________Starting_Shift________________________________________
    App_base.shift_start(appium_driver)

    # ______________________Vehicle_select_____________________________________________
    App_base.vehicle_select(appium_driver, asset_name)


    #Starting Load Order #1
    App_orders.start_load_order(appium_driver, "AutomationTerminal")
    #BOL_form_fill_up_&_Complete_Load_Order#1
    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Def  (for Regular Blend)", volume="500")
    App_orders.complete_load_order(appium_driver)

    #Starting Load Order #2
    print("Starting Load order #2")
    appium_driver.find_element(MobileBy.XPATH, "(//android.widget.TextView[@text ='AutomationTerminal'])[2]").click()
    WebDriverWait(appium_driver, 10).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='fill-btn']"))).click()  # start load btn
    done_loading = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='done-load']")))
    done_loading.click()

    # BOL_form_fill_up_&_Complete_Load_Order#2
    App_orders.bol_form_fillup(
        appium_driver, "Suppliers_Automation", "Regular Diesel  (for Regular Blend)", volume="500")
    App_orders.complete_load_order(appium_driver)

    # ______________________ Starting and Executing_Delivery_Order_______________________
    # start delivery order
    App_orders.start_delivery_order(appium_driver, "HamroShipTo")
    App_orders.execute_delivery_order(appium_driver, "BlendAsset", "1000")
    '''# select_asset_and_volume
    print("Selecting asset and inserting gallons value for delivery")
    asset = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text='#BlendAsset ']"))
    )
    print("Asset BlendAsset  selected")
    asset.click()  # selecting the asset
    # putting values in compartment
    gallon_box = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='compartment-0']"))
    )
    gallon_box.click()
    gallon_box.send_keys("1000")
    print(" Delivered gallon value entered for BlendAsset: 1000 ")
    time.sleep(3)
    appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit-button']").click()
    print("submit button pressed")

    mark_customer_as_complete = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='mark-customer-complete']"))
    )  # Mark customer as complete button
    mark_customer_as_complete.click()
    print("Mark customer as complete button pressed")

    # test_certify_and_submit
    post_ordernote = WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='note']"))
    )
    post_ordernote.click()
    post_ordernote.send_keys("Driver's post order automated note")
    print("Post order note entered")
    # submit
    appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit']").click()
    WebDriverWait(appium_driver, 30).until(
        EC.presence_of_element_located(today_shift))
    print("DELIVERY ORDER EXECUTED")'''

    #End Shift
    App_base.shift_end_normal(appium_driver)
    appium_driver.quit()
    print("BLEND ORDERS EXECUTED FROM THE DRIVER'S APP, NOW VERIFYING FROM THE WEB")
#_______________________Verifying from the Web____________________________________
    driver = web_driver("Blend Feature: Verify 3/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    print("Verifying retain value to be 0 on the Shift Board")
    driver.get("https://"+server+".fleetpanda.com/main/shifts/board")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='"+driver_name+"']"))).click()
    #wait until shift opens
    WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='End of Shift Retain']")))

    #verify shift retain value is 0
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "((//tr[@class='summary'])[last()]//td[text()='0'])[2]")))
        print("Shift retain value for Regular Blend product is 0 as expected")
    except TimeoutException:
        assert False, "Shift retain value for Regular product is NOT 0"

    #verify shift status if it is Completed
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='order-status-selector']//div[contains(text(),'completed')]")))
        print("Shift status is Completed")
    except TimeoutException:
        assert False, "Completed Shift status is not Completed"


    driver.quit()



































