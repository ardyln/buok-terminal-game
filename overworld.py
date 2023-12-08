import curses
import random
import time

class Room:
    def __init__(self, height, width, num_iterations, seed):
        self.seed = seed
        self.dungeon = self.create_dungeon(height, width, num_iterations)
        self.doors = self.place_doors()

    def create_dungeon(self, height, width, num_iterations):
        random.seed(self.seed)
        dungeon = [[' ' for _ in range(width)] for _ in range(height)]

        central_width = min(5, width - 4)
        central_height = min(5, height - 4)
        central_start_x = (width - central_width) // 2
        central_start_y = (height - central_height) // 2

        for y in range(central_start_y, central_start_y + central_height):
            for x in range(central_start_x, central_start_x + central_width):
                dungeon[y][x] = ' '

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if x < central_start_x or x >= central_start_x + central_width or y < central_start_y or y >= central_start_y + central_height:
                    dungeon[y][x] = '#' if random.random() < 0.5 else ' '

        for _ in range(num_iterations):
            new_dungeon = [[' ' for _ in range(width)] for _ in range(height)]
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    neighbors = sum(
                        1 for i in range(-1, 2) for j in range(-1, 2) if dungeon[y + i][x + j] == '#'
                    )
                    new_dungeon[y][x] = '#' if neighbors >= 5 else ' '
            dungeon = new_dungeon

        for i in range(height):
            dungeon[i][0] = dungeon[i][width - 1] = '#'
        for j in range(width):
            dungeon[0][j] = dungeon[height - 1][j] = '#'

        return dungeon

    def place_doors(self):
        height, width = len(self.dungeon), len(self.dungeon[0])
        doors = []

        doors.append((width // 2, 1))
        doors.append((width - 2, height // 2))
        doors.append((width // 2, height - 2))
        doors.append((1, height // 2))

        return doors

def place_gold(dungeon):
    height, width = len(dungeon), len(dungeon[0])
    while True:
        x, y = random.randint(1, width - 2), random.randint(1, height - 2)
        if dungeon[y][x] == ' ':
            dungeon[y][x] = '$'
            return x, y

def place_player(dungeon, room):
    while True:
        x, y = random.randint(1, len(dungeon[0]) - 2), random.randint(1, len(dungeon) - 2)
        if dungeon[y][x] == ' ' and (x, y) not in room.doors:
            return x, y

def remove_gold(dungeon, x, y):
    dungeon[y][x] = ' '

def draw_dungeon(stdscr, dungeon, player_x, player_y, score, doors, current_room_coords, monsters):
    stdscr.clear()

    for y, row in enumerate(dungeon):
        for x, cell in enumerate(row):
            if (x, y) in doors:
                stdscr.addch(y, x, '+', curses.color_pair(4))
            elif cell == '#':
                stdscr.addch(y, x, '#', curses.color_pair(1))
            elif cell == '$':
                stdscr.addch(y, x, '$', curses.color_pair(2))
            else:
                stdscr.addch(y, x, ' ')

    for monster in monsters:
        stdscr.addch(monster.y, monster.x, 'M', curses.color_pair(6))

    stdscr.addch(player_y, player_x, '@', curses.color_pair(3))
    stdscr.addstr(len(dungeon) + 1, 0, f"Score: {score}")
    stdscr.addstr(len(dungeon) + 2, 0, f"Current Room: {current_room_coords}")

def draw_projectile(stdscr, projectile):
    stdscr.addch(projectile['y'], projectile['x'], '*', curses.color_pair(5))

class Monster:
    def __init__(self, dungeon):
        self.x, self.y = self.place_monster(dungeon)
        self.move_delay = 0.15

    def place_monster(self, dungeon):
        while True:
            x, y = random.randint(1, len(dungeon[0]) - 2), random.randint(1, len(dungeon) - 2)
            if dungeon[y][x] == ' ':
                return x, y

    def move_towards_player(self, player_x, player_y, dungeon):
        if random.random() < self.move_delay:
            dx = player_x - self.x
            dy = player_y - self.y

            if dx != 0:
                dx //= abs(dx)

            if dy != 0:
                dy //= abs(dy)

            new_x, new_y = self.x + dx, self.y + dy

            if dungeon[new_y][new_x] == ' ':
                self.x, self.y = new_x, new_y

    def shoot_projectile(self, player_x, player_y):
        return {'x': player_x, 'y': player_y}

def main(stdscr):
    curses.curs_set(0)
    stdscr.timeout(100)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)

    grid_size = 5
    seed_offset = 1000

    rooms = [[Room(20, 50, num_iterations=5, seed=i * grid_size + j + seed_offset) for j in range(grid_size)] for i in range(grid_size)]

    current_room_coords = (0, 0)
    current_room = rooms[current_room_coords[0]][current_room_coords[1]]

    player_x, player_y = place_player(current_room.dungeon, current_room)
    score = 0

    gold_x, gold_y = place_gold(current_room.dungeon)

    monsters = [Monster(current_room.dungeon) for _ in range(3)]

    projectiles = []

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP and player_y > 1 and current_room.dungeon[player_y - 1][player_x] != '#':
            player_y -= 1
        elif key == curses.KEY_DOWN and player_y < len(current_room.dungeon) - 2 and current_room.dungeon[player_y + 1][player_x] != '#':
            player_y += 1
        elif key == curses.KEY_LEFT and player_x > 1 and current_room.dungeon[player_y][player_x - 1] != '#':
            player_x -= 1
        elif key == curses.KEY_RIGHT and player_x < len(current_room.dungeon[0]) - 2 and current_room.dungeon[player_y][player_x + 1] != '#':
            player_x += 1

        # Player transitions to a new room
        if (player_x, player_y) in current_room.doors:
            direction = current_room.doors.index((player_x, player_y))
            if direction == 0:
                new_room_coords = (current_room_coords[0] - 1, current_room_coords[1])
                player_y = len(current_room.dungeon) - 2  # Move the player to the bottom edge of the new room
            elif direction == 1:
                new_room_coords = (current_room_coords[0], current_room_coords[1] + 1)
                player_x = 2  # Move the player to the left edge of the new room
            elif direction == 2:
                new_room_coords = (current_room_coords[0] + 1, current_room_coords[1])
                player_y = 2  # Move the player to the top edge of the new room
            elif direction == 3:
                new_room_coords = (current_room_coords[0], current_room_coords[1] - 1)
                player_x = len(current_room.dungeon[0]) - 2  # Move the player to the right edge of the new room

            if 0 <= new_room_coords[0] < grid_size and 0 <= new_room_coords[1] < grid_size:
                current_room_coords = new_room_coords
                current_room = rooms[current_room_coords[0]][current_room_coords[1]]
                opposite_door = current_room.doors[(direction + 2) % 4]
                player_x - 1, player_y - 1 == opposite_door
                score += 5
            else:
                current_room_coords = (current_room_coords[0] - (player_x == 2) + (player_x == len(current_room.dungeon[0]) - 2),
                                       current_room_coords[1] - (player_y == 2) + (player_y == len(current_room.dungeon) - 2))

        if player_x == gold_x and player_y == gold_y:
            score += 10
            remove_gold(current_room.dungeon, gold_x, gold_y)
            gold_x, gold_y = place_gold(current_room.dungeon)

        for monster in monsters:
            monster.move_towards_player(player_x, player_y, current_room.dungeon)
            projectile = monster.shoot_projectile(player_x, player_y)
            projectiles.append(projectile)

        new_projectiles = []
        for projectile in projectiles:
            draw_projectile(stdscr, projectile)
            projectile['y'] += 1
            if projectile['x'] == player_x and projectile['y'] == player_y:
                score -= 20
            elif 0 < projectile['y'] < len(current_room.dungeon) - 1:
                new_projectiles.append(projectile)

        projectiles = new_projectiles

        draw_dungeon(stdscr, current_room.dungeon, player_x, player_y, score, current_room.doors, current_room_coords, monsters)

        stdscr.refresh()
        time.sleep(0.01)

if __name__ == "__main__":
    curses.wrapper(main)
