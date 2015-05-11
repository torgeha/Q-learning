__author__ = 'Torgeir'

import random
import numpy as np
import queue
import logging

class QLearner:

    def __init__(self, actions, alpha, gamma, epsilon, trace_decay, backup_states):
        self.q = {}
        self.eligibility_traces = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.trace_decay = trace_decay
        self.nof_backup_states = backup_states

        self.backup_states = queue.LifoQueue()
        # self.backup_states = [None] * self.nof_backup_states # state, action pairs

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

    def get_e(self, state, action):
        return self.eligibility_traces.get((state, action), 0.0)

    def decay_states(self, keys):
        # Decay all states in self.eligibility traces
        # The keys list is all keys that needs dacaying

        for k in keys:

            # Calculate decay factor
            decay_value = self.gamma * self.trace_decay

            # Do the decaying
            self.eligibility_traces[k] *= decay_value


    def set_q(self, state, action, value):
        self.q[(state, action)] = value

    def update_SAPs(self, delta):
        # Get eligibility traces for all s,a pairs and update Q based on that and delta
        # Return all keys that is updated, these will later be decayed

        # Keep track of updated entries, will make decaying faster
        keys = []

        for key, value in self.eligibility_traces.items():

            # Do nothing if value is very 0
            if abs(value) > 0.0001:

                keys.append(key)

                # Get state and action
                state, action = key

                # Get q-value
                q_value = self.get_q(state, action)

                # Do the updating
                updated = q_value + (delta * value)

                # Set the new value
                self.set_q(state, action, updated)
        return keys

    def update_q(self, state_current, state_previous, action, reward):

        # Do calculation
        q_temp = self.get_q(state_previous, action)

        delta = self.alpha * (reward + (self.gamma * self._get_best_action(state_current)) - q_temp)

        q_value = q_temp + delta
        # # Update q map

        self.set_q(state_previous, action, q_value)

        if self.nof_backup_states <= 1:
            return

        self.backup_states.put((state_previous, action))

        # If there was a reward, initiate backup scheme
        if reward > 0:
            self.update_backed_up_states()

    def update_backed_up_states(self):

        state_next, action_next = self.backup_states.get()
        q_value_next = self.get_q(state_next, action_next)

        temp_queue = queue.LifoQueue(maxsize=self.nof_backup_states)

        # Remember the pulled pair
        temp_queue.put((state_next, action_next))

        for i in range(self.nof_backup_states - 1):
            if not self.backup_states.empty():

                s, a = self.backup_states.get()
                temp_queue.put((s, a))

                # Calc new q-value
                q_value = q_value_next * self.trace_decay

                # Get current q-value
                current_q = self.get_q(s, a)

                # Only set if value is more extreme
                # if q_value > current_q:
                self.set_q(s, a, q_value + current_q)

                q_value_next = q_value

        # Refill the backup_queue with the pairs extracted
        while not temp_queue.empty():
            self.backup_states.put(temp_queue.get())

    def ets(self):
        # return string of eligibility traces
        s = "{"
        for key, value in self.eligibility_traces.items():
            s += "(" + key[0] + ", " + str(key[1]) + "): " + str(value) + ", "
        return s + "}"

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