import random
import time
import curses

# Constants
TREASURE_PROBABILITY = 0.1
INITIAL_OBJECTS_COUNT = 5
GAME_WIDTH, GAME_HEIGHT = 32, 12

# Helper Functions
def get_key(stdscr):
    return stdscr.getch()

def move_character(stdscr, position):
    curses.curs_set(0)
    position[0] = max(0, min(position[0], GAME_WIDTH - 1))
    position[1] = max(0, min(position[1], GAME_HEIGHT - 1))
    stdscr.addstr(position[1], position[0] * 2, 'C', curses.color_pair(3))
    stdscr.refresh()

def print_game(stdscr, character, treasures, obstacles, score, level):
    stdscr.clear()
    move_character(stdscr, character)

    for obj_list, symbol, color in [(treasures, 'T', 4), (obstacles, 'O', 5)]:
        for obj in obj_list:
            if 0 <= obj[0] < GAME_WIDTH and 0 <= obj[1] < GAME_HEIGHT:
                stdscr.addstr(obj[1], obj[0] * 2, symbol, curses.color_pair(color))

    stdscr.addstr(0, 0, f"Score: {score} | Level: {level}", curses.color_pair(1))
    stdscr.refresh()

def update_game(character, treasures, obstacles, score):
    collision = False

    for obj_list, value in [(treasures, 10), (obstacles, 0)]:
        for obj in list(obj_list):
            if character == obj:
                obj_list.remove(obj)
                score += value
                if value == 0:
                    collision = True

    return collision, score

def print_game_over(stdscr, score):
    stdscr.clear()
    stdscr.addstr(0, 0, "Game Over!", curses.color_pair(2))
    stdscr.addstr(2, 0, f"Your final score is: {score}")
    stdscr.addstr(4, 0, "Press 'q' to quit.")
    stdscr.refresh()

def move_objects_left(treasures, obstacles):
    for obj_list in [treasures, obstacles]:
        for obj in obj_list:
            obj[0] = (obj[0] - 1) % GAME_WIDTH

    if random.random() < TREASURE_PROBABILITY:
        treasures.append([GAME_WIDTH - 1, random.randint(0, GAME_HEIGHT - 1)])

def initialize_objects():
    character = [0, GAME_HEIGHT // 2]
    treasures = [[random.randint(GAME_WIDTH // 2, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)] for _ in range(INITIAL_OBJECTS_COUNT)]
    obstacles = [[random.randint(GAME_WIDTH // 2, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)] for _ in range(INITIAL_OBJECTS_COUNT)]

    return character, treasures, obstacles

def level_up(score, level):
    return score >= level * 100

def pixel_adventure(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    key = ''
    character, treasures, obstacles = initialize_objects()
    score, level = 0, 1

    while key != ord('q'):
        stdscr.clear()
        stdscr.addstr(0, 0, "Welcome to Pixel Adventure!", curses.color_pair(1))
        stdscr.addstr(2, 0, "Press 's' to start the game.")
        stdscr.addstr(3, 0, "Press 'q' to quit.")
        stdscr.refresh()

        key = get_key(stdscr)
        if key is not None and chr(key).lower() == 's':
            break

    while True:
        move_objects_left(treasures, obstacles)
        print_game(stdscr, character, treasures, obstacles, score, level)

        collision, score = update_game(character, treasures, obstacles, score)

        if level_up(score, level):
            level += 1
            obstacles.extend([[GAME_WIDTH - 1, random.randint(0, GAME_HEIGHT - 1)] for _ in range(level)])

        if collision:
            print_game_over(stdscr, score)
            key = get_key(stdscr)
            if key is not None and chr(key).lower() == 'q':
                break

        key = get_key(stdscr)
        if key is not None:
            if key == curses.KEY_UP:
                character[1] = max(0, character[1] - 1)
            elif key == curses.KEY_DOWN:
                character[1] = min(GAME_HEIGHT - 1, character[1] + 1)
            elif key == curses.KEY_LEFT:
                character[0] = max(0, character[0] - 1)
            elif key == curses.KEY_RIGHT:
                character[0] = min(GAME_WIDTH - 1, character[0] + 1)

curses.wrapper(pixel_adventure)

