__author__ = 'Torgeir'

import random
import numpy as np
import logging

class QLearner:

    # TODO: too spesific, make more general

    def __init__(self, actions, alpha, gamma, epsilon):
        self.q = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    # def get_action(self, state):
    #     # Use the q-values for this state as odds of choosing that action.
    #     # High q-value gives greater chance for that action being chosen.
    #
    #     # # Get all q-values
    #     # odds = [self.get_q(state, action) for action in self.actions]
    #     # # Normalize
    #     # odds_sum = sum(odds)
    #     # if odds_sum != 0:
    #     #     for o in odds:
    #     #         o /= odds_sum
    #     # else:
    #     #     odds = [0.25, 0.25, 0.25, 0.25]
    #     # # Choose
    #     # action = np.random.choice(self.actions, p=odds)
    #
    #     # TODO: Is only greedy
    #     # Choose a weighted random action if random < epsilon
    #     q_values = [self.get_q(state, a) for a in self.actions]
    #     max_q = max(q_values)
    #     if random.random() < self.epsilon:
    #         best_actions = [i for i in range(len(self.actions)) if q_values[i] == max_q]
    #         i = random.choice(best_actions)
    #     else:
    #         i = q_values.index(max_q)
    #     action = self.actions[i]
    #     return action

        # # TODO: Strictly greedy, must improve
        # q_values = [self.get_q(state, a) for a in self.actions]
        # max_q = max(q_values)
        # count = q_values.count(max_q)
        # if count > 1:
        #     best_q = [i for i in range(len(self.actions)) if q_values[i] == max_q]
        #     i = random.choice(best_q)
        # else:
        #     i = q_values.index(max_q)
        #
        # action = self.actions[i]
        # return action

    def get_action(self, state, return_q=False):
        q_values = [self.get_q(state, a) for a in self.actions]
        max_q = max(q_values)

        if random.random() < self.epsilon:
            #action = random.choice(self.actions)
            min_q = min(q_values); mag = max(abs(min_q), abs(max_q))
            q_values = [q_values[i] + random.random() * mag - .5 * mag for i in range(len(self.actions))] # add random values to all the actions, recalculate max_q
            max_q = max(q_values)

        count = q_values.count(max_q)
        if count > 1:
            best = [i for i in range(len(self.actions)) if q_values[i] == max_q]
            i = random.choice(best)
        else:
            i = q_values.index(max_q)

        action = self.actions[i]

        if return_q: # if they want it, give it!
            return action, q_values
        return action

    def get_q(self, state, action):
        # Return the value that corresponds to the state, action pair.
        # State should be hashable

        # Return 0.0 if no entry for specified query exist.
        return self.q.get((state, action), 0.0)

        # return self.q[(state, action)]

    def get_e(self, state, action):
        pass

    def set_q(self, state, action, value):
        self.q[(state, action)] = value

    def update_q(self, state_current, state_previous, action, reward):
        # TODO: Should be tested!

        # Create key
        # update_key = (state_previous, action)

        # logging.info("--- in update Q")

        # Do calculation
        q_temp = self.get_q(state_previous, action)

        # logging.info("--- found q_temp")

        # print("q_temp", q_temp)
        # print("a", self.alpha)
        # print("r", reward)
        # print("g", self.gamma)
        # print("best action", self._get_best_action(state_current))

        temp = self.alpha * (reward + (self.gamma * self._get_best_action(state_current)) - q_temp)

        # TODO: get e for state_previous and multiply with temp

        q_value = q_temp + temp
        # logging.info("--- q_value is computed")

        # Update q map
        self.set_q(state_previous, action, q_value)
        # logging.info("--- q value is set, done...")
        # self.q[update_key] = q_value

    def _get_best_action(self, state):
        # Return the highest q-value in state
        return max([self.get_q(state, action) for action in self.actions])

    def get_best_action_index(self, state):
        # Used for visualization

        best = -1
        best_index = -1
        for i in range(len(self.actions)):
            val = self.get_q(state, self.actions[i])
            if val > best:
                best = val
                best_index = i

        return best_index