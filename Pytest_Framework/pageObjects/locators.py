from selenium.webdriver.common.by import By
#from ..testSetup.data_entry import *

#Login page

#Dashboard page
dashboard = (By.XPATH, "//a[normalize-space()='Dashboard']")
settings_btn = (By.XPATH, "//a[@href='/settings']")
create_load_order_btn = (By.XPATH, "//button[contains(text(),'Create Load Order')]")
record_transfer_btn = (By.XPATH, "//button[normalize-space()='Record A Transfer']")
schedule_transfer_btn = (By.XPATH, "//button[normalize-space()='Schedule A Transfer'] | //button[text()='Schedule A Transfer']")
search_box = (By.XPATH, "//input[@id='filter-text-box']") #Orderwells search
tenant_switch_btn = (By.XPATH, "//li[@class='rs-dropdown fpnav__tenant-switch rs-dropdown-placement-bottom-end']")
user_btn = (By.XPATH, "//span[@class='rs-dropdown-toggle rs-dropdown-toggle-custom-title']")
orders_tab = (By.XPATH, "//a[normalize-space()='Orders']")
shift_board = (By.XPATH, "//a[normalize-space()='Shift Board']") #under Orders tab drop down
#customers = (By.XPATH, "//a[@href='https://client."+server+".fleetpanda.com/customers']")
shift_planner = (By.XPATH, "//span[normalize-space()='Shift Planner']")
search_box_shift_planner = (By.XPATH, "//div/input[@id='react-select-2-input']")


#Order_well
order_well = (By.XPATH,"//span[normalize-space()='Order Wells']")


#Shift board page
add_shift = (By.XPATH, "//button[normalize-space()='Add Shift']")
search_box_shift_board = (By.XPATH, "//div[@class='search-filter']//input[@id='filter-text-box']")


#Customers page
add_asset_btn = (By.XPATH, "//p[text()='Add Asset']")

#Self Customer page
add_product = (By.XPATH, "//button[@type='button']//p[text()='Add Product']")

#Delivery Order
delivery_create_order_btn = (By.ID, "searchBtn")
delivery_asset_search_box = (By.XPATH,"//*[contains(@class, 'search_tank')]")

