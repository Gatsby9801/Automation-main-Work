*** Settings ***
Library    String
Library    SeleniumLibrary
##Library    AppiumLibrary

Resource    ../../Keywords/FleetPandaKWs.robot

*** Variables ***
${serachTanks}   //div[contains(@class,'filter')]//input
${submitBtn}    name=commit
${dashboradTitle}   //a/div[text()='Dashboard']
${selfcustomer}    //a/div[text()='Self Customer']
${createOrder}     //a[text()='Create Order'] | //a/div[text()='Create Order']
${selectCustomer}   //*[text()="1. Select Customer"]
${inputCustomerID}   id=customerSelect
${createOrderBtn}   id=searchBtn
${topOffselector}   (//span[contains(@class,'switchery switchery-small')])[1]
${skipLoad}  (//span[contains(@class,'switchery switchery-small')])[2]
${deliveryInstructionSelector}   //textarea[@name='delivery_instructions']
${selectAllTank}    xpath=//label[contains(@class,'top_off_check_label')]
${selectTerminal}   //span[text()='Select Terminal']
${searchTerminal}   //span[@class='select2-search select2-search--dropdown']/input
${productName}  //label/input[contains(@data-product-name,"DEF")]
${loadingInstructionSelector}    //textarea[@name='loading_instruction_1']



*** Keywords ***
Search Tanks While Creating Orders
    [Documentation]  Search the assets while creating orders.
    [Arguments]    ${serachText}
    WAIT UNTIL ELEMENT IS VISIBLE   ${serachTanks}  15
    INPUT TEXT  ${serachTanks}    ${serachText}


CREATING LOADING AND DELIVERY ORDER
    [Documentation]    This keywords is used to create a new loading and delivery order.
    [Arguments]    ${customerName}    ${customerFullName}     ${tankSerach}    ${products}     ${terminalName}    ${suppliersName}    ${selectAllTank}     ${topOffGallon}    
    ...    ${gallonInput}
    CLICK ELEMENT   ${createOrder}
    WAIT UNTIL ELEMENT IS VISIBLE    ${inputCustomerID}    15
    INPUT TEXT     ${inputCustomerID}    ${customerName} 
    WAIT UNTIL ELEMENT IS VISIBLE   //li[contains(text(),'${customerFullName}')]   5
    CLICK ELEMENT   //li[contains(text(),'${customerFullName}')]
    WAIT UNTIL ELEMENT IS ENABLED   ${createOrderBtn}    15
    CLICK BUTTON    ${createOrderBtn}
    SLEEP   2s
    SELECT TANK WHILE CREATING ORDERS    ${tankSerach}    ${products}    ${selectAllTank}
    TOP OFF OR GALLON INPUT    ${topOffGallon}      ${tankSerach}    ${products}    ${gallonInput}
    INPUT TEXT   ${deliveryInstructionSelector}    THIS IS DELIVERY INSTUCTION FROM AUTOMATION...
    CLICK ELEMENT   ${skipLoad}
    ${CreatedTime}   GET VALUE    //input[@name='start_time']
    SET GLOBAL VARIABLE    ${CreatedTime}
    SELECT TERMINAL WHILE CREATING LOAD ORDER    ${terminalName}
    SLEEP   3s
    LOG    Selecting Product at teminals    console=yes
    @{listOfValue}    Split String     ${products}    ,
    FOR    ${value}    IN    @{listOfValue}
        ##Log    Selecting product values: at terminal'${value}'    DEBUG    console=yes
        WAIT UNTIL ELEMENT IS VISIBLE    //label[text()[normalize-space() = '${value}']]//input    5
        Click Element With Log Display    //label[text()[normalize-space() = '${value}']]//input    Selecting product values: at terminal'${value}'    

    END
    LOG   Selecting suppliers  console=yes
    SLEEP   3s
    SELECT SUPPLIERS WHILE CREATING LOAD ORDER    ${suppliersName}
    INPUT TEXT   ${loadingInstructionSelector}  THIS IS LOADING INSTRUCTION FROM AUTOMATION
    LOG   CREATING A LOADING AND DELIVERY ORDER     console=yes
    SLEEP    5s

    CLICK ELEMENT    //button[@class='button submit-btn']
    ###CLICK BUTTON    Create Orders
    [Return]   ${CreatedTime}

SELECT TANK WHILE CREATING ORDERS
    [Documentation]    Either Select all the vehicle or tanks
    [Arguments]         ${tankSerach}    ${products}    ${selectAllTank}    
    RUN KEYWORD IF    '${selectAllTank}'=='YES'    RUN KEYWORDS
    ...    LOG    Selecting all tanks from the list    console=yes
    ...    AND    CLICK ELEMENT   ${selectAllTank}
    ...    ELSE    RUN KEYWORD    SELECT TANK FROM THE LIST    ${tankSerach}    ${products}

 SELECT TANK FROM THE LIST
    [Documentation]    provide list of tanks on comma saperated values and select them
    [Arguments]     ${tankType}    ${productTypes}
    Search Tanks While Creating Orders    ${tankType}
    @{listOfValue}    Split String     ${productTypes}    ,
    FOR    ${value}    IN    @{listOfValue}
        Log    Selecting '${value}' from dropdown '${productTypes}'.    DEBUG    console=yes
        CLICK ELEMENT     //div[contains(text(),'${tankType}')]//following-sibling::div[.//text()[normalize-space() = '${value}']]//parent::div//preceding-sibling::label[input[@type='checkbox']]  

    END

TOP OFF OR GALLON INPUT
    [Documentation]   Provides either topoff options or gallon input option
    [Arguments]    ${topOffGallon}    ${tankType}    ${productTypes}    ${gallonInput}  
    RUN KEYWORD IF    '${topOffGallon}'=='YES'    RUN KEYWORDS
    ...    LOG    TopOff all the selected vehicles    console=yes
    ...    AND    WAIT UNTIL ELEMENT IS VISIBLE   ${topOffselector}   5
    ...    AND    CLICK ELEMENT   ${topOffselector}
    ...    ELSE    RUN KEYWORD    INPUT GALLON VALUES     ${tankType}    ${productTypes}    ${gallonInput}

INPUT GALLON VALUES
    [Documentation]    provides gallon input for searched tanks
    [Arguments]     ${tankType}    ${productTypes}    ${gallonInput}
    #Search Tanks While Creating Orders    ${tankType}
    @{listOfValue}    Split String     ${productTypes}    ,
    FOR    ${value}    IN    @{listOfValue}
        Log    Inputing gallon:${gallonInput} values on product '${value}'    DEBUG    console=yes
        INPUT TEXT    //div[contains(text(),'${tankType}')]//following-sibling::div[.//text()[normalize-space() = '${value}']]//parent::div//following-sibling::div[contains(@class,'fuel-capacity')]/input[contains(@class,'asset_volume')]    ${gallonInput}
    END

SELECT TERMINAL WHILE CREATING LOAD ORDER
    [Documentation]    Select terminal  from the list while creating order
    [Arguments]    ${terminalName}
    LOG    Selecting Terminal:${terminalName} from the list    console=yes
    SLEEP    2s
    CLICK ELEMENT    ${selectTerminal} | //span[@id='select2-terminalSelect1-container' and normalize-space()='${terminalName}']
    WAIT UNTIL ELEMENT IS VISIBLE    id=select2-terminalSelect1-container    5
    SLEEP    3s
    INPUT TEXT    //input[@role='textbox']    ${terminalName}
    LOG    Selecting terminal:${terminalName} from the list of terminal    console=yes
    CLICK ELEMENT   //span[@class='select2-results']//ul 
    SLEEP   3s
    
SELECT SUPPLIERS WHILE CREATING LOAD ORDER
    [Documentation]    Select suppliers  from the list while creating order
    [Arguments]    ${suppliersName}    ${fromRow}=1
    LOG    Selecting first suppliers from the list    console=yes
    CLICK ELEMENT    (//span[text()='Select Supplier'])['${fromRow}']
    INPUT TEXT  ${searchTerminal}   ${suppliersName}
    CLICK ELEMENT   //span[@class='select2-results']//ul
    SLEEP   3s

GET TIME FROM WHILE CREATING ORDER
    [Documentation]    Get time values while creating orders
    ${time}    GET VALUE    //input[@name='start_time']
    [Return]    ${time} 
    