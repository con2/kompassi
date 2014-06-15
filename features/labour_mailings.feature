Feature: Labour messages
  As a volunteer worker
  I need to be informed about working in the event

  As a workforce manager
  I want to keep the workforce posted

  Background:
    Given I am a person
    And there is an event that is accepting applications

  @backend
  Scenario: Receiving a thank you note after signing up
    Given the event has a message that is to be sent to all applicants

    When I sign up for the event
    Then I should receive the message

  @backend
  Scenario: Receiving a notice upon being accepted
    Given the event has a message that is to be sent to all accepted workers

    When I sign up for the event
    And the workforce manager approves my application
    Then I should receive the message

  @backend
  Scenario: Receiving shifts in an email
    Given the event has a message that is to be sent to all workers with finished shifts

    When I sign up for the event
    And the workforce manager approves my application
    And the workforce manager assigns me to shifts
    
    Then I should receive the message
    And the message should include my shifts

  @backend
  Scenario: A message is sent to all applicants
    Given I am signed up to the event

    When a message is added that should be sent to all applicants
    Then I should receive the message

  @backend
  Scenario: A message is sent to all accepted workers
    Given I am signed up to the event
    And my application has been accepted

    When a message is added that should be sent to all accepted workers
    Then I should receive the message

  @backend
  Scenario: A message is sent to all rejected workers
    Given I am signed up to the event
    And my application has been rejected

    When a message is added that should be sent to all rejected workers
    Then I should receive the message