import random
import curses
import time
import string

def generate_object_definition():
    nouns = ["donut", "banana", "feather", "cheese", "potato", "kitten", "rocket", "umbrella", "guitar", "book", "tree", "lighthouse", "star", "ocean", "dragon", "flower", "moon", "diamond", "robot", "apple", "candle", "carrot", "fish", "mailbox", "key", "cloud", "swan"]
    verbs = ["dances with", "talks to", "teleports near", "tickles", "sings to", "giggles at", "flies around", "plays with", "jumps over", "reads to", "climbs", "admires", "explore", "paints", "transforms", "whispers to", "rides", "discovers", "creates", "befriends", "chases", "gazes at", "hugs", "sleeps near", "surprises", "follows", "dances with"]
    adjectives = ["mysterious", "glowing", "invisible", "quantum", "singing", "adorable", "shimmering", "sparkling", "enchanted", "majestic", "colorful", "mysterious", "radiant", "magical", "whimsical", "playful", "fantastic", "ethereal", "mystical", "charming", "gentle", "brilliant", "silent", "peaceful", "curious", "graceful", "joyful"]

    noun = random.choice(nouns)
    verb = random.choice(verbs)
    adjective1 = random.choice(adjectives)
    adjective2 = random.choice(adjectives)

    return f"The {adjective1} {adjective2} {noun} {verb} the {random.choice(adjectives)} {random.choice(adjectives)} {random.choice(nouns)}."

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    # Initialize colors
    curses.start_color()
    for i in range(1, 8):  # Exclude color 0 (black)
        curses.init_pair(i, i, 0)  # Use default background color

    height, width = stdscr.getmaxyx()

    # Check if the terminal size is too small
    if height < 8 or width < 30:
        stdscr.addstr(0, 0, "Terminal window too small. Please enlarge the terminal.")
        stdscr.refresh()
        stdscr.getch()
        return

    center_y, center_x = height // 2, width // 2

    # Initialize the robot, kitten, and objects positions
    robot_y, robot_x = center_y, center_x

    num_objects = 20  # Including the kitten as one of the objects
    objects = [(random.randint(1, height - 2), random.randint(1, width - 2)) for _ in range(num_objects)]
    object_descriptions = [generate_object_definition() for _ in range(num_objects)]
    object_colors = [random.randint(1, 7) for _ in range(num_objects)]  # Use colors 1 to 7 for variety
    object_symbols = [random.choice(string.punctuation) for _ in range(num_objects)]

    # Main game loop
    while True:
        stdscr.clear()

        # Draw the robot and objects with colors and symbols
        stdscr.addch(robot_y, robot_x, 'R', curses.color_pair(1))

        for (obj_y, obj_x), obj_description, obj_color, obj_symbol in zip(objects, object_descriptions, object_colors, object_symbols):
            stdscr.addch(obj_y, obj_x, obj_symbol, curses.color_pair(obj_color))

        # Draw borders
        for i in range(width - 1):  # Adjust loop boundary
            stdscr.addch(0, i, '-')
            stdscr.addch(height - 1, i, '-')
        for i in range(height):
            stdscr.addch(i, 0, '|')
            stdscr.addch(i, width - 2, '|')  # Adjust loop boundary

        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Move the robot based on user input
        if key == curses.KEY_UP and robot_y > 1:
            robot_y -= 1
        elif key == curses.KEY_DOWN and robot_y < height - 2:
            robot_y += 1
        elif key == curses.KEY_LEFT and robot_x > 1:
            robot_x -= 1
        elif key == curses.KEY_RIGHT and robot_x < width - 2:
            robot_x += 1

        # Change symbols and colors for all objects
        for i in range(num_objects):
            object_symbols[i] = random.choice(string.punctuation)
            object_colors[i] = random.randint(1, 7)

        # Check if the robot has found an object
        if (robot_y, robot_x) in objects:
            index = objects.index((robot_y, robot_x))
            description = object_descriptions[index]
            stdscr.addstr(0, 0, f"You found: {description}", curses.color_pair(object_colors[index]))
            stdscr.refresh()
            time.sleep(2)  # Display the description for 2 seconds
            stdscr.clear()

            # Check if the found object is the kitten
            if "kitten" in description:
                stdscr.addstr(height // 2, width // 2 - 5, "You found the kitten! Game Over.", curses.color_pair(1))
                stdscr.refresh()
                stdscr.getch()  # Wait for user input before exiting
                return  # Exit the game

curses.wrapper(main)

