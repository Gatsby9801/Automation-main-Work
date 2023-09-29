*** Settings ***
Library    String
Library    SeleniumLibrary
Library    OperatingSystem
Library    ../../Keywords/GetSeleniumInstances.py
##Resource    PageObject.robot

*** Variable ***
${BROWSER}    chrome
${platfrom}    Windows 10
${submitBtn}    name=commit

${dashboradTitle}   //a/div[text()='Dashboard'] | //a[text()='Dashboard']
${remoteUrl}    https://oauth-dev-99498:9ae49ffe-437a-4697-9a1c-53d7fe974088@ondemand.eu-central-1.saucelabs.com:443/wd/hub    

@{_tmp} 
    ...  browserName: ${BROWSER},
    ...  platform: ${platfrom},
    ...  version: latest,
    # ...  username: %{SAUCE_USERNAME},
    # ...  accessKey: %{SAUCE_ACCESS_KEY},
    ...  Screen Resolution: '2560x1600',
    ...  name: ${SUITE_NAME},
    ...  build: Fleetpanda Automation

${capabilities}     ${EMPTY.join(${_tmp})} 
${remote_url}       ${remoteUrl}

*** Keywords ***
Open My Browser
    [Arguments]    ${url}   ${browserName}=chrome
    [Documentation]    Opens browser
    
    ##Append To Environment Variable  PATH    ${EXECDIR}${/}Driver${/}
    # ${testPath}    set Variable    ${EXECDIR}${/}Driver${/}
    # Log    path:${testPath}    console=yes
    ${chrome_options}=     Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    
    ${prefs}    Create Dictionary    download.default_directory    ${EXECDIR}${/}Downloads${/}    plugins.always_open_pdf_externally    ${TRUE}
    Log    ${prefs}
    ${val}=    Call Method    ${chrome options}    add_experimental_option    prefs    ${prefs}
   
    Call Method    ${chrome_options}    add_argument    --ignore-certificate-errors
    Call Method    ${chrome_options}    add_argument    --disable-extensions
    Call Method    ${chrome_options}    add_argument    --disable-gpu
    Call Method    ${chrome_options}    add_argument    --no-sandbox  
    ${options}     Call Method     ${chrome_options}   to_capabilities
    ##Open Browser    browser=${browserName}    desired_capabilities=${options}  
    ##CREATE WEBDRIVER    Chrome    desired_capabilities=${options}    executable_path=${EXECDIR}${/}Driver${/}chromedriver
    ###Open Browser    browser=chrome    remote_url=${remoteUrl}    desired_capabilities=${capabilities}
    Open Browser    ${url}    chrome    remote_url=${remoteUrl}    desired_capabilities=${capabilities}
 
    ###Set Window Size    1920    1080
    Maximize Browser Window

Open Browser To Login Page1
    [Documentation]    Opens browser for Login
    [Arguments]    ${LOGIN URL}
    Open Browser    ${LOGIN URL}    ${BROWSER}    alias=BrowserA

Input Username
    [Arguments]    ${username}
    SeleniumLibrary.Input Text    name=user[email]    ${username}

Input Pass
    [Arguments]    ${password}
    SeleniumLibrary.Input Text    name=user[password]    ${password}

Close Browsers
    Close All Browsers

LOGIN TO APPLICATION
    [Documentation]     Login to application
    [Arguments]    ${loginUrl}   ${usernName}   ${password}
    OPEN MY BROWSER     ${loginUrl}
    GO TO   ${loginUrl}
    INPUT USERNAME  ${usernName}
    INPUT PASS  ${password}
    SeleniumLibrary.Click Button    ${submitBtn}

    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE   ${dashboradTitle}   15
    LOG    LOGIN SUCESSFULL    console=yes
