*** Settings ***
Resource    ../Pages/PageObject.robot
Library    ../Keywords/GetSeleniumInstances.py

Suite Teardown   close browser
Documentation   This is a Create load order test case

*** Variables ***
${loginUrl}     https://uat.fleetpanda.com
${tenantName}    Zootopia
${slugName}    ZOO
${driverNumber}

*** Test Cases ***
Create A Loading Order
    [Tags]  Smoke_Create Loading Order
    ${all data members}    Get Test Data With Filter    CreateLoadOrder 
    ${member}=    Set Variable    ${all data members}[0]
    LOGIN TO APPLICATION    ${loginUrl}   ${member['userName']}   ${member['password']}
    SLEEP   4s
    SWITCH TENANT    ${slugName}    ${tenantName}
    RELOAD PAGE
    SLEEP    3s
    CREATE LOADING ORDER    ${member['terminal']}    ${member['product']}    ${member['supplier']}
    ...    ${member['gallon']}    ${member['loading_instruction']}



