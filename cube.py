import glfw
from OpenGL.GL import *
import numpy as np
from lib.utils import keyHandler, createWindow, sendVertices
from lib.Cube import Cube
from lib import globals

VERTEX_SHADER_FNAME = './lib/vertex_shader.glsl'
FRAGMENT_SHADER_FNAME = './lib/fragment_shader.glsl'

def main():
    globals.lock_rotation = False

    vertex_code = open(VERTEX_SHADER_FNAME, 'r').read()
    fragment_code = open(FRAGMENT_SHADER_FNAME, 'r').read()

    window, globals.program = createWindow(vertex_code, fragment_code)

    glfw.set_key_callback(window, keyHandler)
    
    globals.cube = Cube()    

    vertices = globals.cube.getVertices()
    sendVertices(globals.program, vertices)

    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)

    glClearColor(0.0, 0.0, 0.0, 1.0)

    globals.cube.rotateCameraX(0.4).rotateCameraY(0.4).rotateCameraZ(0.4)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        globals.cube.draw(globals.program)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
