"""
    SCC0250 - Computação Gráfica (1o semestre de 2023)
    Trabalho 1 - Desenvolver programa envolvendo transformações geométricas
    Membros do grupo:
        - Matheus H. de C. Pinto: 11911104
        - Antonio Italo: 12542290
        - João Favoretti: 11316055
        - Lucas Pimentel: 10633328
        - Gabriel Vicente Rodrigues: 11795377
"""

"""
    Global variables declaration file
"""

# Program variable is used to draw the images correctly on the screen
program = None

# Cube instance that controls the face rotations and camera movements
cube = None

# Lock variable that blocks diferent face movements at the same time
lock_rotation = None
