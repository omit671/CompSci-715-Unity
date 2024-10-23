import sys
import pygame
from pygame.locals import *
from scipy.spatial.transform import Rotation as R

def load_game_data(game_data_file):
    """ Load game data.

    Args:
        game_data_file (string): the log file of the game.
    Return:
        game_data (list): list of game data (x axis, y axis, yaw axis)
    """

    try:
        with open(game_data_file, 'r') as file:
            raw_game_data = file.read()
    except FileNotFoundError:
        print(f"File '{log_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    raw_lines = raw_game_data.split("\n")

    game_data = []

    for line in range(len(raw_lines) - 1):
        line_info = raw_lines[line].split(",")

        time = float(line_info[0])
        position = (float(line_info[1]), float(line_info[2]), float(line_info[3]))
        rotation = (float(line_info[4]), float(line_info[5]), float(line_info[6]), float(line_info[7]))

        euler_rotation = R.from_quat(rotation).as_euler('yxz', degrees=True)
        pygame_position = convert_position((position[0], position[2]))
        game_data.append((pygame_position[0], pygame_position[1], euler_rotation[0], time))

    return game_data

def convert_position(position):
    """Convert position (x, y) from Unity to pygame.

    Args:
        position (tuple): an unity position.
    Return:
        (tuple): pygame position
    """
    def _scale_number(unscaled, to_min, to_max, from_min, from_max):
        return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min
    
    norm_x = position[0] + 1.5
    room_x = norm_x // 300
    converted_x = _scale_number(norm_x, (-room_x * 150) + 300, ((-room_x + 1) * 150) + 300, room_x * 300, room_x * 300 + 3)

    norm_y = position[1] + 3
    room_y = norm_y // 600
    converted_y = _scale_number(norm_y, room_y * 300, (room_y + 1) * 300, room_y * 600, room_y * 600 + 6)
    return (converted_x, converted_y)

def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

if __name__ == '__main__':
    
    game_data_file = input('Enter the game data file: ') or 'MuseumA.txt'
    museum = input('Enter the museum (A or B): ') or 'A'
    step = int(input('Enter the speed of the pawn: '))

    game_data = load_game_data(game_data_file)
    game_data = game_data[::step]
    
    fps = 30
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)

    # set up the window
    DISPLAYSURF = pygame.display.set_mode((1510, 910), 0, 32)
    pygame.display.set_caption(f'Museum {museum} Navigation')

    WHITE = (255, 255, 255)

    floor_plan = pygame.image.load(f'museum{museum}_floor_plan.png')
    pawn = pygame.image.load('pawn.png')
    pawn_offset = pygame.math.Vector2(40, 0)
    frame = 0

    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        text_surface = font.render(f'{game_data[frame][3]}', False, (0, 0, 0))

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(floor_plan, (0, 0))
        DISPLAYSURF.blit(text_surface, (0, 0))
        participant, pos = rotate(pawn, game_data[frame][2], [game_data[frame][1], game_data[frame][0]], pawn_offset)
        DISPLAYSURF.blit(participant, pos)

        pygame.display.flip()
        frame += 1
        if (frame == len(game_data)):
            frame = 0
        
        clock.tick(fps)
