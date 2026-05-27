# core/combat/combat_trigger.py
from core.tracking.mouse_controller import MouseController
import time

class CombatTrigger:
    """
    Detect and click the 'Fight' button when polluted sprite appears.
    """
    def __init__(self, mouse: MouseController, fight_button_template_path=None):
        self.mouse = mouse
        self.template = fight_button_template_path  # optional template matching

    def start_combat(self):
        # Locate fight button (simplified: fixed coordinate)
        # In real implementation: use template matching to find button
        self.mouse.move_to(1000, 800)  # dummy
        self.mouse.click()
        time.sleep(0.5)
