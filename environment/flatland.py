
import random
import math

class World:

    def __init__(self, board, dimension):
        self.dimension = dimension
        self.board = board

    def get_cell_content(self, x, y):
        # Return content of cell. Supports world wrap-around.
        realx = x % self.dimension[0]
        realy = y % self.dimension[1]
        return self.board[realy][realx]

    def __repr__(self):
        retval = ""
        for row in self.board:
            for val in row:
                retval += str(val) + " "
            retval += "\n"
        return retval

class Agent:

    def __init__(self, world, start_position, goal_position):
        """
        Heading = 0,1,2,3 (n,e,s,w)
        """
        self.start_pos = start_position
        self.pos = self.start_pos
        self.goal_position = goal_position
        self.world = world

        # TODO: If same agent-instance for all learning scenarios, reset these
        self.visited = {}
        self.poison_eaten = 0
        self.steps_taken = 0

        # Update the visited map
        self._check_for_food_and_poison()

    def reset(self):
        # Can use same agent in many scenarios by resetting between each.

        self.pos = self.start_pos
        self.visited = {}
        self.poison_eaten = 0
        self.steps_taken = 0

    def move(self, direction):
        # direction = n,e,s,w / 0,1,2,3
        # Returns board content in the cell it arrives at.

        if direction == "n" or direction == 0:
             # north
            self.pos = (self.pos[0], (self.pos[1] - 1) % self.world.dimension[1])
        elif direction == "e" or direction == 1:
            # east
            self.pos = ((self.pos[0] + 1) % self.world.dimension[0], self.pos[1])
        elif direction == "s" or direction == 2:
            # south
            self.pos = (self.pos[0], (self.pos[1] + 1) % self.world.dimension[1])
        elif direction == "w" or direction == 3:
           # west
            self.pos = ((self.pos[0] - 1) % self.world.dimension[0], self.pos[1])

        self.steps_taken += 1

        return self._check_for_food_and_poison()

    def _check_for_food_and_poison(self):
        # Check for food and poison, keep track of where agent has been
        key = str(self.pos[0]) + "-" + str(self.pos[1])
        if key in self.visited.keys():
            return

        # Get content of agents position and return it
        board_val = self.world.get_cell_content(self.pos[0], self.pos[1])
        self.visited[key] = True
        return board_val

    # TODO: REMOVE THESE? --------------------------------------------------------
    def _contains_food(self, x, y):
        # Only used internally, and on cells not visited
        key = str(x) + "-" + str(y)
        if key in self.visited.keys():
            return 0
        elif self.world.get_cell_content(x, y) == 1:
            return 1
        return 0

    def _contains_poison(self, x, y):
        # Only used internally, and on cells not visited
        key = str(x) + "-" + str(y)
        if key in self.visited.keys():
            return 0
        elif self.world.get_cell_content(x, y) == 2:
            return 1
        return 0