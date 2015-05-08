__author__ = 'Torgeir'

import sys

import logging

from environment.flatland import World, Agent
from filereader.filereader import FileReaderAndFormatter
from learner.qlearner import QLearner
from visualization.simulation import FlatlandSimulation

class FlatlandQLearner:
    # blahblah description

    def __init__(self, world, agent, q_learner, nof_iterations):
        self.world = world
        self.agent = agent
        self.q_learner = q_learner
        self.nof_iterations = nof_iterations

    def run(self):
        # TODO: main loop of the flatland q-learner
        logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)

        for k in range(self.nof_iterations):

            print("K: ", k, ", food eaten: ", str(self.agent.food_eaten), ", poison eaten: ", str(self.agent.poison_eaten), ", steps: " + str(self.agent.steps_taken))
            # logging.info("---- " + str(k) + " ------")

            # Reset scenario
            self.restart_scenario()

            state = self.agent.get_state()

            while not self.agent.is_done():

                # logging.info(str(k) + "- Start while")

                # Select action to do
                action = self.q_learner.get_action(state)
                # print("- action found")
                # logging.info(str(k) + "- Action found")
                # Update game
                board_value = self.agent.move(action)
                # print("- Agent moved")
                # logging.info(str(k) + "- Agent moved")

                # Remember previous state, used in updating the Q value
                state_previous = state

                # State after doing action in game
                state = self.agent.get_state()
                # print("- State retrieved")
                # logging.info(str(k) + "- State retrieved")

                # Reward after doing action in game
                reward = self.get_reward(board_value)
                # print("- Reward gotten")
                # logging.info(str(k) + "- Reward gotten")

                # Update q-values
                self.q_learner.update_q(state, state_previous, action, reward)
                # print("- Updated q")
                # logging.info(str(k) + "- Updated q")

        # Visualize the trained agent
        # self._print_q()

        # Reset world and agent before visualizing
        self.world._init_foods()
        self.agent.reset()

        print("Starting Visualization...")

        gui = FlatlandSimulation(self.world.board, (self.world.dimension[0], self.world.dimension[1]), self.agent, self.q_learner)
        gui.mainloop()
        sys.exit()

    def get_reward(self, board_value):
        # TODO: Improve
        if board_value > 0:
            return 1
        if board_value == -1:
            return -1
        if self.agent.is_done():
            return 5
        else:
            return -0.01

    def restart_scenario(self):
        self.world._init_foods()
        self.agent.reset()

    def _print_q(self):
        print("Size: ", len(self.q_learner.q))
        for k, v in self.q_learner.q.items():
            print(str(k) + ": " + str(v))

if __name__ == "__main__":

    # TODO: take parameters from commandline

    # Can sepcify path here
    buffer = FileReaderAndFormatter()

    w = World(buffer.board, (buffer.w, buffer.h))
    a = Agent(w, (buffer.x, buffer.y), buffer.n)

    # TODO: take these as parameters?
    alpha = 0.1
    gamma = 0.1
    epsilon = 0.1
    nof_iterations = 3000

    ql = QLearner([0, 1, 2, 3], alpha, gamma, epsilon) # actions: n, e, s, w

    # gui = FlatlandSimulation(buffer.board, (buffer.w, buffer.h), a, ql)
    # gui.mainloop()
    # sys.exit()

    app = FlatlandQLearner(w, a, ql, nof_iterations)
    app.run()
