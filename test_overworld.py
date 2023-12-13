import unittest
from unittest.mock import patch
import curses
import time
import random

from overworld import main

class TestOverworld(unittest.TestCase):
    def setUp(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.stdscr.timeout(100)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def tearDown(self):
        curses.endwin()

    @patch('builtins.input', side_effect=['q'])
    def test_main_quit(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_once_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_movement(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), 'q'])
    def test_main_inventory(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), 'q'])
    def test_main_inventory_item_usage(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_room_transition(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_gold_collection(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_monster_encounter(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_food_collection(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_monster_spawn(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_projectile_movement(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_player_hunger(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

    @patch('builtins.input', side_effect=[curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 'q'])
    def test_main_dungeon_draw(self, mock_input):
        main(self.stdscr)
        mock_input.assert_called_with('q')

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
import curses
import time
import random

from overworld import main
from overworld import Inventory

import unittest
from overworld import Room

class TestRoom(unittest.TestCase):
    def test_navigable_room(self):
        height = 10
        width = 10
        num_iterations = 5
        seed = 12345

        room = Room(height, width, num_iterations, seed)

        # Verify that the generated dungeon is navigable
        for y in range(height):
            for x in range(width):
                self.assertNotEqual(room.dungeon[y][x], '#', f"Cell at ({x}, {y}) is not navigable")

if __name__ == '__main__':
    unittest.main()