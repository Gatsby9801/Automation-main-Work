*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py
Resource    ../Pages/Create Order/CreateOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot
Resource    ../Pages/Settings Page/SettingsPage.robot

Suite Teardown   Close Browsers

Documentation   This is a Pre-requisite Test case to create resouces
Suite Setup    Set Library Search Order    SeleniumLibrary    AppiumLibrary

*** Variables ***
${loginUrl}    https://uat.fleetpanda.com
${tenantName}    Zootopia
${slugName}    ZOO
${driverNumber}


*** Test Cases ***
Create a Tenant and Customer
    [Tags]   Smoke_Create Tenant and Customer and Enable standAlone
    ${all data members}    Get Test Data With Filter    CreateLoadAndDeliveryOrder 
    ${member}=    Set Variable    ${all data members}[0]
  
    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   2s
    LOG    ************* CREATING NEW TENANT ********    console=yes
    CHECK AND CREAT A NEW TENANT    ${tenantName}    ${slugName}    ${loginUrl}

    GO TO    ${loginUrl} 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //a[@title='Customers'] | //a[text()='Customers']    10
    SLEEP    3s
    SWITCH TENANT    ${slugName}    ${tenantName}
    
    LOG    ************* CREATING NEW Customer ********    console=yes
    CHECK AND CREATE A NEW CUSTOMER    AutomationCustomer    Baker Street, Marylebone, London, UK    New12345    PO_123
    SLEEP    5s
    
    ###ENABLE FEATURE FLAG    fe_standalone_feature    fe_standalone_feature
    FEATURE FLAG ENABLE    transfer_order_feature
    FEATURE FLAG ENABLE    schedule_transfer_order_feature
    FEATURE FLAG ENABLE    self_dispatch_feature
    SELECT TIME ZONE FROM SETTING    Pacific Time (US & Canada)
    SELECT START SHIFT OPTION    one_touch_button
   

    ##CREATE A SHIPTO FOR SELECTED CUSTOMER