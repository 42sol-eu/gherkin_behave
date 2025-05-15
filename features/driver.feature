Feature: Driver Controls
    In order to ensure the driver can control the train

    Background:
        Given a train is active 
        And the driver is in [cab A]
        
    Scenario: Test the horn functionality
        Given the main key in position [occupied] 
        When the driver presses the [horn] button
        Then the horn should sound for [5] seconds
