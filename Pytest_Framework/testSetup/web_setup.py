from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


'''def web_driver(test_name):
    options = ChromeOptions()
    options.browser_version = 'latest'
    options.platform_name = 'Windows 10'
    sauce_options = {}
    sauce_options['username'] = 'oauth-dev-99498'
    sauce_options['accessKey'] = '9ae49ffe-437a-4697-9a1c-53d7fe974088'
    sauce_options['build'] = '<your build id>'
    sauce_options['screenResolution'] = '1920x1080'
    sauce_options['name'] = test_name
    sauce_options['timeZone'] = 'Los_Angeles'
    options.set_capability('sauce:options', sauce_options)

    url = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"
    driver = webdriver.Remote(command_executor=url, options=options)

    return driver'''



#___________________setup for local chrome browser______________________
def web_driver(test_name):
    driver = webdriver.Chrome()
    print(test_name)
    return driver


def Web_Driver(test_name):
    options = ChromeOptions()
    options.browser_version = 'latest'
    options.platform_name = 'Windows 10'
    sauce_options = {}
    sauce_options['username'] = 'oauth-dev-99498'
    sauce_options['accessKey'] = '9ae49ffe-437a-4697-9a1c-53d7fe974088'
    sauce_options['build'] = '<your build id>'
    sauce_options['name'] = test_name
    sauce_options['timeZone'] = 'Los_Angeles'
    options.set_capability('sauce:options', sauce_options)

    url = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"
    driver = webdriver.Remote(command_executor=url, options=options)

    return driver