Feature: Driver Controls

Scenario Outline: Driver controls the train
    In order to ensure the driver can control the train

    Background:
        Given a train is active 
        And driver is in [<cab>]
        
    Examples:
        | cab   |
        | cab A |
        | cab B |

    Scenario: Test the horn functionality
        Given the main key in position [occupied] 
        When the driver presses the [horn] button
        Then the horn should sound for [5] seconds
