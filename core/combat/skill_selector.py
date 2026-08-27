# core/combat/skill_selector.py
from core.tracking.mouse_controller import MouseController
import time

class SkillSelector:
    """
    Choose a skill to use during combat.
    """
    def __init__(self, mouse: MouseController, skill_index=0):
        self.mouse = mouse
        self.skill_index = skill_index  # 0-based

    def use_skill(self):
        # Click skill button (dummy coordinate)
        skill_x = 500 + self.skill_index * 100
        self.mouse.move_to(skill_x, 900)
        self.mouse.click()
        time.sleep(0.8)
