*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Resource    ../Pages/Create Order/CreateOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot
Suite Setup    Set Library Search Order    AppiumLibrary    SeleniumLibrary

Suite Teardown   close browser
Documentation   This is a test case for verifying Data on the Delivery order

*** Variables ***
${loginUrl}     https://uat.fleetpanda.com
${tenantName}    Zootopia
${slugName}    ZOO
${driverNumber}


*** Test Cases ***
Verify Delivery Order Details
    [Tags]   DeliveryOrderDetails
    ${all data members}    Get Test Data With Filter    DeliveryOrderDetails
    ${member}=    Set Variable    ${all data members}[0]
    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   5s
    SWITCH TENANT    ${slugName}    ${tenantName}
    RELOAD PAGE
    SLEEP    3s
    GOTO ORDERS SUBSECTION PAGE   Shift List    Shift Lists
    SLEEP    1s
    SEARCH AND SELECT THE LATEST ORDER    ${member['driver']}    ${member['CustomerName']}   Latest Order by Driver
    VERIFY DELIVERY ORDER VALUES    COMPLETED    ${member['driver']}    ${member['truck']}    ${member['CustomerName']}    
    ...    ${member['list1']}    ${member['list2']}      
  
    ##DOWNLOAD AND VERIFY DELIVERY TICKET    ${member['contentFile']}
    ##VERIFY CONTENTS OF DELIVERY TICKET    ${member['contentFile']}

    
