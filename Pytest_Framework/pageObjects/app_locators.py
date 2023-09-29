from appium.webdriver.common.mobileby import MobileBy


#________________________SIGNIN__________________________
signinbtn = (MobileBy.XPATH, "//*[@resource-id='signin']")
mobile_number_input_field = (MobileBy.XPATH, "//*[@resource-id='phone-number-entry']")
continuebtn = (MobileBy.XPATH, "//*[@resource-id='phone-verify']")
pwd_input_field = (MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText")
loginbtn = (MobileBy.XPATH, "//*[@resource-id='login']")

#____________________SHIFT___________________________
today_shift = (MobileBy.XPATH, '//android.view.View[@text="Today\'s Shift"]')
pre_shift_activities = (MobileBy.XPATH, '//android.widget.TextView[@text="Pre-Shift Activities"]')
start_shiftbtn = (MobileBy.XPATH, "//*[@resource-id='start-shift']")
vehicle_search = (MobileBy.XPATH, "//*[@resource-id='truck']")
clear_all = (MobileBy.XPATH, "//android.widget.TextView[@text= 'Clear All']")
looks_goodbtn = (MobileBy.XPATH, "//*[@resource-id='looks-good']")
post_shift_activities =(MobileBy.XPATH, "//*[@text='Post-Shift Activities']")
certify_submitbtn = (MobileBy.XPATH, "//*[@resource-id='end-shift']")

#______________________Side_menu_________________________________
side_menu = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='menu']")
schedule_load_order = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='Schedule Load Order']")
schedule_delivery_order = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='Schedule Delivery Order']")
record_load_order = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='Record Load Order']")
record_fuel_transfer = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id= 'Record Fuel Transfer']")

#_______________________Record_Load_Order_______________________________________
load_truck = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='asset-0']")
load_trailer_1 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='asset-1']")
load_trailer_2 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='asset-2']")
load_terminal_searchbox = (MobileBy.XPATH, "//android.widget.EditText[@resource-id='search']")
record_load_add_bol_btn = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='submit']")


#______________________Schedule_Load_Order______________________________
product_0 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='product-0']")
gross_0_input_field = (MobileBy.XPATH, "//android.widget.EditText[@resource-id='vol-0']")
supplier_0 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='supplier-0']")

submit_schedule_load_order = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='submit']")
add_more_products = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='add-products']")

product_1 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='product-1']")
gross_1_input_field = (MobileBy.XPATH, "//android.widget.EditText[@resource-id='vol-1']")
supplier_1 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='supplier-1']")

product_2 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='product-2']")
gross_2_input_field = (MobileBy.XPATH, "//android.widget.EditText[@resource-id='vol-2']")
supplier_2 = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='supplier-2']")

#__________________________Schedule_Delivery_Order___________________________
customer_list = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='customer']")
submit_schedule_delivery_order = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='submit']")

#__________________________Executing_Delivery_Order______________________________________
mark_customer_as_complete_btn = (MobileBy.XPATH, "//android.view.ViewGroup[@resource-id='mark-customer-complete']")
start_delivery_btn = (MobileBy.XPATH, "//android.widget.TextView[@text='Start Delivery']")
start_extraction_btn = (MobileBy.XPATH, "//android.widget.TextView[@text='Start Extraction']")
add_new_asset_btn = (MobileBy.XPATH, "//android.widget.TextView[@text= 'Add new asset']")
search_asset_input_field = (MobileBy.XPATH,"//android.widget.EditText[@resource-id='search']")
    #Add New Asset page
select_asset_type = (MobileBy.XPATH, "//android.widget.TextView[@text='Choose asset type']")
select_product_type = (MobileBy.XPATH, "//android.widget.TextView[@text='Choose product type']")
asset_name_input_field = (MobileBy.XPATH, "//android.widget.EditText[@text='Enter asset name']")
add_asset_submit_btn = (MobileBy.XPATH, "//android.widget.TextView[@text='Submit']")
licenseplate_no_input_field = (MobileBy.XPATH, "//android.widget.EditText[@text='Enter Licenseplate No.']")