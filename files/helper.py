from sklearn.preprocessing import MinMaxScaler


# Limites do cubo original
__cube_verts_lim = [
    (-3.0, -3.0, 3.0),      # A - 0
    (-3.0, 3.0, 3.0),       # B - 1
    (3.0, 3.0, 3.0),        # C - 2
    (3.0, -3.0, 3.0),       # D - 3
    (-3.0, -3.0, -3.0),     # E - 4
    (-3.0, 3.0, -3.0),      # F - 5
    (3.0, 3.0, -3.0),       # G - 6
    (3.0, -3.0, -3.0)       # H - 7
]

# Peças de centro
__center_pieces = [[[-1, -1, 3.3],
                    [-1, 1, 3.3],
                    [1, 1, 3.3],
                    [1, -1, 3.3],
                    [-1, -1, 1.3],
                    [-1, 1, 1.3],
                    [1, 1, 1.3],
                    [1, -1, 1.3]],
                   [[-3.3, -1, 1],
                    [-3.3, 1, 1],
                    [-1.3, 1, 1],
                    [-1.3, -1, 1],
                    [-3.3, -1, -1],
                    [-3.3, 1, -1],
                    [-1.3, 1, -1],
                    [-1.3, -1, -1]],
                   [[-1, -1, -1.3],
                    [-1, 1, -1.3],
                    [1, 1, -1.3],
                    [1, -1, -1.3],
                    [-1, -1, -3.3],
                    [-1, 1, -3.3],
                    [1, 1, -3.3],
                    [1, -1, -3.3]],
                   [[1.3, -1, 1],
                    [1.3, 1, 1],
                    [3.3, 1, 1],
                    [3.3, -1, 1],
                    [1.3, -1, -1],
                    [1.3, 1, -1],
                    [3.3, 1, -1],
                    [3.3, -1, -1]],
                   [[-1, 1.3, 1],
                    [-1, 3.3, 1],
                    [1, 3.3, 1],
                    [1, 1.3, 1],
                    [-1, 1.3, -1],
                    [-1, 3.3, -1],
                    [1, 3.3, -1],
                    [1, 1.3, -1]],
                   [[-1, -3.3, 1],
                    [-1, -1.3, 1],
                    [1, -1.3, 1],
                    [1, -3.3, 1],
                    [-1, -3.3, -1],
                    [-1, -1.3, -1],
                    [1, -1.3, -1],
                    [1, -3.3, -1]]]

# Peças intermediárias em eixos
__edge_pieces = [[[[-1, -3.3, 3.3],
                   [-1, -1.3, 3.3],
                   [1, -1.3, 3.3],
                   [1, -3.3, 3.3],
                   [-1, -3.3, 1.3],
                   [-1, -1.3, 1.3],
                   [1, -1.3, 1.3],
                   [1, -3.3, 1.3]],
                  [[-1, 1.3, 3.3],
                   [-1, 3.3, 3.3],
                   [1, 3.3, 3.3],
                   [1, 1.3, 3.3],
                   [-1, 1.3, 1.3],
                   [-1, 3.3, 1.3],
                   [1, 3.3, 1.3],
                   [1, 1.3, 1.3]],
                  [[-1, 1.3, -1.3],
                   [-1, 3.3, -1.3],
                   [1, 3.3, -1.3],
                   [1, 1.3, -1.3],
                   [-1, 1.3, -3.3],
                   [-1, 3.3, -3.3],
                   [1, 3.3, -3.3],
                   [1, 1.3, -3.3]],
                  [[-1, -3.3, -1.3],
                   [-1, -1.3, -1.3],
                   [1, -1.3, -1.3],
                   [1, -3.3, -1.3],
                   [-1, -3.3, -3.3],
                   [-1, -1.3, -3.3],
                   [1, -1.3, -3.3],
                   [1, -3.3, -3.3]]],
                 [[[-3.3, -1, 3.3],
                   [-3.3, 1, 3.3],
                     [-1.3, 1, 3.3],
                     [-1.3, -1, 3.3],
                     [-3.3, -1, 1.3],
                     [-3.3, 1, 1.3],
                     [-1.3, 1, 1.3],
                     [-1.3, -1, 1.3]],
                  [[-3.3, -1, -1.3],
                     [-3.3, 1, -1.3],
                     [-1.3, 1, -1.3],
                     [-1.3, -1, -1.3],
                     [-3.3, -1, -3.3],
                     [-3.3, 1, -3.3],
                     [-1.3, 1, -3.3],
                     [-1.3, -1, -3.3]],
                  [[1.3, -1, -1.3],
                     [1.3, 1, -1.3],
                     [3.3, 1, -1.3],
                     [3.3, -1, -1.3],
                     [1.3, -1, -3.3],
                     [1.3, 1, -3.3],
                     [3.3, 1, -3.3],
                     [3.3, -1, -3.3]],
                  [[1.3, -1, 3.3],
                     [1.3, 1, 3.3],
                     [3.3, 1, 3.3],
                     [3.3, -1, 3.3],
                     [1.3, -1, 1.3],
                     [1.3, 1, 1.3],
                     [3.3, 1, 1.3],
                     [3.3, -1, 1.3]]],
                 [[[-3.3, -3.3, 1],
                   [-3.3, -1.3, 1],
                     [-1.3, -1.3, 1],
                     [-1.3, -3.3, 1],
                     [-3.3, -3.3, -1],
                     [-3.3, -1.3, -1],
                     [-1.3, -1.3, -1],
                     [-1.3, -3.3, -1]],
                  [[-3.3, 1.3, 1],
                     [-3.3, 3.3, 1],
                     [-1.3, 3.3, 1],
                     [-1.3, 1.3, 1],
                     [-3.3, 1.3, -1],
                     [-3.3, 3.3, -1],
                     [-1.3, 3.3, -1],
                     [-1.3, 1.3, -1]],
                  [[1.3, 1.3, 1],
                     [1.3, 3.3, 1],
                     [3.3, 3.3, 1],
                     [3.3, 1.3, 1],
                     [1.3, 1.3, -1],
                     [1.3, 3.3, -1],
                     [3.3, 3.3, -1],
                     [3.3, 1.3, -1]],
                  [[1.3, -3.3, 1],
                     [1.3, -1.3, 1],
                     [3.3, -1.3, 1],
                     [3.3, -3.3, 1],
                     [1.3, -3.3, -1],
                     [1.3, -1.3, -1],
                     [3.3, -1.3, -1],
                     [3.3, -3.3, -1]]]]

# Peças de canto
__corner_pieces = [[[-3.3, -3.3, 3.3],
                   [-3.3, -1.3, 3.3],
                    [-1.3, -1.3, 3.3],
                    [-1.3, -3.3, 3.3],
                    [-3.3, -3.3, 1.3],
                    [-3.3, -1.3, 1.3],
                    [-1.3, -1.3, 1.3],
                    [-1.3, -3.3, 1.3]],
                   [[-3.3, 1.3, 3.3],
                    [-3.3, 3.3, 3.3],
                    [-1.3, 3.3, 3.3],
                    [-1.3, 1.3, 3.3],
                    [-3.3, 1.3, 1.3],
                    [-3.3, 3.3, 1.3],
                    [-1.3, 3.3, 1.3],
                    [-1.3, 1.3, 1.3]],
                   [[1.3, 1.3, 3.3],
                    [1.3, 3.3, 3.3],
                    [3.3, 3.3, 3.3],
                    [3.3, 1.3, 3.3],
                    [1.3, 1.3, 1.3],
                    [1.3, 3.3, 1.3],
                    [3.3, 3.3, 1.3],
                    [3.3, 1.3, 1.3]],
                   [[1.3, -3.3, 3.3],
                    [1.3, -1.3, 3.3],
                    [3.3, -1.3, 3.3],
                    [3.3, -3.3, 3.3],
                    [1.3, -3.3, 1.3],
                    [1.3, -1.3, 1.3],
                    [3.3, -1.3, 1.3],
                    [3.3, -3.3, 1.3]],
                   [[-3.3, -3.3, -1.3],
                    [-3.3, -1.3, -1.3],
                    [-1.3, -1.3, -1.3],
                    [-1.3, -3.3, -1.3],
                    [-3.3, -3.3, -3.3],
                    [-3.3, -1.3, -3.3],
                    [-1.3, -1.3, -3.3],
                    [-1.3, -3.3, -3.3]],
                   [[-3.3, 1.3, -1.3],
                    [-3.3, 3.3, -1.3],
                    [-1.3, 3.3, -1.3],
                    [-1.3, 1.3, -1.3],
                    [-3.3, 1.3, -3.3],
                    [-3.3, 3.3, -3.3],
                    [-1.3, 3.3, -3.3],
                    [-1.3, 1.3, -3.3]],
                   [[1.3, 1.3, -1.3],
                    [1.3, 3.3, -1.3],
                    [3.3, 3.3, -1.3],
                    [3.3, 1.3, -1.3],
                    [1.3, 1.3, -3.3],
                    [1.3, 3.3, -3.3],
                    [3.3, 3.3, -3.3],
                    [3.3, 1.3, -3.3]],
                   [[1.3, -3.3, -1.3],
                    [1.3, -1.3, -1.3],
                    [3.3, -1.3, -1.3],
                    [3.3, -3.3, -1.3],
                    [1.3, -3.3, -3.3],
                    [1.3, -1.3, -3.3],
                    [3.3, -1.3, -3.3],
                    [3.3, -3.3, -3.3]]]


# Escala para coordenadas originais
def __get_scaler():
    scaler = MinMaxScaler(feature_range=(-0.5, 0.5))
    scaler.fit(__cube_verts_lim)
    return scaler


# Conversão usando escala
def __conv(cube_verts):
    cube_verts = __get_scaler().transform(cube_verts)

    cube_verts = [tuple(vertex) for vertex in cube_verts]
    new_verts = []

    # cima
    new_verts.extend([cube_verts[0], cube_verts[1],
                     cube_verts[3], cube_verts[2]])

    # frente
    new_verts.extend([cube_verts[0], cube_verts[1],
                     cube_verts[4], cube_verts[5]])

    # baixo
    new_verts.extend([cube_verts[4], cube_verts[5],
                     cube_verts[7], cube_verts[6]])

    # trás
    new_verts.extend([cube_verts[6], cube_verts[7],
                     cube_verts[2], cube_verts[3]])

    # direita
    new_verts.extend([cube_verts[0], cube_verts[3],
                     cube_verts[4], cube_verts[7]])

    # esquerda
    new_verts.extend([cube_verts[1], cube_verts[2],
                     cube_verts[5], cube_verts[6]])

    return new_verts

# Retorna os vértices do cubo
def get_cube_verts():
    return __conv(__cube_verts_lim)

# Retorna as peças de centro
def get_center_pieces():
    return [__conv(piece) for piece in __center_pieces]

# Retorna as peças de canto
def get_corner_pieces():
    return [__conv(piece) for piece in __corner_pieces]

# Retorna as peças intermediárias
def get_edge_pieces():
    return [[__conv(sec_piece) for sec_piece in piece] for piece in __edge_pieces]

# Retorna as cores
def get_cube_colors():
    return [
        (0.0, 0.318, 0.729),    # Blue
        (0.8, 0.118, 0.118),    # Red
        (0.0, 0.7, 0.2),        # Green
        (1.0, 0.345, 0.0),      # Orange
        (1.0, 1.0, 1.0),        # White
        (1.0, 0.85, 0.1)        # Yellow
    ]

# Rotaciona uma coluna do cubo
def __rot_column(a, b, left=False):
    c = []

    for i in range(len(a)):
        row = []

        if not left:
            row.append(a[i][0])
            row.append(a[i][1])
            row.append(b[i][2])

        else:
            row.append(b[i][0])
            row.append(a[i][1])
            row.append(a[i][2])

        c.append(row)

    return c


class Cube:
    def __init__(self, cubes):
        self.cubes = cubes
        self.original = cubes.copy()

    def __rot_t(self):
        temp = self.cubes[1][0]
        self.cubes[1][0] = self.cubes[2][0][::-1]
        self.cubes[2][0] = self.cubes[3][0][::-1]
        self.cubes[3][0] = self.cubes[4][2]
        self.cubes[4][0] = temp

    def __rot_r(self):
        # Rotate the right face anti-clockwise
        temp = self.cubes[0]
        self.cubes[0] = __rot_column(self.cubes[0], self.cubes[3])
        self.cubes[3] = __rot_column(self.cubes[3], self.cubes[5])
        self.cubes[5] = __rot_column(self.cubes[5], self.cubes[1])
        self.cubes[1] = __rot_column(self.cubes[1], temp)

    def __rot_f(self):
        # Rotate the front face anti-clockwise
        temp = self.cubes[0][2]
        self.cubes[0][2] = self.cubes[2][2][::-1]
        self.cubes[2][2] = self.cubes[5][2]
        self.cubes[5][2] = self.cubes[3][0][::-1]
        self.cubes[3][0] = temp

    def __rot_l(self):
        # Rotate the left face anti-clockwise
        temp = self.cubes[0]
        self.cubes[0] = __rot_column(
            self.cubes[0], self.cubes[3], left=True)
        self.cubes[3] = __rot_column(
            self.cubes[3], self.cubes[5], left=True)
        self.cubes[5] = __rot_column(
            self.cubes[5], self.cubes[1], left=True)
        self.cubes[1] = __rot_column(self.cubes[1], temp, left=True)

    def __rot_b(self):
        # Rotate the bottom face anti-clockwise
        self.cubes[5] = [list(x) for x in self.cubes[5][::-1]]
        temp = self.cubes[1][2]
        self.cubes[1][2] = self.cubes[2][2][::-1]
        self.cubes[2][2] = self.cubes[3][2][::-1]
        self.cubes[3][2] = self.cubes[4][0]
        self.cubes[4][2] = temp

    def rotate_face(self, face):
        # Rotate the specified face
        if face == 'top':
            self.__rot_t()
        elif face == 'right':
            self.__rot_r()
        elif face == 'front':
            self.__rot_f()
        elif face == 'left':
            self.__rot_l()
        elif face == 'bottom':
            self.__rot_b()
        else:
            raise ValueError('Invalid face')

    def __str__(self):

        ret = ''
        for face in self.cubes:
            for row in face:
                ret = ret + ''.join(str(row)) + '\n'
            ret = ret + '\n'

        return ret
