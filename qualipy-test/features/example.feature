# -- FILE: features/example.feature
Feature: Showing off behave

  Background: Load test data
    Given that the Employee data is loaded
    And that the Task data is loaded
    And that the JSON data is loaded
    And that the YAML data is loaded
    And that the XML data is loaded
    And that the Excel data is loaded
    And that the Custom data is loaded

  @TES-1
  Scenario: Run a simple test
    Given we have behave installed
     When we implement 5 tests
     Then behave will test them for us!

  @TES-2
  Scenario: Run a simple test
    Given we have behave installed
     When we implement 5 tests
     Then behave will test them for us!

  Scenario: Check loaded data
    Given that the Employee data is loaded
    Then Employee.bob_id will be 4
    And Employee.alice_id will be 9