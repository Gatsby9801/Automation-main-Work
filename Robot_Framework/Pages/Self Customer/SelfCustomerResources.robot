*** Settings ***
Library    String
Library    SeleniumLibrary
##Library    AppiumLibrary
Resource    ../../Keywords/FleetPandaKWs.robot


*** Variable ***
${ProductBtn}    //button[normalize-space()='Add Product']
${productTitle}    //button[contains(@type,'button')]//p[text()='Add Product']
${headerText}    //h2[contains(@class,'chakra-heading') and text()='Self Customer']
${suppliersTitle}    //button[contains(@type,'button')]//p[text()='Add Supplier']
${suppliersBtn}    //button[normalize-space()='Add Supplier']
${addSupplierHeader}    //h2[contains(@class,'chakra-heading') and text()='Add Supplier']
${addLoadingAcc}    //p[normalize-space()='+ Add Loading Account']
${loadingAccName}    //input[@name='loadingAccountsAttributes.0.carrierCustomerCode']
${loadingAccNumber}    //input[@name='loadingAccountsAttributes.0.loadingNumber']
${terminalTitle}    //button[contains(@type,'button')]//p[text()='Add Terminal']
${terminalBtn}    //button[normalize-space()='Add Terminal']
${addTerminalHeader}    //h2[contains(@class,'chakra-heading') and text()='Add Terminal']

${driverTitle}    //button[contains(@type,'button')]//p[text()='Add Driver']
${driverBtn}    //button[normalize-space()='Add Driver']
${addriverHeader}    //h2[contains(@class,'chakra-heading') and text()='Add New Driver']

${shipToTitle}    //button[contains(@type,'button')]//p[text()='Add ShipTo']
${shipToBtn}    //button[normalize-space()='Add ShipTo']
${shipToHeader}    //h2[contains(@class,'chakra-heading') and text()='Add New ShipTo']

${assetTitle}    //button[contains(@type,'button')]//p[text()='Add Asset']
${assetBtn}    //button[normalize-space()='Add Asset']
${assetHeader}    //h2[contains(@class,'chakra-heading') and text()='Add New Asset']

${userTitle}    //button[contains(@type,'button')]//p[text()='Add User'] | //p[text()='Add User'] | //button[normalize-space()='Add User']
${userBtn}    //button[normalize-space()='Add User']
${addUserHeader}    //h2[contains(@class,'chakra-heading') and text()='Add New User']

*** Keywords ***
CLICK ON SELF CUSTOMER HEADER
    [Documentation]    Click on the headers from Sel customer
    [Arguments]    ${headerTitle}
    WAIT UNTIL ELEMENT IS VISIBLE    ${headerText}    15
    Refresh If Element Not Visible    ${headerText}
    WAIT UNTIL KEYWORD SUCCEEDS    2x    30s    CLICK ELEMENT    //p[normalize-space()='${headerTitle}']



CHECK AND CREATE AND NEW PRODUCT
    [Documentation]    This keyword is used to create a new Product
    [Arguments]    ${category}    ${subCategory}    ${name}    ${erpid}    ${unit}
    SELECT FROM OPERATION HEADER    Self Customer    Self Customer
    SLEEP    3s

    CLICK ON SELF CUSTOMER HEADER    Products
    WAIT UNTIL ELEMENT IS VISIBLE    ${productTitle}    15
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@class,'alias') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Product:${name}    console=yes
    ...    AND    CREATE A PRODUCT    ${category}    ${subCategory}   ${name}    ${erpid}    ${unit}
    ...    ELSE    LOG    Products:${name} already exists    console=yes


CREATE A PRODUCT
    [Arguments]    ${category}    ${subCategory}    ${name}    ${erpid}    ${unit}
    [Documentation]    This keyword is used for creating new Product on self customer
    

    WAIT UNTIL ELEMENT IS VISIBLE    ${ProductBtn}    15
    CLICK ELEMENT    ${ProductBtn}
    SLEEP    3s
    
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[1]    ${category}    Entering Product Category
    SELECT SEARCH VALUES FROM THE LIST    ${category}

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${subCategory}    Entering Product Sub-Category
    SELECT SEARCH VALUES FROM THE LIST    ${subCategory}   


    Input Text With Log Display    //input[@name='erpId']    ${erpid}    Entering the Customer erp_id:${erpid}
    
    Input Text With Log Display    //input[@name='shortName']    ${name}    Entering the Customer Name:${name}
    
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[3]    ${unit}    Entering Product units
    SELECT SEARCH VALUES FROM THE LIST    ${unit}


    Click Element With Log Display    //button[@type='submit']    Submiting the Product Details
    SLEEP    1s
    WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@class,'alias') and normalize-space()='${name}']    15

CHECK AND CREATE AND NEW SUPPLIERS
    [Documentation]    This keyword is used to create a new Suppliers
    [Arguments]    ${name}    ${carrierName}    ${loadingNumber}    ${suppID}=${EMPTY}    ${erpID}=${EMPTY}    ${loadingAccount}=${EMPTY}    
    SELECT FROM OPERATION HEADER    Self Customer    Self Customer
    SLEEP    3s

    CLICK ON SELF CUSTOMER HEADER    Suppliers
    WAIT UNTIL ELEMENT IS VISIBLE    ${suppliersTitle}    15
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Suppliers:${name}    console=yes
    ...    AND    CREATE A SUPPLIERS    ${name}    ${carrierName}    ${loadingNumber}    ${suppID}    ${erpID}    ${loadingAccount}
    ...    ELSE    LOG    Suppliers:${name} already exists    console=yes


CREATE A SUPPLIERS
    [Arguments]    ${name}    ${carrierName}    ${loadingNumber}    ${suppID}    ${erpID}    ${loadingAccount}
    [Documentation]    This keyword is used for creating new suppliers on self customer
    WAIT UNTIL ELEMENT IS VISIBLE    ${suppliersBtn}    15
    CLICK ELEMENT    ${suppliersBtn}
    WAIT UNTIL ELEMENT IS VISIBLE    ${addSupplierHeader}    15
    Input Text With Log Display    name=name    ${name}    Entering Suppliers Name

    Input Text With Log Display    name=supplierCode    ${suppID}    Entering Suppliers supplierCode
    
    Input Text With Log Display    name=erpId    ${erpID}    Entering erp_id for Suppliers

    Run Keyword If    '${loadingAccount}'=='yes'    RUN KEYWORDS
    ...    LOG    Adding loading account with number:${loadingNumber}    console=yes
    ...    AND    CLICK ELEMENT    ${addLoadingAcc}
    ...    AND    WAIT UNTIL ELEMENT IS VISIBLE    ${loadingAccName}    5
    ...    AND    Input Text With Log Display    ${loadingAccName}    ${carrierName}    Entering carrier Name
    ...    AND    Input Text With Log Display    ${loadingAccNumber}    ${loadingNumber}    Entering Loading Number  
    ...    AND    LOG    Loading order has been added    console=yes 

    Click Element With Log Display    //button[@type='submit']    Submiting the Suppliers Details
    SLEEP    1s
    WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    15

CHECK AND CREATE AND NEW TERMINAL
    [Documentation]    This keyword is used to create a new Terminal
    [Arguments]    ${name}    ${address}    ${lat}    ${long}    ${erpID}    ${suppliersName}     ${loadingAcc}    ${radius}=200       
    SELECT FROM OPERATION HEADER    Self Customer    Self Customer
    SLEEP    3s

    CLICK ON SELF CUSTOMER HEADER    Terminals
    WAIT UNTIL ELEMENT IS VISIBLE    ${terminalTitle}    15
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Terminal:${name}    console=yes
    ...    AND    CREATE A TERMINAL    ${name}    ${address}    ${lat}    ${long}    ${erpID}    ${suppliersName}     ${loadingAcc}    ${radius}       
    ...    ELSE    LOG    Terminal:${name} already exists    console=yes


CREATE A TERMINAL
    [Arguments]    ${name}   ${address}    ${lat}    ${long}    ${erpID}    ${suppliersName}    ${loadingAcc}     ${radius}
    [Documentation]    This keyword is used for creating new terminal on self customer
    WAIT UNTIL ELEMENT IS VISIBLE    ${terminalBtn}    15
    CLICK ELEMENT    ${terminalBtn}
    WAIT UNTIL ELEMENT IS VISIBLE    ${addTerminalHeader}    10
    Input Text With Log Display    name=name    ${name}    Entering Terminal Name

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[1]    ${address}    Entering address
    SELECT SEARCH VALUES FROM THE LIST    ${address}

    Input Text With Log Display    name=siteAttributes.lat    ${lat}    Entering Latitude
    Input Text With Log Display    siteAttributes.lng   ${long}    Entering Longtitude
    
    Input Text With Log Display    name=erpId    ${erpID}    Entering erp_id for Terminal

    Input Text With Log Display    name=siteAttributes.radius    ${radius}    Entering Terminal Radius

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${suppliersName}    Selecting Suppliers:${suppliersName}
    SELECT SEARCH VALUES FROM THE LIST    ${suppliersName}

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[3]    ${loadingAcc}    Selecting Suppliers:${suppliersName}
    SELECT SEARCH VALUES FROM THE LIST    ${loadingAcc}

    Click Element With Log Display    //p[normalize-space()='Card in']//parent::span   Selecting CardIn Time

    Click Element With Log Display    //button[@type='submit']    Submiting the Terminal Details
    SLEEP    1s
    WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    15


CHECK AND CREATE AND NEW DRIVER
    [Documentation]    This keyword is used to create a new Driver
    [Arguments]    ${name}    ${erpid}    ${email}     ${phoneNumber}    ${status}=Personal
    SELECT FROM OPERATION HEADER    Self Customer    Self Customer
    SLEEP    3s

    #CLICK ELEMENT    //p[normalize-space()='Products']
    CLICK ON SELF CUSTOMER HEADER        Drivers
    WAIT UNTIL ELEMENT IS VISIBLE    ${driverTitle}    15
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Driver:${name}    console=yes
    ...    AND    CREATE A DRIVER    ${name}    ${erpid}    ${email}     ${phoneNumber}    ${status}
    ...    ELSE    LOG    Driver:${name} already exists    console=yes


CREATE A DRIVER
    [Arguments]    ${name}    ${erpid}    ${email}     ${phoneNumber}    ${status}
    [Documentation]    This keyword is used for creating new Driver on self customer
    

    WAIT UNTIL ELEMENT IS VISIBLE    ${driverBtn}    15
    CLICK ELEMENT    ${driverBtn}
    WAIT UNTIL ELEMENT IS VISIBLE    ${addriverHeader}    10
        
    Input Text With Log Display    //input[@name='name']    ${name}    Entering the Customer Name:${name}
    
    Input Text With Log Display    //input[@name='erpId']    ${erpid}    Entering the Customer erp_id:${erpid}
   
    Input Text With Log Display    //input[@name='email']    ${email}    Entering the email:${email}

    Input Text With Log Display    //input[@name='phoneNumbersAttributes.0.value']    ${phoneNumber}    Entering the number:${phoneNumber}
    
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${status}    Selecting Satatus:${status}
    SELECT SEARCH VALUES FROM THE LIST    ${status}

    Click Element With Log Display    //p[normalize-space()="PRIMARY ?"]//parent::span    Primary check box

    Click Element With Log Display    //button[@type='submit']    Submiting the Driver Details
    SLEEP    1s
    WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    15


CHECK AND CREATE AND NEW SHIPTO
    [Documentation]    This keyword is used to create a new Shipto
    [Arguments]    ${name}    ${address}    ${lat}    ${long}    ${erpID}    ${PO_number}     ${hub}    ${fees}=${EMPTY}    ${radius}=200       
    SELECT FROM OPERATION HEADER    Self Customer    Self Customer
    SLEEP    3s

    CLICK ON SELF CUSTOMER HEADER    ShipTos    
    WAIT UNTIL ELEMENT IS VISIBLE    ${shipToTitle}    15
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new ShipTo:${name}    console=yes
    ...    AND    CREATE A SHIPTO    ${name}    ${address}    ${lat}    ${long}    ${erpID}    ${PO_number}     ${hub}    ${fees}    ${radius}       
    ...    ELSE    LOG    SHIPTO:${name} already exists    console=yes


CREATE A SHIPTO
    [Arguments]    ${name}    ${address}    ${lat}    ${long}    ${erpID}    ${PO_number}     ${hub}    ${fees}    ${radius}
    [Documentation]    This keyword is used for creating new Shipto on self customer
    WAIT UNTIL ELEMENT IS VISIBLE    ${shipToBtn}    15
    CLICK ELEMENT    ${shipToBtn}
    WAIT UNTIL ELEMENT IS VISIBLE    ${shipToHeader}    10
    Input Text With Log Display    //input[@name='name']    ${name}    Entering SHIPTO Name

    Input Text With Log Display   //input[@name='erpId']    ${erpID}    Entering erp_id for Shipto
 
    Input Text With Log Display   //input[@name='poNumber']    ${PO_number}    Entering PO_number for SHipTOp

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${address}    Entering address
    SELECT SEARCH VALUES FROM THE LIST    ${address}

    Input Text With Log Display    name=siteAttributes.lat    ${lat}    Entering Latitude
    Input Text With Log Display    siteAttributes.lng   ${long}    Entering Longtitude
    
    Input Text With Log Display    name=siteAttributes.radius    ${radius}    Entering Terminal Radius

    # Input Text With Log Display    (//div/input[contains(@role,'combobox')])[3]    ${hub}    Selecting Hub
    # SELECT SEARCH VALUES FROM THE LIST    ${hub}

    Click Element With Log Display    //button[@type='submit']    Submiting the Shipto Details
    Sleep    1s
    WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    15

CHECK AND CREATE AND NEW ASSET
    [Documentation]    This keyword is used to create a new Asset in Self Customer
    [Arguments]    ${assetType}    ${name}    ${licenseNum}    ${shipTo}    ${productCategory}    ${useInDelivery}=Yes    ${erpID}=${EMPTY}       
    SELECT FROM OPERATION HEADER    Self Customer    Self Customer
    SLEEP    3s

    CLICK ON SELF CUSTOMER HEADER    Assets
    WAIT UNTIL ELEMENT IS VISIBLE    ${assetTitle}    15
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new Asset:${name}    console=yes
    ...    AND    CREATE A ASSET    ${assetType}    ${name}    ${licenseNum}    ${shipTo}    ${productCategory}    ${useInDelivery}    ${erpID}=${EMPTY}       
    ...    ELSE    LOG    ASSET:${name} already exists    console=yes


CREATE A ASSET 
    [Arguments]    ${assetType}    ${name}    ${licenseNum}    ${shipTo}    ${productCategory}    ${useInDelivery}    ${erpID}=${EMPTY}
    [Documentation]    This keyword is used for creating new Asset on self customer
    WAIT UNTIL ELEMENT IS VISIBLE    ${assetBtn}    15
    CLICK ELEMENT    ${assetBtn}
    WAIT UNTIL ELEMENT IS VISIBLE    ${assetHeader}    10
    SLEEP    3s
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[1]    ${assetType}    Selecting AssetType:
    SELECT SEARCH VALUES FROM THE LIST    ${assetType}

    Input Text With Log Display    //input[@name='name']    ${name}    Entering Asset Name

    ##Input Text With Log Display   //input[@name='erpId']    ${erpID}    Entering erp_id for Shipto
 
    Input Text With Log Display   //input[@name='licensePlateNumber']    ${licenseNum}    Entering License Number for Asset
    
    CLEAR ELEMENT TEXT    (//div/input[contains(@role,'combobox')])[2]
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${shipTo}    Selecting ShipTo for Created Asset
    SELECT SEARCH VALUES FROM THE LIST    ${shipTo}

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[3]    ${productCategory}    Selecting ShipTo
    SELECT SEARCH VALUES FROM THE LIST    ${productCategory}
    Run Keyword If    '${useInDelivery}'=='Yes'    RUN KEYWORDS
    ...    LOG    Using the Asset on Delivery    console=yes
    ...    AND    Click Element With Log Display    //p[normalize-space()="USE IN DELIVERY"]//parent::span    Check box::"USE IN DELIVERY"

    Click Element With Log Display    //button[@type='submit']    Submiting the Asset Details
    SLEEP    1s
    WAIT UNTIL ELEMENT IS VISIBLE    //div[contains(@col-id,'name') and normalize-space()='${name}']    15

CHECK AND CREATE AND NEW USER
    [Documentation]    This keyword is used to create a new User
    [Arguments]    ${name}    ${phone}    ${email}    ${address}    ${status}    ${roles}=${EMPTY}
    SELECT FROM OPERATION HEADER    Self Customer    Self Customer
    SLEEP    3s
    #CLICK ELEMENT    //p[normalize-space()='Products']
    CLICK ON SELF CUSTOMER HEADER        Users
    WAIT UNTIL ELEMENT IS VISIBLE    ${userTitle}    15
    SEARCH FROM TABLE    ${name}
    SLEEP    2s
    ${count}    GET ELEMENT COUNT    //div[contains(@col-id,'name') and normalize-space()='${name}']
    Run Keyword If    ${count}==0    RUN KEYWORDS
    ...    LOG    Creating new User:${name}    console=yes
    ...    AND    CREATE A USER    ${name}    ${phone}    ${email}    ${address}    ${status}    ${roles}
    ...    ELSE    LOG    User:${name} already exists    console=yes

CREATE A USER
    [Documentation]    This is KW used for creating new User
    [Arguments]    ${name}    ${phone}    ${email}    ${address}    ${status}    ${roles}
    WAIT UNTIL ELEMENT IS VISIBLE    ${userBtn}    15
    CLICK ELEMENT    ${userBtn} 
    WAIT UNTIL ELEMENT IS VISIBLE    ${addUserHeader}    10

    Input Text With Log Display    //input[@name='name']    ${name}    Entering User Name: ${name}

    Input Text With Log Display    //input[@name='phone']    ${phone}    Entering User phoneNumber: ${phone}

    Input Text With Log Display    //input[@name='email']    ${email}    Entering User email: ${email}
    SLEEP    1s

    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[1]    ${address}    Entering address
    SELECT SEARCH VALUES FROM THE LIST    ${address}
    SLEEP    1s
    Input Text With Log Display    (//div/input[contains(@role,'combobox')])[2]    ${status}    Entering status
    SELECT SEARCH VALUES FROM THE LIST    ${status}

    SLEEP    2s
    Run Keyword If    '${roles}'!='${EMPTY}'    RUN KEYWORDS
    ...    LOG    Clicking on the desired roles    console=yes
    ...    AND    Click Element With Log Display    //span[normalize-space()="${roles}"]/parent::label/span[1]    Check box::"${roles}"
    
    SLEEP    1s
    Click Element With Log Display    //button[@type='submit']    Submiting the User Details
    
    WAIT UNTIL ELEMENT IS VISIBLE    //h2[contains(@class,'chakra-heading') and text()='Self Customer']    10