from behave import given, when, then

def activate_train(context):
    context.train.active = True
    context.train.main_key_position = "off"

@given('a train is active')
@when('the train is active')
def step_given_train_active(context):
    if not context.train.active:
        activate_train(context)

@given('a driver is in [{cab}]')
@given('the driver is in [{cab}]')
@given('driver is in [{cab}]')
def step_given_driver_in_cab(context, cab):
    if cab.lower() not in context.train.cabs:
        raise ValueError(f"Cab {cab} is not valid. Available cabs are: {context.train.cabs}")
    context.train.driver_cab = cab

@given('the main key in position [{position}]')
def step_given_main_key_position(context, position):
    context.main_key_position = position
    print(context)

@when('the driver presses the [{button}] button')
def step_when_driver_presses_button(context, button):
    context.button_pressed = button

@then('the horn should sound for [{seconds}] seconds')
def step_then_horn_sounds(context, seconds):
    context.horn_duration = int(seconds)
    assert context.horn_duration == 5, f"Expected horn to sound for 5 seconds, but got {context.horn_duration}"
    print(f"Horn sounded for {context.horn_duration} seconds from {context.train.driver_cab}.")
