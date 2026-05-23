Feature: Travel Insurance End-To-End Booking Flow

  Background: Navigate to Insurance Matrix Landing Screen
    Given the user opens the corporate travel portal application homepage
    And the user dismisses initial overlay login alerts if present
    When the user navigates into the Travel Insurance matrix panel page

  # =========================================================================
  # END-TO-END DATA-DRIVEN SUBMISSIONS (HAPPY PATH)
  # =========================================================================
  @e2e @test2
  Scenario Outline: Complete full end-to-end valid submission up to verification
    When the user loads test metrics from row "<Row_Index>" inside CSV file "data/insurance.csv"
    And the system fully automates the valid profile registration stream pipeline
    Then the user profile should clear forms safely with authentication panels triggered

    Examples:
      | Row_Index |
      | 1         |