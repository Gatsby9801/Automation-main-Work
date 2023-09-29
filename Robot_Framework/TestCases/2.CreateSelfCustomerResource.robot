*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Resource    ../Pages/Create Order/CreateOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot

Suite Teardown   Close Browsers
Documentation   This is a Pre-requisite Test case to create resouces on Customer
Suite Setup    Set Library Search Order    SeleniumLibrary    AppiumLibrary

*** Variables ***
${loginUrl}     https://uat.fleetpanda.com
${tenantName}    Zootopia
${slugName}    ZOO
${driverNumber}    9998887775

*** Test Cases ***
Create Resources For Self Customer  
    [Tags]   Smoke_Create Self Customer Resources
    ${all data members}    Get Test Data With Filter    CreateLoadAndDeliveryOrder 
    ${member}=    Set Variable    ${all data members}[0]

    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   2s
    
    GO TO    ${loginUrl} 
    SWITCH TENANT    ${slugName}     ${tenantName}
    RELOAD PAGE
    SLEEP    3s

    LOG    ************* CREATING NEW Products Def and Diesel ********    console=yes
    CHECK AND CREATE AND NEW PRODUCT    Diesel    Regular    Regular Diesel    ERP_RegDeisel    Gallon
    
    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    CHECK AND CREATE AND NEW PRODUCT    Def    Regular    Regular Def    ERP_RegDef_123    Gallon
    
    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW Suppliers ********    console=yes
    CHECK AND CREATE AND NEW SUPPLIERS    Suppliers_Automation    carrierName    009988    loadingAccount=yes   suppID=supp123    erpID=erp009988   

    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW Terminal ********    console=yes
    CHECK AND CREATE AND NEW TERMINAL    AutomationTerminal    Banepa, Nepal    27    86    Term_10210    Suppliers_Automation    carrierName / 009988

    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW Driver ********    console=yes
    CHECK AND CREATE AND NEW DRIVER    Automation Driver    AD_00198    auto@gmail.com    ${driverNumber}

    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW User ********    console=yes
    CHECK AND CREATE AND NEW USER    TestUser    9998887775    test@g.c    Kathmandu, Nepal    Active    roles=ADMIN

    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW ShipTo ********    console=yes
    CHECK AND CREATE AND NEW SHIPTO    Automation ShipTO    Kathmandu, Nepal    28    87    ST_01987    PO_01987    ${tenantName} HQ

    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW Assets ********    console=yes
    CHECK AND CREATE AND NEW ASSET    Tank Wagon    Automation Asset    BaOnePa 23432    Automation ShipTO    Diesel
    
    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW Truck ********    console=yes
    CHECK AND CREATE AND NEW ASSET    Flatbed Truck    Automation Truck    BaTwoPa 23444    Automation ShipTO    Ethanol

    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW Tank ********    console=yes
    CHECK AND CREATE AND NEW ASSET    Tank    Automation Tank    BaThreePa 334455    Automation ShipTO    Regular Diesel    useInDelivery=No

    GOTO LOGIN PAGE AND RELOAD    ${loginUrl}
    LOG    ************* CREATING NEW Tank ********    console=yes
    CHECK AND CREATE AND NEW ASSET    Trailer    Automation Trailer    BaFourPa 445566    Automation ShipTO    Diesel


*** Keywords ***
GOTO LOGIN PAGE AND RELOAD
    [Arguments]    ${loginUrl}                
    GO TO    ${loginUrl} 
    RELOAD PAGE
    SLEEP    3s

    