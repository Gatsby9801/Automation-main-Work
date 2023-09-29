*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Resource    ../Pages/Create Order/CreateOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot

#Suite Teardown   close browser
Documentation   This is a test case for creating Load and delivery order
Suite Setup    Set Library Search Order    SeleniumLibrary    AppiumLibrary

*** Variables ***
${loginUrl}     https://staging.fleetpanda.com

*** Test Cases ***
Create A Loading Plus Delivery Order And Assign Driver  
    [Tags]   Smoke_Create loading and Delivery Order
    ${all data members}    Get Test Data With Filter    DeliveryOrderDetails 
    ${member}=    Set Variable    ${all data members}[0]

    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   5s
    SWITCH TENANT    FUE    Fuel Panda
    RELOAD PAGE
    SLEEP    3s
    CREATING LOADING AND DELIVERY ORDER    ${member['CustomerName']}    ${member['CustomerFullName']}     ${member['tankType']}     ${member['productType']}        
     ...    ${member['terminalName']}    ${member['suppliersName']}    selectAllTank=NO    topOffGallon=No    gallonInput=1200 
    LOG    Assign Driver on the Delivery oreder created    console=yes
    RELOAD PAGE

    SLEEP    3s
    CLICK ELEMENT    //a/div[text()='Dashboard']
    ASSIGN THE SHIFT TO DRIVER BY OPEN ORDER    ${member['driver']}    ${member['CustomerName']}    ${member['CustomerName']}    ${CreatedTime}    showUnassigned=True
    CLICK CLOSE BUTTON  
    SLEEP    3s 
    LOG    Assign driver for the Load order Created    console=yes
    ASSIGN THE SHIFT TO DRIVER BY OPEN ORDER    ${member['driver']}    ${member['customerLoad']}    ${member['customerLoad']}    ${CreatedTime}    showUnassigned=True
    CLICK CLOSE BUTTON




