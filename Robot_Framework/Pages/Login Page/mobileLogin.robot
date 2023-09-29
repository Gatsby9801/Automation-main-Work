*** Settings ***
Library    AppiumLibrary
#Library    XML
Library    SeleniumLibrary
Library    GetSeleniumInstances
Library    OperatingSystem

Documentation    A test suite with single login test
...
...    This test has a workflow that is cread using keywords in
...    the imported resource file
##Resource    ../PageObject.robot

*** Variables ***
${BROWSER}    chrome
${ANDROID_AUTOMATION_NAME}    UIAutomator2
${ANDROID_APP}    ${EXECDIR}${/}APK${/}app-staging-release.apk
${ANDROID_PLATFORM_NAME}    Android
${ANDROID_PLATFORM_VERSION}   %{ANDROID_PLATFORM_VERSION=11}
${signinButton}    //*[@resource-id='signin']
${continueBtn}    //*[@resource-id='phone-verify']
${logInBtn}    //*[@resource-id='login']
${locationAccessPopup}    //android.widget.TextView[@text="Location Access"]
${bluetoothAccessPopup}    //android.widget.TextView[contains(@resource-id,"com.android.permissioncontroller:id/permission_message")]
${allowBTpermssion}    //android.widget.Button[contains(@resource-id,"com.android.permissioncontroller:id/permission_allow_button")]
${locatnPermHeader}    id=com.android.permissioncontroller:id/permission_message
${whileUsingAppBtn}    id=com.android.permissioncontroller:id/permission_allow_foreground_only_button
${backButton}     //android.widget.ImageButton[@content-desc="Back"]
${remoteURl}    https://oauth-dev-99498:9ae49ffe-437a-4697-9a1c-53d7fe974088@ondemand.eu-central-1.saucelabs.com:443/wd/hub
${otaText}    //android.widget.TextView[@text="Restart the app to install the changes?"]
${downloadText}    //android.widget.TextView[contains(@text,'Downloading Updates')]

*** Keywords ***
Open Mobile Application
    [Documentation]    This keyword is used to open application.
#   Open Application  http://127.0.0.1:4723/wd/hub  automationName=${ANDROID_AUTOMATION_NAME}
#   ...  platformName=${ANDROID_PLATFORM_NAME}  platformVersion=${ANDROID_PLATFORM_VERSION}
#   ...  app=${ANDROID_APP}  appPackage=com.fuelpanda.staging  appActivity=com.fleetpanda.MainActivity
    # Open Application   http://127.0.0.1:4723/wd/hub    platformName=Android    platformVersion=12    deviceName=Android Emulator    appPackage=com.fuelpanda.staging	
    # ...    appActivity=com.fleetpanda.MainActivity    automationName=UIAutomator2    app=storage:filename=app-staging-release.apk
    Open Application   ${remoteURl}    platformName=Android    platformVersion=12    deviceName=Android GoogleAPI Emulator    appPackage=com.fuelpanda.staging	
    ...    appActivity=com.fleetpanda.MainActivity    automationName=UiAutomator2    app=storage:filename=app-staging-release.apk

CLICK ON SIGN IN BUTTON
    [Documentation]    Click on the SIGN IN button on mob app
    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    ${signinButton}    10    SignIn button is not visible
    SLEEP    5s
    ${otaDownload}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT   ${otaText} | ${downloadText}
    RUN KEYWORD IF    '${otaDownload}'=='True'  RUN KEYWORDS
    ...    LOG    Clicking Yes    console=yes
    ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   //android.widget.TextView[contains(@text,'Yes')]    10
    ...    AND    AppiumLibrary.CLICK ELEMENT    //android.widget.TextView[contains(@text,'Yes')]
    ...    AND    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${signinButton}    5

    AppiumLibrary.CLICK ELEMENT    ${signinButton}

INPUT MOBILE NUMBER AND CONTINUE
    [Documentation]    Enter mobile number in the application
    [Arguments]    ${phoneNumber}
    SLEEP    3s
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //*[@text="What's your mobile number?"]    30    Text is not visible
    LOG    Entering phone numbers:${phoneNumber}    console=yes
    AppiumLibrary.INPUT TEXT    class=android.widget.EditText     ${phoneNumber}
    SLEEP    2s
    AppiumLibrary.CLICK ELEMENT    //*[@text='Continue']

INPUT PASSWORD AND LOGIN BUTTON
    [Documentation]    Input password button
    [Arguments]    ${password}
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //*[@text='Enter Password']    30    Password input box is not displayed
    LOG    Entering password    console=yes
    AppiumLibrary.INPUT TEXT    class=android.widget.EditText     ${password}
    SLEEP    2s
    AppiumLibrary.CLICK ELEMENT    ${logInBtn} 
    SLEEP    3s
    AppiumLibrary.WAIT UNTIL PAGE CONTAINS ELEMENT    //*[@text="Today's Shift"] | //*[@text="Location Access"] | ${bluetoothAccessPopup}    15    Login Failed 

#CLOSE AUTOUPATE SUGGESTION
   # [Documentation]    CLose the app upgrade suggestion.
   # ${newUpdate}    SET VARIABLE    //[@text='New Update Available']
    #${count}     ${newUpdate}
    #Run Keyword If    ${count}>0
    ##...    CLICK ELEMENT    

ALLOW BLUETOOTH ACCESS
    [Documentation]    This keyword is Allow/deny Bluetooth access
    SLEEP    2s
    LOG    Check for Location and Allow/Deny the access    console=yes
    ${bluetoothMenu}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT   ${bluetoothAccessPopup}
    RUN KEYWORD IF    '${bluetoothMenu}'=='True'  RUN KEYWORDS
    ...    LOG    Clicking Allow BT    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    ${allowBTpermssion} 

LOCATION ACCESS CHECK
    [Documentation]    This keyword is Allow/deny location access
    SLEEP    3s
    LOG    Check for Location Menu and Allow/Deny the access    console=yes
    ${headCount}    RUN KEYWORD AND RETURN STATUS    AppiumLibrary.PAGE SHOULD CONTAIN ELEMENT   ${locationAccessPopup}
    RUN KEYWORD IF    '${headCount}'=='True'  ALLOW/DENY LOCATION ACCESS
    
ALLOW/DENY LOCATION ACCESS
    [Arguments]    ${allow}=yes 
    RUN KEYWORD IF     '${allow}'=='yes'    RUN KEYWORDS
    ...    LOG    Clicking yes to allow access    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    //*[@text="Allow"]
    ...    ELSE    RUN KEYWORDS
    ...    LOG    Clicking deny to deny access    console=yes
    ...    AND    AppiumLibrary.CLICK ELEMENT    //*[@text="Deny"]
    AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   ${locatnPermHeader}    5
    AppiumLibrary.CLICK ELEMENT    ${whileUsingAppBtn}
   ## AppiumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   ${locatnPermHeader}    15
    SLEEP    3s
    AppiumLibrary.CLICK ELEMENT    ${backButton}
    
