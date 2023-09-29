*** Settings ***
Library    String
Library    SeleniumLibrary
Library    AppiumLibrary
Resource    ../../Keywords/FleetPandaKWs.robot


*** Variable ***
${customerBtn}    //div[@class='topmenu__menu-item__label'][normalize-space()='Customers'] | //a[text()='Customers']
${customerTitle}    //div[@class='page-title' and text()='Customers'] | //h2[contains(@class,'chakra-heading') and text()='Customer']
${addCustomer}    //p[normalize-space()='Add Customer'] | //span[normalize-space()='Add Customer']

# ${shipToTitle}    //button[contains(@type,'button')]//p[text()='Add ShipTo']
# ${shipToBtn}    //button[normalize-space()='Add ShipTo']
# ${shipToHeader}    //h2[contains(@class,'chakra-heading') and text()='Add New ShipTo']


*** Keywords ***
CHECK AND CREATE A NEW CUSTOMER
    [Documentation]    This keyword is used to create a new customer
    [Arguments]    ${name}    ${address}    ${erpid}    ${poNumber}
    SeleniumLibrary.CLICK ELEMENT    ${customerBtn}
    Refresh If Element Not Visible    ${customerTitle}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${customerTitle}    10
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    LOG    found:${count}    console=yes
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Customer:${name}    console=yes
    ...    AND    CREATE A CUSTOMER    ${name}    ${address}    ${erpid}    ${poNumber}
    ...    ELSE    LOG    Customer:${name} already exists    console=yes


CREATE A CUSTOMER
    [Arguments]    ${name}    ${address}    ${erpid}    ${poNumber}=${EMPTY}  
    [Documentation]    This keyword is used for creating new customer
    SeleniumLibrary.CLICK ELEMENT    ${addCustomer}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //input[@name='name']    10
    Input Text With Log Display    //input[@name='name']    ${name}    Entering the Customer name:${name}
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[1]     ${address}    Entering the Customer address:${address}
    SELECT SEARCH VALUES FROM THE LIST    ${address}

    Input Text With Log Display    //input[@name='erpId']    ${erpid}    Entering the Customer erp_id:${erpid}

    Run Keyword If    '${poNumber}'!='${EMPTY}'    
    ...    Input Text With Log Display    //input[@name='poNumber']    ${poNumber}    Entering the Customer PO Number:${poNumber}

    Click Element With Log Display    //button[@type='submit']    Submiting the Customer Details
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    10



CHECK AND CREATE A SHIPTO FOR SELECTED CUSTOMER
    [Arguments]    ${customerName}    ${shipToName}    ${address}    ${lat}    ${long}    ${erpID}    ${PO_number}     ${hub}    ${fees}=${EMPTY}    ${radius}=200
    [Documentation]    This keyword checks for the SHIPTO and creates new one if the searched SHIPTO is not available
    Click Element With Log Display    //a[normalize-space()='Customers'] | //a[@title='Customers'] | //a[contains(@data-testid,'top-navbar-item') and text()='Customers']    Customers Header Btn
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${customerTitle}    10
    SLEEP    2s
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'customer-name') and normalize-space()='${customerName}']

    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${shipToTitle}    10
    SEARCH FROM TABLE    ${shipToName}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${shipToName}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new ShipTo:${shipToName}    console=yes
    ...    AND    CREATE A SHIPTO FOR CUSTOMER    ${shipToName}    ${address}    ${lat}    ${long}    ${erpID}    ${PO_number}    ${hub}     ${fees}    ${radius}       
    ...    ELSE    LOG    SHIPTO:${shipToName} already exists    console=yes


CREATE A SHIPTO FOR CUSTOMER
    [Arguments]    ${name}    ${address}    ${lat}    ${long}    ${erpID}    ${PO_number}     ${hub}    ${fees}    ${radius}
    [Documentation]    This keyword is used for creating new Shipto on customer
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${shipToBtn}    5
    SeleniumLibrary.CLICK ELEMENT    ${shipToBtn}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${shipToHeader}    10
    Input Text With Log Display    //input[@name='name']    ${name}    Entering SHIPTO Name

    Input Text With Log Display   //input[@name='erpId']    ${erpID}    Entering erp_id for Shipto
 
    Input Text With Log Display   //input[@name='poNumber']    ${PO_number}    Entering PO_number for SHipTOp

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${address}    Entering address
    SELECT SEARCH VALUES FROM THE LIST    ${address}

    Input Text With Log Display    name=siteAttributes.lat    ${lat}    Entering Latitude
    Input Text With Log Display    siteAttributes.lng   ${long}    Entering Longtitude
    
    Input Text With Log Display    name=siteAttributes.radius    ${radius}    Entering Terminal Radius
    ##Input Text With Log Display    (//div/input[contains(@role,'combobox')])[3]    ${hub}    Entering hub
    ##SELECT SEARCH VALUES FROM THE LIST    ${hub}


    Click Element With Log Display    //button[@type='submit']    Submiting the Customer Details

    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    10

CHECK AND CREATE A ASSET FOR SELECTED CUSTOMER
    [Arguments]    ${customerName}    ${assetType}    ${name}    ${licenseNum}    ${shipTo}    ${productCategory}    ${erpID}=${EMPTY}
    [Documentation]    This keyword checks for the Asset and creates new one if the searched ASSET is not available
    Click Element With Log Display    //a[@title='Customers'] | //a[contains(@data-testid,'top-navbar-item') and text()='Customers']    Customers Header Btn
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${customerTitle}    10
    SLEEP    2s
    SeleniumLibrary.CLICK ELEMENT    //div[contains(@class,'customer-name') and normalize-space()='${customerName}']
    
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${shipToTitle}    10
    SeleniumLibrary.CLICK ELEMENT    //p[normalize-space()='Assets']
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${assetBtn}    5
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Asset:${name}    console=yes
    ...    AND    CREATE A ASSET FOR CUSTOMER    ${assetType}    ${name}    ${licenseNum}    ${shipTo}    ${productCategory}    ${erpID}
    ...    ELSE    LOG    AssetName:${name} already exists    console=yes


CREATE A ASSET FOR CUSTOMER
    [Arguments]    ${assetType}    ${name}    ${licenseNum}    ${shipTo}    ${productCategory}    ${erpID}
    [Documentation]    This keyword is used for creating new Asset on customer
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${assetBtn}    5
    SeleniumLibrary.CLICK ELEMENT    ${assetBtn}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${assetHeader}    10
    SLEEP    3s
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[1]    ${assetType}    Selecting AssetType:
    SELECT SEARCH VALUES FROM THE LIST    ${assetType}

    Input Text With Log Display    //input[@name='name']    ${name}    Entering Asset Name

    ##Input Text With Log Display   //input[@name='erpId']    ${erpID}    Entering erp_id for Shipto
 
    Input Text With Log Display   //input[@name='licensePlateNumber']    ${licenseNum}    Entering License Number for Asset

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${shipTo}    Selecting ShipTo for Created Asset
    SELECT SEARCH VALUES FROM THE LIST    ${shipTo}
    #clicking on latitude to scroll the page
    SeleniumLibrary.Click Element    //input[@name='assetMovementLocation.lat']
    #PUT SCROLL SCRIPT HERE
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[3]    ${productCategory}    Selecting ShipTo
    Press Key    (//div/input[contains(@role,'combobox')])[3]    \\13

    #SELECT SEARCH VALUES FROM THE LIST    ${productCategory}

    # Run Keyword If    '${useInDelivery}'=='Yes'    RUN KEYWORDS
    # ...    LOG    Using the Asset on Delivery    console=yes
    # ...    AND    Click Element With Log Display    //p[normalize-space()="USE IN DELIVERY"]//parent::span    Check box::"USE IN DELIVERY"

    Click Element With Log Display    //button[@type='submit']    Submiting the Customer Details
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    10