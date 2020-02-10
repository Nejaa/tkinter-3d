from typing import List

from rendering.pipeline_step import PipelineStep


class EmptySteps(Exception):
    def __init__(self):
        super().__init__()


class Pipeline:
    def __init__(self, steps: List[PipelineStep]):
        if len(steps) == 0:
            raise EmptySteps()
        self.steps = steps

        for idx in range(len(steps)):
            if idx == 0:
                self.input_queue = steps[0].input_queue
            else:
                steps[idx - 1].output_queue = steps[idx].input_queue
