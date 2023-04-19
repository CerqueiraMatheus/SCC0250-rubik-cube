import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import time
import math

vertex_code = """
    attribute vec3 position;
    uniform mat4 mat_transformation;
    void main(){
        gl_Position = mat_transformation * vec4(position,1.0);
    }
    """

fragment_code = """
    uniform vec4 color;
    void main(){
        gl_FragColor = color;
    }
    """

def keyHandler(window, key, scancode, action, mods):
    global cube, program, lock_rotation
    
    # Camera Scale
    if key == glfw.KEY_I:
        cube.scale(1.1)
    if key == glfw.KEY_O:
        cube.scale(1.0/1.1)
    # Camera Rotation
    if key == glfw.KEY_UP:
        cube.rotateCameraX(0.1)

    if key == glfw.KEY_DOWN:
        cube.rotateCameraX(-0.1)

    if key == glfw.KEY_LEFT:
        cube.rotateCameraY(0.1)

    if key == glfw.KEY_RIGHT:
        cube.rotateCameraY(-0.1)

    # Camera Translation
    if key == glfw.KEY_Z:
        cube.translateCameraZ(0.1)

    if key == glfw.KEY_X:
        cube.translateCameraZ(-0.1)

    if key == glfw.KEY_C:
        cube.translateCameraY(0.1)

    if key == glfw.KEY_V:
        cube.translateCameraY(-0.1)

    if key == glfw.KEY_B:
        cube.translateCameraX(0.1)

    if key == glfw.KEY_N:
        cube.translateCameraX(-0.1)

    # Debug:
    if key == glfw.KEY_P:
        print(cube.is_solved())

    # Face Rotations
    if lock_rotation == True:
        return
    
    if key == glfw.KEY_Q and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (1, 0, 0), np.pi/2)
    
    if key == glfw.KEY_A and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (1, 0, 0), -np.pi/2)

    if key == glfw.KEY_W and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (-1, 0, 0), np.pi/2)

    if key == glfw.KEY_S and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (-1, 0, 0), -np.pi/2)

    if key == glfw.KEY_E and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, 1, 0), np.pi/2)

    if key == glfw.KEY_D and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, 1, 0), -np.pi/2)

    if key == glfw.KEY_R and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, -1, 0), np.pi/2)

    if key == glfw.KEY_F and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, -1, 0), -np.pi/2)

    if key == glfw.KEY_T and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, 0, 1), np.pi/2)

    if key == glfw.KEY_G and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, 0, 1), -np.pi/2)

    if key == glfw.KEY_Y and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, 0, -1), np.pi/2)

    if key == glfw.KEY_H and action == glfw.PRESS:
        cube.drawSlowRotateFace(window, program, (0, 0, -1), -np.pi/2)

def applyShaders(vert_code, frag_code):
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, vert_code)
    glShaderSource(fragment, frag_code)

    glCompileShader(vertex)
    glCompileShader(fragment)

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)
    glUseProgram(program)

    return program

def createWindow(vert_code, frag_code):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(700, 700, "Cubo", None, None)
    glfw.make_context_current(window)

    program = applyShaders(vert_code, frag_code)

    return window, program


def sendVertices(program, vertices):
    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

class Cubie:

    def __init__(self, position, len):
        x, y, z = position
        
        # Seen coordinate from the cubie
        self.pos = (float(x), float(y), float(z), 1.0)
        self.original_pos = (float(x), float(y), float(z), 1.0)
        self.len = len
        
        # Actual coordinate in the cube (opengl coordinate)
        self.central_verts = (x * 2 * len, y * 2 * len, z * 2 * len)
        self.verts = self.defineVertices(self.central_verts, self.len)
        
        self.mat = np.identity(4, dtype=np.float32)
        self.camera = np.identity(4, dtype=np.float32)
        self.camera_rotation = np.identity(4, dtype=np.float32)
        
        self.colors = np.array([(1.0, 0.0, 0.0, 1.0),
                                (0.0, 0.0, 1.0, 1.0),
                                (1.0, 0.6, 0.0, 1.0),
                                (0.0, 1.0, 0.0, 1.0),
                                (1.0, 1.0, 1.0, 1.0),
                                (1.0, 1.0, 0.0, 1.0)])

    def is_solved(self):
        test_vertices = self.defineVertices((2*self.pos[0]*self.len, 2*self.pos[1]*self.len, 2*self.pos[2]*self.len), self.len) - self.verts
        return np.all(abs(test_vertices) < 1e-4)
        
    def defineVertices(self, pos, len):
        return np.array([

            (pos[0] - len, pos[1] - len, pos[2] + len),
            (pos[0] + len, pos[1] - len, pos[2] + len),
            (pos[0] - len, pos[1] + len, pos[2] + len),
            (pos[0] + len, pos[1] + len, pos[2] + len),

            (pos[0] + len, pos[1] - len, pos[2] + len),
            (pos[0] + len, pos[1] - len, pos[2] - len),
            (pos[0] + len, pos[1] + len, pos[2] + len),
            (pos[0] + len, pos[1] + len, pos[2] - len),

            (pos[0] + len, pos[1] - len, pos[2] - len),
            (pos[0] - len, pos[1] - len, pos[2] - len),
            (pos[0] + len, pos[1] + len, pos[2] - len),
            (pos[0] - len, pos[1] + len, pos[2] - len),

            (pos[0] - len, pos[1] - len, pos[2] - len),
            (pos[0] - len, pos[1] - len, pos[2] + len),
            (pos[0] - len, pos[1] + len, pos[2] - len),
            (pos[0] - len, pos[1] + len, pos[2] + len),

            (pos[0] - len, pos[1] - len, pos[2] - len),
            (pos[0] + len, pos[1] - len, pos[2] - len),
            (pos[0] - len, pos[1] - len, pos[2] + len),
            (pos[0] + len, pos[1] - len, pos[2] + len),

            (pos[0] - len, pos[1] + len, pos[2] + len),
            (pos[0] + len, pos[1] + len, pos[2] + len),
            (pos[0] - len, pos[1] + len, pos[2] - len),
            (pos[0] + len, pos[1] + len, pos[2] - len)
        ], dtype=np.float32)
    
    def getVertices(self):
        return self.verts
        
    def scale(self, s):
        mat_scale = np.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]], dtype=np.float32)
        self.camera = mat_scale @ self.camera

    # Use for visual rotation
    def rotateX(self, ang):
        mat_rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(ang), -np.sin(ang), 0],
            [0, np.sin(ang), np.cos(ang), 0],
            [0, 0, 0, 1]
        ])

        self.mat = mat_rot_x @ self.mat

        return self

    # Use for 90 deg rotation
    def rotatePosX(self, ang):
        mat_rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(ang), -np.sin(ang), 0],
            [0, np.sin(ang), np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        self.pos = mat_rot_x @ self.pos
        self.pos = np.round(self.pos)

        return self

    def rotateCameraX(self, ang):
        mat_rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(ang), -np.sin(ang), 0],
            [0, np.sin(ang), np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        self.camera_rotation = mat_rot_x @ self.camera_rotation
        
        return self

    # Use for visual rotation
    def rotateY(self, ang):
        mat_rot_y = np.array([
            [np.cos(ang), 0, np.sin(ang), 0],
            [0, 1, 0, 0],
            [-np.sin(ang), 0, np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        self.mat = mat_rot_y @ self.mat

        return self
    
    # Use for 90 deg rotation
    def rotatePosY(self, ang):
        mat_rot_y = np.array([
            [np.cos(ang), 0, np.sin(ang), 0],
            [0, 1, 0, 0],
            [-np.sin(ang), 0, np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        self.pos = mat_rot_y @ self.pos
        self.pos = np.round(self.pos)
        
        return self
    
    def rotateCameraY(self, ang):
        mat_rot_y = np.array([
            [np.cos(ang), 0, np.sin(ang), 0],
            [0, 1, 0, 0],
            [-np.sin(ang), 0, np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        self.camera_rotation = mat_rot_y @ self.camera_rotation
        
        return self

    # Use for visual rotation
    def rotateZ(self, ang):
        mat_rot_z = np.array([
            [np.cos(ang), -np.sin(ang), 0, 0],
            [np.sin(ang), np.cos(ang), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        self.mat = mat_rot_z @ self.mat
        
        return self
    
    # Use for 90 deg rotation
    def rotatePosZ(self, ang):
        mat_rot_z = np.array([
            [np.cos(ang), -np.sin(ang), 0, 0],
            [np.sin(ang), np.cos(ang), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        self.pos = mat_rot_z @ self.pos
        self.pos = np.round(self.pos)
        
        return self
    
    def rotateCameraZ(self, ang):
        mat_rot_z = np.array([
            [np.cos(ang), -np.sin(ang), 0, 0],
            [np.sin(ang), np.cos(ang), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        self.camera_rotation = mat_rot_z @ self.camera_rotation
        
        return self
    
    def translateCameraX(self, dist):
        mat_transl_x = np.array([
            [1, 0, 0, dist],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.camera = mat_transl_x @ self.camera

        return self
    
    def translateCameraY(self, dist):
        mat_transl_y = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, dist],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.camera = mat_transl_y @ self.camera

        return self
    
    def translateCameraZ(self, dist):
        mat_transl_z = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, dist],
            [0, 0, 0, 1]
        ])

        self.camera = mat_transl_z @ self.camera

        return self

    def drawFace(self, program, vert_start_idx, face):
        loc_color = glGetUniformLocation(program, "color")
        
        colorR, colorG, colorB, colorA = self.colors[face]
        glUniform4f(loc_color, colorR, colorG, colorB, colorA)
        glDrawArrays(GL_TRIANGLE_STRIP, vert_start_idx + face * 4, 4)

        border_vertex_idx = np.array([vert_start_idx + face * 4 + 0, 
                                      vert_start_idx + face * 4 + 1,
                                      vert_start_idx + face * 4 + 3,
                                      vert_start_idx + face * 4 + 2,
                                      vert_start_idx + face * 4 + 0])
        
        glUniform4f(loc_color, 0.0, 0.0, 0.0, 1.0)
        # Increase stroke weight
        glDrawElements(GL_LINE_STRIP, len(border_vertex_idx), GL_UNSIGNED_INT, border_vertex_idx)

    def draw(self, program, vert_start_idx):
        loc_matrix = glGetUniformLocation(program, "mat_transformation")

        result_mat = self.camera @ self.camera_rotation @ self.mat
        glUniformMatrix4fv(loc_matrix, 1, GL_TRUE, result_mat.reshape(16))

        for i in range(6):
            self.drawFace(program, vert_start_idx, i)


class Cube:
    def __init__(self):
        self.cubies = self.generateCubies()
    
    def is_solved(self):
        return all([cubie.is_solved() for cubie in self.cubies])

    def generateCubies(self):
        cubies = []
        len = 0.15

        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                for k in range(-1, 2, 1):
                    cubies.append(Cubie((i, j, k), len))

        return cubies
    
    def getVertices(self):
        vertices = np.empty((0, 3), dtype=np.float32)
        for cubie in self.cubies:
            vertices = np.vstack((vertices, cubie.getVertices()))
        return vertices
    
    def scale(self, s):
        for cubie in self.cubies:
            cubie.scale(s)

    def rotateX(self, ang):
        for cubie in self.cubies:
            cubie.rotateX(ang)
        return self
    
    def rotateCameraX(self, ang):
        for cubie in self.cubies:
            cubie.rotateCameraX(ang)
        return self

    def rotateY(self, ang):
        for cubie in self.cubies:
            cubie.rotateY(ang)
        return self
    
    def rotateCameraY(self, ang):
        for cubie in self.cubies:
            cubie.rotateCameraY(ang)
        return self
    
    def rotateZ(self, ang):
        for cubie in self.cubies:
            cubie.rotateZ(ang)
        return self
    
    def rotateCameraZ(self, ang):
        for cubie in self.cubies:
            cubie.rotateCameraZ(ang)
        return self
    
    def translateCameraX(self, dist):
        for cubie in self.cubies:
            cubie.translateCameraX(dist)
        return self
    
    def translateCameraY(self, dist):
        for cubie in self.cubies:
            cubie.translateCameraY(dist)
        return self
    
    def translateCameraZ(self, dist):
        for cubie in self.cubies:
            cubie.translateCameraZ(dist)
        return self
    
    
    def drawSlowRotateFace(self, window, program, face, ang):
        """
            face: tuple of 3 ints
            ex: (1, 0, 0) rotaciona a face cujo vetor normal é (1, 0, 0)
            obs: Não é muito bem um vetr normal
        """
        global lock_rotation
        
        lock_rotation = True

        # Index of face that is equal to 1 or -1
        face_idx, face_value = [(i, x) for i, x in enumerate(face) if x == 1 or x == -1][0]

        ang_steps = 20
        ang_dt = ang / ang_steps

        cubies_idx_on_face = [i for i, cubie in enumerate(self.cubies) if cubie.pos[face_idx] == face_value]

        for i in range(ang_steps):
            if face_idx == 0:
                for idx in cubies_idx_on_face:
                    self.cubies[idx].rotateX(ang_dt)

            elif face_idx == 1:
                for idx in cubies_idx_on_face:
                    self.cubies[idx].rotateY(ang_dt)

            elif face_idx == 2:
                for idx in cubies_idx_on_face:
                    self.cubies[idx].rotateZ(ang_dt)
            
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw(program)
            glfw.swap_buffers(window)


        if face_idx == 0:
            for idx in cubies_idx_on_face:
                self.cubies[idx].rotatePosX(ang)

        elif face_idx == 1:
            for idx in cubies_idx_on_face:
                self.cubies[idx].rotatePosY(ang)

        elif face_idx == 2:
            for idx in cubies_idx_on_face:
                self.cubies[idx].rotatePosZ(ang)

        lock_rotation = False

        return self

    def draw(self, program):
        
        for index, cubie in enumerate(self.cubies):
            cubie.draw(program, index * 24)

def main():
    global program, cube, lock_rotation

    lock_rotation = False

    window, program = createWindow(vertex_code, fragment_code)

    glfw.set_key_callback(window, keyHandler)
    
    cube = Cube()    

    vertices = cube.getVertices()
    sendVertices(program, vertices)

    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)

    glClearColor(0.0, 0.0, 0.0, 1.0)

    cube.rotateCameraX(0.4).rotateCameraY(0.4).rotateCameraZ(0.4)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube.draw(program)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
