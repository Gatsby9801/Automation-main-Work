*** Settings ***
#Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
##Suite Teardown   close browser
Documentation   This is a test case for Login into mobile app
Resource    ../Pages/Login Page/mobileLogin.robot
Resource   ../Pages/DriverAppExecution/PageObject_DriverApp.robot
Suite Setup    Set Library Search Order    AppiumLibrary    SeleniumLibrary

*** Variables ***
##${loginUrl}     https://staging.fleetpanda.com

*** Test Cases ***
Delivery Order Flow Execution
    [Tags]    SMOKE_Mobile Login
    ${all data members}    Get Test Data With Filter    MobileOrderExecution
    ${member}=    Set Variable    ${all data members}[0]
    Open Mobile Application
    SLEEP    5s
    CLICK ON SIGN IN BUTTON
    INPUT MOBILE NUMBER AND CONTINUE    ${member['phoneNumber']}
    INPUT PASSWORD AND LOGIN BUTTON    ${member['password']}
    LOG    Login to mobile application sucessfull..    console=yes
    SLEEP    3s
    ##ALLOW/DENY LOCATION ACCESS
    LOCATION ACCESS CHECK
    START SHIFT AND SELECT VEHICLE    ${member['truck']}    ${member['trailer1']}
    SLEEP    3s
    DELIVERY ORDER EXECUTION    ${member['CustomerName']}   ${member['tankType']} 

    END SHIFT AND POST ACTIVITIES