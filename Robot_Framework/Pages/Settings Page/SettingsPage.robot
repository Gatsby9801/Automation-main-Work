*** Settings ***
Documentation    Settings Page resources
Library    SeleniumLibrary
Resource    ../PageObject.robot


*** Variables ***
${siteBtn}  //span[normalize-space()='Sites']
${featureBtn}    //span[normalize-space()='Features']
${companyBtn}    //span[normalize-space()='Company']
${saasBtn}    //span[normalize-space()='Saas']
${settingsBtn}    //span[@aria-label='Settings'] | //i[@class='fas fa-cog'] | //a[@href='/settings']

*** Keywords ***
FEATURE FLAG ENABLE
    [Documentation]    Go to Settings and Enable the given FEATURE FLAG
    [Arguments]    ${featureFlagId}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${settingsBtn}    8
    WAIT UNTIL KEYWORD SUCCEEDS    1 min    5 s    SeleniumLibrary.CLICK ELEMENT    ${settingsBtn}

    ${element_present} =    SeleniumLibrary.Element Should Be Visible    id=${featureFlagId}
    ${is_selected} =    Run Keyword And Return Status    Checkbox Should Be Selected    id=${featureFlagId}

    Run Keyword If    not ${is_selected}
    ...    SeleniumLibrary.Click Element    id=${featureFlagId}
    Click Element With Log Display    //input[@name='commit']    Submit Button



SELECT TIME ZONE FROM SETTING
    [Documentation]    Select timezone from the list
    [Arguments]    ${timeZone}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${settingsBtn}    8
    SeleniumLibrary.CLICK ELEMENT    ${settingsBtn}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${companyBtn}    10
    Click Element With Log Display    ${companyBtn}    Company Button on Settings
    Click Element With Log Display    name=settings[timezone]    Selecting timezone
    Click Element With Log Display    //select[@id='settings_timezone']/option[text()="${timeZone}"]    Selecting Timezone:${timeZone}    
    SLEEP    3s
    Click Element With Log Display    //input[@name='commit']    Submit Button


SELECT START SHIFT OPTION
    [Documentation]    Select start shift options from settings page
    [Arguments]    ${option}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${settingsBtn}    8
    WAIT UNTIL KEYWORD SUCCEEDS    1 min    5 s    SeleniumLibrary.CLICK ELEMENT    ${settingsBtn}
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    ${saasBtn}    10
    Click Element With Log Display    ${saasBtn}    Saas Options on Settings
    LOG    waiting and clicking: ${option}    console=yes
    SeleniumLibrary.WAIT UNTIL ELEMENT IS VISIBLE    //div[@class='input-group']//option[@value='${option}']    5
    DOUBLE CLICK ELEMENT    //div[@class='input-group']//option[@value='${option}']
    SLEEP    1s
    Click Element With Log Display    //input[@name='commit']    Submit Button


    