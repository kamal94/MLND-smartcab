import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.actions = (None, 'forward', 'left', 'right')
        self.state = None
        self.old_state = None
        #A 16x4 matrix that represents states and possible actions.
        #Each value in that state row and action column represents the Q(S, A)
        self.Q = [[0]*4 for _ in  range((2**7))] 
        # self.Q = {}
        self.alpha = 0.5
        self.gamma = 0.5

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    #Translates a state to a number to access an array index
    #possible values are from 0 to 15
    def state_to_num(self, state):
        count = 0
        if state['oncoming'] == True:
            count += 2**0
        if state['light'] == 'green':
            count += 2**1
        if state['right'] == True:
            count += 2**2
        if state['left'] == True:
            count += 2 **3
        if state['waypoint'] == 'left':
            count += 2**4
        if state['waypoint'] == 'right':
            count += 2**5
        if state['waypoint'] == 'forward':
            count += 2**6
        return count

    def action_to_num(self, action):
        if action is None:
            return 0
        elif action == "forward":
            return 1
        elif action == "left":
            return 2
        elif action == "right":
            return 3
        else:
            assert False

    def num_to_action(self, num):
        if num == 0:
            return None
        if num == 1:
            return 'forward'
        if num == 2:
            return 'left'
        if num == 3:
            return 'right'
        assert False

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        print("waypoint: ", self.next_waypoint)
        # TODO: Update state
        self.old_state = self.state
        self.state = {'waypoint': self.next_waypoint, 'oncoming': inputs['oncoming'], 'light': inputs['light'], 'right':inputs['right'], 'left':inputs['left']}

        # TODO: Select action according to your policy
        if random.random() < 0.75:
            #choose optimal path action so far
            state_num = self.state_to_num(self.state)
            m = max(self.Q[state_num][:])
            index = self.Q[state_num].index(m)
            action = self.num_to_action(index)
        else:
            #choose random next action to follow
            action = random.choice(self.actions)


        # Execute action and get reward
        reward = self.env.act(self, action)

        stateNum = self.state_to_num(self.state)

        # TODO: Learn policy based on state, action, reward
        # Q = alpha*(reward + gamma*max()) + (1-alpha)*Q
        if self.old_state != None:
            old_s_n = self.state_to_num(self.old_state)
            print("old state numbe: ", old_s_n, ' and is of type', type(old_s_n))
            maxOldState=max(self.Q[old_s_n][:])
        else:
            maxOldState = 0.5
        oldQ = self.Q[stateNum][self.action_to_num(action)]
        self.Q[stateNum][self.action_to_num(action)] = self.alpha*(reward + self.gamma*maxOldState + (1-self.alpha)*oldQ)
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        if t % 100 == 0:
            print("Q: ", np.array(self.Q))


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.2, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
