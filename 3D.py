from __future__ import annotations
from tkinter import Tk, Canvas, Event
from geometry import geometry_options
from geometry.camera import Camera
from geometry.quaternion import Quaternion
from shape.cube import *
from timeloop import Timeloop
from datetime import timedelta
from options import options
from random import random

geometry_options.line_thickness = 1

windowCenter = Vector(x=options.width / 2, y=options.height / 2, z=0)

origin = Vector(x=options.originOffset, y=options.originOffset, z=options.originOffset)

cubeSize = 30
meshes = [
    Cube(cube_size=cubeSize),
    Cube(cube_size=cubeSize / 2, origin=Vector(y=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(y=-(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(x=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(x=-(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(z=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(z=-(cubeSize + cubeSize / 2))),
]
[m.translate(origin) for m in meshes]

rot_speed = 180 / options.tickRate  # deg/s = rot speed/tick
rotationSpeeds = [
    Quaternion.axis_angle(Vector(x=random(), y=random(), z=random()), angle=rot_speed),
    Quaternion.axis_angle(Vector(x=1), angle=-rot_speed),
    Quaternion.axis_angle(Vector(x=1), angle=rot_speed),
    Quaternion.axis_angle(Vector(y=1), angle=rot_speed),
    Quaternion.axis_angle(Vector(y=1), angle=-rot_speed),
    Quaternion.axis_angle(Vector(z=1), angle=rot_speed),
    Quaternion.axis_angle(Vector(z=1), angle=-rot_speed),
]

camera_origin = meshes[0].center + Vector(z=-cubeSize * 4)
camera = Camera(position=camera_origin, focal_length=500)
camera_speed = 1

frames = 0
fps = 0

tl = Timeloop()


@tl.job(interval=timedelta(milliseconds=options.refresh_delay))
def update_view():
    global frames

    for idx, mesh in enumerate(meshes):
        mesh.project_to(camera=camera)
        mesh.translate_projections(windowCenter)

    frames += 1


def draw():
    canvas.delete("all")

    for idx, mesh in enumerate(meshes):
        mesh.draw(canvas, options.debug)

    if options.draw_fps:
        canvas.create_text(20, 10, text=fps)

    if options.debug:
        canvas.create_text(145, 40, text="{}".format(camera))

    canvas.after(ms=options.refresh_delay, func=draw)


@tl.job(interval=timedelta(milliseconds=options.tick_delay))
def update_world():
    for idx, mesh in enumerate(meshes):
        mesh.rotate(rotation=rotationSpeeds[idx])


@tl.job(interval=timedelta(seconds=1))
def fps_counter():
    global fps, frames
    fps = frames
    frames = 0


def move_camera(direction: Vector):
    def mover(_: Event):
        camera.translate(direction)

    return mover


def rotate_camera(direction: Quaternion):
    def mover(_: Event):
        camera.rotate(direction)

    return mover


def adjust_viewport(amount: float):
    def mover(_: Event):
        camera.view_port.translate(Vector(z=amount))

    return mover


def toggle_info(_: Event):
    options.debug = not options.debug


def toggle_fps(_: Event):
    options.draw_fps = not options.draw_fps


tk = Tk()
canvas = Canvas(tk, width=options.width, height=options.height)
canvas.pack()

tk.bind(sequence="w", func=move_camera(Vector(z=camera_speed)))
tk.bind(sequence="s", func=move_camera(Vector(z=-camera_speed)))
tk.bind(sequence="a", func=move_camera(Vector(x=-camera_speed)))
tk.bind(sequence="d", func=move_camera(Vector(x=camera_speed)))
tk.bind(sequence="<Left>", func=rotate_camera(Quaternion.axis_angle(axis=Vector(y=1), angle=-camera_speed)))
tk.bind(sequence="<Right>", func=rotate_camera(Quaternion.axis_angle(axis=Vector(y=1), angle=camera_speed)))
tk.bind(sequence="<Up>", func=rotate_camera(Quaternion.axis_angle(axis=Vector(x=1), angle=-camera_speed)))
tk.bind(sequence="<Down>", func=rotate_camera(Quaternion.axis_angle(axis=Vector(x=1), angle=camera_speed)))
tk.bind(sequence="q", func=rotate_camera(Quaternion.axis_angle(axis=Vector(z=1), angle=camera_speed)))
tk.bind(sequence="e", func=rotate_camera(Quaternion.axis_angle(axis=Vector(z=1), angle=-camera_speed)))
tk.bind(sequence="<space>", func=move_camera(Vector(y=camera_speed)))
tk.bind(sequence="<Shift_L>", func=move_camera(Vector(y=-camera_speed)))
tk.bind(sequence="<Prior>", func=adjust_viewport(camera_speed))
tk.bind(sequence="<Next>", func=adjust_viewport(-camera_speed))
tk.bind(sequence="i", func=toggle_info)
tk.bind(sequence="f", func=toggle_fps)

tl.start()
tk.after(ms=100, func=draw)
tk.mainloop()
