from behave import given, when, then
import re


def regex_step(pattern, contexts=['given', 'when', 'then']):
    def decorator(func):
        # Expand the pattern into multiple step definitions
        base_pattern = re.sub(r"\((.*?)\)", r"{\1}", pattern)
        
        options = re.findall(r"\((.*?)\)", pattern)
        if options:
            for option in options[0].split("|"):
                expanded_pattern = base_pattern.replace(f"{{{options[0]}}}", option.strip())
                expanded_pattern = expanded_pattern.strip()
                expanded_pattern = expanded_pattern.replace(" {", " (")
                expanded_pattern = expanded_pattern.replace("} ", ") ")
                
                
                if expanded_pattern.find("|") != -1:
                    print(f'passing step with additional pattern: {expanded_pattern}')

                    regex_step(expanded_pattern.strip(), contexts)(func)
                else:
                    print(f"Registering step with context: @{contexts} '{expanded_pattern}'")            
                        
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

@regex_step('(a|the|) driver is in [{cab}]')
def step_given_driver_in_cab(context, cab):
    if cab.lower() not in context.train.cabs:
        raise ValueError(f"Cab {cab} is not valid. Available cabs are: {context.train.cabs}")
    context.train.driver_cab = cab

@regex_step('(a|the|) main key in position [{position}]', contexts=['given', 'when'])
def step_given_main_key_position(context, position):
    context.main_key_position = position
    print(context)

@regex_step('(a|the|) driver presses (a|the|) [{button}] button')
def step_when_driver_presses_button(context, button):
    context.button_pressed = button

@regex_step('(a|the|) horn should sound (for|) [{time}] seconds', contexts=['then'])
def step_then_horn_sounds(context, time):
    context.horn_duration = int(time)
    assert context.horn_duration == 5, f"Expected horn to sound for 5 seconds, but got {context.horn_duration}"
    print(f"Horn sounded for {context.horn_duration} seconds from {context.train.driver_cab}.")
