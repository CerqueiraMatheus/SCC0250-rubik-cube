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


class Cube:
    def __init__(self, cubes):
        self.cubes = cubes
        self.original = cubes.copy()

    def __str__(self):

        ret = ''
        for face in self.cubes:
            for row in face:
                ret = ret + ''.join(str(row)) + '\n'
            ret = ret + '\n'

        return ret

    def get_surface_cubes(self, face):
        """
        Return surfaces of a cube
        @param face: 'top', 'right', 'left', 'bottom', 'all'
        """

        sur_cubes = []

        if face == 'top':
            for row in self.cubes[0]:
                for c in row:
                    sur_cubes.append(c)
            sur_cubes.extend(self.cubes[1][0])
            sur_cubes.extend(self.cubes[2][0])
            sur_cubes.extend(self.cubes[3][0])
            sur_cubes.extend(self.cubes[4][0])
            return sur_cubes

        elif face == 'right':
            for row in self.cubes[2]:
                for c in row:
                    sur_cubes.append(c)
            sur_cubes.extend([row[2] for row in self.cubes[0]])
            sur_cubes.extend([row[2] for row in self.cubes[1]])
            sur_cubes.extend([row[2] for row in self.cubes[3]])
            sur_cubes.extend([row[2] for row in self.cubes[5]])
            return sur_cubes

        elif face == 'left':
            for row in self.cubes[4]:
                for c in row:
                    sur_cubes.append(c)
            sur_cubes.extend([row[0] for row in self.cubes[0]])
            sur_cubes.extend([row[0] for row in self.cubes[1]])
            sur_cubes.extend([row[0] for row in self.cubes[3]])
            sur_cubes.extend([row[0] for row in self.cubes[5]])
            return sur_cubes

        elif face == 'bottom':
            for row in self.cubes[5]:
                for c in row:
                    sur_cubes.append(c)
            sur_cubes.extend(self.cubes[1][2])
            sur_cubes.extend(self.cubes[2][2])
            sur_cubes.extend(self.cubes[3][2])
            sur_cubes.extend(self.cubes[4][2])
            return sur_cubes

        elif face == 'all':
            for surface in self.cubes:
                for row in surface:
                    for c in row:
                        sur_cubes.append(c)
            return sur_cubes

        else:
            raise ValueError('Invalid face')
