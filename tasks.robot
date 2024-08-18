*** Settings ***
Library    OperatingSystem
Library    Collections

*** Variables ***
${SEARCH_PHRASE}    ${SEARCH_PHRASE}
${NEWS_CATEGORY}    ${NEWS_CATEGORY}
${MONTHS}           ${MONTHS}

*** Tasks ***
Process News
    Set Environment Variable    SEARCH_PHRASE    ${SEARCH_PHRASE}
    Set Environment Variable    NEWS_CATEGORY    ${NEWS_CATEGORY}
    Set Environment Variable    MONTHS    ${MONTHS}
