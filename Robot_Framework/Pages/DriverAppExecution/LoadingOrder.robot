*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem
#Suite Setup    Set Library Search Order    SeleniumLibrary    AppiumLibrary

Documentation    Loading Order Execution on Mobile app.
...
##Resource    ../PageObject.robot

*** Variables ***
${goForLoadingBtn}    //android.view.ViewGroup[contains(@resource-id,"fill-btn")] 
${arrivedAtTerminal}    //android.view.ViewGroup[contains(@resource-id,"arrive")]  
${doneLoading}    //android.view.ViewGroup[contains(@resource-id,"done-load")]
${bolNumber}    //android.widget.EditText[contains(@resource-id,"bol-number")]
${totalGross}    //android.widget.EditText[contains(@resource-id,'total-gross')]
${compZero}    //android.widget.EditText[contains(@resource-id,"comp-0")]
${cameraPermission}    //android.widget.TextView[contains(@resource-id,'com.android.permissioncontroller:id/permission_message')]
${nextBtn}    //android.view.ViewGroup[contains(@resource-id,'next')]
${cameraBtn}    //android.view.ViewGroup[contains(@resource-id,'camera')]
${cardInTime}    //android.widget.EditText[contains(@resource-id,'card-in-time')]
${cardOutTime}    //android.widget.EditText[contains(@resource-id,'card-out-time')]


*** Keywords ***
LOADING ORDER EXECUTION
    [Documentation]    This keyword is used for Loading Order execution on Mobile App (driver app)
    [Arguments]    ${cutomerName}
    SLEEP    2s
    
    LOG    Clicking on the customer Name:${cutomerName} from the list    console=yes
    WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER    xpath=//android.widget.TextView[contains(@text,'${cutomerName}')]
    
    SLEEP    3s
    ${status}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    ${goForLoadingBtn}
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    LOG    Clicking on Go for Loading    console=yes
    ...    AND    WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER    ${goForLoadingBtn}
    
    SLEEP    3s
    ${status}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    ${arrivedAtTerminal}
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    LOG    Clicking on Go for Arrived at Terminal    console=yes
    ...    AND    WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER    ${arrivedAtTerminal} 

    SLEEP    3s
    ${status}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    ${doneLoading}
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    LOG    Clicking on Done Loading    console=yes
    ...    AND    WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER    ${doneLoading} 

   
WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER
    [Documentation]    Wait for a given element and Click Them.
    [Arguments]    ${GivenXpath}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     ${GivenXpath}    5
    AppiumLibrary.CLICK ELEMENT    ${GivenXpath}

ADD BOL DATA AND SUBMIT ORDER
    [Documentation]    Add BOL information on the form
    [Arguments]    ${bolId}    ${supplier}    ${product}    ${grossTotal}    ${compFirst}    ${cardIn}    ${cardOut}    ${carrier}=${EMPTY}    ${demmNote}=${EMPTY}           
    SLEEP    5s
    ${status}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    ${cameraPermission}
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    LOG    Allow Permission for camera   console=yes
    ...    AND    WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER    id=com.android.permissioncontroller:id/permission_allow_foreground_only_button 
    
    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${bolNumber}    8
    LOG    Entering BolNumber:${bolId}    console=yes
    AppiumLibrary.INPUT TEXT    ${bolNumber}    ${bolId}
    SLEEP    1s

    LOG    Entering suppliers:${supplier}   console=yes
    AppiumLibrary.CLICK ELEMENT   //android.view.ViewGroup[contains(@resource-id,"supplier")]
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[@text='Select a Supplier']    5
    DRIVER APP:SEARCH AND SELECT VALUES    ${supplier}
    
    SLEEP    1s
    LOG    Entering Product:${product}    console=yes
    AppiumLibrary.CLICK ELEMENT   //android.view.ViewGroup[contains(@resource-id,"select-product")]
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[@text='Select a Product']    5
    AppiumLibrary.CLICK ELEMENT   //android.widget.TextView[contains(@text,'${product}')]

    SLEEP    1s
    LOG    Entering Gross Value:${grossTotal}    console=yes
    AppiumLibrary.INPUT TEXT    ${totalGross}    ${grossTotal}
    
    SLEEP    1s
    LOG    Entering first Compartment:${compFirst}   console=yes
    AppiumLibrary.INPUT TEXT    ${compZero}    ${compFirst}
    SLEEP    2s
    ${invalidCOm}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    //android.widget.TextView[contains(@text,'Incorrect Compartment')]
    ##LOG    Invalid Comp:${invalidCOm}    console=yes
    Run Keyword If     '${invalidCOm}'=='True'    RUN Keywords
    ...    LOG    The Compartment have invalid products but we will load it anyways!!!    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT   //android.view.ViewGroup[contains(@resource-id,"success-btn")]
    ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${compZero}    10
    ...    AND    AppiumLibrary.CLEAR TEXT    ${compZero}
    ...    AND    AppiumLibrary.INPUT TEXT    ${compZero}    ${compFirst}
        

    SLEEP    1s
    LOG    Uploading Image from the list    console=yes
    AppiumLibrary.CLICK ELEMENT    //android.view.ViewGroup[contains(@resource-id,"camera-btn")]
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[contains(@text,"Take a Photo")]    5
    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[contains(@text,"Take a Photo")]
    SLEEP    5s
    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    //android.view.View[contains(@resource-id,"com.fuelpanda.staging:id/texture_view")]    5
    AppiumLibrary.CLICK ELEMENT    ${cameraBtn}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[@text='Ok']    5
    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[@text='Ok']    
    SLEEP    8s
    LOG    Entering Card in time:${cardIn}    console=yes
    AppiumLibrary.CLICK ELEMENT     ${cardInTime}
    AppiumLibrary.CLEAR TEXT    ${cardInTime}
    AppiumLibrary.INPUT TEXT    ${cardInTime}    ${cardIn}
    SLEEP    1s

    LOG    Entering Card out time:${cardOut}    console=yes
    AppiumLibrary.CLICK ELEMENT     ${cardOutTime}
    AppiumLibrary.INPUT TEXT    ${cardOutTime}    ${cardOut}
    SLEEP    1s
    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[contains(@text,'Card In time')]
    SLEEP    1s
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${nextBtn}    5
    
    AppiumLibrary.CLICK ELEMENT    ${nextBtn}
    
    ADD DEMURRAGE NOTE    ${demmNote}

DRIVER APP:SEARCH AND SELECT VALUES
    [Documentation]    Serach and select truck and trailer from the listConvert
    [Arguments]    ${value} 
    LOG    Searching and selecting:${Value}     console=yes
    ${searchBox}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    //android.widget.EditText[@text='Search']
    Run Keyword If   '${searchBox}'=='True'    RUN KEYWORDS
    ...    LOG    Searcing and selecting VALUES    console=yes
    ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   //android.widget.EditText[@text='Search']    5
    ...    AND    AppiumLibrary.INPUT TEXT    //android.widget.EditText[@text='Search']    ${Value}
    ...    AND    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[contains(@text,'${value}
    ...  ELSE    RUN KEYWORDS
    ...  LOG    Selecting VALUES    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[contains(@text,'${value}')]


ADD DEMURRAGE NOTE
    [Documentation]    Add a demurrage Note
    [Arguments]    ${note}    ${addNote}=NO
    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    //android.widget.TextView[@text="Was there any delay?"]    7
    RUN KEYWORD IF    '${addNote}'=='YES'    RUN KEYWORDS
    ...    LOG    Adding demurrage Notes    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    //android.view.ViewGroup[contains(@resource-id,'delay-yes')] 
    ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.EditText[contains(@resource-id,'delay-reason')]    2
    ...    AND    LOG    Entering demurrage message:${note}    console=yes
    ...    AND    AppiumLibrary.INPUT TEXT    //android.widget.EditText[contains(@resource-id,'delay-reason')]    ${note}
    ...    ELSE    RUN KEYWORDS
    ...    LOG    CLicking "NO" on demurrage Notes    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    //android.view.ViewGroup[contains(@resource-id,'delay-no')]

EXECUTE SCHEDULED TRANSFER ORDER
    [Documentation]    Execute Transfer Order
    SLEEP    2s
    LOG    Clicking on the Transfer from the list    console=yes
    WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER    xpath=//android.widget.TextView[contains(@text,'Transfer Order')]
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[@text='Record Fuel Transfer']    5
    WAIT AND CLICK DRIVER APP ELEMENT IN LOADING ORDER    //android.widget.TextView[@text='Submit']