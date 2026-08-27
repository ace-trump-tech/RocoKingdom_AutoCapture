# core/resource/gem_route.py
from core.tracking.mouse_controller import MouseController
import time

class GemRoute:
    """
    Navigate to 'Gem Source' to collect Locke coins.
    """
    def __init__(self, mouse: MouseController, map_coords: dict):
        self.mouse = mouse
        self.coords = map_coords.get("gem_source", {})

    def collect_gem(self):
        # Click minimap -> select gem source -> talk to NPC -> claim
        self.mouse.move_to(self.coords.get("minimap", (100,100)))
        self.mouse.click()
        time.sleep(1)
        self.mouse.move_to(self.coords.get("npc", (500,400)))
        self.mouse.click()
        time.sleep(0.5)
        self.mouse.move_to(self.coords.get("claim_button", (600,500)))
        self.mouse.click()
        time.sleep(1)
