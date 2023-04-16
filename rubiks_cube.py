from cubie import *

class RubiksCube:
    def __init__(self, colors):
        self.colors = colors
        self.cubies = [Cubie(CubieType.CORNER, (0,0), CubiePosition(0,FaceOrientation.UP)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(1,FaceOrientation.UP)), 
                       Cubie(CubieType.CORNER, (0,0), CubiePosition(2,FaceOrientation.UP)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(3,FaceOrientation.UP)), 
                       Cubie(CubieType.CENTER, (0,0), CubiePosition(4,FaceOrientation.UP)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(5,FaceOrientation.UP)), 
                       Cubie(CubieType.CORNER, (0,0), CubiePosition(6,FaceOrientation.UP)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(7,FaceOrientation.UP)), 
                       Cubie(CubieType.CORNER, (0,0), CubiePosition(8,FaceOrientation.UP)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(9,FaceOrientation.LEFT)), 
                       Cubie(CubieType.CENTER, (0,0), CubiePosition(10,FaceOrientation.LEFT)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(11,FaceOrientation.LEFT)), 
                       Cubie(CubieType.CENTER, (0,0), CubiePosition(12,FaceOrientation.FRONT)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(13,FaceOrientation.FRONT)), 
                       Cubie(CubieType.CENTER, (0,0), CubiePosition(14,FaceOrientation.RIGHT)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(15,FaceOrientation.RIGHT)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(16,FaceOrientation.BACK)), 
                       Cubie(CubieType.CORNER, (0,0), CubiePosition(17,FaceOrientation.DOWN)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(18,FaceOrientation.DOWN)), 
                       Cubie(CubieType.CORNER, (0,0), CubiePosition(19,FaceOrientation.DOWN)), 
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(20,FaceOrientation.DOWN)),
                       Cubie(CubieType.CENTER, (0,0), CubiePosition(21,FaceOrientation.DOWN)),
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(22,FaceOrientation.DOWN)),
                       Cubie(CubieType.CORNER, (0,0), CubiePosition(23,FaceOrientation.DOWN)),
                       Cubie(CubieType.EDGE, (0,0), CubiePosition(24,FaceOrientation.DOWN)),
                       Cubie(CubieType.CORNER, (0,0), CubiePosition(25,FaceOrientation.DOWN))]
        self.rotation_orientations = {"R": {FaceOrientation.UP: FaceOrientation.BACK, 
                                            FaceOrientation.BACK: FaceOrientation.DOWN, 
                                            FaceOrientation.DOWN: FaceOrientation.FRONT, 
                                            FaceOrientation.FRONT: FaceOrientation.UP, 
                                            FaceOrientation.RIGHT: FaceOrientation.RIGHT
                                            },
                                      "L": {FaceOrientation.UP: FaceOrientation.FRONT,
                                            FaceOrientation.FRONT: FaceOrientation.DOWN,
                                            FaceOrientation.DOWN: FaceOrientation.BACK,
                                            FaceOrientation.BACK: FaceOrientation.UP,
                                            FaceOrientation.LEFT: FaceOrientation.LEFT
                                            },
                                      "U": {FaceOrientation.UP: FaceOrientation.UP,
                                            FaceOrientation.BACK: FaceOrientation.RIGHT,
                                            FaceOrientation.RIGHT: FaceOrientation.FRONT,
                                            FaceOrientation.FRONT: FaceOrientation.LEFT,
                                            FaceOrientation.LEFT: FaceOrientation.BACK
                                            },
                                      "F": {FaceOrientation.UP: FaceOrientation.RIGHT,
                                            FaceOrientation.RIGHT: FaceOrientation.DOWN,
                                            FaceOrientation.DOWN: FaceOrientation.LEFT,
                                            FaceOrientation.LEFT: FaceOrientation.UP,
                                            FaceOrientation.FRONT: FaceOrientation.FRONT
                                            },
                                      "B": {FaceOrientation.UP: FaceOrientation.LEFT,
                                            FaceOrientation.LEFT: FaceOrientation.DOWN,
                                            FaceOrientation.DOWN: FaceOrientation.RIGHT,
                                            FaceOrientation.RIGHT: FaceOrientation.UP,
                                            FaceOrientation.BACK: FaceOrientation.BACK
                                            },
                                      "D": {FaceOrientation.DOWN: FaceOrientation.DOWN,
                                            FaceOrientation.LEFT: FaceOrientation.FRONT,
                                            FaceOrientation.FRONT: FaceOrientation.RIGHT,
                                            FaceOrientation.RIGHT: FaceOrientation.BACK,
                                            FaceOrientation.BACK: FaceOrientation.LEFT},
                                      "R'": {FaceOrientation.UP: FaceOrientation.FRONT,
                                             FaceOrientation.FRONT: FaceOrientation.DOWN,
                                             FaceOrientation.DOWN: FaceOrientation.BACK,
                                             FaceOrientation.BACK: FaceOrientation.UP,
                                             FaceOrientation.RIGHT: FaceOrientation.RIGHT
                                             },
                                      "L'": {FaceOrientation.UP: FaceOrientation.BACK,
                                             FaceOrientation.BACK: FaceOrientation.DOWN,
                                             FaceOrientation.DOWN: FaceOrientation.FRONT,
                                             FaceOrientation.FRONT: FaceOrientation.UP,
                                             FaceOrientation.LEFT: FaceOrientation.LEFT
                                             },
                                      "U'": {FaceOrientation.UP: FaceOrientation.UP,
                                             FaceOrientation.LEFT: FaceOrientation.FRONT,
                                             FaceOrientation.FRONT: FaceOrientation.RIGHT,
                                             FaceOrientation.RIGHT: FaceOrientation.BACK,
                                             FaceOrientation.BACK: FaceOrientation.LEFT
                                             },
                                      "B'": {FaceOrientation.UP: FaceOrientation.RIGHT,
                                             FaceOrientation.RIGHT: FaceOrientation.DOWN,
                                             FaceOrientation.DOWN: FaceOrientation.LEFT,
                                             FaceOrientation.LEFT: FaceOrientation.UP,
                                             FaceOrientation.BACK: FaceOrientation.BACK
                                             },
                                      "F'": {FaceOrientation.UP: FaceOrientation.LEFT,
                                             FaceOrientation.LEFT: FaceOrientation.DOWN,
                                             FaceOrientation.DOWN: FaceOrientation.RIGHT,
                                             FaceOrientation.RIGHT: FaceOrientation.UP,
                                             FaceOrientation.FRONT: FaceOrientation.FRONT
                                             },
                                      "D'": {FaceOrientation.DOWN: FaceOrientation.DOWN,
                                             FaceOrientation.BACK: FaceOrientation.RIGHT,
                                             FaceOrientation.RIGHT: FaceOrientation.FRONT, 
                                             FaceOrientation.FRONT: FaceOrientation.LEFT,
                                             FaceOrientation.LEFT: FaceOrientation.BACK
                                             }
                                      }
        self.rotation_positions =  {"R": [2,19,25,8,5,15,22,13],
                                    "L": [0,6,23,17,3,11,20,9],
                                    "U": [0,2,8,6,1,5,7,3],
                                    "F": [6,8,25,23,7,13,24,11],
                                    "B": [2,0,17,19,1,9,18,15],
                                    "D": [17,23,25,19,18,20,24,22],
                                    "R'": [2,8,25,19,5,13,22,15],
                                    "L'": [0,17,23,6,3,9,20,11],
                                    "U'": [0,6,8,2,1,3,7,5],
                                    "F'": [6,23,25,8,7,11,24,13],
                                    "B'": [2,19,17,0,1,15,18,9],
                                    "D'": [17,19,25,23,18,22,24,20]
                                    }

    def is_solved(self):
        return all([x.position == x.correct_position for x in self.cubies])

    def rotate(self, rotation):
        if rotation[-1] == '2':
            rotation = rotation[:-1]
            self.rotate(rotation)

        rotated_cubies = self.rotation_positions[rotation]
        # Change cubie's contents
        for i,j in enumerate(rotated_cubies):
            this_cubie = self.cubies[j]
            this_cubie.position.orientation = self.rotation_orientations[rotation][this_cubie.position.orientation]
            if i < 4:
                this_cubie.position.position = rotated_cubies[(i + 1) % 4]
            else:
                this_cubie.position.position = rotated_cubies[4 + (i - 3) % 4] 
            
        # Change cubie's positions in array (Corners)
        aux = self.cubies[rotated_cubies[0]]
        for i in range(3,0,-1):
            self.cubies[rotated_cubies[(i + 1) % 4]] = self.cubies[rotated_cubies[i]]
        self.cubies[rotated_cubies[1]] = aux

        # Change cubie's positions in array (Edges)
        aux = self.cubies[rotated_cubies[4]]
        for i in range(7,4,-1):
            self.cubies[rotated_cubies[4 + (i - 3) % 4]] = self.cubies[rotated_cubies[i]]
        self.cubies[rotated_cubies[5]] = aux

if __name__ == "__main__":
    cube = RubiksCube(0)
    contador = 0
    sequencia = input().split()
    while True:
        for s in sequencia:
            print(s)
            cube.rotate(s)
        contador += 1
        if cube.is_solved():
            break
    print(contador)
