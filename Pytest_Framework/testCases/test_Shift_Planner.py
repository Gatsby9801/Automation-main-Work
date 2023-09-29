import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pytest_Framework.testSetup.mobile_setup import mobile_driver
from Pytest_Framework.pageObjects.app_functions import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import string
from selenium.webdriver.common.action_chains import ActionChains
from Pytest_Framework.testSetup.web_setup import web_driver
from Pytest_Framework.pageObjects.functions import *
from Pytest_Framework.pageObjects.locators import *
from Pytest_Framework.testSetup.data_entry import *


def test_shift_planner_functionalities():
    driver = web_driver("Shift Planner: Functionalities 1/3")
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
    print("STARTING DRIVER'S APP")
    #___________________________Phone_Execution_______________________________________
    appium_driver = mobile_driver("Shift Planner: Functionalities 2/3")
    appium_driver.implicitly_wait(15)
    # login
    App_base.phone_login(appium_driver, driver_number, driver_password)
    App_base.ota_update(appium_driver)
    App_base.end_shift_if_active(appium_driver)

    # ___________________Scheduling_Load_Order___________________________
    App_orders.schedule_load_order(
        appium_driver, "AutomationTerminal - Term_10210", "default-Regular Def", "55555",
        "default-Suppliers_Automation")

    # ______________Scheduling_Delivery_Order____________________________
    App_orders.schedule_delivery_order(
        appium_driver, "AutomationCustomer - New12345", "default-HamroShipTo")

    # _____________________Recording_Transfer_Order____________________________
    App_orders.record_transfer_order(
        appium_driver, "default-Tank Automation Tank", "default-Tank Wagon Automation Asset", "default-Regular Def",
        "55555")

    # shift start
    print("Starting shift")
    WebDriverWait(appium_driver, 30).until(
        EC.element_to_be_clickable(pre_shift_activities))  # Pre-Shift Activities
    while True:
        try:
            appium_driver.find_element(*pre_shift_activities).click()
            print("Pre-Shift Activities clicked")
            time.sleep(5)  # Wait for 5 seconds before attempting again
        except NoSuchElementException:
            break
    WebDriverWait(appium_driver, 12).until(
        EC.element_to_be_clickable(start_shiftbtn)).click()

    # vehicle select
    search_vehicle = WebDriverWait(appium_driver, 12).until(
        EC.element_to_be_clickable(vehicle_search)
    )
    print("********Selecting a vehicle to execute the shift*********")
    time.sleep(9)
    search_vehicle.click()

    # Selecting the vehicle(selects the vehicle from the list if not found then attempts to search from the searchbox
    try:
        WebDriverWait(appium_driver, 6).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='" + asset_name + "']"))
        ).click()
    except TimeoutException:
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.EditText[@text='Search']").send_keys(asset_name)
        appium_driver.find_element(MobileBy.XPATH,
                                   "//android.view.ViewGroup[@resource-id='" + asset_name + "']").click()
    # Changing initial inventory
    appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='product-truck-0']").click()
    WebDriverWait(appium_driver, 12).until(
        EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='default-Regular Def']"))).click()
    appium_driver.find_element(MobileBy.XPATH, "//android.widget.EditText[@resource-id='comp-truck-0']").send_keys(
        "55555")
    # looks good button
    WebDriverWait(appium_driver, 10).until(
        EC.element_to_be_clickable(looks_goodbtn)).click()
    print("vehicle selected")

    WebDriverWait(appium_driver, 15).until(
        EC.presence_of_element_located(today_shift))
    appium_driver.quit()

#__________________________Web app execution______________________________________________
    print("NOW BOOTING WEB APP TO VERIFY FROM SHIFT PLANNER")

    driver = web_driver("Shift Planner: Functionalities 3/3")
    driver.implicitly_wait(30)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)

    #Close OrderWells
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='hide-button action-icon']"))).click()

    #Open Shift planner
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(shift_planner)).click()
    #Expanding Shift planner window
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//i[@class='fas fa-expand']"))).click()

    #Searching for driver
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(search_box_shift_planner)).send_keys(driver_name)
    WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((By.XPATH,"//div[text()='"+driver_name+"']"))).click()

    #Verify Driver is active (green dot icon)
    print ("Verifying if the Green dot icon for Active driver is displayed")
    driver.find_element(By.XPATH, "//div[@title='Driver on duty']")
    print("Green dot icon for Active driver is displayed")

    #expand driver detail
    driver.find_element(By.XPATH,"//button[@title='Expand row']").click()

    #Verify Load Order hover details
    print("Verifying Load order mouse hover details")
    terminal_name = driver.find_element(By.XPATH, "//div[@class='shift-planner-task__content']//div[text()='AutomationTerminal']")
    #terminal_detail = driver.find_element(By.XPATH, "//div[@class='shift-planner-popover rs-popover-content']//div[text()='Loading']")

    driver.implicitly_wait(10)
    actions=ActionChains(driver)
    actions.move_to_element(terminal_name).perform()
    driver.find_element(By.XPATH, "//div[@class='shift-planner-popover rs-popover-content']//div[text()='Loading']")
    print("Load order details are displayed")

    #Verify Delivery order hover details
    print("Verifying Delivery order mouse hover details")
    shipto_name = driver.find_element(By.XPATH,"//div[@class='react-contextmenu-wrapper shift-planner__timeline__lane__task shift-planner-task shift-planner-task--type-delivery shift-planner-task--status-scheduled']//div[@class='shift-planner-task__label'][normalize-space()='HamroShipTo']")
    actions.move_to_element(shipto_name).perform()
    driver.find_element(By.XPATH, "//div[@class='shift-planner-popover rs-popover-content']//div[text()='Delivery']")
    print("Delivery order details are displayed")

    #Verify Transfer order hover details
    print("Verifying Transfer order mouse hover details")
    #transfer_order = driver.find_element(By.XPATH, "//div[contains(text(), 'Transfer order')]")
    transfer_order = driver.find_element(By.XPATH, "//div[@class='react-contextmenu-wrapper shift-planner__timeline__lane__task shift-planner-task shift-planner-task--type-transfer shift-planner-task--status-completed']//div[text()= '"+tenant+"']")
    actions.move_to_element(transfer_order).perform()
    driver.find_element(By.XPATH, "//div[@class='shift-planner-popover rs-popover-content']//div[text()='Transfer']")
    print("Transfer order details are displayed")

    #Verify Inventory hover
    print("Verifying  Inventory hover details")
    inventory = driver.find_element(By.XPATH, "//div[@class='inventory-product']")
    actions.move_to_element(inventory).perform()
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='inventory-product__popover']//th[normalize-space()='Compartment']")))
    print("Inventory is displayed")


    #Ending the shift
    print("Ending the shift from Shift Planner")
    driver.find_element(By.XPATH, "//a[@class='driver-actions  false']").click()
    WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='View Shift']"))).click()
    driver.find_element(By.XPATH, "//div[contains(text(),'active')]").click()
    print("Selecting COMPLETED to end the shift")
    WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='completed']"))).click()
    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='order-status-selector']//div[contains(text(),'completed')]")))
    print("Shift successfully Completed")
    driver.quit()