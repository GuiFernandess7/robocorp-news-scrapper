*** Settings ***
Library    OperatingSystem
Library    Collections

*** Variables ***
${SEARCH_PHRASE}    ${SEARCH_PHRASE}
${CATEGORY}         ${CATEGORY}
${MONTHS}           ${MONTHS}

*** Tasks ***
Process News
    Set Environment Variable    SEARCH_PHRASE    ${SEARCH_PHRASE}
    Set Environment Variable    CATEGORY    ${CATEGORY}
    Set Environment Variable    MONTHS    ${MONTHS}
