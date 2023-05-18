# Imports
import pygame, sys, math
from pygame.locals import *
from coordinates import coordinate
from matrix import mat4x4

ELAPSED_TIME = 0.005 # time between frame redraws -- do not touch

# Screen Variables
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cube Coordinates
COORD_A = coordinate(0, 0, 0)
COORD_B = coordinate(0, 0, 1)
COORD_C = coordinate(0, 1, 0)
COORD_D = coordinate(0, 1, 1)
COORD_E = coordinate(1, 0, 0)
COORD_F = coordinate(1, 0, 1)
COORD_G = coordinate(1, 1, 0)
COORD_H = coordinate(1, 1, 1)

TRIANGLE_CUBE = [
        [COORD_A, COORD_C, COORD_G],
        [COORD_A, COORD_E, COORD_G],
        [COORD_G, COORD_E, COORD_H],
        [COORD_H, COORD_E, COORD_F],
        [COORD_A, COORD_B, COORD_D],
        [COORD_A, COORD_C, COORD_D],
        [COORD_F, COORD_B, COORD_D],
        [COORD_D, COORD_H, COORD_F],
        [COORD_C, COORD_G, COORD_H],
        [COORD_C, COORD_D, COORD_H],
        [COORD_A, COORD_E, COORD_B],
        [COORD_E, COORD_B, COORD_F]
    ]

# i - input matrix
# o - output matrix
# matrix - matrix to multiply with 
def multiply_matrix_vector(i, o, matrix):
    o.x = i.x * matrix.m[0][0] + i.y * matrix.m[1][0] + i.z * matrix.m[2][0] + matrix.m[3][0]
    o.y = i.x * matrix.m[0][1] + i.y * matrix.m[1][1] + i.z * matrix.m[2][1] + matrix.m[3][1]
    o.z = i.x * matrix.m[0][2] + i.y * matrix.m[1][2] + i.z * matrix.m[2][2] + matrix.m[3][2]

    w = i.x * matrix.m[0][3] + i.y * matrix.m[1][3] + i.z * matrix.m[2][3] + matrix.m[3][3]
    
    if(w != 0):
        o.x /= w
        o.y /= w
        o.z /= w

# draws a triangle between three coordinates
def draw_triangle(x_coord_1, y_coord_1, x_coord_2, y_coord_2, x_coord_3, y_coord_3, color):
    pygame.draw.line(SCREEN, color, (x_coord_1, y_coord_1), (x_coord_2, y_coord_2), 3)
    pygame.draw.line(SCREEN, color, (x_coord_2, y_coord_2), (x_coord_3, y_coord_3), 3)
    pygame.draw.line(SCREEN, color, (x_coord_3, y_coord_3), (x_coord_1, y_coord_1), 3)

def main():
    # Projection Matrix
    mat_projection = mat4x4()
    f_near = 0.1
    f_far = 1000
    FOV = 90
    aspect_ratio = SCREEN_HEIGHT / SCREEN_WIDTH
    FOV_Radians = 1.0 / math.tan(FOV * 0.5 / 180.0 * math.pi)

    mat_projection.m[0][0] = aspect_ratio * FOV_Radians
    mat_projection.m[1][1] = FOV_Radians
    mat_projection.m[2][2] = f_far / (f_far - f_near)
    mat_projection.m[3][2] = (-f_far * f_near) / (f_far - f_near)
    mat_projection.m[2][3] = 1

    # Rotational Matrices
    mat_rotate_x = mat4x4() 
    mat_rotate_z = mat4x4() 

    # Creates window
    pygame.init()

    # Caption
    pygame.display.set_caption('3D Rendering')

    triangle_projected = [coordinate(0, 0, 0), coordinate(0, 0, 0), coordinate(0, 0, 0)]
    triangle_rotated_z = [coordinate(0, 0, 0), coordinate(0, 0, 0), coordinate(0, 0, 0)]
    triangle_rotated_zx = [coordinate(0, 0, 0), coordinate(0, 0, 0), coordinate(0, 0, 0)]
    theta = 0

    # Main window loop
    while True:
        SCREEN.fill(BLACK)
        for triangle in TRIANGLE_CUBE:

            theta += ELAPSED_TIME

            # Rotate Z
            mat_rotate_z.m[0][0] = math.cos(theta)
            mat_rotate_z.m[0][1] = math.sin(theta)
            mat_rotate_z.m[1][0] = -math.sin(theta)
            mat_rotate_z.m[1][1] = math.cos(theta)
            mat_rotate_z.m[2][2] = 1
            mat_rotate_z.m[3][3] = 1

            # Rotate X
            mat_rotate_x.m[0][0] = 1
            mat_rotate_x.m[1][1] = math.cos(theta * 0.5)
            mat_rotate_x.m[1][2] = -math.sin(theta * 0.5)
            mat_rotate_x.m[2][1] = math.sin(theta * 0.5)
            mat_rotate_x.m[2][2] = math.cos(theta * 0.5)
            mat_rotate_x.m[3][3] = 1

            # Z axis rotation
            multiply_matrix_vector(triangle[0], triangle_rotated_z[0], mat_rotate_z)
            multiply_matrix_vector(triangle[1], triangle_rotated_z[1], mat_rotate_z)
            multiply_matrix_vector(triangle[2], triangle_rotated_z[2], mat_rotate_z)
            
            # X axis rotation
            multiply_matrix_vector(triangle_rotated_z[0], triangle_rotated_zx[0], mat_rotate_x)
            multiply_matrix_vector(triangle_rotated_z[1], triangle_rotated_zx[1], mat_rotate_x)
            multiply_matrix_vector(triangle_rotated_z[2], triangle_rotated_zx[2], mat_rotate_x)
            
            # Translate away from camera
            triangle_rotated_zx[0].z += 3
            triangle_rotated_zx[1].z += 3
            triangle_rotated_zx[2].z += 3

            multiply_matrix_vector(triangle_rotated_zx[0], triangle_projected[0], mat_projection)
            multiply_matrix_vector(triangle_rotated_zx[1], triangle_projected[1], mat_projection)
            multiply_matrix_vector(triangle_rotated_zx[2], triangle_projected[2], mat_projection)

            # Scale to size
            triangle_projected[0].x += 1
            triangle_projected[0].y += 1
            triangle_projected[1].x += 1
            triangle_projected[1].y += 1
            triangle_projected[2].x += 1
            triangle_projected[2].y += 1

            triangle_projected[0].x *= 0.5 * SCREEN_WIDTH
            triangle_projected[0].y *= 0.5 * SCREEN_HEIGHT
            triangle_projected[1].x *= 0.5 * SCREEN_WIDTH
            triangle_projected[1].y *= 0.5 * SCREEN_HEIGHT
            triangle_projected[2].x *= 0.5 * SCREEN_WIDTH
            triangle_projected[2].y *= 0.5 * SCREEN_HEIGHT


            draw_triangle(triangle_projected[0].x, triangle_projected[0].y, triangle_projected[1].x, triangle_projected[1].y, triangle_projected[2].x, triangle_projected[2].y, WHITE)

            pygame.display.flip()

        # quit on exit    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main()

