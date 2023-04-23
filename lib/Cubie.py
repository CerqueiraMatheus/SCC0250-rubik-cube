import numpy as np
from OpenGL.GL import *

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
        self.camera = np.identity(4, dtype=np.float32)
        self.camera_rotation = np.identity(4, dtype=np.float32)
        
        self.colors = np.array([(1.0, 0.0, 0.0, 1.0),
                                (0.0, 0.0, 1.0, 1.0),
                                (1.0, 0.6, 0.0, 1.0),
                                (0.0, 1.0, 0.0, 1.0),
                                (1.0, 1.0, 1.0, 1.0),
                                (1.0, 1.0, 0.0, 1.0)])

    def is_solved(self):
        test_vertices = np.array([(self.mat @ np.array([vert[0], vert[1], vert[2], 1.0]).T) - np.array([vert[0], vert[1], vert[2], 1.0]).T for vert in self.verts])
        print(abs(test_vertices))
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
