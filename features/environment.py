
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Train:
    active: bool = False
    order: int = 0
    length: int = 0
    speed: int = 0
    driver_cab: str = ""
    main_key_position: str = "off"
    cabs: List[str] = field(default_factory=list)
    buttons: List[str] = field(default_factory=list)
    last_button_pressed: str = ""
    horn_duration: int = 0



def before_scenario(context, scenario):
    # Add your setup logic here
    print(f"Before scenario: {scenario.name}")
    context.train = Train()
    context.train.cabs = ["cab a", "cab b"]
    context.train.buttons = ["horn", "brake", "accelerate"]
    context.train.order = 1
    context.train.length = 1
