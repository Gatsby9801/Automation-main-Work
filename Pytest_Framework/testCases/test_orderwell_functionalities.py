import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..testSetup.mobile_setup import mobile_driver
from ..pageObjects.app_locators import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import string
from ..testSetup.data_entry import *
from ..testSetup.web_setup import web_driver
from ..pageObjects.app_functions import *
from ..pageObjects.functions import *


def test_orderwell_functionalities():
    driver = web_driver("Delivery Order: add asset 1/2")
    driver.implicitly_wait(30)
    action = ActionChains(driver)
    # goto baseurl
    Config.goto_website(driver, url=base_url)
    # login
    Base.test_Login(driver, dispatcher_number, dispatcher_password)
    print(driver.title)
    # switching tenant
    Base.switch_tenant(driver)
    time.sleep(5)


    #------------puts random gallon number-------------
    gallon = str(random.randint(1, 99999)) 
    Orders.create_delivery_order(driver,'ak', 'AutomationCustomer - New12345', 'HamroShipTo - NewCustomer123 - Kathmandu, Nepal','NewHamroAssetAutomation(HA_01876)', gallon, 'Automation Driver')

    #----------closes all tabs(Order well and shift planner)----------
    driver.implicitly_wait(3)
    try:
        driver.find_element(By.XPATH, "(//div[@class = 'hide-button action-icon'])[1]").click()
    except:
        print('closed!')

    try:
        driver.find_element(By.XPATH, "(//div[@class = 'hide-button action-icon'])[1]").click()
    except:
        print('closed!!')

    driver.implicitly_wait(30)
    #----------open up orderwell tab---------------
    
    driver.find_element(By.XPATH, "//span[normalize-space()='Order Wells']/parent::node()").click()

    #-----------maximize the tab-------------------

    driver.find_element(By.XPATH, "(//i[@class = 'fas fa-expand'])[1]").click()

    #----------checks if the tab is maximized or not----------------
    #  
    if driver.find_element(By.XPATH, "//i[@class='fas fa-compress']").is_displayed():
        print('The tab is maxmized!!')
    driver.refresh()

    
    driver.find_element(By.XPATH, "//div[@class = 'box']/child::node()//div[@class = 'search-wrapper']//input").send_keys("scheduled delivery "+ gallon +"")
    #checks for gallon number and clicks scheduled
    WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text() = "+ gallon +"]"))).click()
   
    print('scheduled!!')

    #Changing status from Scheduled to Completed.
    driver.find_element(By.XPATH, "//div[@class = 'order-toolbar dod-modal__toolbar']//div[@class = 'order-status-selector__value']").click()
    print('option!!')
    #clicks completed option
    time.sleep(3)
    driver.find_element(By.XPATH, "//span[text() = 'Completed']/parent::node()").click()
    print('completed!!')
    if driver.find_element(By.XPATH, "//div[text() = 'Completed']").is_displayed():
        print("It showes completed status on Window after clicking completed at dropdown.")
    #closes the tab after switching to completed
    driver.find_element(By.XPATH, "//button[@class = 'panda-modal__header__close-button']").click()
    print('completed and closed!!')
    
    driver.refresh()
    #search for specific order using gallon as unique id
    driver.find_element(By.XPATH, "//div[@class = 'box']/child::node()//div[@class = 'search-wrapper']//input").send_keys("unverified delivery "+ gallon +"")
    print('search!')
    #clicks the tick mark at checkbox to make verification eligible.
    driver.find_element(By.XPATH, "(//div[@class = 'ag-body-viewport ag-layout-normal ag-row-animation']//input[@ref = 'eInput'])[1]").click()
    print('check mark!!')
    #clicks verify button
    driver.find_element(By.XPATH, "//button[text() = 'Verify']").click()
    print('verified!')
    #pop up review window!!
    driver.find_element(By.XPATH, "//div[@class= 'content']//div[@class = 'checkbox-wrapper']//input[@type='checkbox']").click()
    print('Reviewed!')
    #clicks ok on that tab
    driver.find_element(By.XPATH,"//button[text() = 'Approve Jobs']").click()
    print('verified!!')

    # check if the verification functionalities works or not.
    driver.refresh()
    driver.find_element(By.XPATH, "//div[@class = 'box']/child::node()//div[@class = 'search-wrapper']//input").send_keys("verified delivery "+ gallon +"")
    if driver.find_element(By.XPATH, "//span[text() = 'Verified']").is_displayed():
        print("Verification functionalities works.")


    #----------------list of gallon------------------------
    g1 = str(random.randint(1, 99999))
    g2 = str(random.randint(1, 99999))
    gallon = [g1, g2]


    #----------------repeat creating order two times-------
    for i in range(2):
        driver.implicitly_wait(30)
        Orders.create_delivery_order(driver,'ak', 'AutomationCustomer - New12345', 'HamroShipTo - NewCustomer123 - Kathmandu, Nepal','NewHamroAssetAutomation(HA_01876)', gallon[i], 'Automation Driver')
        print("Order is created time!!")

    driver.implicitly_wait(3)
    #----------closes all tabs(Order well and shift planner)----------
    try:
        driver.find_element(By.XPATH, "(//div[@class = 'hide-button action-icon'])[1]").click()#closing orderl well
    except:
        print('closed!')

    try:
        driver.find_element(By.XPATH, "(//div[@class = 'hide-button action-icon'])[1]").click()#closing shift panner
    except:
        print('closed!!')
    driver.implicitly_wait(30)
    #----------open up orderwell tab---------------
    
    driver.find_element(By.XPATH, "//span[normalize-space()='Order Wells']/parent::node()").click()

    #-----------maximize the tab-------------------

    driver.find_element(By.XPATH, "(//i[@class = 'fas fa-expand'])[1]").click()


    
    #-----------changing two order from scheduled status to completed-----------------
    for i in range(2):
        driver.implicitly_wait(30)
        #checks for gallon number and clicks scheduled
        time.sleep(3)
        driver.refresh()
        driver.find_element(By.XPATH, "//div[@class = 'box']/child::node()//div[@class = 'search-wrapper']//input").send_keys("scheduled delivery "+ gallon[i] +"")
        WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text() = "+ gallon[i] +"]"))).click()
        #Changing status
        driver.find_element(By.XPATH, "//div[@class = 'order-toolbar dod-modal__toolbar']//div[@class = 'order-status-selector__value']").click()
        
        #clicks completed 
        driver.find_element(By.XPATH, "//span[text() = 'Completed']/parent::node()").click()
        print('completed!!') #verify complete status here

        #closes the tab after switching to completed
        driver.find_element(By.XPATH, "//button[@class = 'panda-modal__header__close-button']").click() 
        print('Changed!!')
        driver.find_element(By.XPATH, "//div[@class = 'box']/child::node()//div[@class = 'search-wrapper']//input").clear()    
    print('changing two order from scheduled status to completed!!')

    driver.refresh()
    time.sleep(5)
    #click check box to verify Unverified
    driver.find_element(By.XPATH, "//div[@class='ag-header-viewport']//div[@class= 'ag-header-select-all ag-labeled ag-label-align-right ag-checkbox ag-input-field']//input[@ref='eInput']").click()
    #clicks verify button
    driver.find_element(By.XPATH, "//button[text() = 'Verify']").click()
    print('verification button clicked!')
    #clicks the tick mark at checkbox to make verification eligible.
    time.sleep(4)
    driver.find_element(By.XPATH, "//div[@class= 'content']//div[@class = 'checkbox-wrapper']//input[@type='checkbox']").click()
    driver.find_element(By.XPATH, "(//div[@class= 'content']//div[@class = 'checkbox-wrapper']//input[@type='checkbox'])[2]").click()
    print('check mark!!')
    #clicks ok on that tab
    driver.find_element(By.XPATH,"//button[text() = 'Approve Jobs']").click()
    print('verified!!')
    time.sleep(3)

    #***********************check if the tuggle button works.********************
    WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class = 'rs-btn-toggle rs-btn-toggle-sm']"))).click()
    print("Tuggle button clicked.")
    time.sleep(3)
    #****************ignore because this method cannot make make assertion error************** 
    # status = ['verified', 'scheduled','departed', 'active', 'unverified' ]
    # for index, val in enumerate(status):
    #     if WebDriverWait(driver,15).until(
    #         EC.element_to_be_clickable((By.XPATH, "//div[@class='ag-react-container']//span[@class='ag-cell-value ag-cell-value__"+ val +"']"))).is_displayed():
    #         assert False, "There is unwanted status "+ val +" of index "+ str(index) +"."
    #     else:
    #         print(f"Pass!! \n No wrong status "+ val +" of index " + str(index) + ".")
    #***************ignore****************************
    status = []
    for the_status in driver.find_elements(By.XPATH, "//div[@class='ag-react-container']//span[contains(@class, 'ag-cell-value ag-cell-value__')]"):
        status.append(the_status.text)
    print(status)
    for index, val in enumerate(status):
        if val != "Unassigned":
            assert False, f"There is {val} on the index {str(index)}"
        else:
            print(f"The value is {val} on the index {str(index)}")

    
    #checking if there is any unassigned driver
    
        
    
    time.sleep(5)
    driver.quit()
