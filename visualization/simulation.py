import threading
import time
import sys
import collections
import random
import numpy as np
from tkinter import *
from collections import deque
from phenotypes import FlatlandPhenotype
from ann import Network


class FlatlandSimulation(Tk):

    def __init__(self, phenotype_weights, board, agent):
        Tk.__init__(self)

        # Arrows should not work if algorithm mode
        # self.bind_all("<Left>", self.move)
        # self.bind_all("<Up>", self.move)
        # self.bind_all("<Down>", self.move)
        # self.bind_all("<Right>", self.move)
        self.bind_all("<q>", self.quit)
        self.bind_all("<Escape>", self.quit)

        self.ann = Network([6,0,3])

        self.board = board
        self.agent = agent
        self.phenotype_weights = phenotype_weights
        self.refresh_rate = 1

        # Init canvas
        self.canvas_flatland = CanvasFlatland(parent=self, width=800, height=800, bg="#BDAD9E")
        self.canvas_flatland.grid(row=0, column=0, rowspan=3, columnspan=4, sticky=W + N, padx=5, pady=5)

        # Start button
        run_btn = Button(self, text="Run", width=10, borderwidth=4, padx=5, pady=5, font=("Helvetica", 12), command=self.start_simulation)
        run_btn.grid(row=6, column=0, rowspan=1, columnspan=2, sticky=W)

        # Speed slider
        # TODO add slider that controlls refresh rate!
        self.refresh_slider = Scale(self, from_=0, to=999, width=20, orient=HORIZONTAL, command=self.set_refresh_value)
        self.refresh_slider.set(self.refresh_rate)
        self.refresh_slider.grid(row=6, column=2, rowspan=1, columnspan=4, sticky=E)


        self.moves_queue = deque() # TODO is this the right data structure?

        # print(self.model)

    def set_refresh_value(self, value):
        self.refresh_rate = 1000 - self.refresh_slider.get()

    def start_simulation(self):
        # TODO: called when run button is pressed, starts the simulation
        print("Simulation started")

        self.canvas_flatland.start_drawing() # Will draw until draw_queue is empty
        self.canvas_flatland.stop_drawing()

    def quit(self, event):
        sys.exit(0)

    # def solve_2048(self):
    #     """
    #     Called when the minimax algorithm should start.
    #     """
    #
    #     depth = 4
    #
    #     def callback():
    #         ct = int(round(time.time() * 1000))
    #         self.canvas_flatland.start_drawing()
    #         s = Search(depth)
    #         s.subscribe(self)
    #         s.minimax_search()
    #         self.canvas_flatland.stop_drawing()
    #
    #         # Calculate runtime
    #         dt = int(round(time.time() * 1000))
    #         print("Runtime: ", (dt - ct) / 1000, "secs")
    #
    #     t = threading.Thread(target=callback)
    #     t.daemon = True
    #     t.start()


    # def move(self, event=None):
    #     """
    #     Get the keycode for the arrow pressed. Used to play manually.
    #     """
    #
    #     dir = repr(event.keycode)
    #
    #     if dir == '37':
    #         dir = "left"
    #     elif dir == '38':
    #         dir = "up"
    #     elif dir == '39':
    #         dir = "right"
    #     elif dir == '40':
    #         dir = "down"
    #     else:
    #         return
    #     # print(dir)
    #
    #     cells = self.model.move(dir)
    #     # print(cells)
    #     print(self.model)
    #
    #     self.canvas_flatland.set_board(cells)
    #
    # def notify(self, node):
    #     """
    #     Method needed as an observer. Called from the Observable when a property_change has occurred.
    #     """
    #     self.moves_queue.append(node)

class CanvasFlatland(Canvas):
    """
    The canvas inside the main frame. Specifies how the cells in the board is drawn.
    The grid is only drawn once, later calls to update the gui only updates the components.
    """

    def __init__(self, parent, width, height, bg):

        self.timesteps = 60
        self.width = width
        self.height = height
        self.parent = parent
        # self.cells = []
        # self.values = []
        self.graphics_dict = {}  # x0y0: (rect, text)

        self.agent_last_pos = parent.agent.pos

        self.offset = 3
        self.size = 10
        self.cell_size = (self.width) / self.size

        # self.colors = {0: "#CBC2B3",
        #                2: ("#EEE6DB", "#767267", 40),
        #                4: ("#ECE0C8", "#767267", 40),
        #                8: ("#EFB27C", "#FDFAF3", 40),
        #                16: ("#F39768", "#FDFAF3", 40),
        #                32: ("#F37D63", "#FDFAF3", 40),
        #                64: ("#F46042", "#FDFAF3", 40),
        #                128: ("#EACF76", "#FDFAF3", 35),
        #                256: ("#ECC85A", "#FDFAF3", 35),
        #                512: ("#E8BE4E", "#FDFAF3", 35),
        #                1024: ("#CCA545", "#FDFAF3", 30),
        #                2048: ("#BC870B", "#FDFAF3", 30),
        #                4196: ("#BA8B99", "#FDFAF3", 30)} # Dict with colors {int value : String color, string color}

        self.colors = {0: "#CBC2B3",
                       1: "green",
                       2: "red",
                       3: ("blue", {0:"▲", 1:"▶", 2:"▼", 3:"◀"})}


        super().__init__(parent, width=width, height=height, bg=bg, borderwidth=3, relief="sunken")
        self.draw_grid()

    def start_drawing(self):
        self.stopped = False
        self.repaint()

    def stop_drawing(self):
        self.stopped = True
        print("Done")

    def repaint(self):
        """
        Draw loop. Called every 'refresh-rate' milliseconds
        """

        inputs = self.parent.agent.get_inputs()

        outputs = self.parent.ann.feedforward3(inputs, self.parent.phenotype_weights)

        choice = self._make_choice(outputs)

        self.parent.agent.move(choice)

        # set cell to 0 where agent has been
        self.set_cell(self.agent_last_pos[0], self.agent_last_pos[1], 0)
        self.set_cell(self.parent.agent.pos[0], self.parent.agent.pos[1], 3)
        self.agent_last_pos = self.parent.agent.pos

        refresh_rate = self.parent.refresh_rate
        if not self.stopped or self.timesteps > 0:
            self.timesteps -= 1
            self.after(refresh_rate, self.repaint)
        else:
            print("Drawing has stopped")
            print("food: ", self.parent.agent.food_eaten)
            print("poison: ", self.parent.agent.poison_eaten)

    def _make_choice(self, outputs):
            l = collections.Counter(outputs)
            # print("outputs", outputs, "l", l)
            maximum = np.argmax(outputs)
            for occ in l.values():
                if occ == 3:
                    return 0
            return maximum

    def set_board(self, cells):
        rg = range(len(cells))
        for x in rg:
            for y in rg:
                self.set_cell(x, y, cells[y][x])

    def set_cell(self, x, y, value):
        """
        Set value for cell x, y
        """

        rect, text = self.graphics_dict[str(x) + str(y)]

        # Special case for drawing agent
        if value == 3:
            self.itemconfig(rect, fill=self.colors[value][0])
            self.itemconfig(text, fill="#767267", text=self.colors[value][1][self.parent.agent.heading], font=("Consolas", 40))
            return

        self.itemconfig(rect, fill=self.colors[value])

    def draw_grid(self):
        """
        Only called once for every puzzle instance, populates the grid
        """

        # print("createing this:", self.parent.board)

        # Populate graphics dict
        for y in range(self.size):
            for x in range(self.size):
                # TODO: can i remove self.drawtext?
                self.graphics_dict[str(x) + str(y)] = (self.draw_cell(x, y), self.draw_text(x, y))
                # self.graphics_dict[str(x) + str(y)] = (self.draw_cell(x, y))

        # Set board values on grid
        for x in range(len(self.parent.board)):
            for y in range(len(self.parent.board)):
                self.set_cell(x, y, self.parent.board[y][x])

        # Set agent initial position
        self.set_cell(self.parent.agent.start_pos[0], self.parent.agent.start_pos[1], 3)

    def draw_cell(self, x, y):
        # Check if given params are inside grid dimensions
        if x > self.width or y > self.height:
            raise Exception("Parameters out of grid bound! Given params: X:" +
                            str(x) + " Y: " + str(y))

        pix_x0 = x * self.cell_size
        pix_y0 = y * self.cell_size
        pix_x1 = self.cell_size + pix_x0
        pix_y1 = self.cell_size + pix_y0


        return self.create_rectangle(pix_x0 + (self.offset + 2), pix_y0 + (self.offset + 2), pix_x1, pix_y1, fill=self.colors[0], outline="#BBADA0", width=self.offset)

    def draw_text(self, x, y):
        # Check if given params are inside grid dimensions
        if x > self.width or y > self.height:
            raise Exception("Parameters out of grid bound! Given params: X:" +
                            str(x) + " Y: " + str(y))

        pix_x0 = x * self.cell_size
        pix_y0 = y * self.cell_size

        return self.create_text(pix_x0 + (self.cell_size / 2), pix_y0 + (self.cell_size / 2))

#----------------------------------
# START A RANDOM SCENARIO
#-------------------------

from flatland import World, Agent

# board = [[2, 1, 2, 2, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 1, 1, 0, 1, 1, 2], [1, 1, 2, 0, 1, 0, 0, 1, 1, 1], [1, 0, 0, 2, 0, 0, 2, 0, 0, 0], [2, 1, 0, 0, 2, 0, 0, 2, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 1, 2, 0, 0, 0, 0, 2, 1, 1], [0, 2, 0, 0, 0, 2, 1, 2, 1, 0], [1, 2, 1, 1, 0, 0, 2, 1, 0, 1], [1, 1, 0, 0, 2, 2, 0, 2, 1, 0]]
#
# w1 = World(board)
# w2 = World(board)

# print("b1")
# print(w1.board)
# print("----")
# print("b2")
# print(w2.board)


# a = Agent(0, w1)
# a2 = Agent(0, w2)
# print(w1.board == w2.board)
# gui = FlatlandSimulation([[0.587345869461,-0.0876158748166,0.448576913051,-0.796555177028,1.13549922992,-0.910921610781],[1.62629024948,0.935821573645,1.33603285328,1.21476052906,-1.70501706972,-1.10118719911],[0.332941085804,-0.152751334073,3.11515867017,0.171148745604,-1.25946859328,-1.3080164473]], w2.board, a2) # cOPY PASTE best weights!
# gui.mainloop()
# [[0.587345869461,-0.0876158748166,0.448576913051,-0.796555177028,1.13549922992,-0.910921610781],[1.62629024948,0.935821573645,1.33603285328,1.21476052906,-1.70501706972,-1.10118719911],[0.332941085804,-0.152751334073,3.11515867017,0.171148745604,-1.25946859328,-1.3080164473]]