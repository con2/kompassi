Feature: Verifying the email address of a user
    As the system administrator
    I require all my users to have valid e-mail addresses
    Lest they bring my wrath upon them

    @backend
    Scenario: Verifying the email address upon registration
        When I register a new user account
        And I have not verified my email address
        Then I should receive an email verification message

        When I click the link in the email verification message
        Then my email address should be verified

    @backend
    Scenario: Verifying the email address upon email change
        Given I am a person
        And I change my email address
        Then I should receive an email verification message

        When I click the link in the email verification message
        Then my email address should be verified

    @fullstack
    Scenario: Email change reminder upon login
        Given I am a person
        And I have not verified my email address

        When I log in
        Then I should be reminded to verify my email address

