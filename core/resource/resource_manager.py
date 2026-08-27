# core/resource/resource_manager.py
from .ball_counter import BallCounter
from .gem_route import GemRoute
from .shop_route import ShopRoute

class ResourceManager:
    """
    Orchestrate gem collection and ball purchase when low.
    """
    def __init__(self, ball_counter: BallCounter, gem_route: GemRoute, shop_route: ShopRoute, min_balls=10):
        self.ball_counter = ball_counter
        self.gem_route = gem_route
        self.shop_route = shop_route
        self.min_balls = min_balls

    def ensure_sufficient_balls(self) -> bool:
        count = self.ball_counter.get_count()
        if count >= self.min_balls:
            return True
        # Not enough: go collect gem, then buy balls
        self.gem_route.collect_gem()
        self.shop_route.buy_balls()
        # Verify again
        return self.ball_counter.get_count() >= self.min_balls
