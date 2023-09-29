*** Settings ***
Library    AppiumLibrary
Documentation    Transfer Order Execution on Mobile app.
Resource    PreShiftActivities.robot
Resource    ../Create Order/CreateOrder.robot

*** Variables ***
${hamburgurMenu}    //android.view.ViewGroup[contains(@resource-id,'menu')]
${recordFuelTransferBtn}    xpath=//android.view.ViewGroup[contains(@resource-id,'Record Fuel Transfer')]
${fromTruck}    //android.view.ViewGroup[contains(@resource-id,'fromTruck')]
${toTruck}    //android.view.ViewGroup[contains(@resource-id,'toTruck')]
${fromComp1}    //*[contains(@resource-id,'fromComp_0')]
${toComp1}    //*[contains(@resource-id,'toComp_0')]
${noteInput}    //android.widget.EditText[contains(@resource-id,'notes')]
${submitBtn}    //android.view.ViewGroup[contains(@resource-id,'submit')]

*** Keywords ***
SELF DISPATCH RECORD FUEL TRANSFER
    [Documentation]    Keyword is used for self dispatch transfer order execution
    [Arguments]    ${truck1}    ${truck2}    ${product}    ${gallon}    ${note}=THis is test note from Automation
    AppiumLibrary.CLICK ELEMENT    ${hamburgurMenu}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${recordFuelTransferBtn}    5
    AppiumLibrary.CLICK ELEMENT    ${recordFuelTransferBtn}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[contains(@text,"DAY OF TRANSFER")]    5
    SLEEP    2s
    LOG    Selecting From Truck    console=yes
    AppiumLibrary.CLICK ELEMENT    ${fromTruck}
    DRIVER APP:SEARCH AND SELECT TRUCKS/TRAILERS    ${truck1}
    SLEEP    2s
    
    LOG    Selecting to Truck    console=yes
    AppiumLibrary.CLICK ELEMENT    ${toTruck}
    DRIVER APP:SEARCH AND SELECT TRUCKS/TRAILERS    ${truck2}

    SLEEP    2s
    LOG    Selecting From Compartment    console=yes
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${fromComp1}    10 
    AppiumLibrary.CLICK ELEMENT    ${fromComp1}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[@text,"Select a Compartment"]    5
    AppiumLibrary.CLICK ELEMENT    //android.view.ViewGroup[contains(@resource-id,"default-Comp 1")]
    SLEEP    2s

    LOG    Selecting to Compartment    console=yes
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${toComp1}    10
    AppiumLibrary.CLICK ELEMENT    ${toComp1}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[@text,"Select a Compartment"]    5
    AppiumLibrary.CLICK ELEMENT    //android.view.ViewGroup[contains(@resource-id,"default-Comp 1")]
    SLEEP    2s

    LOG    Entering Product:${product}    console=yes
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //*[contains(@resource-id,'transferProd_0')]    5  
    AppiumLibrary.CLICK ELEMENT   //*[contains(@resource-id,'transferProd_0')]
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.TextView[@text='Select a Product']    5
    AppiumLibrary.CLICK ELEMENT   //android.widget.TextView[contains(@text,'${product}')]
    SLEEP    2s
    LOG    Entering Gallon values    console=yes
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //android.widget.EditText[contains(@resource-id,'gal_0')]    10 
    AppiumLibrary.CLICK ELEMENT    //android.widget.EditText[contains(@resource-id,'gal_0')]
    AppiumLibrary.INPUT TEXT    //android.widget.EditText[contains(@resource-id,'gal_0')]    ${gallon}
    
    AppiumLibrary.PRESS KEY CODE    4
    SLEEP    2s
    LOG    Entering Notes values    console=yes
    AppiumLibrary.CLICK ELEMENT    ${noteInput}
    AppiumLibrary.INPUT TEXT    ${noteInput}    ${note}    
    
    AppiumLibrary.PRESS KEY CODE    4
    SLEEP    2s
    AppiumLibrary.CLICK ELEMENT    ${submitBtn}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${todaysShift}    10
    LOG    The trasfer order has been executed sucessfully    console=yes
