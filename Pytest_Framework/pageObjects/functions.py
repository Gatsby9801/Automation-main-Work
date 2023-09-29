from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from ..pageObjects.locators import *
from ..testSetup.data_entry import *

class Config:

    #_______________Goto base URL.______________________
    def goto_website(driver, url):
        # driver = webdriver.Chrome('./chromedriver')
        driver.get(url)
        print("\n Page title: " + driver.title)
        driver.maximize_window()

class Base:
    #_______________________login______________________________
    def test_Login(driver, username, password):

        username_input = driver.find_element(By.NAME, 'user[email]')
        username_input.send_keys(username)

        password_input = driver.find_element(By.ID, 'user_password')
        password_input.send_keys(password)
        time.sleep(2)
        signin_button = driver.find_element(By.NAME, 'commit')
        signin_button.click()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(dashboard)
        )
        print("Successfully logged in")

    #_____________Switch Tenant____________________
    def switch_tenant(driver):
        WebDriverWait(driver,30).until(
            EC.presence_of_element_located(tenant_switch_btn)).click()
        WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='" + slugname + "']"))).click()
        #TODO:capture toaster message to verify
        WebDriverWait(driver,30).until(
           EC.element_to_be_clickable(user_btn)).click()
        WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='" + tenant + "']")))
        print ("Tenant successfully switched to: "+tenant)
        # driver.find_element(*user_btn).click()


    #_________________Refresh when Application Error_____________________
    def refresh_when_application_error(driver):
        try:
            # Check if Application Error is displayed
            WebDriverWait(driver,6).until(
                EC.title_contains("Application Error"))
            print(driver.title)
            driver.back()
            time.sleep(5)
            driver.forward()
        except TimeoutException:
            pass



    #_____________Feature flag check to turn ON_______________________
    def Feature_flag_check(driver, FeatureFlag_checkbox_ID):
        WebDriverWait(driver,30).until(
            EC.element_to_be_clickable(settings_btn)).click()
       # driver.find_element(By.XPATH,"//span[contains(text(),'Features')]").click()
        if driver.find_element(By.ID, FeatureFlag_checkbox_ID).is_selected():
            print("Feature flag " + FeatureFlag_checkbox_ID + " is already ON")
        else:
            driver.find_element(By.ID, FeatureFlag_checkbox_ID).click()
            print("Feature flag "+ FeatureFlag_checkbox_ID + " turned ON")
        driver.find_element(By.NAME, "commit").click()
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Dashboard')]")))
        #Returning to main page Dashboard
        driver.find_element(By.XPATH,"//div[contains(text(),'Dashboard')]").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(dashboard)
        )
        print("Returned to Dashboard")

    #___________Feature flag check to turn OFF_________________________
    def Feature_flag_off(driver, feature_flag_id):
        driver.find_element(By.XPATH, "//*[contains(@class, 'rs-icon rs-icon-cog')]").click()
        #driver.find_element(By.XPATH, "//span[contains(text(),'Features')]").click()
        if driver.find_element(By.ID, feature_flag_id).is_selected():
            driver.find_element(By.ID, feature_flag_id).click()
            print("Feature flag "+ feature_flag_id + " turned OFF")
        else:
            print("Feature flag " + feature_flag_id + " is OFF")
        driver.find_element(By.NAME, "commit").click()
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Dashboard')]")))
        # Returning to main page Dashboard
        driver.find_element(By.XPATH, "//div[contains(text(),'Dashboard')]").click()
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(dashboard))
        print("Returned to Dashboard")


class Api:
    #_________Extract_API access Token______________________________
    def get_api_key(driver):
        # Extract cookies from the current session
        cookies = driver.get_cookies()

        # Look for the API key or access token cookie (replace 'api_key_cookie_name' with the actual cookie name)
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


class Self_customer:

    # ________________________Create_Blend_Product_______________________________________________
    def create_blend_product(driver, display_name):
        print("**************Creating a Blend product****************")
        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable(add_product)).click()
        print("Selecting product category")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "(//div/input[contains(@role,'combobox')])[1]"))
        ).send_keys("ethanol")
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Ethanol']"))).click()

        print("Entering ERP-ID")
        erp_id = str(random.randint(1, 99999))
        driver.find_element(By.NAME, "erpId").send_keys(erp_id)

        print("Entering Display Name")
        driver.find_element(By.NAME, "shortName").send_keys(display_name)

        print("Selecting Unit as Gallons")
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3]").click()
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Gallon']"))).click()

        print("Selecting Product Type as Blend")
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[4]").click()
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Blend']"))).click()

        print("Adding 1st Constituents")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='+ Add Constituents']"))).click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@role='group']//input[@role='combobox'])[5]"))).send_keys(
            "regular def")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[normalize-space()='Regular Def']"))).click()  # selecting product from the list
        driver.find_element(By.NAME, "productConstituentsAttributes.0.percentage").send_keys("40")

        print("Adding 2nd Constituents")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='+ Add Constituents']"))).click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@role='group']//input[@role='combobox'])[6]"))).send_keys(
            "regular diesel")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//div[normalize-space()='Regular Diesel']"))).click()  # selecting product from the list
        driver.find_element(By.NAME, "productConstituentsAttributes.1.percentage").send_keys("60")

        print("Clicking Submit button")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@role='status']//div[text()='Product created successfully']")))
        print("BLEND PRODUCT CREATED")

    # _______________________Create_new_Driver________________________________________________________
    def create_driver(driver, driver_name, erp_id, email, driver_number):
        print("***************Creating a new driver*********************")
        WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='button']//p[text()='Add Driver']"))).click()
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "name"))).send_keys(driver_name)
        driver.find_element(By.NAME, "erpId").send_keys(erp_id)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phoneNumbersAttributes.0.value").send_keys(driver_number)

        #select phone number status from the list
        driver.find_element(By.XPATH, "//p[text()='status']/parent::node()/parent::node()/parent::node()//input[@role='combobox']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[text()='Company']").click()

        #Checkmark primary
        driver.find_element(By.XPATH, "//p[normalize-space()='PRIMARY ?']//parent::span").click()

        #submit button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        # TODO: add toaster verification here
        WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='presentation']")))
        print("DRIVER CREATED")

    # ___________________________Create_new_self customer Vehicle/Asset__________________________________
    def create_vehicle_asset(driver, asset_type, asset_name, unique_id):
        print("Creating new vehicle asset")
        WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(add_asset_btn)).click()

        # Asset name
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "name"))).send_keys(asset_name)
        print("Asset name entered: " + asset_name)

        # Unique ID
        driver.find_element(By.NAME, "licensePlateNumber").send_keys(unique_id)
        print("Unique id entered: " + unique_id)

        # Selecting Asset Type
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[1]").send_keys(asset_type)
        time.sleep(3)
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[1]").send_keys(Keys.ENTER)
        print("Asset Type entered: "+ asset_type)

        # selecting shipto
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[2]").send_keys("" + tenant + " HQ")
        time.sleep(2)
        driver.find_element(By.XPATH, "(//div[text() = 'Tootopia HQ'])").click()
        print('shipto type selected Tootopia HQ')

        # selecting product category
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3]").send_keys("diese")
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='Diesel']").click()
        print('product_category_found')

        # Checkmark: Use for Delivery
        driver.find_element(By.XPATH, "//p[normalize-space()='USE IN DELIVERY']//parent::span").click()
        # compartments
        # driver.find_element(By.NAME, "compartments.0.name").send_keys("C1")

        # submit button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='presentation']")))
        print("VEHICLE ASSET CREATED")

    # ______________Create new self-customer Vehicle/asset with 2 compartments____________________________
    def create_vehicle_asset_with_2_compartments(driver, asset_type, asset_name, unique_id):
        print("Creating new vehicle asset")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(add_asset_btn)).click()
        # Asset name
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "name"))).send_keys(asset_name)
        print("Asset name entered: " + asset_name)

        # Unique ID
        driver.find_element(By.NAME, "licensePlateNumber").send_keys(unique_id)

        # Selecting Asset Type
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[1]").send_keys(asset_type)
        time.sleep(3)
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[1]").send_keys(Keys.ENTER)

        # selecting shipto
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[2]").send_keys("Automation Ship")
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='Automation ShipTO']").click()

        # selecting product category
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3]").send_keys("diese")
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='Diesel']").click()

        # Checkmark: Use for Delivery
        driver.find_element(By.XPATH, "//p[normalize-space()='USE IN DELIVERY']//parent::span").click()

        # Adding compartments
        driver.find_element(By.XPATH, "//p[text()='+ Add Compartment']").click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.NAME, "compartments.0.name"))).send_keys("One")

        driver.find_element(By.XPATH, "//p[text()='+ Add Compartment']").click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.NAME, "compartments.1.name"))).send_keys("One")
        time.sleep(2)

        # submit button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='presentation']")))
        print("VEHICLE ASSET WITH 2 COMPARTMENTS CREATED")

    # ____________________Create Terminal_____________________________
    def create_terminal(driver, name, erpid, supplier, carrier):
        print("*******Creating a new Terminal*******")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button//p[text()='Add Terminal']"))).click()

        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.NAME, "name"))).send_keys(name)
        driver.find_element(By.NAME, "erpId").send_keys(erpid)
        print("Entering Address")
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[1]").send_keys("California")
        time.sleep(4)
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[1]").send_keys(Keys.ENTER)
        print("Address entered")

        driver.find_element(By.NAME, "siteAttributes.radius").send_keys("100")
        print("Radius entered")

        driver.find_element(By.XPATH, "//p[normalize-space()='Card in']").click()
        print("Selecting Suppliers")
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[2]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//div[contains(text(),'" + supplier + "')]").click()

        print("Selecting Carrier/Loading Account")
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3]").click()
        driver.find_element(By.XPATH, "//div[contains(text(),'" + carrier + "')]").click()

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Display Name']")))
        print("Terminal created")

    #______________record fuel transfer________________
    def record_a_transfer(driver):
        driver.implicitly_wait(5)
        #record_transfer_button
        driver.find_element(By.XPATH, "//button[text() = 'Record A Transfe']").click()
        #date_click
        driver.find_element(By.XPATH, "//label[text()='Date of transfer']/parent::node()//input[@type = 'text']").click()
        #select_date
        driver.find_element(By.XPATH, "//div[text() = '14']").click()
        #select_time
        driver.find_element(By.XPATH,"//label[text() = 'Time of transfer']/parent::node()//a[@role='combobox']").click()
        #select_hour
        driver.find_element(By.XPATH, "//span[text() = 'Hours']/parent::node()/parent::node()//a[text() = '18']").click()
        #apply_time
        driver.find_element(By.XPATH, "//button//span[text() = 'OK']").click()
        
        # ___________________From___________________

        #driver 
        driver.find_element(By.XPATH, "((//tbody//tr[1])//div[text()='Select Driver'])[1]/parent::node()").click() 
        driver.find_element(By.XPATH, "//div[text() = '"+ driver_name +"']").click()
        #asset
        driver.find_element(By.XPATH, "((//tbody//tr[1])//label[text() = 'Asset'])[1]//following-sibling::node()").click()
        driver.find_element(By.XPATH, "//div[text() = '"+ asset_name +"']").click()

        #fule type 1
        driver.find_element(By.XPATH, "(//tbody//tr[2]//td[1])//div[text() = 'Select Fuel']/parent::node()").click()
        driver.find_element(By.XPATH, "(//tbody//tr[2]//td[1])//div[text() = 'ERP_RegDeisel']").click()
        # comp 1 
        driver.find_element(By.XPATH, "(//tbody//tr[2]//td[2])/child::node()/child::div/child::div").click()
        driver.find_element(By.XPATH, "(//tbody//tr[2]//td[2])/child::node()/child::div/child::div/following-sibling::node()//div[text() = 'compartment-1']").click()
        #fuel type 2
        driver.find_element(By.XPATH, "(//tbody//tr[3]//td[1])//div[text() = 'Select Fuel']/parent::node()").click()
        driver.find_element(By.XPATH, "(//tbody//tr[3]//td[1])//div[text() = 'ERP_RegDef_123']").click()
        #comp 2
        driver.find_element(By.XPATH, "(//tbody//tr[3]//td[2])/child::node()/child::div/child::div").click()
        driver.find_element(By.XPATH, "(//tbody//tr[3]//td[2])/child::node()/child::div/child::div/following-sibling::node()//div[text() = 'compartment-1']").click()
        

        #___________________To______________________
        #driver
        driver.find_element(By.XPATH, "((//tbody//tr[1])//div[text()='Select Driver'])[1]/parent::node()").click()
        driver.find_element(By.XPATH, "(//div[text() = '"+ driver_name +"'])[2]").click()
        #asset
        driver.find_element(By.XPATH, "((//tbody//tr[1])//label[text() = 'Asset'])[2]//following-sibling::node()").click()
        driver.find_element(By.XPATH, "(//div[text() = '"+asset_name+"'])[2]").click()

        #comp1
        driver.find_element(By.XPATH, "(//tbody//tr[2]//td[4])/child::node()/child::div/child::div").click()
        driver.find_element(By.XPATH, "(//tbody//tr[2]//td[4])/child::node()/child::div/child::div/following-sibling::node()//div[text() = 'compartment-1']").click()

        #Gallons 1
        driver.find_element(By.XPATH, "(//tbody//tr[2]//td[5])//input").send_keys('80')
        #comp2
        driver.find_element(By.XPATH, "(//tbody//tr[3]//td[4])/child::node()/child::div/child::div").click()
        driver.find_element(By.XPATH, "(//tbody//tr[3]//td[4])/child::node()/child::div/child::div/following-sibling::node()//div[text() = 'compartment-1']").click()
        #Gallons 2
        driver.find_element(By.XPATH, "(//tbody//tr[3]//td[5])//input").send_keys('70')

        #_______________________transfer_note______________________
        driver.find_element(By.XPATH,"//textarea[@id = 'NewTransferOrderNotes']").send_keys('I am robot!!! got it?')

        #_______________________Record Fuel Transfer_______________
        driver.find_element(By.XPATH, "//button[text() = 'Record Fuel Transfer']").click()


class Customer:

    # _____________________Navigate_to_Customer_Asset_page__________________________
    def navigate_to_customer_asset(driver, customername):
        driver.get(client_url)
        # Application error check
        Base.refresh_when_application_error(driver)

        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='" + customername + "']"))).click()
        time.sleep(3)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Assets']"))).click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Asset Type']")))
        print("Navigated to Customer Asset page for customer: " + customername)

    # ____________________________Create_Customer_Asset______________________________________________
    def create_customer_asset(driver, asset_name, shipto, product):
        print("******************Creating a new  Customer Asset*******************")
        driver.find_element(*add_asset_btn).click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Add New Asset']")))
        print("Navigated to Add Asset page to create an Asset")
        time.sleep(5)

        # Entering random unique id
        print("Entering Unique ID")
        unique_id = random.randint(1, 99999)
        driver.find_element(By.XPATH, "//input[@name='licensePlateNumber']").send_keys(str(unique_id))

        # Asset name
        print("Entering Asset name")
        driver.find_element(By.XPATH, "//input[@name='name']").send_keys(asset_name)
        time.sleep(2)

        # Selecting Shipto
        print("Selecting Shipto from a list: " + shipto)
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[2] ").send_keys(shipto)
        time.sleep(2)
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[2] ").send_keys(Keys.ENTER)
        print("Blend product selected from the list")
        time.sleep(2)

        # Selecting a product
        print("Selecting a product from a list: "+product)
        driver.find_element(By.XPATH, "(//div/input[contains(@role,'combobox')])[3] ").send_keys(product)
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='" + product + "']").click()
        print(product + " product selected from the list")
        time.sleep(3)

        # click create button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(add_asset_btn))
        print("ASSET NAME, " + asset_name + " WITH A PRODUCT " + product + " CREATED")


class Orders:

    #__________________________Create Load Order____________________________________
    def create_load_order(driver, terminal, product, gallons, supplier, motorist):
        #clicking Create Load Order
        print("**********Creating a Load Order*************")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(create_load_order_btn)).click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Select a Terminal')]")))
        #Selecting a terminal
        print("Selecting a terminal")
        driver.find_element(By.XPATH, "//div[@class='input-group terminal-input']//input[@role='combobox']").click()
        driver.find_element(By.XPATH, "//div[@class='input-group terminal-input']//input[@role='combobox']").send_keys(terminal)
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[@class='input-group terminal-input']//input[@role='combobox']").send_keys(Keys.ENTER)
        #Selecting a product
        print("Selecting a Product")
        driver.find_element(By.XPATH, "(//*[contains(@id, 'NewLoadOrderProduct')]//*[contains(@class, 'ui-select__input')])[2]").send_keys(product)
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[text()='" + product + "']").click()
        #Entering gallon volume
        print("Entering gallon volume")
        driver.find_element(By.XPATH, "//*[contains(@type, 'number')]").send_keys(gallons)
        #Selecting a supplier
        print("Selecting a supplier")
        driver.find_element(By.XPATH, "(//*[contains(@class, 'ui-select__control')])[3]//*[contains(@autocapitalize, 'none')]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//div[text()='" + supplier + "']").click()
        #Writing Loading Instructions
        print("Writing Loading instructions")
        driver.find_element(By.ID, "dark-loading-instruction").send_keys(
            "This is automated text for loading order")
        #clicking Load Order submit button
        print("clicking Load Order Submit button")
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        ).click()
        print("Load Order submit button clicked")

        #Selecting a driver from order Wells
        driver.refresh()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(search_box))
        time.sleep(5)
        driver.find_element(*search_box).click()
        driver.find_element(*search_box).send_keys("loading Unassigned " + gallons)
        time.sleep(5)
        driver.find_element(By.XPATH, "(//span[contains(text(), 'Loading')])[last()]").click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='panda-widget__content description-list-widget__content lod-modal__driver-details__content']//button[@type='button']")))
        driver.find_element(By.XPATH, "//div[@class='panda-widget__content description-list-widget__content lod-modal__driver-details__content']//button[@type='button']").click()
        driver.find_element(By.XPATH,
                            "//input[@role='combobox']").click()
        driver.find_element(By.XPATH,
                            "//input[@role='combobox']").clear()
        driver.find_element(By.XPATH,
                            "//input[@role='combobox']").send_keys(motorist)
        time.sleep(5)
        driver.find_element(By.XPATH,
                            "//input[@role='combobox']").send_keys(Keys.ENTER)
        print("Driver Selected: "+motorist)
        time.sleep(5)
        driver.find_element(By.XPATH,
                            "//button[normalize-space()='×']").click() #closing the loading order modal.
        print("LOAD ORDER CREATED AND DRIVER ASSIGNED")
        time.sleep(5)

    #_______________________________Add_Shift_on_Shift_Board________________________
    def add_shift_on_shift_board(driver, driver_name, asset_name_tankwagon, asset_name_trailer):
        #Adding Shift on Shift Board page
        print("*********Adding Shift from Shift Board Page************")
        WebDriverWait(driver,30).until(
            EC.element_to_be_clickable(add_shift)).click()

        print("Selecting SHIFT START DATE")
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='date'])[1]//input[@class='datepicker-input']"))).click()
        WebDriverWait(driver,8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Previous Month']"))).click()

        print("selecting 12th day of previous month")
        driver.find_element(By.XPATH, "(//div[@class='date'])[1]//div[contains(@class, 'react-datepicker__day react-datepicker__day--012')]").click()
        print("SHIFT START DATE selected")

        print("Selecting SHIFT START TIME")
        driver.find_element(By.XPATH,"(//div[@class='time'])[1]//a[@class='rs-btn rs-btn-default rs-picker-toggle']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//button[@class='rs-picker-toolbar-right-btn-ok']").click()

        print("Selecting SHIFT END DATE")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='date'])[2]//input[@class='datepicker-input']"))).click()
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Previous Month']"))).click()

        print("Selecting 13th day of previous month")
        driver.find_element(By.XPATH,
                            "(//div[@class='date'])[2]//div[contains(@class,  'react-datepicker__day react-datepicker__day--013')]").click()
        print("SHIFT END DATE selected")

        print("Selecting SHIFT END TIME")
        driver.find_element(By.XPATH, "(//div[@class='time'])[2]//a[@class='rs-btn rs-btn-default rs-picker-toggle']").click()
        time.sleep(3)
        #driver.find_element(By.XPATH, "//div[@class='rs-calendar-time-dropdown-row']//*[@data-key='hours-10']").click()
        #print("Hours selected")
        #driver.find_element(By.XPATH, "//div[@class='rs-calendar-time-dropdown-row']//*[@data-key='minutes-25']").click()
        #print("Minutes selected")
        driver.find_element(By.XPATH, "//button[@class='rs-picker-toolbar-right-btn-ok']").click()
        print("Selecting Driver")
        driver.find_element(By.XPATH, "(//input[@role='combobox'])[2]").send_keys(driver_name)
        driver.find_element(By.XPATH, "//div[text()='"+driver_name+"']").click()

        print("Selecting Truck")
        driver.find_element(By.XPATH, "(//input[@role='combobox'])[3]").send_keys(asset_name_tankwagon)
        driver.find_element(By.XPATH, "//div[text()='"+asset_name_tankwagon+"']").click()

        print("Selecting Trailer")
        driver.find_element(By.XPATH, "(//div[@class='add-trailer']//input[@role='combobox'])[1]").send_keys(asset_name_trailer)
        driver.find_element(By.XPATH, "//div[text()='"+asset_name_trailer+"']").click()

        #submit button to create shift
        print("Clicking Create Shift button")
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

    #________________________________Create Delivery Order_________________________________

    def create_delivery_order(driver, customer_search, customer, shipto, asset, gallons, motorist):
        print("****************Creating Delivery order******************")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Create Order')]"))).click()

        print("Page title: "+ driver.title)
        print("Page URL: " + driver.current_url)

        # selecting a Customer from the list
        print("Selecting Customer from the list")
        WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.ID, "customerSelect"))).click()
        driver.find_element(By.ID, "customerSelect").send_keys(customer_search)
        driver.find_element(By.XPATH, "//li[normalize-space()='"+customer+"']").click()

        # selecting Shipto from the list
        print("Selecting Shipto from the list")
        select = Select(driver.find_element(By.ID, "branchSelect"))
        select.select_by_visible_text(shipto)
        # clicking create order button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(delivery_create_order_btn)).click()
        # Searching for asset
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(delivery_asset_search_box)).send_keys(asset)

        # putting values to product input box
        print("Entering gallon value for asset: " + asset)
        driver.find_element(By.XPATH,
                            "//div[contains(text(), '"+asset+"')]/parent::node()/parent::node()//input[@name ='asset_volume']").send_keys(gallons)
        # Selecting a driver
        driver.find_element(By.XPATH, "//span[contains(text(),'Select Driver')]").click()
        driver.find_element(By.XPATH, "//*[contains(@class,'select2-search__field')]").send_keys(motorist)
        driver.find_element(By.XPATH, "//*[contains(@class,'select2-search__field')]").send_keys(Keys.ENTER)
        print("Driver selected: " + motorist)
        # Delivery instruction
        Delivery_instruction = driver.find_element(By.XPATH, "//*[contains(@name,'delivery_instructions')]")
        Delivery_instruction.clear()
        Delivery_instruction.send_keys(
            "Automated text for the driver")
        print("Delivery instruction Entered")
        # submit button to create the order
        driver.find_element(By.XPATH, "//button[contains(text(),'Create Orders')]").click()
        # Verify order created
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH,"//span[normalize-space()='Order Wells']")))
        print("DELIVERY ORDER CREATED")

    #________________________________Record Fuel Transfer________________________________
    def record_transfer_order(driver, from_driver, from_asset, from_fueltype, from_comp, to_driver, to_asset, to_comp, gallons):
        print("**************Recording Fuel Transfer***********************")
        WebDriverWait(driver,30).until(
            EC.element_to_be_clickable(record_transfer_btn)).click()

        print("Selecting date and time")
        #selecting 20th day of previous month
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='nto-modal__datepicker__input']"))).click()
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Previous Month']"))).click()
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='react-datepicker__month-container']//div[text()='20']"))).click()

        #time
        driver.find_element(By.XPATH, "//span[@class='rs-picker-toggle-value']").click()
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='rs-picker-toolbar-right-btn-ok']"))).click()

        # selecting from-driver
        print("Selecting from-driver")
        driver.find_element(By.XPATH, "(//label[text()='Driver']/parent::node()//input[@role='combobox'])[1]").send_keys(from_driver)
        time.sleep(2)
        driver.find_element(By.XPATH, "(//label[text()='Driver']/parent::node()//input[@role='combobox'])[1]").send_keys(Keys.ENTER)

        #selecting from-asset
        print("Selecting from-asset")
        driver.find_element(By.XPATH,"//td[@class='nto-modal__form__table__cell nto-modal__form__table__cell--asset-from']//input[@role='combobox']").send_keys(from_asset)
        time.sleep(2)
        driver.find_element(By.XPATH,
                            "//td[@class='nto-modal__form__table__cell nto-modal__form__table__cell--asset-from']//input[@role='combobox']").send_keys(Keys.ENTER)

        # selecting to-asset
        print("selecting to-asset")
        driver.find_element(By.XPATH,
                            "//td[@class='nto-modal__form__table__cell nto-modal__form__table__cell--asset-to']//input[@role='combobox']").send_keys(
            to_asset)
        time.sleep(2)
        driver.find_element(By.XPATH,
                            "//td[@class='nto-modal__form__table__cell nto-modal__form__table__cell--asset-to']//input[@role='combobox']").send_keys(
            Keys.ENTER)

        #selecting from-fueltype
        print("Selecting from-fueltype")
        driver.find_element(By.XPATH, "//label[text()='Fuel Type']/parent::node()//input[@role='combobox']").send_keys(from_fueltype)
        time.sleep(2)
        driver.find_element(By.XPATH, "//label[text()='Fuel Type']/parent::node()//input[@role='combobox']").send_keys(Keys.ENTER)

        #selecting from-comp
        print("selecting from-compartment")
        driver.find_element(By.XPATH, "(//label[text()='Comp']/parent::node()//input[@role='combobox'])[1]").send_keys(from_comp)
        time.sleep(2)
        driver.find_element(By.XPATH, "(//label[text()='Comp']/parent::node()//input[@role='combobox'])[1]").send_keys(Keys.ENTER)

        #selecting to-driver
        print("selecting to-driver")
        driver.find_element(By.XPATH, "(//label[text()='Driver']/parent::node()//input[@role='combobox'])[2]").send_keys(to_driver)
        time.sleep(2)
        driver.find_element(By.XPATH, "(//label[text()='Driver']/parent::node()//input[@role='combobox'])[2]").send_keys(Keys.ENTER)


        # selecting to-comp
        print("selecting to-compartment")
        driver.find_element(By.XPATH, "(//label[text()='Comp']/parent::node()//input[@role='combobox'])[2]").send_keys(to_comp)
        time.sleep(2)
        driver.find_element(By.XPATH, "(//label[text()='Comp']/parent::node()//input[@role='combobox'])[2]").send_keys(Keys.ENTER)

        # Entering gallons
        print("Entering gallons")
        driver.find_element(By.XPATH, "//input[@id='NewTransferOrderVolume']").send_keys(gallons)

        # Entering Transfer note
        driver.find_element(By.XPATH, "//textarea[@id='NewTransferOrderNotes']").send_keys("Automated Transfer note")

        #submit button
        print("Clicking submit button")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()


        #Verify toast message and Dashboard page
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='toast toast-success']")))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(dashboard))
        print( "SUCCESSFULLY RECORDED TRANSFER")

    #______________________Schedule Transfer Order____________________________________
    def schedule_transfer_order(driver, from_asset, to_asset, from_fueltype, from_comp, to_comp, gallons, driver_name):
        print("***********Scheduling Transfer Order***************")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(schedule_transfer_btn)).click()
        #selecting from-asset
        print("Selecting from-asset")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='NewTransferOrderAssetFrom']//parent::div//input"))).send_keys(from_asset)
        time.sleep(2)
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderAssetFrom']//parent::div//input").send_keys(Keys.ENTER)

        #Selecting to-asset
        print("Selecting to-asset")
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderAssetTo']//parent::div//input").send_keys(to_asset)
        time.sleep(2)
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderAssetTo']//parent::div//input").send_keys(Keys.ENTER)

        #Selecting fueltype
        print("Selecting Fuel type")
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderProduct']//parent::div//input").send_keys(from_fueltype)
        time.sleep(2)
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderProduct']//parent::div//input").send_keys(Keys.ENTER)

        #Selecting from-compartment
        print("Selecting from-compartment")
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderCompartmentFrom']//parent::div//input").send_keys(from_comp)
        time.sleep(2)
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderCompartmentFrom']//parent::div//input").send_keys(Keys.ENTER)

        # Selecting to-compartment
        print("Selecting to-compartment")
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderCompartmentTo']//parent::div//input").send_keys(to_comp)
        time.sleep(2)
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderCompartmentTo']//parent::div//input").send_keys(Keys.ENTER)

        #Entering gallon
        print("Entering gallon value: " + str(gallons))
        driver.find_element(By.XPATH, "//label[@for='NewTransferOrderVolume']//parent::div//input").send_keys(gallons)

        #Driver name
        print("Entering driver's name: "+driver_name)
        driver.find_element(By.XPATH, "//div[contains(@class,'select__placeholder') and text()='Select Driver']//parent::div//input").send_keys(driver_name)
        time.sleep(2)
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//label[text()='Driver']/parent::node()//input"))).send_keys(Keys.ENTER)

        #Transfer order note
        print("Entering Transfer order note")
        driver.find_element(By.XPATH, "//textarea[@id='NewTransferOrderNotes']").send_keys("Automated transfer order note")

        #submit button
        print("Clicking submit button")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        #verify toast message
        WebDriverWait(driver,8).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='toast toast-success']")))

        print("TRANSFER ORDER SCHEDULED")


    #______________________________Create_Extraction_Order___________________________________
    def create_extraction_order(driver, customer_search, customer, shipto, asset, gallons, driver_name):
        print("****************Creating Extraction Order******************")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Create Order')]"))).click()

        print("Page title: " + driver.title)
        print("Page URL: " + driver.current_url)

        # selecting a Customer from the list
        print("Selecting Customer from the list")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "customerSelect"))).click()
        driver.find_element(By.ID, "customerSelect").send_keys(customer_search)
        driver.find_element(By.XPATH, "//li[normalize-space()='" + customer + "']").click()

        # selecting Shipto from the list
        print("Selecting Shipto from the list")
        select = Select(driver.find_element(By.ID, "branchSelect"))
        select.select_by_visible_text(shipto)

        # clicking create order button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(delivery_create_order_btn)).click()

        # Select extraction tab
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Extraction Order')]"))).click()

        #searching asset
        driver.find_element(*delivery_asset_search_box).send_keys(asset)

        # putting values to product input box
        print("Entering gallon value for asset: " + asset)
        driver.find_element(By.XPATH,
                            "//div[contains(text(), '" + asset + "')]/parent::node()/parent::node()//input[@name ='asset_volume']").send_keys(gallons)

        # Selecting a driver
        driver.find_element(By.XPATH, "//span[contains(text(),'Select Driver')]").click()
        driver.find_element(By.XPATH, "//*[contains(@class,'select2-search__field')]").send_keys(driver_name)
        driver.find_element(By.XPATH, "//*[contains(@class,'select2-search__field')]").send_keys(Keys.ENTER)
        print("Driver selected: " + motorist)

        # Extraction instruction
        extraction_instruction = driver.find_element(By.XPATH, "//textarea[contains(@name,'delivery_instructions')]")
        extraction_instruction.clear()
        extraction_instruction.send_keys("Automated text for the driver")
        print("Delivery instruction Entered")

        # submit button to create the order
        driver.find_element(By.XPATH, "//button[contains(text(),'Create Orders')]").click()

        # Verify order created
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Order Wells']")))
        print("EXTRACTION ORDER CREATED")























































