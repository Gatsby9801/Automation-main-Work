*** Settings ***
Library    String
Documentation    Custom Keywords for Fleetpanda
Library    SeleniumLibrary
Library    Collections
##Library    XML
Library    GetSeleniumInstances.py
Library    DateTime
Resource    ../Pages/PageObject.robot


*** Variable ***
${tenantSwitcher}    //i[@class='fa fa-exchange']//parent::div[@title='Switch Tenant'] | //span[contains(@class,'fal fa-exchange')] | //i[@class='rs-icon rs-icon-exchange']
${tenantMenu}    //div[@class='topmenu__submenu topmenu__submenu--center topmenu__submenu--arrow topmenu__user-menu'] | (//div[contains(@id,'menu-list') and contains(@class,'chakra-menu__menu-list')])[5]
...     | //li[@class='rs-dropdown fpnav__tenant-switch rs-dropdown-placement-bottom-end rs-dropdown-open']//ul[@role='menu']
${todayButton}    //div[@class='filter-wrapper']//button[@class='date-filter__button date-filter__button--today'][normalize-space()='Today']
${showUnassignedBtn}    //div[@class='filter-wrapper__status']//span[@role='button']
${assignDiverTitle}    //div/h3[@class='title' and text()='Assign Driver']
${linkOrderTitle}    //div[contains(@class,'modal__header__title') and text()='Assign Linked Order']


*** Keywords ***

SEARCH FROM TABLE
    [Documentation]    Search table elements. Generic Keyword
    [Arguments]    ${searchKeys}
    LOG    Seraching elements:${searchKeys}    console=yes
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   //input[@id='filter-text-box'] | //input[contains(@class,'chakra-input')]    15
    Input Text With Log Display    //input[@id='filter-text-box'] | //input[contains(@class,'chakra-input')]    ${searchKeys}    Search Input box
    SLEEP    2s

Get List Of Values
    [Documentation]    Return one or Multiple values to the list
    [Arguments]    ${locator}
    @{elem} =   SeleniumLibrary.Get WebElements     ${locator}
    ${rowList}=  Create List
	FOR  ${item}  IN  @{elem}
		${elementText}=    Remove String    ${item.text}    [    ]
	    ${elementText}=    Set Variable    ${elementText.strip()}
        Append To List    ${rowList}    ${elementText}
    END
    ${newList}    REMOVE NEWLINE    ${rowList}
    [Return]    ${newList}


SELECT SEARCH VALUES FROM THE LIST
    [Documentation]    Select serached values from the list of selector
    [Arguments]    ${value}    
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@class,'select__option') and text()='${value}'] | //div[contains(@class,'select_dark__option') and text()='${value}'] | //div[contains(@id,'listbox')]//div[text()='${value}'] | //div[text()="${value}"]    10
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'select__option') and text()='${value}'] | //div[contains(@class,'select_dark__option') and text()='${value}'] | //div[contains(@id,'listbox')]//div[text()='${value}'] | //div[contains(@id,'react-select') and text()='${value}']

SEARCH ORDER WELLS
    [Documentation]    Search table elements 
    [Arguments]    ${searchKeys}
    LOG    Seraching elements:${searchKeys}    console=yes
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   //input[@id='filter-text-box']    15
    SeleniumLibrary.INPUT TEXT    //input[@id='filter-text-box']    ${searchKeys}
    ##${count}    GET ELEMENT COUNT    //div[@col-id='customer' and contains(text(),"${searchKeys}")]

VERIFY SEARCH ELEMENT IS AVAILABLE ON TABLE 
    [Documentation]    Provide title and content to verify search element is available. E.g: Customer and "Jay Small Moves"
    [Arguments]    ${title}    ${contents}
    ${count}    SeleniumLibrary.GET ELEMENT COUNT    //div[contains(@col-id,'${title}') and text()="${contents}"]
    SHOULD BE TRUE    ${count}>0
    LOG    The Serach elements are available on the Table   console=yes

VERIFY SEARCH ELEMENT IS NOT AVAILABLE ON TABLE 
    [Documentation]    Provide title and content to verify search element is available. E.g: Customer and "Jay Small Moves"
    [Arguments]    ${title}    ${contents}
    SLEEP    8s
    ${count}    SeleniumLibrary.GET ELEMENT COUNT    //div[contains(@col-id,'${title}') and text()="${contents}"]
    SHOULD BE TRUE    ${count}==0
    LOG    The Serach elements are not available on the Table   console=yes

ASSIGN THE SHIFT TO DRIVER BY OPEN ORDER
    [Documentation]    Search the order and assign them to driver
    [Arguments]    ${driver}    ${searchKeys}    ${customerName}    ${createdTime}    ${showUnassigned}=False
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${todayButton}    30
    SeleniumLibrary.CLICK ELEMENT    ${todayButton}
    SEARCH ORDER WELLS    ${searchKeys}  
    RUN KEYWORD IF    '${showUnassigned}'=='True'    RUN KEYWORDS
    ...    LOG    CLicking show Unassigned button    console=yes
    ...    AND    SeleniumLibrary.CLICK ELEMENT    ${showUnassignedBtn}
    # OPEN CONTEXT MENU    (//div[contains(@col-id,'${customer}') and text()="${customerName}"])[1]
    # WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@class,'menu-list') and @role='tree']    15
    # CLICK ELEMENT    //span[normalize-space()='Reassign driver'] | //span[normalize-space()='Assign Driver']
    # WAIT UNTIL ELEMENT IS VISIBLE    ${assignDiverTitle}    15
    # CLICK ELEMENT    name=driver
    # SLEEP    3s
    # CLICK ELEMENT    //div[contains(@class,'driver-container') and text()='${driver}']
    # CLICK BUTTON    Assign
    SLEEP    4s
    #CLICK ELEMENT    (//div[contains(@col-id,'${customer}') and text()="${customerName}"])[1]
    ${latestOrder}    SET VARIABLE    //div[contains(@col-id,'customer') and text()="${customerName}"]//parent::div/div//span[contains(text(),'${createdTime}')]
    ${orderlist}    RUN KEYWORD AND RETURN STATUS   SeleniumLibrary.PAGE SHOULD CONTAIN ELEMENT    ${latestOrder}
    RUN KEYWORD IF    '${orderlist}'=='True'    RUN KEYWORDS
    ...    LOG    Selecting Latest created order    console=yes
    ...    AND    SeleniumLibrary.CLICK ELEMENT    ${latestOrder}
    ...    ELSE    RUN KEYWORDS
    ...    LOG    Clicking Next and Searching recent Shift    console=yes
    ...    AND    SeleniumLibrary.CLICK ELEMENT    //button[@class='date-filter__button date-filter__button--next']
    ...    AND    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    (//span[contains(text(),'${createdTime}')])[last()]    5
    ...    AND    SeleniumLibrary.CLICK ELEMENT    ${latestOrder}
    
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@title,'${customerName}')] | //a[contains(@title,'${customerName}')]    10
    SeleniumLibrary.CLICK ELEMENT    //div[normalize-space()='Driver Name']//parent::div//button[contains(@class,'inline-editable__action')]
    
    
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     //div[contains(@class,'placeholder') and text()='Select a Driver']//parent::div//input | //div[contains(@class,'select_dark__single-value') and text()='${driver}']//parent::div//input    15
    SeleniumLibrary.INPUT TEXT     //div[contains(@class,'placeholder') and text()='Select a Driver']//parent::div//input    ${driver}
    SELECT SEARCH VALUES FROM THE LIST    ${driver}
    SLEEP    3s
    ${linkStatus}    RUN KEYWORD AND RETURN STATUS   SeleniumLibrary.PAGE SHOULD CONTAIN ELEMENT    ${linkOrderTitle}
    RUN KEYWORD IF    '${linkStatus}'=='True'    RUN KEYWORDS
    ...    LOG    Assigning linked order    console=yes
    ...    AND    SeleniumLibrary.CLICK ELEMENT    //button[normalize-space()='Yes']
    Sleep    2s

SWITCH TENANT
    [Documentation]    Select and Switch tenant. Example: Alias:TYR and Name:Tyree
    [Arguments]    ${tenantAlias}    ${TenantName}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${tenantSwitcher}    10
    SeleniumLibrary.CLICK ELEMENT    ${tenantSwitcher}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${tenantMenu}     15
    SeleniumLibrary.CLICK ELEMENT    //div[@class='topmenu__submenu topmenu__submenu--center topmenu__submenu--arrow topmenu__user-menu']//a/div[text()='${tenantAlias}'] | (//div[contains(@id,'menu-list') and contains(@class,'chakra-menu__menu-list')])[5]//a/div[text()='${tenantAlias}'] | //a[normalize-space()='${tenantAlias}']
    SLEEP    5s
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //p[@class='fpnav__user-menu__main-icon'] | //div[@aria-label='User menu'] | //span[contains(@class,'chakra-avatar')]//parent::div//span[contains(@class,'fal fa-chevron-down')]    10
    SeleniumLibrary.CLICK ELEMENT    //p[@class='fpnav__user-menu__main-icon'] | //div[@aria-label='User menu'] | //span[contains(@class,'chakra-avatar')]//parent::div//span[contains(@class,'fal fa-chevron-down')]
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //p[@class='fpnav__user-menu__info-tenant'] | //div[@class='topmenu__user-menu__user-data__customer'] | (//div[contains(@id,'menu-list') and contains(@class,'chakra-menu__menu-list')])[6]   30
    ${tenantText}=    SeleniumLibrary.GET TEXT   //p[@class='fpnav__user-menu__info-tenant'] | //div[@class='topmenu__user-menu__user-data__customer']
    SHOULD BE EQUAL AS STRINGS    ${TenantName}     ${tenantText}
    LOG    The tenant has been switched to:${TenantName}    console=yes

Click Element With Log Display
    [Documentation]    For Clicking element and displaying log    
    [Arguments]    ${location}    ${elementName}
    Log    Clicking on ${elementName}    DEBUG    console=yes
    SeleniumLibrary.Click Element    ${location}

Input Text With Log Display
    [Documentation]    For Input element value and displaying log 
    [Arguments]     ${locator}    ${elementText}    ${fieldName} 
    Log    Entering '${fieldName}' field value as:${elementText}     DEBUG    console=yes
    Clear Element Text    ${locator}
    SeleniumLibrary.Input Text    ${locator}   ${elementText}


Click Using JavaScript
    [Documentation]    Click DOM Element By Id using javascript. Element id is search using Xpath
    [Arguments]    ${locator}
    ${elementId}    SeleniumLibrary.Get Element Attribute    xpath=${locator}    id
    Execute Javascript    document.getElementById('${elementId}').click()

CLICK AND WAIT FOR ELEMENT
    [Documentation]    Click Element and Wait for Another Element is to Appear
    [Arguments]    ${clickElementLocator}    ${waitElementLocator}
    Log    Clicking and Waiting for another element    DEBUG    console=yes
    SeleniumLibrary.Wait Until Element Is Visible    ${clickElementLocator}    30
    SeleniumLibrary.Click Element    ${clickElementLocator}
    Run Keyword And Ignore Error    SeleniumLibrary.Wait Until Element Is Visible     ${waitElementLocator}    30
    Refresh If Element Not Visible     ${waitElementLocator}
    SeleniumLibrary.Wait Until Element Is Visible     ${waitElementLocator}    30

# Click Element With Retry
#     [Documentation]    Clicks element and if element is still present, clicks again using Javascript
#     [Arguments]    ${locator}
#     Wait Until Element Is Enabled    ${locator}    15
#     Click Element    ${locator}
#     ${status}=    Run Keyword And Return Status    Wait Until Element Is Not Visible    ${locator}    30      
#     Run Keyword Unless    ${status}    Click Using Javascript    ${locator}

Click Until Element Appear
    [Documentation]    Click Element Multiple time Untill Another Element is not Appear
    [Arguments]    ${clickElementLocator}    ${waitElementLocator}    ${attemptNumber}
    ${result} =    Wait Until Keyword Succeeds    ${attemptNumber}x    3 sec    CLICK AND WAIT FOR ELEMENT    ${clickElementLocator}    ${waitElementLocator}

Refresh If Element Not Visible
    [Arguments]    ${location}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    2    Wait Until Element Is Enabled    ${location}    30
    ${elementCount}    Get Element Count    ${location}
    Run Keyword If    ${elementCount} <1   Run Keywords
    ...    Reload Page
    ...    AND    Wait Until Keyword Succeeds    4x    2    Wait Until Element Is Enabled    ${location}    30


CHECK AND CREAT A NEW TENANT
    [Arguments]    ${tenantName}    ${slug}    ${url}
    [Documentation]    Check and create new tenants
    GO TO    ${url}/admin
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //a[normalize-space()='Tenants']    15
    SeleniumLibrary.CLICK ELEMENT    //a[normalize-space()='Tenants']
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //input[@id='q_name']    10
    SeleniumLibrary.INPUT TEXT    //input[@id='q_slug']    Automation
    ${count}    GET ELEMENT COUNT    //td[normalize-space()='${tenantName}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Tenants    console=yes
    ...    AND    CREATE A NEW TENANT    ${tenantName}    ${slug} 
    ...    ELSE    LOG    Tenent:${tenantName} already exists    console=yes   


CREATE A NEW TENANT
    [Arguments]    ${tenantName}    ${slug}
    SeleniumLibrary.CLICK ELEMENT    //a[normalize-space()='New Tenant']
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     //input[@id='tenant_name']
    Input Text With Log Display    //input[@id='tenant_name']    ${tenantName}    Tenant Name
    Input Text With Log Display    //input[@id='tenant_slug']    ${slug}   Tenant SLUG
    SeleniumLibrary.CLICK ELEMENT    //select[@id='tenant_status']
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //*[@id="tenant_status"]/option[text()='active']    5
    SeleniumLibrary.CLICK ELEMENT    //*[@id="tenant_status"]/option[text()='active']
    SLEEP    3s
    SeleniumLibrary.CLICK ELEMENT    //input[@name='commit']

INPUT TEXT BY HEADER OR LABEL NAME
    [Arguments]    ${labelName}    ${inputText}
    [Documentation]    Select input box using the label
    LOG    Seleting Input Box with Label Header text:${labelName}    console=yes
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //*[text()='${labelName}']//parent::div//input[contains(@class,'select__input')]    10
    SeleniumLibrary.INPUT TEXT   //*[text()='${labelName}']//parent::div//input[contains(@class,'select__input')]    ${inputText}

SELECT DATE PICKER DATE
    [Documentation]     Select given day from datepicker
    
    ##Input Text  ${dateElem}    ${Empty}    # open the datepicker
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[@class='filter-wrapper']//div[@class='date-filter']//div[@class='date-filter__selector']//div//button[@class='date-filter__input']    10
    Click Element With Log Display    //div[@class='filter-wrapper']//div[@class='date-filter']//div[@class='date-filter__selector']//div//button[@class='date-filter__input']   Clicking Date Picker
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[@class='react-datepicker__current-month']    10
    ${monthyear}=   SeleniumLibrary.GET TEXT    //div[@class='react-datepicker__current-month']
    LOG    Today's Month:${monthyear}    console=yes
    
    ${getSelectedDate}=    SeleniumLibrary.GET TEXT    //div[contains(@class,'react-datepicker__day--selected')]
    LOG    SelectedDate: ${getSelectedDate}    console=yes

        

Get Datepicker MonthYear
    [Documentation]     Return current month + year from datepicker
    [Return]    ${monthyear}
    ${month}=   SeleniumLibrary.GET TEXT    //div[@class='react-datepicker__current-month']
    # ${year}=    Get Element Text  //*/div[@id='ui-datepicker-div']//*/div[@class='ui-datepicker-title']/span[@class='ui-datepicker-year']
    # ${monthyear}=   Catenate    ${month}  ${year}
    