__author__ = 'Torgeir'

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

        for k in range(self.nof_iterations):
            # TODO: Restart scenario

            while not self.agent.is_done():
                # Select action to do
                action = self.q_learner.get_action()

                # Update game
                board_value = self.agent.move(action)

                # State after doing action in game
                state = self.agent.get_state()

                # Reward after doing action in game
                # reward = get_reward()

                # Update q-values
                self.q_learner.update_q(state, action, reward)


import sys

if __name__ == "__main__":

    # TODO: take parameters from commandline

    # Can sepcify path here
    buffer = FileReaderAndFormatter()

    w = World(buffer.board, (buffer.w, buffer.h))
    a = Agent(w, (buffer.x, buffer.y), buffer.n)

    gui = FlatlandSimulation(buffer.board, (buffer.w, buffer.h), a)
    gui.mainloop()


    sys.exit()

    # TODO: take these as parameters?
    alpha = 0.1
    gamma = 0.1
    epsilon = 0.1
    nof_iterations = 100

    ql = QLearner(["n", "e", "s", "w"], alpha, gamma, epsilon)


    app = FlatlandQLearner(w, a, ql, nof_iterations)
    app.run()
