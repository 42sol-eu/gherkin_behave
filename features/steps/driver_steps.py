from behave import given, when, then


from behave import given
import re

def regex_step(contexts, pattern):
    def decorator(func):
        # Expand the pattern into multiple step definitions
        base_pattern = re.sub(r"\((.*?)\)", r"{\1}", pattern)
        options = re.findall(r"\((.*?)\)", pattern)
        if options:
            for option in options[0].split("|"):
                expanded_pattern = base_pattern.replace(f"{{{options[0]}}}", option.strip())
                print(f'Registering step with pattern: {expanded_pattern}')

                for context in contexts:
                    match context:
                        case "given":
                            given(expanded_pattern.strip())(func)
                        case "when":
                            when(expanded_pattern.strip())(func)
                        case "then":
                            then(expanded_pattern.strip())(func)
                        case _:
                            raise ValueError(f"Unknown context: {context}")
        else:
            for context in contexts:
                    match context:
                        case "given":
                            given(pattern.strip())(func)
                        case "when":
                            when(pattern.strip())(func)
                        case "then":
                            then(pattern.strip())(func)
                        case _:
                            raise ValueError(f"Unknown context: {context}")
        return func
    return decorator


def activate_train(context):
    context.train.active = True
    context.train.main_key_position = "off"

@given('a train is active')
@when('the train is active')
def step_given_train_active(context):
    if not context.train.active:
        activate_train(context)

@regex_step(['given', 'then'], '(a|the|) driver is in [{cab}]')
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
