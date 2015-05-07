
import collections

class World:

    def __init__(self, board, dimension):
        self.dimension = dimension
        self.board = board
        self.foods_eaten = None # Ordered Dict
        self._init_foods()

    def _init_foods(self):
        # Populate map with all food on board. False since it is not eaten yet.
        # TODO: can use id of food instead
        d = {}
        for y in range(self.dimension[1]):
            for x in range(self.dimension[0]):
                if self.get_cell_content(x, y) > 0:
                    key = str(x) + "-" + str(y)
                    d[key] = False
        self.foods_eaten = collections.OrderedDict(sorted(d.items(), key=lambda t: t[0]))

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

    def __init__(self, world, start_position, total_food):
        """
        Heading = 0,1,2,3 (n,e,s,w)
        """
        self.start_pos = start_position
        self.pos = self.start_pos
        self.world = world

        self.total_food = total_food
        self.visited = {}
        self.poison_eaten = 0
        self.food_eaten = 0
        self.steps_taken = 0

        # Update the visited map
        self._check_for_food_and_poison()

    def reset(self):
        # Can use same agent in many scenarios by resetting between each.

        self.pos = self.start_pos
        self.visited = {}
        self.poison_eaten = 0
        self.food_eaten = 0
        self.steps_taken = 0

    def is_done(self):
        # Return true if at start_position and all food is eaten
        return self.food_eaten == self.total_food and self.pos == self.start_pos

    def get_state(self):
        # Return current state. State consist of position and food eaten
        s = ""
        s += str(self.pos[0]) + "-" + str(self.pos[1]) + ":"
        # print(self.world.foods_eaten)
        for v in self.world.foods_eaten.values():
            if v:
                s += "1"
            elif not v:
                s += "0"
        return s

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

        board_value = self._check_for_food_and_poison()
        self._update_stats(board_value)
        return board_value

    def _update_stats(self, board_value):
        # At start position
        if board_value == -2:
            return
        # Poison eaten
        elif board_value == -1:
            self.poison_eaten += 1
        # Empty cell
        elif board_value == 0:
            return
        # Food eaten
        elif board_value > 0:
            self.food_eaten += 1
            key = str(self.pos[0]) + "-" + str(self.pos[1])
            self.world.foods_eaten[key] = True


    def _check_for_food_and_poison(self):
        # Check for food and poison, keep track of where agent has been
        key = str(self.pos[0]) + "-" + str(self.pos[1])
        if key in self.visited.keys():
            return 0

        # Get content of agent's position and return it
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