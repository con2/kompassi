Feature: Signing up for an event
  As a prospective volunteer worker
  I want to sign up for volunteer work in an event

  @fullstack
  Scenario: Signing up for an event
    Given there is an event that is open for applications
    And I am logged in

    When I move to sign up for an event
    And I fill in the requested extra details

    Then I should be signed up for the event

  @fullstack
  Scenario: Signing up for an event while not logged in
    Given there is an event that is open for applications
    And I am not yet logged in

    When I move to sign up for an event
    Then I should see the login page

    When I log in
    And I fill in the requested extra details

    Then I should be signed up for the event