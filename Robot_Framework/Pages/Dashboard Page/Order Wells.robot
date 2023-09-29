*** Settings ***
Library    String
Documentation    Custom Keywords for Fleetpanda
Library    SeleniumLibrary
Library    Collections
Library    XML
Library    ../../Keywords/GetSeleniumInstances.py
Library    Process
Resource    ../../Pages/PageObject.robot



*** Variable ***
${crossbtn}    //button[normalize-space()='×']
${statusText}    //div[@class='order-status-selector__value']
${downloadBtn}    //button[@class='order-toolbar__actions__btn dod-modal__toolbar']

*** Keywords ***
CLICK CLOSE BUTTON
    [Documentation]    Click on the close button
    LOG    Closing the page    console=yes
    SeleniumLibrary.CLICK BUTTON    ${crossbtn}


VERIFY DELIVERY ORDER VALUES
    [Documentation]    Search the order and Verify Delivery order
    [Arguments]    ${status}    ${driver}    ${shiftTitle}    ${customerName}    ${list1}    ${list2}
    SLEEP    3s
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@title,'${shiftTitle}')]    15
    VERIFY ORDER STATUS    ${status}

    Click Element With Log Display    //div[contains(@title,'${customerName}')]    Customer Name 
    SLEEP    5s 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@title,'${customerName}')]    15    Title with ${customerName} not Found
    VERIFY ORDER STATUS    ${status}
    VERIFY ASSIGNED DRIVER    ${driver}
    VERIFY LINE ITEMS WITH GIVEN XPATH AND LIST     ${list1}    xpath=(//div[@class='dod-modal__delivery-details__table__row'])[1]
    VERIFY LINE ITEMS WITH GIVEN XPATH AND LIST    ${list2}    xpath=(//div[@class='dod-modal__delivery-details__table__row'])[2]
    
    
VERIFY ORDER STATUS
    [Documentation]    Verify the status of the selected order
    [Arguments]    ${status}
    LOG    Verifying the order status    console=yes
    ${getStatus}    SeleniumLibrary.GET TEXT    ${statusText}
    SHOULD BE EQUAL AS STRINGS    ${status}    ${getStatus}    The status:${getStatus} is not ${status}
    LOG    The status is ${getStatus}    console=yes
    


VERIFY ASSIGNED DRIVER
    [Documentation]    Get the driver value and verify the value matches with given driver values
    [Arguments]    ${driver}
    LOG    Verifying the driver Value    console=yes
    ${getDriver}    SeleniumLibrary.GET TEXT    //div[normalize-space()='Driver Name']//parent::div//div[@class="inline-editable__formatted"]
    SHOULD BE EQUAL AS STRINGS    ${driver}    ${getDriver}    The Driver:${getDriver} is not ${driver}
    LOG    The Driver is Mr:${getDriver}    console=yes


VERIFY LINE ITEMS WITH GIVEN XPATH AND LIST
    [Documentation]    Verify Details contains the Line items DeliveryOrderDetails
    [Arguments]    ${list}    ${xpath}
    @{deliveryRow}    Get List Of Values    ${xpath}
    LOG    Delivery Row:@{deliveryRow}    console=yes
    @{givenList}    SPLIT STRING    ${list}    ,
    @{newList}    SPLIT STRING    @{deliveryRow}    ,
    FOR    ${values}    IN    @{givenList} 
        LOG    Verifying list:${newList} contains value:${values}    console=yes
        LIST SHOULD CONTAIN VALUE    ${newList}    ${values}
    END


DOWNLOAD AND VERIFY DELIVERY TICKET
    [Documentation]    remove old delivery TICKET
    [Arguments]    ${filecontains}
    LOG    removing existing older files     console=yes
    RUN PROCESS    rm -f ${EXECDIR}${/}Downloads${/}*    shell=True
    SLEEP    5s   
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${downloadBtn}    15
    SeleniumLibrary.CLICK ELEMENT    ${downloadBtn}
    SLEEP    8s
    ${newfileLoc}    MOVE FILE    ${EXECDIR}${/}Downloads${/}*-delivery-ticket*.pdf    ${EXECDIR}${/}Downloads${/}delivery-ticket.pdf
    LOG    New File:${newfileLoc}    console=yes
    VERIFY CONTENTS OF DELIVERY TICKET    ${filecontains}


VERIFY CONTENTS OF DELIVERY TICKET
    [Documentation]    verify the delivery ticket contents given list of values
    [Arguments]    ${filecontains}
    @{eachValues}    SPLIT STRING    ${filecontains}    ,
    FOR    ${element}    IN    @{eachValues}
        LOG    verifying element:${element} contains on the ticket    console=yes
        Verify file contains    ${EXECDIR}${/}Downloads${/}    delivery-ticket.pdf    ${element}
        
    END
    ##Verify file contains    ${EXECDIR}${/}Downloads${/}    delivery-ticket.pdf    {filecontains}


SEARCH AND START THE ORDER FROM ORDER WELL
    [Documentation]    This keyword is used for searching the order well and starting the Schduled ${ordersTitle}
    [Arguments]    ${searchKeys}    ${shipto}    ${status}=Started
    SEARCH ORDER WELLS    ${searchKeys}
    SLEEP    2s
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'shipTo') and contains(text(),'${shipto}')]    10
    Click Element With Log Display    //div[contains(@col-id,'shipTo') and contains(text(),'${shipto}')]    Clicking the order with shipto:${shipto}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //a[contains(@title,'${shipto}')]    15
    ${getStatus}    SeleniumLibrary.GET TEXT    //div[@class='order-status-selector__value']
    Run Keyword If    '${getStatus}' == 'SCHEDULED'    RUN KEYWORDS  
    ...    Click Element With Log Display    //div[@class='order-status-selector__trigger']    Starting the shift
    
    ...    AND    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[@class='order-status-selector__list order-status-selector__list--open']    10
    ...    AND    Click Element With Log Display    //span[@class='order-status-selector__list__item__label' and text()='${status}']    Clicking Started Button 
    ...    AND    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[@class='order-status-selector__value' and text()="${status}"]    15
    
    Click Element With Log Display    //button[normalize-space()='×']    Clickig close button