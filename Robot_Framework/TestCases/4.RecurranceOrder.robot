*** Settings ***
Resource    ../Pages/PageObject.robot
Resource    ../Pages/Settings Page/SettingsPage.robot
Resource    ../Pages/Orders/RecurranceOrder.robot
Resource    ../Pages/Dashboard Page/Order Wells.robot
Library    ../Keywords/GetSeleniumInstances.py


Suite Teardown   close browser


*** Variables ***
${loginUrl}     https://uat.fleetpanda.com
${tenantName}    Zootopia
${slugName}    ZOO
${driverNumber}

*** Test Cases ***
Create A Recurrance Order and Verify
    [Tags]  Recurrance_Order_Test
    ${all data members}    Get Test Data With Filter    RecurranceOrder 
    ${member}=    Set Variable    ${all data members}[0]
    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   4s
    SWITCH TENANT    ${slugName}    ${tenantName}
    RELOAD PAGE
    SLEEP    3s
    LOG    ************* Enabling FLag that controls Recurrance feature********    console=yes
    FEATURE FLAG ENABLE    recurring_order_feature
    
    LOG    ************* Removing Existing order and creating new Recurrance Order********    console=yes
    GOTO RECURRANCE ORDER PAGE
    ADD NEW RECURRANCE RULE    AutomationCustomer    HamroShipTo    Automation Driver    Daily

    LOG    ************* Verifying order created follows rule applied********    console=yes

    SLEEP    2s
    VERIFY ORDER CREATED FOR RULES:DAILY    AutomationCustomer Recurring scheduled    customer    AutomationCustomer

    LOG    ************* Verifying order edited********    console=yes
    
    SLEEP    2s
    EDIT RECURRANCE RULES    HamroShipTo    Every weekday (Monday to Friday)

    LOG    ************* Verifying order is updated ********    console=yes
    
    VERIFY ORDER CREATED FOR RULES:WEEKDAYS ONLY    AutomationCustomer Recurring    customer    AutomationCustomer

    SLEEP    3s
    LOG    ************* Verifying Started Order is not Removed when main rule is deleted ********    console=yes
    DELETE AND VERIFY STARTED ORDER ARE NOT REMOVED    AutomationCustomer Recurring    HamroShipTo    customer    AutomationCustomer
    