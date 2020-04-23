from __future__ import annotations

from datetime import timedelta
from random import random
from tkinter import Tk, Canvas, Event
import time
from timeloop import Timeloop

from geometry import geometry_options
from geometry.camera import Camera
from geometry.mesh import Mesh
from custom_math.quaternion import Quaternion
from custom_math.vector3d import Vector3D
from options import options
from rendering.collectorStep import CollectorStep
from rendering.pipeline import Pipeline
from rendering.projectionStep import ProjectionStep
from rendering.renderingStep import RenderingStep
from rendering.screenClippingStep import ScreenClippingStep
from rendering.tkinterRenderer import TkinterRenderer
from scene.entity import Entity
from scene.scene import Scene
from shape.cube import Cube
from shape.plane import Plane

geometry_options.line_thickness = 1

windowCenter = Vector3D(x=options.width / 2, y=options.height / 2, z=0)

origin = Vector3D(x=options.originOffset, y=options.originOffset, z=options.originOffset)

tk = Tk()
tk.config(cursor="none")
renderer = TkinterRenderer(tk, width=options.width, height=options.height)

m = Mesh.import_from("ressources/Cylinder.obj")
m.scale(20)
m.rotate(rotation=Quaternion.axis_angle(Vector3D(y=1), 180))
cubeSize = 20
plane = Plane(length=4, grid_size=20.0)
plane.translate(Vector3D(x=-cubeSize, y=-cubeSize, z=cubeSize))
cube = Cube(cube_size=cubeSize)
meshes = [
    cube,
    # m,
    plane,
    plane.copy().rotate(rotation=Quaternion.axis_angle(Vector3D(x=1), angle=-90)),
    plane.copy().rotate(rotation=Quaternion.axis_angle(Vector3D(y=1), angle=90)),
    # cube,
    # Cube(cube_size=cubeSize / 2, origin=Vector(y=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(y=-(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(x=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(x=-(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(z=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(z=-(cubeSize + cubeSize / 2))),
]
[m.translate(origin) for m in meshes]
entities = [Entity(geometry=m) for m in meshes]
m.translate(Vector3D(x=cubeSize * 2))

scene = Scene()
[scene.scene_root.add_entity(e) for e in entities]

rot_speed = 180 / options.tickRate  # deg/s = rot speed/tick
cube_rot_axis = Vector3D(x=random(), y=random(), z=random())
point2 = cube_rot_axis.copy() * 100
point1 = -point2
rotationSpeeds = [
    # None,
    # None,
    # None,
    # Quaternion.axis_angle(cube_rot_axis, angle=rot_speed),
    # Quaternion.axis_angle(Vector(x=1), angle=-rot_speed),
    # Quaternion.axis_angle(Vector(x=1), angle=rot_speed),
    # Quaternion.axis_angle(Vector(y=1), angle=rot_speed),
    # Quaternion.axis_angle(Vector(y=1), angle=-rot_speed),
    # Quaternion.axis_angle(Vector(z=1), angle=rot_speed),
    # Quaternion.axis_angle(Vector(z=1), angle=-rot_speed),
]

camera_origin = cube.center + Vector3D(z=-cubeSize * 4)
camera = Camera(position=camera_origin, focal_length=500, viewport_offset=windowCenter)
camera_speed = 1.5

frames = 0
fps = 0

pipeline = Pipeline(steps=[
    CollectorStep(),
    ProjectionStep(camera=camera),
    ScreenClippingStep(renderer=renderer),
    RenderingStep(renderer=renderer)
])

tl = Timeloop()


@tl.job(interval=timedelta(milliseconds=options.refresh_delay / 2))
def update_view():
    local_scene = scene.copy()
    pipeline.push_scene(scene=local_scene)


@tl.job(interval=timedelta(milliseconds=options.tick_delay))
def update_world():
    for idx, mesh in enumerate(meshes):
        if idx > len(rotationSpeeds) - 1:
            break
        if rotationSpeeds[idx] is None:
            continue
        mesh.rotate(rotation=rotationSpeeds[idx])


def move_camera(direction: Vector3D):
    def mover(_: Event):
        camera.translate(direction, options.global_movement)

    return mover


def rotate_camera(axis: Vector3D, angle: float):
    def mover(_: Event):
        camera.rotate(axis, angle)

    return mover


previous_position = None

mouse_deadzone = 10


def follow_mouse(event: Event):
    global previous_position

    move = Vector3D(x=event.x, y=event.y)

    if move.is_same(windowCenter):
        return

    offset = move - windowCenter

    if offset.magnitude() < mouse_deadzone:
        return

    offset = offset.normalize()

    axis = Vector3D()
    if offset.x < 0:
        camera.rotate(Vector3D(y=1), camera_speed * offset.x, True)
        axis.y = -1
    elif offset.x > 0:
        camera.rotate(Vector3D(y=1), camera_speed * offset.x, True)
        axis.y = 1

    if offset.y < 0:
        camera.rotate(Vector3D(x=1), camera_speed * offset.y)
        axis.x = -1
    elif offset.y > 0:
        camera.rotate(Vector3D(x=1), camera_speed * offset.y)
        axis.x = 1

    tk.event_generate('<Motion>', warp=True, x=windowCenter.x, y=windowCenter.y)


def adjust_viewport(amount: float):
    def mover(_: Event):
        camera.view_port = camera.view_port.translate(Vector3D(z=amount))

    return mover


def toggle_info(_: Event):
    options.debug = not options.debug


def toggle_fps(_: Event):
    options.draw_fps = not options.draw_fps


view_up = rotate_camera(axis=Vector3D(x=-1), angle=camera_speed)
view_down = rotate_camera(axis=Vector3D(x=1), angle=camera_speed)
view_left = rotate_camera(axis=Vector3D(y=-1), angle=camera_speed)
view_right = rotate_camera(axis=Vector3D(y=1), angle=camera_speed)

tk.bind(sequence="w", func=move_camera(Vector3D(z=camera_speed)))
tk.bind(sequence="s", func=move_camera(Vector3D(z=-camera_speed)))
tk.bind(sequence="a", func=move_camera(Vector3D(x=-camera_speed)))
tk.bind(sequence="d", func=move_camera(Vector3D(x=camera_speed)))
tk.bind(sequence="<Left>", func=view_left)
tk.bind(sequence="<Right>", func=view_right)
tk.bind(sequence="<Up>", func=view_up)
tk.bind(sequence="<Down>", func=view_down)
tk.bind(sequence="q", func=rotate_camera(axis=Vector3D(z=1), angle=camera_speed))
tk.bind(sequence="e", func=rotate_camera(axis=Vector3D(z=1), angle=-camera_speed))
tk.bind(sequence="<space>", func=move_camera(Vector3D(y=camera_speed)))
tk.bind(sequence="<Shift_L>", func=move_camera(Vector3D(y=-camera_speed)))
tk.bind(sequence="<Prior>", func=adjust_viewport(camera_speed))
tk.bind(sequence="<Next>", func=adjust_viewport(-camera_speed))
tk.bind(sequence="<Motion>", func=follow_mouse)
tk.bind(sequence="i", func=toggle_info)
tk.bind(sequence="f", func=toggle_fps)

tl.start()
tk.mainloop()
pipeline.stop()
