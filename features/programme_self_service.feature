Feature: Inputting programme details as self service
    As the Programme Manager
    In order to reduce mine own workload
    I would like the programme organizers to input details about their programme themselves

    @backend
    Scenario: The Programme Manager creates a new programme and sends the edit code
        Given there is an event that has the programme functionality enabled
        When I create a new programme
        And I send the edit code to the programme host
        Then the programme host receives the edit code via e-mail

    @fullstack
    Scenario: Editing a programme via an edit code
        Given there is an event that has the programme functionality enabled
        And there is a programme
        And its edit code has been sent to the programme host

        When the programme host receives the edit code via e-mail
        And clicks the link in the message
        Then they should see the self-service editing page for the email

        When the programme host edits the details of the programme
        And submits the changes to the programme
        Then the changes to the programme should have been saved
