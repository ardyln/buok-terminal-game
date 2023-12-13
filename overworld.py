import curses
import random
import time
class Item:
    def __init__(self, name, color, symbol):
        self.name = name
        self.color = color
        self.symbol = symbol

class Food(Item):
    def __init__(self, name, color, symbol, hunger, rarity):
        super().__init__(name, color, symbol)
        self.hunger = hunger
        self.rarity = rarity

class Inventory:
    def __init__(self):
        self.invlist = []

    def add_food(self, item):
        self.invlist.append(item)

    def remove_food(self, item):
        if item in self.invlist:
            self.invlist.remove(item)

class Player:
    def __init__(self, hunger):
        self.hunger = 100

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

        # Create open corridors from the center of each room to the center of the dungeon
        central_x = central_start_x + central_width // 2
        central_y = central_start_y + central_height // 2
        for y in range(central_start_y, central_start_y + central_height):
            if dungeon[y][central_x] == '#':
                dungeon[y][central_x] = ' '
        for x in range(central_start_x, central_start_x + central_width):
            if dungeon[central_y][x] == '#':
                dungeon[central_y][x] = ' '

        return dungeon

    def place_doors(self):
        height, width = len(self.dungeon), len(self.dungeon[0])
        doors = []

        doors.append((width // 2, 1))
        doors.append((width - 2, height // 2))
        doors.append((width // 2, height - 2))
        doors.append((1, height // 2))

        return doors

def food_items():
    items = [
        Food("Apple", curses.COLOR_BLUE, 'A', 10, 0.5),
        Food("Banana", curses.COLOR_YELLOW, 'B', 15, 0.3),
        Food("Carrot", curses.COLOR_GREEN, 'C', 8, 0.7)
    ]
    return items

def pick_up_food(dungeon, x, y, inventory):
    for food in food_items():
        if dungeon[y][x] == food.symbol:
            dungeon[y][x] = ' '
            inventory.add_food(food)
            break

def use_food(inventory, player, food):
    inventory.remove_food(food)
    # Replenish hunger by the amount of the food
    player.hunger += food.hunger

def place_gold(dungeon):
    height, width = len(dungeon), len(dungeon[0])
    while True:
        x, y = random.randint(1, width - 2), random.randint(1, height - 2)
        if dungeon[y][x] == ' ':
            dungeon[y][x] = '$'
            return x, y

def place_food(dungeon):
    height, width = len(dungeon), len(dungeon[0])
    while True:
        for food in food_items():
            if random.random() < food.rarity:
                # Generate random coordinates for the food item
                x = random.randint(1, width - 2)
                y = random.randint(1, height - 2)
                # Add the food item to the world
                dungeon[y][x] = food.symbol
                return x, y

def place_player(dungeon, room):
    while True:
        x, y = random.randint(1, len(dungeon[0]) - 2), random.randint(1, len(dungeon) - 2)
        if dungeon[y][x] == ' ' and (x, y) not in room.doors:
            return x, y

def remove_gold(dungeon, x, y):
    dungeon[y][x] = ' '

def draw_dungeon(stdscr, dungeon, player_x, player_y, score, doors, current_room_coords, monsters, food_items):
    stdscr.clear()

    for y, row in enumerate(dungeon):
        for x, cell in enumerate(row):
            if (x, y) in doors:
                stdscr.addch(y, x, '+', curses.color_pair(4))
            elif cell == '#':
                stdscr.addch(y, x, '#', curses.color_pair(1))
            elif cell == '$':
                stdscr.addch(y, x, '$', curses.color_pair(2))
            elif cell in [food.symbol for food in food_items()]:
                food = next((food for food in food_items() if food.symbol == cell), None)
                stdscr.addch(y, x, food.symbol, curses.color_pair(food.color))
            else:
                stdscr.addch(y, x, ' ')

    for monster in monsters:
        stdscr.addch(monster.y, monster.x, 'X', curses.color_pair(6))

    stdscr.addch(player_y, player_x, 'O', curses.color_pair(3))
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
    """
    Main function that runs the game loop for the overworld.

    Args:
        stdscr (curses.window): The curses window object.

    Returns:
        None
    """
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

    gold_positions = []
    for row in rooms:
        for room in row:
            gold_x, gold_y = place_gold(room.dungeon)
            gold_positions.append((gold_x, gold_y))

    food_positions = []
    for row in rooms:
        for room in row:
            food_x, food_y = place_food(room.dungeon)  # Call place_food() on the room object
            food_positions.append((food_x, food_y))
    

    monsters = [Monster(current_room.dungeon) for _ in range(3)]

    projectiles = []

    inventory = Inventory()  # Initialize an empty inventory
    player = Player(100)
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
        elif ord('1') <= key <= ord('9'):  # Check if a number key is pressed
            index = key - ord('1')  # Convert the key to an index
            if 0 <= index < len(inventory.invlist):  # Check if the index is valid
                item = inventory.invlist[index]
                # Use the item (you can add the logic here)
                inventory.invlist.pop(index)  # Remove the item from the inventory
                use_food(inventory, player, item)

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

        if (player_x, player_y) in gold_positions:
            score += 50
            gold_positions.remove((player_x, player_y))
            remove_gold(current_room.dungeon, player_x, player_y)
        

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
        ### code so that if a monster touches the player, it will get removed from the game area:
        for monster in monsters:
            if monster.x == player_x and monster.y == player_y:
                monsters.remove(monster)
                score -= 100
                break
        ### also make sure that a new monster is spawned randomly in the room if one of the monsters have disappeared that way:
        if (player_x, player_y) in food_positions:
            score += 10
            food_positions.remove((player_x, player_y))
            pick_up_food(current_room.dungeon, player_x, player_y, inventory)
        if len(monsters) < 3:
            monsters.append(Monster(current_room.dungeon))  # add a new monster to the room

        projectiles = new_projectiles
        
        player.hunger -= random.uniform(0.1, 0.2)
        draw_dungeon(stdscr, current_room.dungeon, player_x, player_y, score, current_room.doors, current_room_coords, monsters, food_items)

        # Draw the inventory at the bottom of the game area
        stdscr.addstr(len(current_room.dungeon) + 4, 0, "Inventory:")
        for i, item in enumerate(inventory.invlist):
            stdscr.addstr(len(current_room.dungeon) + 5, i * 10, f"{i+1}. {item.name}")
        
        # Display hunger level
        stdscr.addstr(len(current_room.dungeon) + 6, 0, f"Hunger Level: {int(player.hunger)}")
        stdscr.refresh()
        time.sleep(0.01)
        

if __name__ == "__main__":
    curses.wrapper(main)
