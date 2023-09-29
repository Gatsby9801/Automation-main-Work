*** Settings ***
Library    AppiumLibrary


Documentation    Delivery Order Execution on Mobile app.
...
##Resource    ../PageObject.robot

*** Variables ***
#${goForDeliveryBtn}    //android.view.ViewGroup[contains(@resource-id,"stroke-btn")]
${goForDeliveryBtn}     //android.widget.TextView[@text='Start Delivery']
${arrivedAtCustomer}    //android.view.ViewGroup[contains(@resource-id,"arrive")]


*** Keywords ***
DELIVERY ORDER EXECUTION
    [Documentation]    This keyword is used for delivery Order execution on Mobile App (driver app)
    [Arguments]    ${cutomerName}    ${tankType}
    SLEEP    2s
    
    LOG    Clicking on the customer Name:${cutomerName} from the list    console=yes
    WAIT AND CLICK DRIVER APP ELEMENT    xpath=//android.widget.TextView[contains(@text,'${cutomerName}')]
    
    SLEEP    3s
    ${status}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    ${goForDeliveryBtn}
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    LOG    Clicking on Go for Delivery    console=yes
    ...    AND    WAIT AND CLICK DRIVER APP ELEMENT    ${goForDeliveryBtn}
    
    SLEEP    3s
    ${status}    RUN KEYWORD AND RETURN STATUS    PAGE SHOULD CONTAIN ELEMENT    ${arrivedAtCustomer}
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    LOG    Clicking on Go for Arrived at Customer    console=yes
    ...    AND    WAIT AND CLICK DRIVER APP ELEMENT    ${arrivedAtCustomer} 

   
    # LOG    Clicking on Button: I've arrived   console=yes
    # WAIT AND CLICK DRIVER APP ELEMENT    //android.widget.Button[@text="I'VE ARRIVED"]

    # LOG    Clicking on "Start Delivery"    console=yes
    # WAIT AND CLICK DRIVER APP ELEMENT     //android.widget.TextView[@text="Start Delivery"]

    SELECT ASSET AND INPUT GALLON VALUES    ${tankType}


    # LOG    Clicking Truck type:${tankType}   console=yes
    # WAIT AND CLICK DRIVER APP ELEMENT     //android.widget.TextView[contains(@text,"${tankType}")]
    
    # LOG    Selecting Product Type:Regular Diesel    console=yes
    # WAIT AND CLICK DRIVER APP ELEMENT    //android.widget.TextView[@text='Regular Diesel']
    
    # WAIT UNTIL ELEMENT IS VISIBLE   (//android.widget.EditText[contains(@resource-id,"text-input")])[2]    6
    # INPUT TEXT    (//android.widget.EditText[contains(@resource-id,"text-input")])[2]    1200
    # CLICK ELEMENT    //android.widget.TextView[@text='Submit']
    # SLEEP    2s

    WAIT AND CLICK DRIVER APP ELEMENT    //android.widget.TextView[@text='Mark Customer as Complete']
    ###    WAIT AND CLICK DRIVER APP ELEMENT    //android.widget.TextView[@text='Finalize all delivery details']

    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    //android.widget.EditText[@text='Optional']    5
    AppiumLibrary.INPUT TEXT    //android.widget.EditText[@text='Optional']    This is a test note from Automation
    
    WAIT AND CLICK DRIVER APP ELEMENT    //android.widget.TextView[@text='Certify & Submit']
    
   
WAIT AND CLICK DRIVER APP ELEMENT
    [Documentation]    Wait for a given element and Click Them.
    [Arguments]    ${GivenXpath}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE     ${GivenXpath}    5
    AppiumLibrary.CLICK ELEMENT    ${GivenXpath}

# CHECK AND NAVIGATE APP PAGE
#     [Documentation]    check for element and click next
#     [Arguments]    ${buttonText}

    

SELECT ASSET AND INPUT GALLON VALUES
    [Arguments]    ${tankType}    ${gallonValues}=1200   
    [Documentation]    Selects Assets and input gallon values
    LOG    Clicking Truck type:${tankType}   console=yes
    WAIT AND CLICK DRIVER APP ELEMENT     //android.widget.TextView[contains(@text,"${tankType}")]
    ### This will require for multiple order
    # LOG    Selecting Product Type:DEF    console=yes
    # WAIT AND CLICK DRIVER APP ELEMENT    //android.widget.TextView[@text='DEF']
    # SLEEP    3s
    WAIT UNTIL ELEMENT IS VISIBLE    //*[@resource-id='compartment-0']   12
    INPUT TEXT    //*[@resource-id='compartment-0']   ${gallonValues}
    CLICK ELEMENT    //android.widget.TextView[@text='Submit']
    SLEEP    2s


 #//*[@resource-id='compartment-0']