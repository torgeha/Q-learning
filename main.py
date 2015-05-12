__author__ = 'Torgeir'

import sys
import argparse
import logging
import time

from environment.flatland import World, Agent
from filereader.filereader import FileReaderAndFormatter
from learner.qlearner import QLearner
from visualization.simulation import FlatlandSimulation

class FlatlandQLearner:

    def __init__(self, world, agent, q_learner, nof_iterations):
        self.world = world
        self.agent = agent
        self.q_learner = q_learner
        self.nof_iterations = nof_iterations

    def run(self):
        # Main loop of the flatland q-learner
        logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)

        # Time the run
        start = time.time()

        # Epsilon gradually descends, find how often
        reduce_e_at = self.nof_iterations / 10

        for k in range(self.nof_iterations):

            # Print progression to console
            print("K: ", k,
                  ",\t food eaten: ", str(self.agent.food_eaten),
                  ",\t poison eaten: ", str(self.agent.poison_eaten),
                  ",\t epsilon: ", str(self.q_learner.epsilon),
                  ",\t steps: " + str(self.agent.steps_taken))

            # Find out if epsilon should be reduced
            if k % reduce_e_at == 0:
                if self.q_learner.epsilon < 0.002:
                    self.q_learner.epsilon = 0.0
                else:
                    self.q_learner.epsilon /= 2.0

            # Reset scenario
            self.restart_scenario()

            state = self.agent.get_state()

            while not self.agent.is_done():

                # Select action to do
                action = self.q_learner.get_action(state)

                # Update game
                board_value = self.agent.move(action)

                # Remember previous state, used in updating the Q value
                state_previous = state

                # State after doing action in game
                state = self.agent.get_state()

                # Reward after doing action in game
                reward = self.get_reward(board_value)

                # Update q-values
                self.q_learner.update_q(state, state_previous, action, reward)

        # Visualize the trained agent
        # self._print_q()

        # Print runtime
        end = time.time()
        print("Runtime: ", end - start, " s. or ", ((end - start) / 60), " min.")

        # Reset world and agent before visualizing
        self.world._init_foods()
        self.agent.reset()

        print("Starting Visualization...")

        gui = FlatlandSimulation(self.world.board, (self.world.dimension[0], self.world.dimension[1]), self.agent, self.q_learner)
        gui.mainloop()
        sys.exit()

    def get_reward(self, board_value):
        if board_value > 0:
            return 1
        if board_value == -1:
            return -1
        # if self.agent.is_done():
        #     return 5
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

    # Can sepcify path here
    buffer = FileReaderAndFormatter()

    w = World(buffer.board, (buffer.w, buffer.h))
    a = Agent(w, (buffer.x, buffer.y), buffer.n)

    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1
    trace_decay = 0.5
    backup_states = 6
    nof_iterations = 2000

    parser = argparse.ArgumentParser()

    # Add arguments here
    parser.add_argument("-a", help="Learning rate", type=float)
    parser.add_argument("-g", help="Discount rate", type=float)
    parser.add_argument("-e", help="Exploration likelihood", type=float)
    parser.add_argument("-td", help="Trace decay factor", type=float)
    parser.add_argument("-bs", help="States to be backed up", type=int)
    parser.add_argument("-i", help="Number of iterations", type=int)
    args = parser.parse_args()

    if args.a:
        alpha=args.a
    if args.g:
        gamma=args.g
    if args.e:
        epsilon=args.e
    if args.td:
        trace_decay = args.td
    if args.bs:
        backup_states = args.bs
    if args.i:
        nof_iterations=args.i

    ql = QLearner([0, 1, 2, 3], alpha, gamma, epsilon, trace_decay, backup_states) # actions: n, e, s, w

    # gui = FlatlandSimulation(buffer.board, (buffer.w, buffer.h), a, ql)
    # gui.mainloop()
    # sys.exit()

    app = FlatlandQLearner(w, a, ql, nof_iterations)
    app.run()
