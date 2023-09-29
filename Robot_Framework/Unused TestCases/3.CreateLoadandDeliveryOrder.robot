*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Library    AppiumLibrary
Resource    ../Pages/Create Order/CreateOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot
Resource    ../Pages/Login Page/mobileLogin.robot
Resource   ../Pages/DriverAppExecution/PageObject_DriverApp.robot

Suite Teardown   close browser
Documentation   This is a test case for creating Load and delivery order
Suite Setup    Set Library Search Order    SeleniumLibrary    AppiumLibrary

*** Variables ***
${loginUrl}     https://uat.fleetpanda.com
${postShiftBtn}    //android.widget.TextView[@text="Post-Shift Activities"]
${tenantName}    Zootopia
${slugName}    Zoo
${driverNumber}    9998887775

*** Test Cases ***
Create A Loading Plus Delivery Order And Assign Driver  
    [Tags]   Smoke_Create loading and Delivery Order
    ${all data members}    Get Test Data With Filter    CreateLoadAndDeliveryOrder 
    ${member}=    Set Variable    ${all data members}[0]
    Wait Until Keyword Succeeds    2x    30    LOGIN TO MOBILE APP AND DELETE ALL ORDERS    ${member['phoneNumber']}    ${member['driverPassword']}    ${member['truck']}
    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   5s
    SWITCH TENANT    ${slugName}    ${tenantName} 
    RELOAD PAGE
    SLEEP    3s
    CREATING LOADING AND DELIVERY ORDER    ${member['CustomerName']}    ${member['CustomerFullName']}     ${member['tankType']}     ${member['productType']}        
     ...    ${member['terminalName']}    ${member['suppliersName']}    selectAllTank=NO    topOffGallon=No    gallonInput=1200 
    LOG    Assign Driver on the Delivery oreder created    console=yes
    RELOAD PAGE
    SLEEP    3s
    ##CLICK ELEMENT    //a/div[text()='Dashboard']
    ASSIGN THE SHIFT TO DRIVER BY OPEN ORDER    ${member['driver']}    ${member['CustomerName']}    ${member['CustomerName']}    ${CreatedTime}    showUnassigned=True

    CLICK CLOSE BUTTON  
    # SLEEP    3s 
    # LOG    Assign driver for the Load order Created    console=yes
    # ASSIGN THE SHIFT TO DRIVER BY OPEN ORDER    ${member['driver']}    ${member['customerLoad']}    ${member['customerLoad']}    ${CreatedTime}    showUnassigned=True
    # CLICK CLOSE BUTTON

*** Keywords ***
LOGIN TO MOBILE APP AND DELETE ALL ORDERS
    [Documentation]    Login to Mobile app and Delete Older orders    
    [Arguments]    ${member['phoneNumber']}    ${member['driverPassword']}    ${member['truck']}
    Open Mobile Application
    SLEEP    5s
    CLICK ON SIGN IN BUTTON
    INPUT MOBILE NUMBER AND CONTINUE    ${driverNumber}
    INPUT PASSWORD AND LOGIN BUTTON    ${member['driverPassword']}
    LOG    Login to mobile application sucessfull..    console=yes
    SLEEP    3s
    ALLOW BLUETOOTH ACCESS
    LOCATION ACCESS CHECK
    START SHIFT AND SELECT VEHICLE    ${member['truck']}
    SLEEP    3s
    ${status}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT  ${postShiftBtn}
    LOG    status:${status}    console=yes
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    LOG    Ending Shift and sending to Dispatch    console=yes
    ...    AND    END SHIFT AND POST ACTIVITIES
    ...    AND    SLEEP    3s
    ...    ELSE    RUN KEYWORD    
    ...    LOG    No Shift to close    console=yes
    AppiumLibrary.CLOSE APPLICATION