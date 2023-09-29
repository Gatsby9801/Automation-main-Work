*** Settings ***
Library    String
Library    SeleniumLibrary
Resource    ../../Keywords/FleetPandaKWs.robot
Resource    ../Dashboard Page/Order Wells.robot


*** Variables ***
${orderMenu}    //div[@class='topmenu__menu-item__label'][normalize-space()='Orders'] | //*[normalize-space()='Orders']
${OrdersMenuWait}    //div[@class='topmenu__item topmenu__menu-item topmenu__item--has-submenu topmenu__item--open']//div[@class='topmenu__submenu'] | //li[@class='rs-dropdown rs-dropdown-placement-bottom-start rs-dropdown-open']//ul[@role='menu']
${recurranceOrder}    //a[@title='Recurring Orders'] | //a[normalize-space()='Recurring Orders']
${recurranceOrderTitle}    //div[@class='page-title' and text()='Recurring Schedule']
${addRecurrenceBtn}    //button[@class='button btn-primary']
${addNewRuleHeader}    //div[@role='heading' and text()='Add New Recurring Refuel']
${prevBtn}    //div[@class='filter-wrapper']//button[@class='date-filter__button date-filter__button--previous']
${fridayBeforeWeekend}    //div[contains(@class,'react-datepicker__day--selected')]//following-sibling::div[contains(@class,'react-datepicker__day--weekend')]//preceding-sibling::div[contains(@aria-label,'Choose Friday')] | (//div[contains(@class,'react-datepicker__day--selected')]//following-sibling::div[contains(@class,'react-datepicker__day--weekend')]//preceding-sibling::div)[6]


*** Keywords ***
GOTO RECURRANCE ORDER PAGE
    [Documentation]    This keyword is created for navigation to Recurrance order
    Click Element With Log Display    ${orderMenu}    Opening Order ${orderMenu}
   # WAIT UNTIL ELEMENT IS VISIBLE    ${OrdersMenuWait}    10
    Click Element With Log Display    ${recurranceOrder}    Clicking Recurrance Order
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${recurranceOrderTitle}    15
    

ADD NEW RECURRANCE RULE
    [Arguments]     ${customerName}    ${shipTo}    ${driver}    ${frequency}   
    [Documentation]    This Keyword is used for creating new Recuurance Rule
    DELETE THE EXISTING RECURRANCE RULE    ${shipTo} 
    SLEEP    2s
    Click Element With Log Display    ${addRecurrenceBtn}    Click Add new Recuurance Order
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${addNewRuleHeader}    15

    INPUT TEXT BY HEADER OR LABEL NAME    Customer    ${customerName}  
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     //div[contains(@class,'select__option') and contains(text(),'${customerName}')]    10
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'select__option') and contains(text(),'${customerName}')]

    INPUT TEXT BY HEADER OR LABEL NAME    Site    ${shipTo} 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     //div[contains(@class,'select__option') and contains(text(),'${shipTo}')]    10
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'select__option') and contains(text(),'${shipTo}')]


    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //input[@placeholder='Search']    10
    
    SELECT CHECKBOX    name=vehicle1

    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //span[normalize-space()='Top Off Selected']    10
    
    ####CLICK ELEMENT    //span[@class='no-switch-slider no-switch-round']
    
    INPUT TEXT BY HEADER OR LABEL NAME    Driver    ${driver} 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     //div[contains(@class,'select__option') and contains(text(),'${driver}')]    10
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'select__option') and contains(text(),'${driver}')]


    INPUT TEXT BY HEADER OR LABEL NAME    Frequency    ${frequency} 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     //div[contains(@class,'select__option') and contains(text(),'${frequency}')]    10
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'select__option') and contains(text(),'${frequency}')]

    WAIT UNTIL ELEMENT IS ENABLED    //button[@type='submit']
    SeleniumLibrary.CLICK ELEMENT    //button[@type='submit']
    
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${customerName}']    15


DELETE THE EXISTING RECURRANCE RULE
    [Arguments]    ${search}    ${frequncy}=Daily
    [Documentation]    Remove existing Rule 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${addRecurrenceBtn}    15
    SEARCH FROM TABLE    ${search}

    ${status}    RUN KEYWORD AND RETURN STATUS    SeleniumLibrary.PAGE SHOULD CONTAIN ELEMENT    //div[contains(@col-id,'customerBranch.name') and contains(text(),'${search}')]//parent::div//input
    
    Run Keyword If    ${status} == True    RUN KEYWORDS  
    ...    Click Element With Log Display    (//*[contains(@id,"input") and contains(@aria-label,"Press Space to toggle all rows selection")])[1]    Selecting serached Rules
    ...    AND    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //button[@class='button btn-error']    10
    ...    AND    Click Element With Log Display    //button[@class='button btn-error']    Clicking Delete ${clickButton}
    ...    AND    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //input[@placeholder='Enter text here.']    10
    ...    AND    Input Text With Log Display    //input[@placeholder='Enter text here.']    Delete future orders    Entering: "Delete future orders"
    ...    AND    WAIT UNTIL ELEMENT IS ENABLED    //button[@type='submit']    5
    ...    AND    Click Element With Log Display    //button[@type='submit']    CLicking Delete Button
   

VERIFY ORDER CREATED FOR RULES:DAILY
    [Arguments]    ${searchKeywords}    ${colID}    ${customer}    
    [Documentation]    This keyword verifies recurrence rules created based upon the Rules
    SeleniumLibrary.CLICK ELEMENT    //a[text()='Dashboard']
    SEARCH ORDER WELLS    ${searchKeywords}
   
    Click Element With Log Display    ${todayButton}    Clicking Today Button
    SLEEP    2s
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'${colID}') and text()="${customer}"]    30
    VERIFY SEARCH ELEMENT IS AVAILABLE ON TABLE    ${colID}    ${customer}

    LOG    verify the order is not avalable on previous day    console=yes
    Click Element With Log Display    ${prevBtn}    Clicking on Previous day
    SLEEP    2s
    VERIFY SEARCH ELEMENT IS NOT AVAILABLE ON TABLE    ${colID}    ${customer}


EDIT RECURRANCE RULES
    [Arguments]    ${shipTo}    ${frequency}       
    [Documentation]    Edit the recurrance rules
    GOTO RECURRANCE ORDER PAGE
    SEARCH FROM TABLE    ${shipTo} 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[@col-id="customerBranch.name" and text()="${shipTo}"]    10
    Click Element With Log Display    //div[@col-id="customerBranch.name" and text()="${shipTo}"]    Clicking on the existing Job
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[@role='heading' and text()='Update Recurring Refuel']    15
    SLEEP    2s

    LOG    Updating the frequency    console=yes
    INPUT TEXT BY HEADER OR LABEL NAME    Frequency    ${frequency} 
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     //div[contains(@class,'select__option') and contains(text(),'${frequency}')]    10
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'select__option') and contains(text(),'${frequency}')]

    Click Element With Log Display    //button[@type='submit']    clicking submit button

VERIFY ORDER CREATED FOR RULES:WEEKDAYS ONLY
    [Arguments]    ${searchKeywords}    ${colID}    ${customer}    
    [Documentation]    This keyword verifies recurrence rules created based upon the Rules
    LOG    Verifying the rules are available for weekdays only    console=yes
    SeleniumLibrary.CLICK ELEMENT    //a[text()='Dashboard']
    SEARCH ORDER WELLS    ${searchKeywords}
   
    Click Element With Log Display    ${todayButton}    Clicking Today Button
    SLEEP    2s
    SELECT DATE PICKER DATE
    SLEEP    2s
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@class,'react-datepicker__day--selected')]//following-sibling::div[contains(@class,'react-datepicker__day--weekend')]    10
    Click Element With Log Display    //div[contains(@class,'react-datepicker__day--selected')]//following-sibling::div[contains(@class,'react-datepicker__day--weekend')]    CLicking the closest weekend day
    SLEEP    2s
    VERIFY SEARCH ELEMENT IS NOT AVAILABLE ON TABLE    ${colID}    ${customer}
    LOG    ****The order is listed avalibale on Weekend****    console=yes

    RELOAD PAGE
    SLEEP    3s
    
    SELECT DATE PICKER DATE
    SLEEP    2s
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${fridayBeforeWeekend}    10
    Click Element With Log Display    ${fridayBeforeWeekend}    Selecting Friday before the weekend
    
    VERIFY SEARCH ELEMENT IS AVAILABLE ON TABLE    ${colID}    ${customer}   
    LOG    ****The order is listed on Weekdays****    console=yes

    
DELETE AND VERIFY STARTED ORDER ARE NOT REMOVED
    [Documentation]    Delete and verify that started order are not deleted when main rule is Removed
    [Arguments]    ${searchKeys}    ${shipTo}    ${colID}    ${customer}    ${status}=Scheduled
    SLEEP    3s
    SEARCH AND START THE ORDER FROM ORDER WELL    ${searchKeys} ${status}    ${shipTo}
    GOTO RECURRANCE ORDER PAGE
    LOG    Deleting the main rule    console=yes
    DELETE THE EXISTING RECURRANCE RULE    ${shipTo}
    SeleniumLibrary.CLICK ELEMENT    //a[text()='Dashboard']
    
    LOG    Verifying the started rule is not deleted    console=yes
    SELECT DATE PICKER DATE
    SLEEP    2s
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${fridayBeforeWeekend}    10
    Click Element With Log Display    ${fridayBeforeWeekend}    Selecting Friday before the weekend
    
    SLEEP    2s
    SEARCH ORDER WELLS    ${searchKeys} Active
    SLEEP    3s
    VERIFY SEARCH ELEMENT IS AVAILABLE ON TABLE    ${colID}    ${customer}   
    LOG    ****The order is listed on Weekdays****    console=yes

    LOG    verify the order is not avalable on previous day    console=yes
    Click Element With Log Display    ${prevBtn}    Clicking on Previous day
    SLEEP    2s
    VERIFY SEARCH ELEMENT IS NOT AVAILABLE ON TABLE    ${colID}    ${customer}