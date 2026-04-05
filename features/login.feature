# login.feature
# Practice Test Automation Login Scenarios
# URL: https://practicetestautomation.com/practice-test-login/

Feature: User Login Functionality
  As a registered user
  I want to log in to the application
  So that I can access the dashboard

  Background:
    Given the user is on the login page

  @smoke @positive
  Scenario: Successful login with valid credentials
    When the user enters username "student" and password "Password123"
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the dashboard should display a success message

  @negative
  Scenario: Login fails with invalid username
    When the user enters username "wrongUser" and password "Password123"
    And the user clicks the login button
    Then an error message should be displayed
    And the error message should contain "Your username is invalid!"

  @negative
  Scenario: Login fails with invalid password
    When the user enters username "student" and password "wrongPass"
    And the user clicks the login button
    Then an error message should be displayed
    And the error message should contain "Your password is invalid!"

  @smoke @logout
  Scenario: User can log out after successful login
    When the user enters username "student" and password "Password123"
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    When the user clicks the logout button
    Then the user should be redirected back to the login page
