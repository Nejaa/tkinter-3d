from __future__ import annotations

import copy
from datetime import timedelta
from math import sqrt
from random import random
from tkinter import Tk, Canvas, Event
import time
from timeloop import Timeloop

from geometry import geometry_options
from geometry.camera import Camera
from geometry.mesh import Mesh
from geometry.quaternion import Quaternion
from geometry.vector import Vector
from options import options
from rendering.collectorStep import CollectorStep
from rendering.pipeline import Pipeline
from scene.entity import Entity
from scene.scene import Scene
from shape.cube import Cube
from shape.plane import Plane

geometry_options.line_thickness = 1

windowCenter = Vector(x=options.width / 2, y=options.height / 2, z=0)

origin = Vector(x=options.originOffset, y=options.originOffset, z=options.originOffset)

m = Mesh().import_from("ressources/Cylinder.obj")
m.scale(20)
m.rotate(rotation=Quaternion.axis_angle(Vector(y=1), 180))
cubeSize = 20
plane = Plane(length=4, grid_size=20.0)
plane.translate(Vector(x=-cubeSize, y=-cubeSize, z=cubeSize))
cube = Cube(cube_size=cubeSize)
meshes = [
    cube,
    m,
    plane,
    plane.copy().rotate(rotation=Quaternion.axis_angle(Vector(x=1), angle=-90)),
    plane.copy().rotate(rotation=Quaternion.axis_angle(Vector(y=1), angle=90)),
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
m.translate(Vector(x=cubeSize*2))

scene = Scene()
[scene.scene_root.add_entity(e) for e in entities]

rot_speed = 180 / options.tickRate  # deg/s = rot speed/tick
cube_rot_axis = Vector(x=random(), y=random(), z=random())
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

camera_origin = cube.center + Vector(z=-cubeSize * 4)
camera = Camera(position=camera_origin, focal_length=500, viewport_offset=windowCenter)
camera_speed = 1.5

frames = 0
fps = 0

pipeline = Pipeline(steps=[
    CollectorStep(),
])

tl = Timeloop()


@tl.job(interval=timedelta(milliseconds=options.refresh_delay / 2))
def update_view():
    local_scene = scene.copy()
    ent = local_scene.entities()
    mhs = [entity.geometry for entity in ent]

    for idx, mesh in enumerate(mhs):
        mesh.project_to(camera=camera)

    pipeline.push_scene(scene=local_scene)


last_scene = None


def draw():
    global frames, last_scene

    b_pull = time.time()
    new_scene = pipeline.pull_scene()
    if new_scene is not None:
        last_scene = new_scene
    # print("pull time = {:.6}ms".format((time.time() - b_pull) * 1000))

    if last_scene is None:
        canvas.after(ms=10, func=draw)
        return

    b_extract = time.time()
    msh = [entity.geometry for entity in last_scene.entities()]
    # print("extract time = {:.6}ms".format((time.time() - b_extract) * 1000))

    canvas.delete("all")

    b_draw = time.time()

    for mesh in msh:
        m_draw = time.time()
        mesh.draw(canvas, options.debug)
        # print("mesh draw time = {:.6}ms".format((time.time() - m_draw) * 1000))

    if options.draw_fps:
        canvas.create_text(20, 10, text=fps)

    canvas.create_line(windowCenter.x, windowCenter.y - options.cross_hair_scale,
                       windowCenter.x, windowCenter.y + options.cross_hair_scale,
                       width=2)
    canvas.create_line(windowCenter.x - options.cross_hair_scale, windowCenter.y,
                       windowCenter.x + options.cross_hair_scale, windowCenter.y,
                       width=2)
    if options.debug:
        canvas.create_text(145, 40, text="{}".format(camera))
    # print("draw time = {:.6}ms".format((time.time() - b_draw) * 1000))

    frames += 1

    # print("full draw time = {:.6}ms\n---------------------------------".format((time.time() - b_draw) * 1000))

    canvas.after(ms=1, func=draw)


@tl.job(interval=timedelta(milliseconds=options.tick_delay))
def update_world():
    for idx, mesh in enumerate(meshes):
        if idx > len(rotationSpeeds) - 1:
            break
        if rotationSpeeds[idx] is None:
            continue
        mesh.rotate(rotation=rotationSpeeds[idx])


@tl.job(interval=timedelta(seconds=1))
def fps_counter():
    global fps, frames
    fps = frames
    frames = 0


def move_camera(direction: Vector):
    def mover(_: Event):
        camera.translate(direction, options.global_movement)

    return mover


def rotate_camera(axis: Vector, angle: float):
    def mover(_: Event):
        camera.rotate(axis, angle)

    return mover


previous_position = None

mouse_deadzone = 10


def follow_mouse(event: Event):
    global previous_position

    move = Vector(x=event.x, y=event.y)

    if move.is_same(windowCenter):
        return

    offset = move - windowCenter

    if offset.magnitude() < mouse_deadzone:
        return

    offset = offset.normalize()

    axis = Vector()
    if offset.x < 0:
        camera.rotate(Vector(y=1), camera_speed * offset.x, True)
        axis.y = -1
    elif offset.x > 0:
        camera.rotate(Vector(y=1), camera_speed * offset.x, True)
        axis.y = 1

    if offset.y < 0:
        camera.rotate(Vector(x=1), camera_speed * offset.y)
        axis.x = -1
    elif offset.y > 0:
        camera.rotate(Vector(x=1), camera_speed * offset.y)
        axis.x = 1

    tk.event_generate('<Motion>', warp=True, x=windowCenter.x, y=windowCenter.y)


def adjust_viewport(amount: float):
    def mover(_: Event):
        camera.view_port.translate(Vector(z=amount))

    return mover


def toggle_info(_: Event):
    options.debug = not options.debug


def toggle_fps(_: Event):
    options.draw_fps = not options.draw_fps


view_up = rotate_camera(axis=Vector(x=-1), angle=camera_speed)
view_down = rotate_camera(axis=Vector(x=1), angle=camera_speed)
view_left = rotate_camera(axis=Vector(y=-1), angle=camera_speed)
view_right = rotate_camera(axis=Vector(y=1), angle=camera_speed)

tk = Tk()
tk.config(cursor="none")
canvas = Canvas(tk, width=options.width, height=options.height)
canvas.pack()

tk.bind(sequence="w", func=move_camera(Vector(z=camera_speed)))
tk.bind(sequence="s", func=move_camera(Vector(z=-camera_speed)))
tk.bind(sequence="a", func=move_camera(Vector(x=-camera_speed)))
tk.bind(sequence="d", func=move_camera(Vector(x=camera_speed)))
tk.bind(sequence="<Left>", func=view_left)
tk.bind(sequence="<Right>", func=view_right)
tk.bind(sequence="<Up>", func=view_up)
tk.bind(sequence="<Down>", func=view_down)
tk.bind(sequence="q", func=rotate_camera(axis=Vector(z=1), angle=camera_speed))
tk.bind(sequence="e", func=rotate_camera(axis=Vector(z=1), angle=-camera_speed))
tk.bind(sequence="<space>", func=move_camera(Vector(y=camera_speed)))
tk.bind(sequence="<Shift_L>", func=move_camera(Vector(y=-camera_speed)))
tk.bind(sequence="<Prior>", func=adjust_viewport(camera_speed))
tk.bind(sequence="<Next>", func=adjust_viewport(-camera_speed))
tk.bind(sequence="<Motion>", func=follow_mouse)
tk.bind(sequence="i", func=toggle_info)
tk.bind(sequence="f", func=toggle_fps)

tl.start()
tk.after(ms=100, func=draw)
tk.mainloop()
pipeline.stop()
