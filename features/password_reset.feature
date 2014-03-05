Feature: Resetting a forgotten password
    As a user
    I am sometimes forgetful
    But it should not stop me from using Turska

    @backend
    Scenario: Resetting a forgotten password
        Given I am a person
        And I have forgotten my password

        When I view the login page
        And request a password reset
        Then I should receive a password reset message

        When I click the link in the password reset message
        And set up a new password
        Then my password should have been changed
