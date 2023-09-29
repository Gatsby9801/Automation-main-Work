from appium import webdriver
def test_mobile_driver(test_name):
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '9'
    desired_caps['deviceName'] = '127.0.0.1:62025'
    desired_caps['appPackage'] = 'com.netease.lglr.yeshen'
    desired_caps['appActivity'] = 'com.netease.lagrange.Client'
    desired_caps['noReset'] = True
    desired_caps['automationName']="UiAutomator2"
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.implicitly_wait(30)
    print(test_name)

    return driver
abc = test_mobile_driver('test')
# from appium import webdriver

# def test_mobile_driver():
#     desired_caps = {
#         'platformName': 'Android',
#         'deviceName': 'Pixel',
#         
#     }

#     # Initialize the Appium driver
#     driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)


#     # Perform actions on the website (e.g., click, type, etc.)
#     # Example: driver.find_element_by_name('q').send_keys('Appium')

#     # Close the browser
#     driver.quit()


