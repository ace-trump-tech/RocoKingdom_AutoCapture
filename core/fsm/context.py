# core/fsm/context.py
class SharedContext:
    """
    Holds global data accessible by all modules.
    """
    def __init__(self, config: dict):
        self.config = config
        self.current_target_box = None
        self.target_type = None   # 'shiny', 'polluted', 'normal'
        self.balls_remaining = 99
        self.is_running = False
        self.current_map = "unknown"

    def update_balls(self, count: int):
        self.balls_remaining = count

    def set_target(self, box, typ):
        self.current_target_box = box
        self.target_type = typ
