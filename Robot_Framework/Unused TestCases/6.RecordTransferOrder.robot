*** Settings ***
#Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Suite Teardown    CLOSE APPLICATION
Documentation   This is a test case for Login into mobile app
Resource    ../Pages/Login Page/mobileLogin.robot
Resource   ../Pages/DriverAppExecution/PageObject_DriverApp.robot
Resource    ../Pages/Login Page/LoginPage.robot
Resource    ../Keywords/FleetPandaKWs.robot
Suite Setup    Set Library Search Order    AppiumLibrary    SeleniumLibrary

*** Variables ***
##${loginUrl}     https://uat.fleetpanda.com
${driverNumber}    9998887775
*** Test Cases ***
TRANSFER ORDER EXECUTION
    [Tags]    SMOKE_Self Dispatch Transfer Order Execution
    ${all data members}    Get Test Data With Filter    MobileOrderExecution
    ${member}=    Set Variable    ${all data members}[0]
    Open Mobile Application
    ##SLEEP    3s
    CLICK ON SIGN IN BUTTON
    INPUT MOBILE NUMBER AND CONTINUE    ${driverNumber}
    INPUT PASSWORD AND LOGIN BUTTON    ${member['password']}
    LOG    Login to mobile application sucessfull..    console=yes
    SLEEP    3s
    ALLOW BLUETOOTH ACCESS
    LOCATION ACCESS CHECK
    SELF DISPATCH RECORD FUEL TRANSFER    ${member['fromAsset']}    ${member['toAsset']}    ${member['product1']}    1500
    LOG    *************THe transfer order from Driver app is completed sucessfully*************    console=yes