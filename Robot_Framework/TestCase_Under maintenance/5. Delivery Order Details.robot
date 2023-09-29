*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Resource    ../Pages/Create Order/CreateOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot


###Suite Teardown   close browser
Documentation   This is a test case for verifying Data on the Delivery order

*** Variables ***
${loginUrl}     https://staging.fleetpanda.com

*** Test Cases ***
Verify Delivery Order Details
    [Tags]   LOADING AND DELIVERY ORDER
    ${all data members}    Get Test Data With Filter    DeliveryOrderDetails
    ${member}=    Set Variable    ${all data members}[0]
    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   5s
    SWITCH TENANT    FUE    Fuel Panda
    RELOAD PAGE
    SLEEP    3s
    GOTO ORDERS SUBSECTION PAGE   Shifts List    Shift Lists
    SEARCH AND SELECT THE LATEST ORDER    ${member['driver']}   Latest Order by Driver
    VERIFY DELIVERY ORDER VALUES    COMPLETED    ${member['driver']}    ${member['truck']}    ${member['CustomerName']}    
    ...    ${member['list1']}    ${member['list2']}      
  
    DOWNLOAD AND VERIFY DELIVERY TICKET    ${member['contentFile']}
    ##VERIFY CONTENTS OF DELIVERY TICKET    ${member['contentFile']}