class Options:
    def __init__(self):
        self.debug = False
        self.__draw_fps = True
        self.tickRate = 200
        self.refreshRate = 120
        self.width = 1200
        self.height = 1000
        self.originOffset = 1000
        self.cross_hair_scale = 10
        self.global_movement = False

    @property
    def tick_delay(self):
        return int(1000 / self.tickRate)

    @property
    def refresh_delay(self):
        return int(1000 / self.refreshRate)

    @property
    def draw_fps(self):
        return self.__draw_fps or self.debug

    @draw_fps.setter
    def draw_fps(self, draw_fps: bool):
        self.__draw_fps = draw_fps


options = Options()
