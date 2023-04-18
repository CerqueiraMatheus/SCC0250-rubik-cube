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
        self.len = len
        
        # Actual coordinate in the cube (opengl coordinate)
        self.central_verts = (x * 2 * len, y * 2 * len, z * 2 * len)
        self.verts = self.defineVertices(self.central_verts, self.len)
        
        self.mat = np.identity(4, dtype=np.float32)
        self.cam = np.identity(4, dtype=np.float32)
        
        self.colors = np.array([(1.0, 0.0, 0.0, 1.0),
                                (0.0, 1.0, 0.0, 1.0),
                                (0.0, 0.0, 1.0, 1.0),
                                (1.0, 1.0, 0.0, 1.0),
                                (1.0, 0.0, 1.0, 1.0),
                                (0.0, 1.0, 1.0, 1.0)])

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

    def rotateCamX(self, ang):
        mat_rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(ang), -np.sin(ang), 0],
            [0, np.sin(ang), np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        self.cam = mat_rot_x @ self.cam
        
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
    
    def rotateCamY(self, ang):
        mat_rot_y = np.array([
            [np.cos(ang), 0, np.sin(ang), 0],
            [0, 1, 0, 0],
            [-np.sin(ang), 0, np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        self.cam = mat_rot_y @ self.cam
        
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
    
    def rotateCamZ(self, ang):
        mat_rot_z = np.array([
            [np.cos(ang), -np.sin(ang), 0, 0],
            [np.sin(ang), np.cos(ang), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        self.cam = mat_rot_z @ self.cam
        
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

        result_mat = self.cam @ self.mat
        glUniformMatrix4fv(loc_matrix, 1, GL_TRUE, result_mat.reshape(16))

        for i in range(6):
            self.drawFace(program, vert_start_idx, i)


class Cube:
    def __init__(self):
        self.cubies = self.generateCubies()

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
    
    def rotateX(self, ang):
        for cubie in self.cubies:
            cubie.rotateX(ang)
        return self
    
    def rotateCamX(self, ang):
        for cubie in self.cubies:
            cubie.rotateCamX(ang)
        return self

    def rotateY(self, ang):
        for cubie in self.cubies:
            cubie.rotateY(ang)
        return self
    
    def rotateCamY(self, ang):
        for cubie in self.cubies:
            cubie.rotateCamY(ang)
        return self
    
    def rotateZ(self, ang):
        for cubie in self.cubies:
            cubie.rotateZ(ang)
        return self
    
    def rotateCamZ(self, ang):
        for cubie in self.cubies:
            cubie.rotateCamZ(ang)
        return self
    
    
    def drawSlowRotateFace(self, window, program, face, ang):
        """
            face: tuple of 3 ints
            ex: (1, 0, 0) rotaciona a face cujo vetor normal é (1, 0, 0)
            obs: Não é muito bem um vetr normal
        """
        # Index of face that is equal to 1 or -1
        face_idx, face_value = [(i, x) for i, x in enumerate(face) if x == 1 or x == -1][0]

        ang_steps = 100
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

        return self


    def draw(self, program):
        
        for index, cubie in enumerate(self.cubies):
            cubie.draw(program, index * 24)

def main():
    window, program = createWindow(vertex_code, fragment_code)

    cube = Cube()
    vertices = cube.getVertices()
    sendVertices(program, vertices)

    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)

    glClearColor(1.0, 1.0, 1.0, 1.0)

    cube.rotateCamX(0.4).rotateCamY(0.4).rotateCamZ(0.4)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        cube.drawSlowRotateFace(window, program, (1, 0, 0), np.pi / 2)
        cube.drawSlowRotateFace(window, program, (0, 1, 0), np.pi / 2)

    glfw.terminate()
    

if __name__ == '__main__':
    main()