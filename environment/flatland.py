
import random
import math

class World:

    def __init__(self, board=None, dimension=(10, 10), fdr=(0.3, 0.3)):
        self.dimension = dimension
        populate_now = False
        if board == None:
            self.board = [[0] * self.dimension[1] for x in range(self.dimension[0])]
            populate_now = True
        else:
            self.board = board
        self.board_length = len(self.board)

        # Distribute food/posion based on fdr, food = 1, posion = -1
        # TODO: more efficient way of doing this? distribute with some numpy shit while building grid?
        nof_cells = dimension[0] * dimension[1]
        self.nof_food = math.ceil(nof_cells * fdr[0])
        self.nof_poison = math.ceil((nof_cells - self.nof_food) * fdr[1])

        if populate_now:
            self._populate_world()

    def _populate_world(self):
        # Agent startpos is always 9,9, dont place anyting there
        for food in range(self.nof_food):
            x, y = self.get_random_pos()

            self.board[y][x] = 1

            if food < self.nof_poison:
                x, y = self.get_random_pos()
                self.board[y][x] = 2

    def get_cell_content(self, x, y):
        # TODO: handle torroidal
        realx = x % self.board_length
        realy = y % self.board_length
        return self.board[realy][realx]

    def get_random_pos(self):
        # TODO: replace with some numpy shit
        x, y = random.randint(0, (self.dimension[0] - 1)), random.randint(0, (self.dimension[0] - 1))
        while True:
            if self.board[y][x] == 0 and (y != 9 or x != 9):
                # Nothing is already placed and startposition of agent is not touched.
                break
            x, y = random.randint(0, self.dimension[0] - 1), random.randint(0, self.dimension[0] - 1)

        return x, y

    def __repr__(self):
        retval = ""
        for row in self.board:
            for val in row:
                retval += str(val) + " "
            retval += "\n"
        return retval

class Agent:

    def __init__(self, heading, world):
        """
        Heading = 0,1,2,3 (n,e,s,w)
        """
        self.start_pos = 9,9 # TODO: startposition is alwasy 9.9
        self.pos = self.start_pos
        self.heading = heading
        self.world = world
        # self.board_length = len(board)
        self.food_eaten = 0
        self.poison_eaten = 0
        self.visited = {}

        self._check_for_food_and_poison()


    def move(self, direction):
        """
        direction=f,l,r
        """

        if direction == "f" or direction == 0:
            self._move_forward() # No need to turn, move the way its heading
        elif direction == "l" or direction == 1:
            self.heading = (self.heading - 1) % 4
            self._move_forward()
        elif direction == "r" or direction == 2:
            self.heading = (self.heading + 1) % 4
            self._move_forward()

    def get_inputs(self):
        """
        Return list range(6) with 1 or 0 depending on food/posion in all
        """
        inputs = [0] * 6
        x = self.pos[0]
        y = self.pos[1]

        # inputs = [f,l,r,f,l,r], food - poison
        if self.heading == 0:
            inputs[0] = self._contains_food(x, y - 1)
            inputs[1] = self._contains_food(x - 1, y)
            inputs[2] = self._contains_food(x + 1, y)
            inputs[3] = self._contains_poison(x, y - 1)
            inputs[4] = self._contains_poison(x - 1, y)
            inputs[5] = self._contains_poison(x + 1, y)
        elif self.heading == 1:
            inputs[0] = self._contains_food(x + 1, y)
            inputs[1] = self._contains_food(x, y - 1)
            inputs[2] = self._contains_food(x, y + 1)
            inputs[3] = self._contains_poison(x + 1, y)
            inputs[4] = self._contains_poison(x, y - 1)
            inputs[5] = self._contains_poison(x, y + 1)
        elif self.heading == 2:
            inputs[0] = self._contains_food(x, y + 1)
            inputs[1] = self._contains_food(x + 1, y)
            inputs[2] = self._contains_food(x - 1, y)
            inputs[3] = self._contains_poison(x, y + 1)
            inputs[4] = self._contains_poison(x + 1, y)
            inputs[5] = self._contains_poison(x - 1, y)
        elif self.heading == 3:
            inputs[0] = self._contains_food(x - 1, y)
            inputs[1] = self._contains_food(x, y + 1)
            inputs[2] = self._contains_food(x, y - 1)
            inputs[3] = self._contains_poison(x - 1, y)
            inputs[4] = self._contains_poison(x, y + 1)
            inputs[5] = self._contains_poison(x, y - 1)
        return inputs


    def _move_forward(self):

        # move one cell in the direction it is headed
        if self.heading == 0:
            # north
            self.pos = (self.pos[0], (self.pos[1] - 1) % self.world.board_length)
        elif self.heading == 1:
            # east
            self.pos = ((self.pos[0] + 1) % self.world.board_length, self.pos[1])
        elif self.heading == 2:
            # south
            self.pos = (self.pos[0], (self.pos[1] + 1) % self.world.board_length)
        elif self.heading == 3:
            # west
            self.pos = ((self.pos[0] - 1) % self.world.board_length, self.pos[1])

        self._check_for_food_and_poison()

    def _check_for_food_and_poison(self):
        # Check for food and poison, keep track of where agent has been
        key = str(self.pos[0]) + "-" + str(self.pos[1])
        if key in self.visited.keys():
            return

        # board_val = self.board[self.pos[1]][self.pos[0]]
        board_val = self.world.get_cell_content(self.pos[0], self.pos[1])
        if board_val == 1:
            self.food_eaten += 1
        elif board_val == 2:
            self.poison_eaten += 1

        self.visited[key] = True

    def _contains_food(self, x, y): # TODO not tested
        key = str(x) + "-" + str(y)
        if key in self.visited.keys():
            return 0
        elif self.world.get_cell_content(x, y) == 1:
            return 1
        return 0

    def _contains_poison(self, x, y): # TODO not tested
        key = str(x) + "-" + str(y)
        if key in self.visited.keys():
            return 0
        elif self.world.get_cell_content(x, y) == 2:
            return 1
        return 0