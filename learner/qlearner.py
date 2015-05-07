__author__ = 'Torgeir'

import random

class QLearner:

    # TODO: too spesific, make more general

    def __init__(self, actions, alpha, gamma, epsilon):
        self.q = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_action(self, state):
        # TODO: Do not return random. IMPROVE
        return random.choice(self.actions)

    def get_q(self, state, action):
        # Return the value that corresponds to the state, action pair.
        # State should be hashable

        # Return 0.0 if no entry for specified query exist.
        return self.q.get((state, action), 0.0)

        # return self.q[(state, action)]

    def set_q(self, state, action, value):
        self.q[(state, action)] = value

    def update_q(self, state_current, state_previous, action, reward):
        # TODO: Should be tested!

        # Create key
        # update_key = (state_previous, action)

        # Do calculation
        q_temp = self.get_q(state_previous, action)

        # print("q_temp", q_temp)
        # print("a", self.alpha)
        # print("r", reward)
        # print("g", self.gamma)
        # print("best action", self._get_best_action(state_current))

        temp = self.alpha * (reward + (self.gamma * self._get_best_action(state_current)) - q_temp)
        q_value = q_temp + temp

        # Update q map
        self.set_q(state_previous, action, q_value)
        # self.q[update_key] = q_value

    def _get_best_action(self, state):
        # Return the highest q-value in state
        return max([self.get_q(state, action) for action in self.actions])

