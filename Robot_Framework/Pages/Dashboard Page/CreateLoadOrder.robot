*** Settings ***
Library    String
Library    SeleniumLibrary

#Resource    ../../test.robot
Resource    ../../Keywords/FleetPandaKWs.robot

*** Variables ***
${createLoadOrderBtn}
${selectAterminal}   //div[contains(@class,'ui-select__placeholder') and text()='Select a Terminal']//parent::div//input
${selectProduct}    //div[contains(@class,'ui-select__placeholder') and text()='Select a Product']//parent::div//input
${gallonInput}    name=loading_orders[0].products[0].gross_quantity
${selectSupplier}    (//div[contains(@class,'ui-select__placeholder') and text()='Select a Supplier']//parent::div//input)[1]
${loadingInstructionInput}    name=loading_orders[0].loading_instruction
${clickButton}    //button[@type="submit"]
${operationBtn}     //*[text()='Operations'] | //button[contains(@id,'menu-button')]//*[text()='Operations']

##//button[contains(@id,'menu-button')]//*[text()='Operations'] |

*** Keywords ***
CREATE LOADING ORDER
    [Documentation]    This keyword is used to create loading only order
    [Arguments]    ${terminalName}    ${productName}    ${supplier}     ${gallon}     ${loading_instruction}   
    CLICK BUTTON    Create Load Order
    SEARCH AND SELECT TERMINAL    ${terminalName}
    SEARCH AND SELECT PRODUCT    ${productName}
    INPUT TEXT    ${gallonInput}    ${gallon}
    SEARCH AND SELECT SUPPLIER    ${supplier}
    INPUT TEXT    ${loadingInstructionInput}     ${loading_instruction} 
    CLICK BUTTON    ${clickButton}

SEARCH AND SELECT TERMINAL
    [Documentation]    This keyowrd is used to search and select terminal in load order creation UI
    [Arguments]    ${terminalName}
    Wait Until Element Is Visible    ${selectAterminal}    10
    CLICK ELEMENT   ${selectAterminal}
    INPUT TEXT  ${selectAterminal}   ${terminalName}
    SELECT SEARCH VALUES FROM THE LIST    ${terminalName}
    

SEARCH AND SELECT PRODUCT 
    [Documentation]    This keyword is used to search and select product in load order creation UI
    [Arguments]    ${productName}
    INPUT TEXT    ${selectProduct}    ${productName}
    SELECT SEARCH VALUES FROM THE LIST    ${productName}

SEARCH AND SELECT SUPPLIER
    [Documentation]    This keyword is used to search and select supplier in load order creation UI
    [Arguments]    ${supplierName}
    CLICK ELEMENT   ${selectSupplier}
    INPUT TEXT    ${selectSupplier}    ${supplierName}
    SELECT SEARCH VALUES FROM THE LIST    ${supplierName}


SELECT FROM OPERATION HEADER
    [Documentation]    Select values from Ooperations Documents, Self Customer, Tank Monitor
    [Arguments]    ${values}    ${header}
    SLEEP    3s
    ${count}    GET ELEMENT COUNT    ${operationBtn} 
    Run Keyword If    ${count}==1    RUN KEYWORDS
    ...    CLICK ELEMENT    ${operationBtn}
    ...    AND    SLEEP    3s
    ...    AND    CLICK ELEMENT    //a[normalize-space()='${values}']
    ...    AND    WAIT UNTIL ELEMENT IS VISIBLE    //h2[contains(@class,'chakra-heading') and text()='${header}'] | //*[contains(@class,'topmenu') and text()='${header}']    15
    ...    AND    Refresh If Element Not Visible    //h2[contains(@class,'chakra-heading') and text()='${header}'] | //*[contains(@class,'topmenu') and text()='${header}']
    ...    ELSE    Click Element With Log Display    //a[@title='Self Customer']    Clicking Self Customer
    


