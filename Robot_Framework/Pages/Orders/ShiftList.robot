*** Settings ***
Library    String
Library    SeleniumLibrary
Resource    ../../Keywords/FleetPandaKWs.robot


*** Variables ***
${ordersTitle}   //div[@class='topmenu__menu-item__label'][normalize-space()='Orders'] | //a[normalize-space()='Orders']
${orderSubsection]}    //div[contains(@class,'opmenu__item--has-submenu topmenu__item--open')]//div[@class='topmenu__submenu'] | //li[contains(@class,'rs-dropdown-open')]//ul




*** Keywords ***
GOTO ORDERS SUBSECTION PAGE
    [Documentation]    Navigate to given page of the Orders page
    [Arguments]    ${pageTitle}    ${waitPageTitle}  
    WAIT UNTIL ELEMENT IS VISIBLE    ${ordersTitle}    10
    CLICK ELEMENT    ${ordersTitle}
    WAIT UNTIL ELEMENT IS VISIBLE    ${orderSubsection]}    5
    CLICK AND WAIT FOR ELEMENT   //a[@title='${pageTitle}'] | //a[normalize-space()="${pageTitle}"]    //div[@class='page-title' and text()="${waitPageTitle}"]


SEARCH AND SELECT THE LATEST ORDER
    [Documentation]    Search and select driver 
    [Arguments]    ${keyname}    ${customer}    ${keyType}    
    SEARCH FROM TABLE    ${keyname}
    SLEEP    3s
    Click Element With Log Display    (//div[contains(text(),'${keyname}')]//following-sibling::div[@col-id='customers' and contains(text(),'${customer}')])[1]   ${keyType}
    
