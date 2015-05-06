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
                self.agent.move(action)

                # State after doing action in game
                state = self.agent.get_state()

                # Reward after doing action in game
                # reward = get_reward()

                # Update q-values
                self.q_learner.update_q(state, action, reward)



if __name__ == "__main__":

    # TODO: take parameters from commandline
    app = FlatlandQLearner()
    app.run()
