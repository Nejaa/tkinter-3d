class Options:
    def __init__(self):
        self.debug = True
        self.draw_fps = True
        self.tickRate = 150
        self.refreshRate = 60
        self.width = 800
        self.height = 600
        self.originOffset = 1000

    @property
    def tick_delay(self):
        return int(1000 / self.tickRate)

    @property
    def refresh_delay(self):
        return int(1000 / self.refreshRate)

    @property
    def draw_fps(self):
        return self.__draw_fps | self.debug

    @draw_fps.setter
    def draw_fps(self, draw_fps: bool):
        self.__draw_fps = draw_fps


options = Options()
