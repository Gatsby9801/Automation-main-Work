*** Settings ***
Library    AppiumLibrary
Documentation    Pre shift appActivities on mobile Application.
...
##Resource    ../PageObject.robot


*** Variables ***
${todaysShift}    //android.view.View[@text="Today's Shift"]
${preShiftBtn}    //android.widget.TextView[@text="Pre-Shift Activities"]
${startShiftText}    //*[@text='You are about to start your shift for the day']
${shartShiftBtn}    //*[@resource-id='start-shift']
${selectVehicleHeader}    //android.view.View[@text='Select Vehicle']
${selectTruck}    xpath=//android.widget.TextView[@text='Truck']
${selectTrailer1}    //android.widget.TextView[@text='Trailer 1']
${lookGood}    //android.widget.TextView[@text='Looks Good']
${shiftStartedText}    //android.widget.TextView[@text="You cannot edit this screen because you have already started your tasks"]
${backBtn}    //android.widget.Button[@content-desc=" , back"]/android.widget.ImageView

*** Keywords ***

START SHIFT AND SELECT VEHICLE
    [Documentation]    Start shift on the mobile app.
    ...    Provide fullname for The truck and Trailer to be selected from the list
    [Arguments]    ${truckFullName}    ${trailer}=${EMPTY}
    ##Log    Clicking pre-shift button    console=yes
    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${todaysShift}    10
    SLEEP    2s
    ${preshiftText}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT    ${preShiftBtn}
    RUN KEYWORD IF    '${preshiftText}'=='True'    RUN KEYWORDS
    ...    LOG    Clicking Shift start button    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT   ${preShiftBtn} 
    ...    AND    START SHIFT AND SELECT VEHICLE IF AVAILABLE    ${truckFullName}    ${trailer}
    ...    ELSE   RUN KEYWORD    LOG    No Shft to start    console=yes

    # SLEEP    2s
    # ${status}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT    ${startShiftText}
    # RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    # ...    Log    Starting shift    console=yes
    # # ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${preShiftBtn}    15
    # # ...    AND    AppiumLibrary.CLICK ELEMENT      ${preShiftBtn}
    # ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${startShiftText}    5
    # ...    AND    AppiumLibrary.CLICK ELEMENT    ${shartShiftBtn}
    
    # SLEEP    2s
    # ${shftStart}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT    ${shiftStartedText}
    # LOG    shiftstatedText:${shftStart}    console=yes
    # RUN KEYWORD IF    '${shftStart}'=='False'    RUN KEYWORDS
    # ...    SELECT TRUCK AND TRAILERS FROM DRIVER APP    ${truckFullName}    ${trailer}
    # ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT   ${selectVehicleHeader}    5
    # ...    AND    AppiumLibrary.CLICK ELEMENT    ${lookGood}
    # ...    AND    LOG    Shift Started with truck:${TruckFullName} 
    # ...    ELSE    RUN KEYWORDS   
    # ...    LOG    Shift alredy started    console=yes
    # ...    AND    AppiumLibrary.CLICK ELEMENT    ${backBtn}
    # ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${preShiftBtn}    10

SELECT TRUCK AND TRAILERS FROM DRIVER APP
    [Documentation]    select truck and trailer.
    [Arguments]    ${truckFullName}    ${trailer}
    SLEEP   3s
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${selectVehicleHeader}    5
    ${inventoryText}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT    //android.widget.TextView[@text="Verify and update starting inventory detail"]
    LOG    inventoryText:${inventoryText}    console=yes
    RUN KEYWORD IF    '${inventoryText}'=='False'    RUN KEYWORDS
    ...    LOG    Selecting Truck: ${truckFullName}     console=yes
    ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${selectTruck}    5
    ...    AND    AppiumLibrary.CLICK ELEMENT    ${selectTruck}
    ...    AND    DRIVER APP:SEARCH AND SELECT TRUCKS/TRAILERS    ${truckFullName}
    #...    AND    AppiumLibrary.CLICK ELEMENT    (//android.widget.TextView[@text='Clear All'])[1]
    ...    ELSE    RUN KEYWORD  
    ...    LOG    Vehicle already selected    console=yes
    # ...    AND    AppiumLibrary.CLICK ELEMENT    ${backBtn}
    # ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${preShiftBtn}    5
    
    RUN KEYWORD IF    '${trailer}'!='${EMPTY}'    RUN KEYWORDS
    ...    LOG    Selecting Truck: ${Trailer}     console=yes
    ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT   ${selectTrailer1}    5
    ...    AND    SLEEP    2s
    ...    AND    AppiumLibrary.CLICK ELEMENT    ${selectTrailer1} 
    ...    AND    DRIVER APP:SEARCH AND SELECT TRUCKS/TRAILERS    ${Trailer} 
    ...    AND    SLEEP    2s
     

DRIVER APP:SEARCH AND SELECT TRUCKS/TRAILERS
    [Documentation]    Serach and select truck and trailer from the listConvert
    [Arguments]    ${truckName} 
    LOG    Searching and selecting:${truckName}     console=yes
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   //android.widget.TextView[@text='Select an Asset']    10
    ${searchAsset}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT    //android.widget.EditText[@text='Search For Assets'] | //android.widget.EditText[@resource-id,'search']
    RUN KEYWORD IF    '${searchAsset}'=='True'    RUN KEYWORDS
    ...    LOG    Searching and selecting Asset    console=yes
    ...    AND    AppiumLibrary.INPUT TEXT    //android.widget.EditText[@text='Search For Assets'] | //android.widget.EditText[@resource-id,'search']    ${truckName} 
    ...    AND    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[contains(@text,'${truckName}')]
    ...    ELSE    RUN KEYWORDS
    ...    LOG    Selecting Asset form the list    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[contains(@text,'${truckName}')]


START SHIFT AND SELECT VEHICLE IF AVAILABLE
    [Documentation]    Start shift and select vehilce if exist on the timeline
    [Arguments]    ${truckFullName}    ${trailer}
    SLEEP    3s
    ${status}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT    ${startShiftText}
    RUN KEYWORD IF    '${status}'=='True'    RUN KEYWORDS
    ...    Log    Starting shift    console=yes
    # ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${preShiftBtn}    15
    # ...    AND    AppiumLibrary.CLICK ELEMENT      ${preShiftBtn}
    ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${startShiftText}    5
    ...    AND    AppiumLibrary.CLICK ELEMENT    ${shartShiftBtn}

    SLEEP    3s
    ${shftStart}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT    ${shiftStartedText}
    LOG    shiftstatedText:${shftStart}    console=yes
    RUN KEYWORD IF    '${shftStart}'=='False'    RUN KEYWORDS
    ...    SELECT TRUCK AND TRAILERS FROM DRIVER APP    ${truckFullName}    ${trailer}
    ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT   ${selectVehicleHeader}    5
    ...    AND    LOG    Clicking looks good    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    ${lookGood}
    ...    AND    LOG    Shift Started with truck:${TruckFullName} 
    ...    ELSE    RUN KEYWORDS   
    ...    LOG    Shift already started    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    ${backBtn}
    ...    AND    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${preShiftBtn}    10
