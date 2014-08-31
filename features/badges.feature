Feature: Badges and entry lists
    As a badge helper
    I want to print badges for event workers

    Scenario: Badges are created for workers
        Given I am a person
        And there is an event that is accepting applications
        And the event has badge types

        When I sign up for the event
        And the workforce manager approves my application
        Then I should have a badge of the correct type

    Scenario: Badges are created for lecturers
        Given there is an event that has the programme functionality enabled
        And the event has badge types
        And there is a programme

        # XXX THIS SHOULD NOT PASS
        Then the programme host should have a badge of the correct type