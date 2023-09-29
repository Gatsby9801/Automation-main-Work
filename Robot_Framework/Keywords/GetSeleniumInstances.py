import os
import sys
from zipfile import ZipFile
import csv
from ast import literal_eval
import socket
import time
import re
import json
import textract
import ast
from selenium.webdriver.chrome.options import Options as ChromeOptions

def get_test_data_with_filter(fileName, testDataKey="", testDataValues="", excludeDataValue=""):
    """ Read JSON file and return test data.
        Examples (Robot Framework):
            | ${data}=    Get Test Data With Filter    newTestData    scenario    ${testDataType}    ${testExcludeDataType}
            | ${data}=    Get Test Data With Filter    newTestData
            | ${data}=    Get Test Data With Filter    newTestData    scenario    ${testDataType}
            | ${data}=    Get Test Data With Filter   newTestData    scenario    {'SSH Certificate With Old Log','Password authentication Without Old Log'}
            | ${data}=    Get Test Data With Filter    fileName=newTestData    testDataKey=scenario    testDataValues=''    excludeDataValue={'SSH Certificate With Old Log','Password authentication With Old Log'}
            | ${data}=    Get Test Data With Filter    newTestData    scenario    ${EMPTY}    {'SSH Certificate With Old Log','Password authentication With Old Log'}
        Examples(Python):
            | getFilterTestData('fileName', 'scenario', {'scenario_1','scenario_5'}) | Return test set where value of key 'scenario' is scenario_1 and scenario_2 |
            | getFilterTestData('fileName', 'scenario', 'All') | Return all test set available in file |
            | getFilterTestData('fileName', 'scenario', '', {'scenario_5','scenario_10'}) | Return all test set except scenario_5 and scenario_10 |
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/testData/' + fileName + '.json'
    data = json.load(open(root_dir))
    dataString = ""
    if testDataKey == "":
        print('Either Key or Value is not provided. So all Test data were selected by default.')
        output_dict = data
    else:
        common_data = [x for x in data if x[testDataKey] in {''}]

        for y in common_data:
            common_Data_Dict = y

        if testDataValues == 'All':
            data_list = [x for x in data if not x[testDataKey] in {''}]

        elif excludeDataValue != "":
            print("else")
            data_list = [x for x in data if x[testDataKey] not in excludeDataValue and not x[testDataKey] in {''}]
        else:
            print("inelse")
            data_list = [x for x in data if x[testDataKey] in testDataValues and not x[testDataKey] in {''}]
        output_dict = []
        for x in data_list:
            temp = common_Data_Dict.copy()
            temp.update(x)
            output_dict.append(temp)
    return output_dict

def Verify_file_contains(file_path,fileName,containTexts):    
	print(("=== Verifying " + fileName + " file contains. ==="))    
	fileType = fileName.split('.')    
	verifyList = containTexts.split(',')    
	if fileType[1]== "pdf" :        
		fileContains = str(textract.process(file_path+fileName)) 
        
        ##test=type(fileContains)     
		for value in verifyList:
			print(('Verifying ' + value + ' in given ' + fileType[1] + ' file.'))            
			if value not in fileContains:                
				raise ValueError('Could not found'+value)
                ##raise ValueError('Could not found {value}'.format(value=repr(value)))

def get_file_contains(file_path,fileName):
    fileContains = textract.process(file_path+fileName)
    return fileContains


def remove_newline(list):
    rep = []
    for sub in list:
        rep.append(sub.replace("\n", ","))
    return rep


def get_all_texts(locator):
    """Returns the text value of elements identified by `locator`.
        See `introduction` for details about locating elements.
        """
    elements = _element_find(locator, False, True)
    texts = []
    for element in elements:
        if element is not None:
            texts.append(element.text)
    return texts if texts else None


# def setUp(appPath):
#         "Setup for the test"
#          # Using the apk link directly to launch the app
#         app = appPath
#         self.driver = webdriver.Remote(
#             command_executor='http://$USERNAME:$ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub',
#             desired_capabilities={
#                 'platformName': 'Android',
#                 'deviceName': 'Android Emulator',
#                 'platformVersion': '11.0',
#                 'app': app,
#                 'name': 'Appium Python Android Test for Chess App',
#                 'appPackage': 'com.fuelpanda.staging',
#                 'appActivity': 'com.fleetpanda.MainActivity'
#             })
    
# from selenium import webdriver

# download_dir = "C:\\Temp\\Dowmload"  # for linux/*nix, download_dir="/usr/Public"
# options = webdriver.ChromeOptions()

# profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
#                "download.default_directory": download_dir , "download.extensions_to_open": "applications/pdf"}
# options.add_experimental_option("prefs", profile)
# driver = webdriver.Chrome('//Server/Apps/chrome_driver/chromedriver.exe', chrome_options=options)  # Optional argument, if not specified will search path.

# driver.get(`https://www.troweprice.com/content/dam/trowecorp/Pdfs/TRPIL%20MiFID%20II%20Execution%20Quality%20Report%202017.pdf`)


# def capabalities()
#     options = ChromeOptions()
#     options.browser_version = 'latest'
#     options.platform_name = 'Windows 10'
#     sauce_options = {}
#     sauce_options['build'] = '<your build id>'
#     sauce_options['name'] = '<your test name>'
#     sauce_options['screenResolution'] = '1920x1080'
#     options.set_capability('sauce:options', sauce_options)

#     url = "https://oauth-dev-99498:9ae49ffe-437a-4697-9a1c-53d7fe974088@ondemand.eu-central-1.saucelabs.com:443/wd/hub"
#     driver = webdriver.Remote(command_executor=url, options=options)


