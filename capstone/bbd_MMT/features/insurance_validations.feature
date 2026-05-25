Feature: Travel Insurance Form Validations and Layout Checkpoints

  Background: Navigate to Insurance Matrix Landing Screen
    Given the user opens the corporate travel portal application homepage
    And the user dismisses initial overlay login alerts if present
    And the user navigates into the Travel Insurance matrix panel page

  # =========================================================================
  # POSITIVE PRESENTATION CHECKPOINTS
  # =========================================================================
  @positive @test_pos_1
  Scenario Outline: Validate plan grids UI matrix presentation layer loading
    When the user loads test metrics from row "<Row_Index>" inside CSV file "data/insurance.csv"
    And the user configures the flow map targeting destination country from data
    And the user configures traveler volume parameters from data
    And the user clicks the explore plans button to execute searches
    Then the choice of insurance plan grid matrix structure must load successfully

    Examples:
      | Row_Index |
      | 1         |

  @positive @test_pos_2
  Scenario Outline: Validate presence of international travel and medical insurance branding
    When the user loads test metrics from row "<Row_Index>" inside CSV file "data/insurance.csv"
    And the user configures the flow map targeting destination country from data
    And the user configures traveler volume parameters from data
    Then the visibility of international travel and medical insurance policy headers must be confirmed

    Examples:
      | Row_Index |
      | 1         |

  @positive @test_pos_3
  Scenario Outline: Verify transition to checkout page and user profile info form view
    When the user loads test metrics from row "<Row_Index>" inside CSV file "data/insurance.csv"
    And the user configures the flow map targeting destination country from data
    And the user configures traveler volume parameters from data
    And the user executes plan searches and clicks buy now on plan card from data
    Then the traveler contact form layout layer view visibility should be confirmed

    Examples:
      | Row_Index |
      | 1         |

  @positive @test_pos_4
  Scenario Outline: Verify successful end-to-end form submission with valid profile metrics
    When the user loads test metrics from row "<Row_Index>" inside CSV file "data/insurance.csv"
    And the user configures the flow map targeting destination country from data
    And the user configures traveler volume parameters from data
    And the user executes plan searches and clicks buy now on plan card from data
    And the user injects valid profile fields from loaded data mapping
    Then the authentication intercept overlay login screen should be displayed without form errors

    Examples:
      | Row_Index |
      | 1         |

  # =========================================================================
  # NEGATIVE TESTING CHECKPOINTS (DATA-DRIVEN VALIDATION LOGIC)
  # =========================================================================
  @negative
  Scenario Outline: Validate traveler details form validation logic errors
    When the user loads test metrics from row "<Row_Index>" inside CSV file "data/insurance.csv"
    And the user configures the flow map targeting destination country from data
    And the user configures traveler volume parameters from data
    And the user executes plan searches and clicks buy now on plan card from data
    And the user attempts context dynamic info validations on fields
    Then the system field tracking validation engine must surface the expected error from data

    Examples:
      | Row_Index |
      | 2         |
      | 3         |
      | 4         |