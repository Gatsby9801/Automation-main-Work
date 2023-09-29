*** Settings ***
#Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
#Suite Teardown    RUN KEYWORDS
#...    RUN KEYWORD IF ALL TESTS PASSED    END SHIFT AND POST ACTIVITIES
#...    AND    CLOSE APPLICATION
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
EXECUTE SCHEDULED TRANSFER ORDER AND RECORD TRANSFER ORDER
    [Tags]    SMOKE_Execute Loading Order
    ${all data members}    Get Test Data With Filter    MobileOrderExecution
    ${member}=    Set Variable    ${all data members}[0]
    Open Mobile Application
    SLEEP    3s
    CLICK ON SIGN IN BUTTON
    INPUT MOBILE NUMBER AND CONTINUE    ${driverNumber}
    INPUT PASSWORD AND LOGIN BUTTON    ${member['password']}
    LOG    Login to mobile application sucessfull..    console=yes
    SLEEP    3s
    ALLOW BLUETOOTH ACCESS
    LOCATION ACCESS CHECK
    Swipe    450    1000    450    1500
    Wait Until Keyword Succeeds    2x    30    START SHIFT AND SELECT VEHICLE    ${member['truck']}
    SLEEP    3s
    #LOADING ORDER EXECUTION    ${member['terminalName']}
    #ADD BOL DATA AND SUBMIT ORDER   ${member['bolNumber']}    ${member['supplier']}    ${member['product']}    ${member['grossTotal']}    ${member['compFirst']}    1500    1600    demmNote=There was a road block

    #SLEEP    3s

    #Execute scheduled Transfer Order
    RUN KEYWORD AND CONTINUE ON FAILURE    EXECUTE SCHEDULED TRANSFER ORDER
    

    SLEEP    12s
    #DELIVERY ORDER EXECUTION    ${member['CustomerName']}   ${member['tankType']}

    #Record Transfer Order
    SELF DISPATCH RECORD FUEL TRANSFER    ${member['fromAsset']}    ${member['toAsset']}    ${member['product1']}    1500
    LOG    *************THe transfer order from Driver app is completed sucessfully*************    console=yes
    AppiumLibrary.CLOSE APPLICATION



    ##END SHIFT AND POST ACTIVITIES

