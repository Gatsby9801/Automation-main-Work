*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem


Documentation    POST shift appActivities on mobile Application.
Resource    PageObject_DriverApp.robot

*** Variables ***
${postShiftBtn}    //android.widget.TextView[@text="Post-Shift Activities"]
${areYouSure}    //android.widget.TextView[@text="Are you sure?"]
${continue}    //android.widget.TextView[@text='Continue']
${orderSkip}    //android.widget.TextView[@text='Some orders are skipped']  
${skipNote}    //android.widget.EditText[contains(@text,'Note is Required')]  
${sendBcktoDispatch}    //android.widget.TextView[@text='Send back to Dispatch'] 
${certifyAndSubmit}    //android.widget.TextView[@text='Certify & Submit']  


*** Keywords ***

END SHIFT AND POST ACTIVITIES
    [Documentation]    Post shift Activities and ending shift   
    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${postShiftBtn}    5
    AppiumLibrary.CLICK ELEMENT      ${postShiftBtn}
    SLEEP    5s
    ${AreYouSure}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${areYouSure}    
    RUN KEYWORD IF    '${AreYouSure}'=='True'    RUN KEYWORDS
    ...    LOG    Selecting back or Continue    console=yes
    ...    AND    WAIT AND CLICK DRIVER APP ELEMENT    ${continue} 
    WAIT AND CLICK DRIVER APP ELEMENT    ${certifyAndSubmit}  
    SLEEP    5s
    ${skipOrder}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${orderSkip}    
    RUN KEYWORD IF    '${skipOrder}'=='True'    RUN KEYWORDS
    ...    LOG    Skipping Order    console=yes
    ...    AND    AppiumLibrary.INPUT TEXT    ${skipNote}    Automation: Will complete in another truck  
    ...    AND    LOG    Ending shift on another truck    console=yes   
    ...    AND    AppiumLibrary.CLICK ELEMENT    ${sendBcktoDispatch}   
    ...    AND    LOG    Completing the Shift    console=yes
    ##...    AND    WAIT AND CLICK DRIVER APP ELEMENT    ${certifyAndSubmit}           
    



