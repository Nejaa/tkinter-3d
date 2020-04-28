from builders.matrixBuilders import build_look_at_matrix, build_point_at_matrix
from custom_math.vector3d import Vector3D
from geometry.camera import Camera, ProjectionType
from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class WorldTransformStep(PipelineStep):
    def __init__(self, camera: Camera):
        super().__init__()
        self.step_name = "World Transform"
        self.camera = camera

    def process_scene(self, scene: Scene):
        scene.build_global_positions()

        if self.camera.projection_type is not ProjectionType.RealPerspective:
            world_transform_matrix = build_look_at_matrix(
                position=self.camera.position,
                target=self.camera.position + self.camera.globalBearing,
                up=self.camera.up
            )

            for entity in scene.entities():
                mesh = entity.geometry
                for vertex in mesh.vertices:
                    screenPos = world_transform_matrix @ vertex.to_matrix()
                    vertex.move_to(Vector3D(x=screenPos[0][0], y=screenPos[1][0], z=screenPos[2][0]))
                    vertex.w = screenPos[3][0]
