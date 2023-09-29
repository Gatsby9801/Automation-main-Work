*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py


Suite Teardown    Close Browsers
Documentation   This is a test case for Schedule and assign Fuel transfer

*** Variables ***
${loginUrl}     https://uat.fleetpanda.com
${tenantName}    Zootopia
${slugName}    ZOO
${driverNumber}

*** Test Cases ***
SCHEDULE FUEL TRANSFER AND ASSIGN DRIVER
    [Tags]   SCHEDULE A FUEL TRANSFER
    ${all data members}    Get Test Data With Filter    ScheduleFuelTransfer 
    ${member}=    Set Variable    ${all data members}[0]
    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   5s
    SWITCH TENANT    ${slugName}    ${tenantName}
    RELOAD PAGE
    SLEEP    3s
    SCHEDULE A FUEL TRANSFER    ${member['fromAsset']}    ${member['toAsset']}    ${member['fuleType']}     ${member['fromComp']}    
    ...    ${member['toComp']}     ${member['gallons']}    driver=${member['driver']}       
    