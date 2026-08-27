# core/fsm/state_machine.py
import time
import logging
from .state import State
from .context import SharedContext
from core.capture.screen_grabber import ScreenGrabber
from core.capture.preprocessor import ImagePreprocessor
from core.detection import Detector, Classifier, PostProcessor, ModelLoader
from core.tracking import TargetTracker, MouseController, TrajectoryPredictor
from core.combat import CombatTrigger, SkillSelector, CombatMonitor
from core.resource import BallCounter, GemRoute, ShopRoute, ResourceManager

logger = logging.getLogger(__name__)

class StateMachine:
    def __init__(self, config: dict, ctx: SharedContext):
        self.config = config
        self.ctx = ctx
        self.state = State.IDLE

        # Initialize components
        self.grabber = ScreenGrabber(config['capture'].get('region'))
        self.preprocessor = ImagePreprocessor()
        model_loader = ModelLoader(config['model']['detection'],
                                   config['model']['classifier'],
                                   config['model']['device'])
        self.detector = Detector(model_loader, config['model']['conf_threshold'])
        self.classifier = Classifier(model_loader)
        self.post_processor = PostProcessor(config['priority'])
        self.tracker = TargetTracker()
        self.mouse = MouseController(config['capture']['aim_smoothness'])
        self.predictor = TrajectoryPredictor()
        self.combat_trigger = CombatTrigger(self.mouse)
        self.skill_selector = SkillSelector(self.mouse, config['combat']['auto_skill_index'])
        self.combat_monitor = CombatMonitor(self.grabber)
        self.ball_counter = BallCounter(self.grabber)
        self.gem_route = GemRoute(self.mouse, {})  # load from map_coords
        self.shop_route = ShopRoute(self.mouse, {})
        self.resource_manager = ResourceManager(self.ball_counter, self.gem_route, self.shop_route,
                                                config['resource']['min_balls'])

    def start(self):
        self.ctx.is_running = True
        self.state = State.SEARCHING
        self._run()

    def stop(self):
        self.ctx.is_running = False
        self.state = State.PAUSE

    def _run(self):
        while self.ctx.is_running:
            if self.state == State.SEARCHING:
                self._do_search()
            elif self.state == State.TRACKING:
                self._do_tracking()
            elif self.state == State.THROWING:
                self._do_throw()
            elif self.state == State.COMBAT:
                self._do_combat()
            elif self.state == State.COLLECTING_GEM:
                self._do_collect_gem()
            elif self.state == State.BUYING_BALLS:
                self._do_buy_balls()
            elif self.state == State.PAUSE:
                time.sleep(0.2)
            else:
                time.sleep(0.1)

    def _do_search(self):
        img = self.grabber.capture()
        processed = self.preprocessor.preprocess(img)
        detections = self.detector.detect(processed)
        # Classify each detection
        classified = []
        for box in detections:
            crop = self._crop_image(img, box.xyxy[0])
            label = self.classifier.classify(crop)
            classified.append((box.xyxy[0], label, box.conf[0]))
        target_box = self.post_processor.select_target(classified)
        if target_box is not None:
            self.ctx.set_target(target_box, label)
            self.state = State.TRACKING
        else:
            # Check ball count
            if self.ball_counter.get_count() < self.config['resource']['min_balls']:
                self.state = State.COLLECTING_GEM
            time.sleep(0.05)

    def _do_tracking(self):
        # Update tracker with current target position
        # Simulate: move mouse towards target
        center = self._box_center(self.ctx.current_target_box)
        predicted = self.predictor.predict()
        self.mouse.move_to(predicted[0], predicted[1], 0.05)
        # If target is close enough, start throwing
        self.state = State.THROWING

    def _do_throw(self):
        # Simulate throw: hold and release
        hold_time = self.config['capture']['hold_time_min']
        self.mouse.hold_and_release(hold_time)
        # After throw, wait for result, then back to SEARCHING
        time.sleep(1)
        self.state = State.SEARCHING

    def _do_combat(self):
        self.combat_trigger.start_combat()
        self.skill_selector.use_skill()
        self.combat_monitor.wait_for_combat_end()
        self.state = State.SEARCHING

    def _do_collect_gem(self):
        self.gem_route.collect_gem()
        self.state = State.BUYING_BALLS

    def _do_buy_balls(self):
        self.shop_route.buy_balls(self.config['resource']['shop_route']['buy_quantity'])
        self.state = State.SEARCHING

    @staticmethod
    def _box_center(box):
        x1, y1, x2, y2 = box
        return ((x1+x2)//2, (y1+y2)//2)

    @staticmethod
    def _crop_image(img, box):
        x1,y1,x2,y2 = map(int, box)
        return img[y1:y2, x1:x2]
