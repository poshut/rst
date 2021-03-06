import unittest
from util import redirect_stdout
from battleground import Battleground
from robot import Robot
from searches.follow_right import FollowRight
from searches.follow_left  import FollowLeft
from searches.dfs import DFS


class TestRobot(unittest.TestCase):

    small_terrain = [
        [0,0],
        [0,0]
    ]

    small_terrain_repr = """
= _ 
_ _ 
"""

    empty_terrain = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]

    empty_terrain_repr = """
= _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
"""

    # Currently failing to follow_side
    blocked_terrain = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [3,3,3,3,3,3,3],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]

    blocked_terrain_repr = """
= _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
^ ^ ^ ^ ^ ^ ^ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
_ _ _ _ _ _ _ 
"""

    narrow_terrain = [
        [0,0,0,0,0,0,0],
        [0,3,3,3,3,3,3],
        [0,3,0,0,0,0,0],
        [0,3,0,3,3,3,0],
        [0,3,0,3,0,0,0],
        [0,3,0,3,0,3,3],
        [0,0,0,3,0,0,0]
    ]

    narrow_terrain_repr = """
= _ _ _ _ _ _ 
_ ^ ^ ^ ^ ^ ^ 
_ ^ _ _ _ _ _ 
_ ^ _ ^ ^ ^ _ 
_ ^ _ ^ _ _ _ 
_ ^ _ ^ _ ^ ^ 
_ _ _ ^ _ _ _ 
"""


    test_behaviour_table = [
        {
            "terrain": small_terrain,
            "goal": None,
            "solvable": True,
            "moves_left": 2,
            "moves_right": 2
        },
        {
            "terrain": small_terrain,
            "goal": (1,0),
            "solvable": True,
            "moves_left": 3,
            "moves_right": 1,
        },
        {
            "terrain": empty_terrain,
            "goal": None,
            "solvable": True,
            "moves_left": 12,
            "moves_right": 12
        },
        {
            "terrain": empty_terrain,
            "goal": (6,0),
            "solvable": True,
            "moves_left": 18,
            "moves_right": 6,
        },
        {
            "terrain": blocked_terrain,
            "goal": None,
            "solvable": False,
            "moves_left": 16,
            "moves_right": 16,
        },
        {
            "terrain": narrow_terrain,
            "goal": None,
            "solvable": True,
            "moves_left": 36,
            "moves_right": 24,
        }
    ]

    test_output_table = [
        {
            "terrain": small_terrain,
            "repr": small_terrain_repr
        },
        {
            "terrain": empty_terrain,
            "repr": empty_terrain_repr
        },
        {
            "terrain": blocked_terrain,
            "repr": blocked_terrain_repr
        }
    ]

    def test_robot_behaviour(self):

        for entry in TestRobot.test_behaviour_table:
            if entry["goal"] is None and entry["solvable"]:
                goal = (len(entry["terrain"]) - 1, len(entry["terrain"]) - 1)
            elif entry["goal"] is None:
                goal = (0,0)
            else:
                goal = entry["goal"]

            battleground = Battleground(terrain=entry["terrain"])
            robot = Robot(battleground, search=Robot.SEARCH_DFS, goal=entry["goal"])
            self.assertEqual(robot.run(), entry["solvable"])
            self.assertEqual(goal, (robot.x, robot.y))

            battleground = Battleground(terrain=entry["terrain"])
            robot = Robot(battleground, search=Robot.SEARCH_FOLLOW_LEFT, goal=entry["goal"])
            self.assertEqual(robot.run(), entry["solvable"])
            self.assertEqual(robot.moves(), entry["moves_left"])
            self.assertEqual(goal, (robot.x, robot.y))

            battleground = Battleground(terrain=entry["terrain"])
            robot = Robot(battleground, search=Robot.SEARCH_FOLLOW_RIGHT, goal=entry["goal"])
            self.assertEqual(robot.run(), entry["solvable"])
            self.assertEqual(robot.moves(), entry["moves_right"])
            self.assertEqual(goal, (robot.x, robot.y))

    def test_robot_output(self):

        for entry in TestRobot.test_output_table:
            with redirect_stdout() as file:
                battleground = Battleground(terrain=entry["terrain"])
                robot = Robot(battleground)
                print(robot)
            with open(file, 'r') as f:
                self.assertEqual(f.read().strip(), entry["repr"].strip())

            with redirect_stdout() as file:
                battleground = Battleground(terrain=entry["terrain"])
                robot = Robot(battleground, display=Robot.DISPLAY_COLOR)
                robot.render()
            with open(file, 'r') as f:
                self.assertEqual(f.read().strip(), entry["repr"].strip())
