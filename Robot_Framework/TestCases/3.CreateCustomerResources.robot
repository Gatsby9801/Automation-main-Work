*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Resource    ../Pages/Create Order/CreateOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot

Suite Teardown   close browser
Documentation   This is a Pre-requisite Test case to create resouces on Self Customer
Suite Setup    Set Library Search Order    SeleniumLibrary    AppiumLibrary

*** Variables ***
${loginUrl}     https://uat.fleetpanda.com
${tenantName}    Zootopia
${slugName}    ZOO
${driverNumber}

*** Test Cases ***
Create Resources for Selected Customer 
    [Tags]   Smoke_Create Customer Resources
    ${all data members}    Get Test Data With Filter    CreateLoadAndDeliveryOrder 
    ${member}=    Set Variable    ${all data members}[0]

    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   2s
    
    GO TO    ${loginUrl} 
    SWITCH TENANT    ${slugName}    ${tenantName}
    RELOAD PAGE
    SLEEP    3s

    LOG    ************* CREATING NEW ShipTo for Customer********    console=yes
    CHECK AND CREATE A SHIPTO FOR SELECTED CUSTOMER    AutomationCustomer    HamroShipTo    Kathmandu, Nepal    26    87    NewCustomer123    HamroPOnumber_123    ${tenantName} HQ    
    
    RELOAD PAGE
    SLEEP    3s
   
    LOG    ************* CREATING NEW Assets For Customer********    console=yes
    CHECK AND CREATE A ASSET FOR SELECTED CUSTOMER    AutomationCustomer    Tank    HamroAssetAutomation    HA_01987    HamroShipTo    Regular Diesel
    

    LOG    ************* CREATING Second Assets For Customer********    console=yes
    CHECK AND CREATE A ASSET FOR SELECTED CUSTOMER    AutomationCustomer    Tank    NewHamroAssetAutomation    HA_01876    HamroShipTo    Regular Def