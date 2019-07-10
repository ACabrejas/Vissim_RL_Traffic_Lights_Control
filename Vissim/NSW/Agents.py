# Agent Class 
'''
The only method and Agent needs is one that chooses the next action
'''
from collections import defaultdict
import numpy as np
#############################
## THIS IS A GENERIC AGENT ##
#############################
class Agent():     
    # Initialize agent with dimension of state and action space
    def __init__(self,state_size, action_size,actions):
        # Number of states, action space and memory
        self.state_size = state_size
        self.action_size = action_size
        self.actions = actions

    # Choose and action
    def Action(self, state, actions=None):
        if actions is None:
            actions = self.actions
        pass
    
    # Learning routine
    def Learn(self,sarsa):
        pass
    
    # learn from a batch
    def Learn_Batch(self,Sarsa, batch_size=32):
        pass
    
'''
MaxWeight Agent
'''
# MaxWeight Agent 
class MaxWeight(Agent):
    def Action(self,state,actions=None):
        if actions is None:
            actions=self.actions
            
        opt_val = 0
        for act in actions : 
            val = np.dot(act,state)
            if val >= opt_val :
                opt_val = val
                opt_act = act
        return opt_act
    
    
'''
Easy Q_learner
'''
class Q_function(Agent):
    def __init__(self, actions = None):
        # Q function
        self.Q = defaultdict(lambda: defaultdict(float))
        # number of visits
        self.N = defaultdict(lambda: defaultdict(float))
        self.actions = actions

    def Check(self,state,actions=None):
        if actions is None :
            actions = self.actions
        
        if state not in self.Q.keys():
            for action in actions:
                self.Q[state][action] = 0

    def Max(self,state):
        Q_maximum = np.max(list(self.Q[state].values()))
        return Q_maximum

    def Action(self,state,epsilon=0):
        if np.random.rand() < epsilon :
            idx = np.random.randint(len(actions))
            action = actions[idx]
        else :
            self.Check(state,actions)
            action = max(self.Q[state], key=self.Q[state].get)
        return action

    def Learn(self,sars,learning_rate=0.1,discount_factor=0.5):
        state, action, reward, next_state = sars
        # Check if state,action and next_state are in Q
        self.Check(state)
        self.Check(next_state)
        self.N_update(state,action)

        dQ = reward \
            + discount_factor * self.Max(next_state) \
            - self.Q[state][action]
        self.Q[state][action] = self.Q[state][action] + learning_rate * dQ 
        
        return self.Q

    def N_update(self,state,action,actions=None):
        if actions is None :
            actions = self.actions
        
        if state not in self.N.keys():
            for action in actions:
                self.N[state][action] = 0 
        self.N[state][action] = self.N[state][action] + 1
        return self.N[state][action]

    def Print(self):
        for state in Q_fn.Q.keys():
            for action in Q_fn.Q[state].keys():
                print(state,action,Q_fn.N[state][action],Q_fn.Q[state][action])
    
