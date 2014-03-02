Feature: Labour messages
  As a volunteer worker
  I need to be informed about working in the event

  As a workforce manager
  I want to keep the workforce posted

  @backend
  Scenario: Receiving a thank you note after signing up
    Given I am a person
    And there is an event that is accepting applications
    And the event has a message that is to be sent to all applicants

    When I sign up for the event
    Then I should receive the message

  @backend
  Scenario: Receiving a notice upon being accepted
    Given I am a person
    And there is an event that is accepting applications
    And the event has a message that is to be sent to all accepted workers

    When I sign up for the event
    And the workforce manager approves my application
    Then I should receive the message

  @backend
  Scenario: A message is sent to all applicants
    Given I am a person
    And there is an event that is accepting applications
    And I am signed up to the event

    When a message is added that should be sent to all applicants
    Then I should receive the message

  @backend
  Scenario: A message is sent to all accepted workers
    Given I am a person
    And there is an event that is accepting applications
    And I am signed up to the event
    And my application has been accepted

    When a message is added that should be sent to all accepted workers
    Then I should receive the message
