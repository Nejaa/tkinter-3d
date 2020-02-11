from __future__ import annotations

from datetime import timedelta
from random import random
from tkinter import Tk, Canvas, Event

from timeloop import Timeloop

from geometry import geometry_options
from geometry.camera import Camera
from geometry.quaternion import Quaternion
from geometry.vector import Vector
from options import options
from shape.cube import Cube
from shape.plane import Plane

geometry_options.line_thickness = 1

windowCenter = Vector(x=options.width / 2, y=options.height / 2, z=0)

origin = Vector(x=options.originOffset, y=options.originOffset, z=options.originOffset)

cubeSize = 20
plane = Plane(length=10, grid_size=5.0)
plane.translate(Vector(x=-cubeSize, y=-cubeSize, z=cubeSize))
cube = Cube(cube_size=cubeSize)
meshes = [
    plane,
    plane.copy().rotate(rotation=Quaternion.axis_angle(Vector(x=1), angle=-90)),
    plane.copy().rotate(rotation=Quaternion.axis_angle(Vector(y=1), angle=90)),
    cube,
    # Cube(cube_size=cubeSize / 2, origin=Vector(y=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(y=-(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(x=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(x=-(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(z=(cubeSize + cubeSize / 2))),
    # Cube(cube_size=cubeSize / 2, origin=Vector(z=-(cubeSize + cubeSize / 2))),
]
[m.translate(origin) for m in meshes]
rot_speed = 180 / options.tickRate  # deg/s = rot speed/tick
cube_rot_axis = Vector(x=random(), y=random(), z=random())
point2 = cube_rot_axis.copy() * 100
point1 = -point2
rotationSpeeds = [
    None,
    None,
    None,
    Quaternion.axis_angle(cube_rot_axis, angle=rot_speed),
    # Quaternion.axis_angle(Vector(x=1), angle=-rot_speed),
    # Quaternion.axis_angle(Vector(x=1), angle=rot_speed),
    # Quaternion.axis_angle(Vector(y=1), angle=rot_speed),
    # Quaternion.axis_angle(Vector(y=1), angle=-rot_speed),
    # Quaternion.axis_angle(Vector(z=1), angle=rot_speed),
    # Quaternion.axis_angle(Vector(z=1), angle=-rot_speed),
]

camera_origin = cube.center + Vector(z=-cubeSize * 4)
camera = Camera(position=camera_origin, focal_length=500)
camera_speed = 1

frames = 0
fps = 0

tl = Timeloop()

updating_view = False


# disabled for now
@tl.job(interval=timedelta(milliseconds=options.refresh_delay))
def update_view():
    global frames, updating_view

    if drawing:
        return

    updating_view = True
    for idx, mesh in enumerate(meshes):
        mesh.project_to(camera=camera)
        mesh.translate_projections(windowCenter)

    frames += 1
    updating_view = False


drawing = False


def draw():
    global frames, drawing

    if updating_view:
        canvas.after(ms=1, func=draw)
        return

    drawing = True
    canvas.delete("all")

    for idx, mesh in enumerate(meshes):
        mesh.draw(canvas, options.debug)

    drawing = False
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
        camera.translate(direction)

    return mover


def rotate_camera(axis: Vector, angle: float):
    def mover(_: Event):
        camera.rotate(axis, angle)

    return mover


previous_position = None


def follow_mouse(event: Event):
    global previous_position

    x = event.x
    y = event.y

    if (windowCenter.x == x) & (windowCenter.y == y):
        return

    x_off = x - windowCenter.x
    y_off = y - windowCenter.y

    if x_off < 0:
        view_left(event)
    elif x_off > 0:
        view_right(event)

    if y_off < 0:
        view_up(event)
    elif y_off > 0:
        view_down(event)

    tk.event_generate('<Motion>', warp=True, x=windowCenter.x, y=windowCenter.y)


def adjust_viewport(amount: float):
    def mover(_: Event):
        camera.view_port.translate(Vector(z=amount))

    return mover


def toggle_info(_: Event):
    options.debug = not options.debug


def toggle_fps(_: Event):
    options.draw_fps = not options.draw_fps


view_up = rotate_camera(axis=Vector(x=1), angle=-camera_speed)
view_down = rotate_camera(axis=Vector(x=1), angle=camera_speed)
view_left = rotate_camera(axis=Vector(y=1), angle=-camera_speed)
view_right = rotate_camera(axis=Vector(y=1), angle=camera_speed)

tk = Tk()
tk.config(cursor="none")
canvas = Canvas(tk, width=options.width, height=options.height)
canvas.pack()

tk.bind(sequence="z", func=move_camera(Vector(z=camera_speed)))
tk.bind(sequence="s", func=move_camera(Vector(z=-camera_speed)))
tk.bind(sequence="q", func=move_camera(Vector(x=-camera_speed)))
tk.bind(sequence="d", func=move_camera(Vector(x=camera_speed)))
tk.bind(sequence="<Left>", func=view_left)
tk.bind(sequence="<Right>", func=view_right)
tk.bind(sequence="<Up>", func=view_up)
tk.bind(sequence="<Down>", func=view_down)
tk.bind(sequence="a", func=rotate_camera(axis=Vector(z=1), angle=camera_speed))
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
