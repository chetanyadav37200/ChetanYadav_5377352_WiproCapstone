Feature: Travel Insurance Form Validations and Booking

  Background: Navigate to Insurance Matrix Landing Screen
    Given the user opens the corporate travel portal application homepage
    And the user dismisses initial overlay login alerts if present
    When the user navigates into the Travel Insurance matrix panel page

  # =========================================================================
  # POSITIVE PRESENTATION CHECKPOINTS
  # =========================================================================
  @positive @test1
  Scenario: Validate plan grids and international insurance branding layouts
    Then the choice of insurance plan grid matrix structure must load successfully
    And the visibility of international travel and medical insurance policy headers must be confirmed

  # =========================================================================
  # NEGATIVE TESTING CHECKPOINTS (SEPARATED EXAMPLES FOR SINGLE ROW RUNS)
  # =========================================================================
  @negative
  Scenario Outline: Validate traveler details form validation logic errors
    When the user configures the flow map targeting destination country "<Country>"
    And the user configures traveler volume parameters for "<Travellers>" rows
    And the user executes plan searches and clicks buy now on plan card position "<plan_index>"
    And the user attempts info validation using name <name>, dob <dob>, gender <gender>, mobile <mobile>, and email <email>
    Then the system field tracking validation engine must surface the error "<expected_error>" for field type "<Error_Type>"

    @row1
    Examples: John Doe - Blank DOB
      | Country | Travellers | plan_index | name     | dob | gender | mobile     | email         | expected_error                   | Error_Type |
      | UAE     | 1          | 1          | John Doe |     | Male   | 9876543210 | john@test.com | Please enter valid Date of Birth | DOB        |

    @row2
    Examples: Jane Smith - Blank Mobile
      | Country | Travellers | plan_index | name       | dob      | gender | mobile | email         | expected_error             | Error_Type |
      | UAE     | 1          | 2          | Jane Smith | 15081995 | Female |        | jane@test.com | Please enter mobile number | MOBILE     |

    @row3
    Examples: Alex Wilson - Invalid Mobile
      | Country | Travellers | plan_index | name        | dob      | gender | mobile | email         | expected_error                | Error_Type |
      | UAE     | 1          | 1          | Alex Wilson | 22111992 | Male   | 12345  | alex@test.com | Please enter valid Mobile No. | MOBILE     |

  # =========================================================================
  # END-TO-END FUNCTIONAL CHECKPOINTS (NO CSV DEPENDENCY)
  # =========================================================================
  @e2e @test2
  Scenario: Complete full end-to-end valid submission up to verification
    When the user processes the following valid customer registration profile:
      | Country | Travellers | plan_index | name         | dob      | gender | mobile     | email             |
      | UAE     | 1          | 1          | Suneet Kumar | 12121998 | Male   | 9876543210 | suneet@test.com   |
    And the system fully automates the valid profile registration stream pipeline
    Then the user profile should clear forms safely with authentication panels triggered