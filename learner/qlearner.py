__author__ = 'Torgeir'

class QLearner:

    def __init__(self, actions, alpha, gamma, epsilon):
        self.q = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_action(self, state):
        # Return the action the agent should take
        pass

    def update_q(self):
        pass
