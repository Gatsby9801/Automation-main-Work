*** Settings ***
Library    String
Library    SeleniumLibrary
Resource    ../../Keywords/FleetPandaKWs.robot

*** Variables ***
${scheduleTranferBtn}    //button[normalize-space()='Schedule A Transfer'] | //button[text()='Schedule A Transfer']
${scheduleFuelTransferHeaderText}    //div[@role='heading' and text()='Schedule Fuel Transfer']
${selectDriverPlaceholder}    //div[contains(@class,'select__placeholder') and text()='Select Driver']//parent::div//input
${submitBtn}    //button[@type='submit'] 
    


*** Keywords ***
SCHEDULE A FUEL TRANSFER 
    [Documentation]    SCHEDULE A FUEL TRANSFER
    [Arguments]    ${fromAsset}    ${toAsset}    ${fuleType}    ${fromComp}    ${toComp}    ${gallons}    ${driver}=${EMPTY}    
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${scheduleTranferBtn}    30
    SeleniumLibrary.CLICK BUTTON    ${scheduleTranferBtn}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${scheduleFuelTransferHeaderText}    10
    SLEEP    2s
    LOG    Selecting Truck:${fromAsset} from Asset list    console=yes
    CLICK INPUT BOX WITH CUSTOM HEADER    NewTransferOrderAssetFrom
    SeleniumLibrary.INPUT TEXT    //label[@for='NewTransferOrderAssetFrom']//parent::div//input    ${fromAsset}
    SELECT SEARCH VALUES FROM THE LIST    ${fromAsset}

    LOG    Selecting Truck:${toAsset} from Asset list    console=yes
    CLICK INPUT BOX WITH CUSTOM HEADER    NewTransferOrderAssetTo
    SeleniumLibrary.INPUT TEXT    //label[@for='NewTransferOrderAssetTo']//parent::div//input    ${toAsset} 
    SELECT SEARCH VALUES FROM THE LIST    ${toAsset}

    LOG    Selecting Fuel type: ${fuleType}    console=yes
    CLICK INPUT BOX WITH CUSTOM HEADER    NewTransferOrderProduct
    SeleniumLibrary.INPUT TEXT    //label[@for='NewTransferOrderProduct']//parent::div//input    ${fuleType}
    SELECT SEARCH VALUES FROM THE LIST    ${fuleType}

    LOG    Selecting from compartment:${fromComp}    console=yes
    CLICK INPUT BOX WITH CUSTOM HEADER    NewTransferOrderCompartmentFrom
    SeleniumLibrary.INPUT TEXT    //label[@for='NewTransferOrderCompartmentFrom']//parent::div//input    ${fromComp}
    SELECT SEARCH VALUES FROM THE LIST    ${fromComp}

    LOG    Selecting To compartment:${toComp}    console=yes
    CLICK INPUT BOX WITH CUSTOM HEADER    NewTransferOrderCompartmentTo
    SeleniumLibrary.INPUT TEXT    //label[@for='NewTransferOrderCompartmentTo']//parent::div//input    ${toComp}
    SELECT SEARCH VALUES FROM THE LIST    ${toComp}
    
    LOG    Inputting gallons:${gallons}     console=yes
    SeleniumLibrary.INPUT TEXT    //label[@for='NewTransferOrderVolume']//parent::div//input    ${gallons} 

    LOG    Inputting Transfer Instruction    console=yes
    SeleniumLibrary.INPUT TEXT    //textarea[@id='NewTransferOrderNotes']    This is transfer Instruction from Automation

    RUN KEYWORD IF    '${driver}'!='${EMPTY}'    RUN KEYWORDS
    ...    LOG    SELECTING DRIVER:${driver}    console=yes
    ...    AND    SeleniumLibrary.CLICK ELEMENT    ${selectDriverPlaceholder}
    ...    AND    SeleniumLibrary.INPUT TEXT    ${selectDriverPlaceholder}    ${driver}
    ...    AND    SELECT SEARCH VALUES FROM THE LIST   ${driver}

    SLEEP    2s

    SeleniumLibrary.CLICK BUTTON    //button[@type='submit'] 
    LOG    FUEL TRANSFER SCHDULED AND ASSIGNED SUCESSFULLY    console=yes



CLICK INPUT BOX WITH CUSTOM HEADER
    [Documentation]    Select input box with given header "for" element identifier while inspecting elements
    [Arguments]    ${headerFor}
    LOG    Selecting the input box with given title    console=yes
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //label[@for='${headerFor}']//parent::div//input    10
    SeleniumLibrary.CLICK ELEMENT    //label[@for='${headerFor}']//parent::div//input 
