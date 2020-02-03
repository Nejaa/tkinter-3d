from __future__ import annotations
from tkinter import Tk, Canvas
from geometry import Camera, geometry_options
from cube import *
from timeloop import Timeloop
from datetime import timedelta

debug = False
drawFps = debug | True
tickRate = 150
tickDelay = int(1000 / tickRate)
refreshRate = 60
refreshDelay = int(1000 / refreshRate)
width = 800
height = 600
windowCenter = Vector(x=width / 2, y=height / 2, z=0)

originOffset = 1000
origin = Vector(x=originOffset, y=originOffset, z=originOffset)

cubeSize = 30
meshes = [
    Cube(cube_size=cubeSize),
    Cube(cube_size=cubeSize / 2, center=Vector(y=-(cubeSize + cubeSize / 2))),
    Cube(cube_size=cubeSize / 2, center=Vector(y=(cubeSize + cubeSize / 2))),
    Cube(cube_size=cubeSize / 2, center=Vector(x=(cubeSize + cubeSize / 2))),
    Cube(cube_size=cubeSize / 2, center=Vector(x=-(cubeSize + cubeSize / 2))),
]
[m.translate(origin) for m in meshes]

rot_speed = 360 / tickRate  # deg/s = rot speed/tick
rotationSpeeds = [
    0,
    rot_speed,
    -rot_speed,
    rot_speed,
    -rot_speed,
]

geometry_options.line_thickness = 1

camera_origin = meshes[0].center + Vector(z=-200)
camera = Camera(position=camera_origin, focal_length=20)
camera_speed = 0

frames = 0
fps = 0

updating_view = False
drawing_view = False

view_tl = Timeloop()
tl = Timeloop()


@view_tl.job(interval=timedelta(milliseconds=refreshDelay))
def update_view():
    global frames

    for idx, mesh in enumerate(meshes):
        mesh.project_to(camera=camera)
        mesh.translate_projections(windowCenter)

    # loop
    frames += 1


def draw():
    canvas.delete("all")

    for idx, mesh in enumerate(meshes):
        mesh.draw(canvas, debug)

    if drawFps:
        canvas.create_text(20, 10, text=fps)

    canvas.after(ms=refreshDelay, func=draw)


@tl.job(interval=timedelta(milliseconds=tickDelay))
def update_world():
    for idx, mesh in enumerate(meshes):
        mesh.rotate_y(angle=rotationSpeeds[idx])

    # test different positions
    camera.position.x += camera_speed
    if camera.position.x > camera_origin.x + cubeSize:
        camera.position.x = camera_origin.x - cubeSize
        camera.position.y += camera_speed * 2
        if camera.position.y > camera_origin.y + cubeSize:
            camera.position.y = camera_origin.y - cubeSize


@tl.job(interval=timedelta(seconds=1))
def fps_counter():
    global fps, frames
    fps = frames
    frames = 0


tk = Tk()
canvas = Canvas(tk, width=width, height=height)
canvas.pack()
tl.start()
view_tl.start()
tk.after(ms=100, func=draw)
tk.mainloop()
