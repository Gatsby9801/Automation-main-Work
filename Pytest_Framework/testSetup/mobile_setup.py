from appium import webdriver


'''def mobile_driver(test_name):
    caps = {}
    caps['platformName'] = 'Android'
    caps['appium:app'] = 'storage:filename=app-staging-release.apk'
    caps['appium:deviceName'] = 'Android GoogleAPI Emulator'
    caps['appium:deviceOrientation'] = 'portrait'
    caps['appium:platformVersion'] = '13.0'
    caps['appium:automationName'] = 'UiAutomator2'
    caps['appium:autoGrantPermissions'] = True
    caps['sauce:options'] = {}
    caps['sauce:options']['appiumVersion'] = '1.22.3'
    caps['sauce:options']['username'] = 'oauth-dev-99498'
    caps['sauce:options']['accessKey'] = '9ae49ffe-437a-4697-9a1c-53d7fe974088'
    caps['sauce:options']['build'] = '<your build id>'
    caps['sauce:options']['name'] = test_name

    url = 'https://ondemand.eu-central-1.saucelabs.com:443/wd/hub'
    appium_driver = webdriver.Remote(url, caps)

    return appium_driver'''



#____Setup for local emulator

def mobile_driver(test_name):
    desired_caps = {
        'platformName': 'Android',
        'deviceName': 'Pixel',
        'app': 'C:\\Program Files\\app-staging-release.apk',
        # 'appPackage': 'com.fleetpanda.',
        'appActivity': 'com.fleetpanda.MainActivity',
        'autoGrantPermissions': True
    }

    appium_driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    appium_driver.implicitly_wait(30)
    print(test_name)

    return appium_driver

