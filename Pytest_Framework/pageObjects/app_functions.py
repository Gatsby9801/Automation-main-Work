#from appium import webdriver

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.action_chains import ActionChains
from ..pageObjects.app_locators import *

class App_base:
    #_________________________Phone_Login___________________________________________
    def phone_login(appium_driver, phone_number, password):
        # sign in button
        signin = WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located(signinbtn)
        )
        signin.click()
        # mobile number input field
        mobile_number = WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located(mobile_number_input_field)
        )
        mobile_number.click()
        mobile_number.send_keys(phone_number)
        print("\n Phone number entered for login")
        time.sleep(1)
        appium_driver.find_element(*continuebtn).click()

        pwd = WebDriverWait(appium_driver, 30).until(
            EC.visibility_of_element_located(pwd_input_field)
        )
        time.sleep(1)
        pwd.click()
        pwd.send_keys(password)
        print("Password entered")
        time.sleep(1)
        appium_driver.find_element(*loginbtn).click()  # loginbtn
        print("Login button clicked")

        WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located(today_shift)
        )
        print("Successfully logged into driver's app")

    #______________________Shift_Start________________________
    def shift_start(appium_driver):
        WebDriverWait(appium_driver, 12).until(
            EC.element_to_be_clickable(pre_shift_activities))# Pre-Shift Activities
        print("**********Starting Shift***********")
        appium_driver.find_element(*pre_shift_activities).click()
        print("Pre-Shift Activities clicked")

        #if shift is already started go back, Else start the shift.
        try:
            WebDriverWait(appium_driver, 12).until(
                EC.presence_of_element_located(start_shiftbtn)).click()  # Starting the shift
            WebDriverWait(appium_driver, 20).until(
            EC.presence_of_element_located(vehicle_search))
            print("SHIFT STARTED")

        except TimeoutException:
            WebDriverWait(appium_driver, 5).until(
            EC.presence_of_element_located(
                (MobileBy.XPATH, "//android.widget.TextView[@text='Verify and update starting inventory detail']")))
            print("Shift already started")
            appium_driver.find_element(MobileBy.XPATH, "//android.widget.Button[@content-desc=' , back']").click()
            WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located(today_shift))


    #__________________Vehicle_select_______________________________
    def vehicle_select(appium_driver, asset_name):
        search_vehicle = WebDriverWait(appium_driver, 10).until(
            EC.presence_of_element_located(vehicle_search)
        )
        print("********Selecting a vehicle to execute the shift**********")
        time.sleep(5)
        search_vehicle.click()
        # Selecting the vehicle(selects the vehicle from the list if not found then attempts to search from the searchbox
        try:
            WebDriverWait(appium_driver, 6).until(
                EC.element_to_be_clickable((MobileBy.XPATH,"//android.view.ViewGroup[@resource-id='"+asset_name+"']"))
            ).click()
        except TimeoutException:
            appium_driver.find_element(MobileBy.XPATH, "//android.widget.EditText[@text='Search']").send_keys(asset_name)
            appium_driver.find_element(MobileBy.XPATH,"//android.view.ViewGroup[@resource-id='" + asset_name + "']").click()
        # clear compartments
        comp1 = WebDriverWait(appium_driver, 12).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.EditText[@resource-id = 'comp-truck-0']")))
        if comp1.text.strip():
            appium_driver.find_element(*clear_all).click()
            print("Cleared all compartments")
        else:
            print("Compartment is already empty")
        # looks good button
        WebDriverWait(appium_driver, 10).until(
            EC.element_to_be_clickable(looks_goodbtn)).click()
        WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located(today_shift))
        print("VEHICLE SELECTED")
    #________________________________________Shift_End________________________________________________________
    def shift_end(appium_driver):
        print("Ending the Shift")
        WebDriverWait(appium_driver, 10).until(
            EC.presence_of_element_located(pre_shift_activities))
        #Scrolling just incase "post shift activities" is not visible
        actions = ActionChains(appium_driver)
        actions.w3c_actions.pointer_action.move_to_location(343, 882)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(354, 311)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        WebDriverWait(appium_driver, 5).until(
            EC.presence_of_element_located(post_shift_activities)
        ).click()
        try:
            WebDriverWait(appium_driver,5).until(
                EC.presence_of_element_located((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='success-btn']")
            )).click()
            appium_driver.find_element(*certify_submitbtn).click()
            
            print("Entering reason for skipping orders")
            appium_driver.find_element(MobileBy.XPATH,"//android.widget.EditText[@text='Note is Required *']").send_keys("automated skip note")
            print("Note entered")
            appium_driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='Send back to Dispatch']").click()

        except TimeoutException:
            print("Ending the shift without skipping any orders")
            WebDriverWait(appium_driver, 30).until(
                EC.presence_of_element_located(certify_submitbtn)).click()
            # Verify if shift is completed
            great_text = (MobileBy.XPATH, "//*[@text= 'Great! you do not have any tasks right now to perform']")
            try:
                WebDriverWait(appium_driver, 60).until(EC.presence_of_element_located(great_text))
                print("Shift completed successfully")
            except TimeoutException:
                assert False, "Failed to end the shift"

    #____________________________Shift End Normal_______________________________________
    def shift_end_normal(appium_driver):
        print("Ending the Shift")
        WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located(post_shift_activities)
        ).click()

        appium_driver.find_element(*certify_submitbtn).click()
        # Verify if shift is completed
        great_text = (MobileBy.XPATH, "//*[@text= 'Great! you do not have any tasks right now to perform']")
        try:
            WebDriverWait(appium_driver, 60).until(EC.presence_of_element_located(great_text))
            print("Shift completed successfully")
        except TimeoutException:
            assert False, "Failed to end the shift"


    #_____________________________Install_OTA_update______________________________________________
    def ota_update(appium_driver):
        try:
            WebDriverWait(appium_driver,1).until(
                EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text='Yes']"))
            ).click()
            print("Clicked Yes to restart the app and install OTA update")
        except TimeoutException:
            pass
    #______________________________Perform Swipe__________________________________
    #TODO: Replace all the swipes with this function
    def perform_swipe(driver, x_start, y_start, x_end, y_end):
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(x_start, y_start)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(x_end, y_end)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    #_________________________End the Shift_If Active________________________________________
    def end_shift_if_active(appium_driver):
        print("Checking and ending the shift, if active")
        try:
            WebDriverWait(appium_driver, 8).until(
                EC.presence_of_element_located(pre_shift_activities)).click()
            WebDriverWait(appium_driver, 8).until(
                EC.presence_of_element_located(
                    (MobileBy.XPATH, "//android.widget.TextView[@text='Verify and update starting inventory detail']")))
            appium_driver.find_element(MobileBy.XPATH, "//android.widget.Button[@content-desc=' , back']").click()
            App_base.shift_end(appium_driver)  # Ending the Shift

        except TimeoutException:
            try:
                WebDriverWait(appium_driver, 1).until(
                    EC.presence_of_element_located(
                        (MobileBy.XPATH, "//android.widget.ImageButton[@content-desc='Navigate up']"))).click()
                print("Shift is not active...")
            except TimeoutException:
                print("Shift is not active...")


class App_orders:

    #__________________________Schedule_Delivery_Order___________________________________________
    def schedule_delivery_order(appium_driver,delivery_customer_name, customer_site):
        print("Scheduling Delivery Order")
        appium_driver.find_element(*side_menu).click()
        appium_driver.find_element(*schedule_delivery_order).click()
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='"+delivery_customer_name+"']").click()
        appium_driver.find_element(*customer_list).click()
        appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='"+customer_site+"']").click()
        appium_driver.find_element(*submit_schedule_delivery_order).click()

    #__________________________Start_Delivery_Order_____________________________________________
    def start_delivery_order(appium_driver, shipto):

        WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "(//android.widget.TextView[@text='" + shipto + "'])[last()]"))
        ).click()
        try:
            WebDriverWait(appium_driver, 10).until(
                EC.presence_of_element_located(start_delivery_btn)).click()  # start delivery button click
            print("Delivery order started")

        except TimeoutException:
            print("Delivery order already started")

    #__________________________Start_Delivery_Order____________________________________
    def execute_delivery_order(appium_driver, asset, gallons):
        # select_asset_and_volume
        print("********Executing Delivery Order**********")
        print("Selecting asset and inserting gallons value for delivery")
        WebDriverWait(appium_driver, 20).until(
            EC.presence_of_element_located(
                (MobileBy.XPATH, "//android.widget.TextView[contains(@text, '"+asset+"')]"))).click()
        print("Asset " + asset + "selected")

        # putting values in compartment
        WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='compartment-0']"))
        ).send_keys(gallons)
        print("Delivery gallon value entered for " + asset)
        time.sleep(3)

        appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit-button']").click()
        print("submit button pressed")
        mark_customer_as_complete = WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='mark-customer-complete']"))
        )  # Mark customer as complete button
        mark_customer_as_complete.click()
        print("Mark customer as complete button pressed")

        # test_certify_and_submit
        WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text = '" + gallons + "']"))
        )  # verify correct extracted gallon is displayed

        post_ordernote = WebDriverWait(appium_driver, 5).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='note']")))
        post_ordernote.click()
        post_ordernote.send_keys("Driver's post order automated note")
        print("post order note Entered")

        # submit
        appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit']").click()
        WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located(today_shift))
        print("DELIVERY ORDER EXECUTED")


    #____________________________Start_Extraction_Order____________________________________

    def start_extraction_order(appium_driver, shipto):
        print("********Starting Extraction Order************")
        WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located(
                (MobileBy.XPATH, "(//android.widget.TextView[@text='" + shipto + "'])[last()]"))
        ).click()
        try:
            WebDriverWait(appium_driver, 10).until(
                EC.presence_of_element_located(start_extraction_btn)).click()  # start extraction button click
            print("EXTRACTION ORDER STARTED")

        except TimeoutException:
            print("Extraction order already started")

#__________________________Execute Extraction Order_________________________________
    def execute_extraction_order(appium_driver, asset, gallons):
        # select_asset_and_volume
        print("********Executing Extraction Order**********")
        print("Selecting asset and inserting gallons value for extraction")
        WebDriverWait(appium_driver, 20).until(
            EC.presence_of_element_located(
                (MobileBy.XPATH, "//android.widget.TextView[contains(@text, '"+asset+"')]"))).click()
        print("Asset " + asset + "selected")

        # putting values in compartment
        WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='compartment-0']"))
        ).send_keys(gallons)
        print("Extraction gallon value entered for " + asset)
        WebDriverWait(appium_driver,5).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text= 'Extraction']")))#Extraction label verification
        time.sleep(3)

        appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit-button']").click()
        print("submit button pressed")
        mark_customer_as_complete = WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='mark-customer-complete']"))
        )  # Mark customer as complete button
        mark_customer_as_complete.click()
        print("Mark customer as complete button pressed")

        # test_certify_and_submit
        WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//android.widget.TextView[@text = '" + gallons + "']"))
        )  # verify correct extracted gallon is displayed

        post_ordernote = WebDriverWait(appium_driver, 5).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='note']")))
        post_ordernote.click()
        post_ordernote.send_keys("Driver's post order automated note")
        print("post order note Entered")

        # submit
        appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='submit']").click()
        WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located(today_shift))
        print("EXTRACTION ORDER EXECUTED")


    #_________________________Start_Load_Order__________________________________________
    def start_load_order(appium_driver, terminal):
        print("Starting Load order")
        appium_driver.find_element(MobileBy.XPATH, "(//android.widget.TextView[@text ='"+terminal+"'])[last()]").click()
        try:
            WebDriverWait(appium_driver, 10).until(
                EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='fill-btn']"))).click()  # start load btn
        except TimeoutException:
            print("Load order already started, now executing")

        done_loading = WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='done-load']")))
        done_loading.click()

    #_____________________________Record_Load_Order___________________________________
    def record_load_order(appium_driver, vehicle, trailer_1, trailer_2, terminal):
        print("Recording Load Order")
        appium_driver.find_element(*side_menu).click()
        appium_driver.find_element(*record_load_order).click()

        print("Selecting Truck")
        appium_driver.find_element(*load_truck).click()
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='"+vehicle+"']").click()

        print("trailer1")
        appium_driver.find_element(*load_trailer_1).click()
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='"+trailer_1+"']").click()

        print("Trailer2")
        appium_driver.find_element(*load_trailer_2).click()
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='"+trailer_2+"']").click()

        print("Selecting Terminal")
        appium_driver.find_element(*load_terminal_searchbox).send_keys(terminal)
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='"+terminal+"']").click()

        print("Clicking Add BOL button")
        appium_driver.find_element(*record_load_add_bol_btn).click()

    #________________________________BOL_form_fill_up_and complete_Load_Order_______________________
    def bol_form_fillup(appium_driver, supplier, product, volume):

        print("*********Filling up BOL*********")
        bol_num = WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='bol-number']"))
        )
        bol_num.send_keys("1122")
        print("BOL number:1122")
        card_in_time = appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='card-in-time']")  # card in time
        card_in_time.click()
        card_in_time.send_keys("1500")
        card_out_time = appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='card-out-time']")  # card out time
        card_out_time.click()
        card_out_time.send_keys("1550")
        action = TouchAction(appium_driver)
        action.press(x=436, y=616).release().perform()
        # supplier
        print("selecting supplier")
        supplier_select = appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='supplier']")
        supplier_select.click()

        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//*[normalize-space(@text)='{}']".format(supplier)))
        ).click()
        #appium_driver.find_element(MobileBy.XPATH, "//*[normalize-space(@text)='{}']".format(supplier)).click()
        print("supplier selected: " + supplier)

        print("selecting product")
        product_select = appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='select-product']")
        product_select.click()
        appium_driver.find_element(MobileBy.XPATH, "//*[@text = '" + product + "']").click()
        print("product selected :" + product)
        appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='total-net']").send_keys(volume)  # Total net
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.EditText[@resource-id='total-gross']").send_keys(
            volume)  # Total gross
        appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='comp-0']").send_keys(volume)  # compartment 1st
        try:
            WebDriverWait(appium_driver,3).until(
                EC.element_to_be_clickable((MobileBy.XPATH, "//*[@text='Continue']"))).click()
        except TimeoutException:
            pass
        # uploading bol image
        print("Taking a camera pic for BOL image")
        image_btn = appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='camera-btn']")
        image_btn.click()
        '''appium_driver.find_element(MobileBy.XPATH, "//*[@text = 'Choose from Library']").click()#choose image from gallery
        time.sleep(10)# refactor to take a pic from the camera
        action.press(x=117, y=756).release().perform()#selecting an img from gallery '''
        appium_driver.find_element(MobileBy.XPATH, "//*[@text = 'Take a Photo']").click()  # taking a pic from camera
        time.sleep(5)
        appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='camera']").click()
        print("camera snapshot button clicked")
        time.sleep(5)
        appium_driver.find_element(MobileBy.XPATH, "//*[@text = 'Ok']").click()
        print("clicking ok to confirm the  bol image")
        time.sleep(8)
        print("BOL form completed")
    #_______________________Complete_Load_Order____________________________________________
    def complete_load_order(appium_driver):
        print("completing the Load order")
        next = appium_driver.find_element(MobileBy.XPATH, "//*[@resource-id='next']")
        next.click()
        no_delay = WebDriverWait(appium_driver, 30).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='delay-no']"))
        )
        no_delay.click()
        WebDriverWait(appium_driver, 20).until(
            EC.presence_of_element_located(today_shift)
        )
        print("LOAD ORDER EXECUTED")

    #________________________Schedule_Load_Order_____________________________________________________
    def schedule_load_order(appium_driver, terminal, product, volume, supplier):
        print("**********Scheduling Load Order**********")
        WebDriverWait(appium_driver, 10).until(
            EC.element_to_be_clickable(side_menu)).click()
        appium_driver.find_element(*schedule_load_order).click()

        print("Selecting Terminal")
        appium_driver.find_element(MobileBy.XPATH,
                                   "//android.widget.TextView[@text='"+terminal+"']").click()

        print("Selecting a Product")
        appium_driver.find_element(*product_0).click()
        appium_driver.find_element(MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='"+product+"']").click()
        print("Product Selected")

        print("Entering Gross value")
        appium_driver.find_element(*gross_0_input_field).send_keys(volume)

        print("Selecting a Supplier")
        appium_driver.find_element(*supplier_0).click()
        appium_driver.find_element(MobileBy.XPATH,
                                   "//android.view.ViewGroup[@resource-id='"+supplier+"']").click()
        print("Supplier selected")

        # Submit to schedule a load order
        print("Clicking submit button to schedule a Load Order")
        appium_driver.find_element(*submit_schedule_load_order).click()
        print("submit button clicked to schedule Load Order")
        WebDriverWait(appium_driver, 20).until(
            EC.presence_of_element_located(today_shift)
        )
        print("LOAD ORDER SCHEDULED")

    #_______________Record_Transfer_Order________________________________________
    def record_transfer_order(appium_driver, transfer_in_vehicle, transfer_out_vehicle, product, volume):
        print("Recording Transfer Order")
        appium_driver.find_element(*side_menu).click()
        appium_driver.find_element(*record_fuel_transfer).click()

        print("Selecting Transfer-in vehicle")
        WebDriverWait(appium_driver, 12).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='fromTruck']"))).click()
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id = '"+transfer_in_vehicle+"']"))).click()

        print("Selecting Transfer-out vehicle")
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id = 'toTruck']"))).click()
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id = '"+transfer_out_vehicle+"']"))).click()

        print("Selecting compartments")
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id= 'fromComp_0']"))).click()
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@text, 'Comp 1')]"))).click()
        #toCompartment
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='toComp_0']"))).click()
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@text, 'Comp 1')]"))).click()

        print("Selecting product")
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='transferProd_0']"))).click()
        WebDriverWait(appium_driver, 8).until(
            EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='"+product+"']"))).click()
        try:
            WebDriverWait(appium_driver, 5).until(
                EC.element_to_be_clickable((MobileBy.XPATH, "//android.widget.Button[@text='CONTINUE']"))).click()
        except TimeoutException:
            pass

        print("Entering Volume")
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.EditText[@resource-id='gal_0']").send_keys(volume)

        print("Entering note")
        appium_driver.find_element(MobileBy.XPATH, "//android.widget.EditText[@resource-id='notes']").send_keys("Automated transfer order note")

        print("Clicking submit button")
        WebDriverWait(appium_driver, 8).until(
        EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.ViewGroup[@resource-id= 'submit']"))).click()

        WebDriverWait(appium_driver, 15).until(
            EC.presence_of_element_located(today_shift))
        print("Transfer Order successfully recorded")



























