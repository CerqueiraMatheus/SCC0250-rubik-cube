import glfw
import numpy as np
from lib import globals
from OpenGL.GL import *
from lib.Cubie import Cubie

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
        
        globals.lock_rotation = True

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

        globals.lock_rotation = False

        return self

    def draw(self, program):
        
        for index, cubie in enumerate(self.cubies):
            cubie.draw(program, index * 24)
