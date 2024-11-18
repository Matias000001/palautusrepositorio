*** Settings ***
Library    SeleniumLibrary
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Create User   valid_username    valid_password
    Input Text    id=username    valid_username
    Input Text    id=password_confirmation    valid_password
    Click Button  register_button

Register With Too Short Username And Valid Password
    Create User   short_username    valid_password
    Input Text    id=username    short_username
    Input Text    id=password_confirmation    valid_password
    Click Button  register_button

Register With Valid Username And Too Short Password
    Create User   valid_username    short_password
    Input Text    id=username    valid_username
    Input Text    id=password_confirmation    short_password
    Click Button  register_button

Register With Valid Username And Invalid Password
    Create User   valid_username    invalid_password
    Input Text    id=username    valid_username
    Input Text    id=password_confirmation    invalid_password
    Click Button  register_button

Register With Nonmatching Password And Password Confirmation
    Create User   valid_username    valid_password
    Input Text    id=username    valid_username
    Input Text    id=password    valid_password
    Input Text    id=password_confirmation    different_password
    Click Button  register_button

Register With Username That Is Already In Use
    Create User   existing_username    valid_password
    Input Text    id=username    existing_username
    Input Text    id=password_confirmation    valid_password
    Click Button  register_button

Login After Successful Registration
    Create User    valid_username    valid_password
    Input Text     id=username    new_user
    Input Text     id=password    new_password
    Click Button   login_button

Login After Failed Registration
    Create User    invalid_user    valid_password
    Input Text     id=username    short
    Input Text     id=password_confirmation    valid_password
    Click Button   register_button
    Input Text     id=username    short
    Input Text     id=password    valid_password
    Click Button   login_button

*** Keywords ***

Reset Application Create User And Go To Register Page
    Reset Application
    Create User    valid_username    valid_password
    Go To Register Page

Go To Register Page
    SeleniumLibrary.Go To    ${REGISTER_URL}
