Feature: Separation of programme into those that are and are not visible in the schedule
  As a programme manager
  I want to publish most of the programme in the schedule
  But there are also some programmes that should not be displayed there
  And they should be shown on a separate page

  @backend
  @wip
  Scenario: Schedule- and non-schedule public programmes
    Given there is an event that has the programme functionality enabled
    When I create a new programme
    And I assign it a schedule slot
    And I publish it

    And I create another programme
    And I publish it
    But I do not assign it a schedule slot

    Then I should see the first programme in the schedule
    But I should not see the second programme in the schedule
    And I should see the second programme on the non-schedule programme page
    But I should not see the first programme on the non-schedule programme page