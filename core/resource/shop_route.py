# core/resource/shop_route.py
from core.tracking.mouse_controller import MouseController
import time

class ShopRoute:
    """
    Navigate to Annie's shop and buy advanced Gulu Balls.
    """
    def __init__(self, mouse: MouseController, map_coords: dict):
        self.mouse = mouse
        self.coords = map_coords.get("annie_shop", {})

    def buy_balls(self, quantity=50):
        # Open map, select Annie Shop, interact, buy
        self.mouse.move_to(self.coords.get("world_map", (200,200)))
        self.mouse.click()
        time.sleep(1)
        self.mouse.move_to(self.coords.get("shop_icon", (800,500)))
        self.mouse.click()
        time.sleep(1)
        self.mouse.move_to(self.coords.get("buy_button", (1000,700)))
        self.mouse.click()
        # Set quantity (simplified)
        time.sleep(0.5)
        self.mouse.move_to(self.coords.get("confirm", (1100,800)))
        self.mouse.click()
        time.sleep(1)
