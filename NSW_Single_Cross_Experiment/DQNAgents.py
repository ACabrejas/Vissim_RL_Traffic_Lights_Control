from collections import deque
import numpy as np
import random
#import PER

from General_agent import RLAgent

import tensorflow as tf
import tensorflow.keras.layers as kl

import tensorflow.keras.losses as kls
from tensorflow.python.keras import backend as K
from tensorflow.keras.models import load_model, Sequential, Model
from tensorflow.keras.layers import Dense, Input, Lambda, Flatten
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.losses as kls
from tensorflow.keras import regularizers
from tensorflow.keras.activations import relu



###
#leaky relu
lrelu = lambda x : relu(x, alpha =0.01)

###
######################################################################################
## Deep Q Learning Agent (Use DoubleDQN flag to swap to DDQN)
######################################################################################

class DQNAgent(RLAgent):
    def __init__(self, 
                 state_size,
                 action_size, 
                 ID, 
                 memory_size, 
                 gamma, 
                 epsilon, 
                 alpha, 
                 copy_weights_frequency, 
                 PER_activated, 
                 DoubleDQN, 
                 Dueling):
        
        super().__init__(ID)
        # Agent Junction ID and Controller ID
        self.signal_id = ID

        # Number of states, action space and memory
        self.state_size = state_size
        self.action_size = action_size

        # Agent Hyperparameters
        self.gamma = gamma                  # discount rate
        self.epsilon = epsilon              # exploration rate
        self.learning_rate = alpha          # learning rate

        # Agent Architecture
        self.DoubleDQN = DoubleDQN            # Double Deep Q Network Flag
        self.Dueling = Dueling                # Dueling Q Networks Flag
        self.PER_activated = PER_activated    # Prioritized Experience Replay Flag
        self.type = 'DQN'                     # Type of the agent

        # Model and target networks
        self.copy_weights_frequency = copy_weights_frequency    # Frequency to copy weights to target network
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.target_model.set_weights(self.model.get_weights())

        self.model.summary()

        # Architecture Debug Messages
        if self.DoubleDQN:
            if self.Dueling:
                print("Deployed instance of Dueling Double Deep Q Learning Agent(s) at Intersection " + str(ID) + "\n")
            else:
                print("Deployed instance of Double Deep Q Learning Agent(s) at Intersection " + str(ID) + "\n")
        else:
            if self.Dueling:
                print("Deployed instance of Dueling Deep Q Learning Agent(s) at Intersection " + str(ID) + "\n")
            else:
                print("Deployed instance of Standard Deep Q Learning Agent(s) at Intersection " + str(ID) + "\n")

        # Initial Setup of S, A, R, S_
        self.state = np.zeros(state_size)[np.newaxis,:]
        self.newstate = np.zeros(state_size)[np.newaxis,:]
        self.action = 0
        self.newaction = 0
        self.reward = 0
        
        # Metrics Storage Initialization
        self.episode_reward = []
        self.episode_memory = []
        self.reward_storage = []
        self.loss = []


        # Metrics for the testing
        self.queues_over_time = [[0,0,0,0]]
        self.accumulated_delay= [0]
        self.flow_in_intersection = []
        
        if self.PER_activated:
            # If PER_activated spawn BinaryTree and Memory object to store priorities and experiences
            self.memory = Memory(memory_size)
        else:
            # Else use the deque structure to only store experiences which will be sampled uniformly
            self.memory = deque(maxlen=memory_size)
   
    
    def _build_model(self):
        '''
        This method builds the neural network at the core of the agent
        '''
        if self.Dueling:
            # Architecture for the Neural Net in the Dueling Deep Q-Learning Model
            #model = Sequential()
            input_layer = Input(shape = self.state_size )
            # conv1 = kl.Conv2D(32, (3, 3), activation= 'relu', padding='same', kernel_regularizer=regularizers.l2(0.001), name = 'value_conv1')(input_layer)
            # conv2 = kl.Conv2D(64, (3, 3), activation= 'relu', padding='same', kernel_regularizer=regularizers.l2(0.001), name = 'value_conv2')(conv1)
            # conv3 = kl.Conv2D(64, (3, 3), activation= 'relu', padding='same', kernel_regularizer=regularizers.l2(0.001), name = 'value_conv3')(conv2)
            # flatten = Flatten()(conv3)
            dense1 = Dense(24, activation= 'relu', kernel_regularizer=regularizers.l2(0.001))(input_layer)
            dense2 = Dense(24, activation= 'relu', kernel_regularizer=regularizers.l2(0.001))(dense1)
            
            fc1 = Dense(24)(dense2)
            dueling_actions = Dense(self.action_size,kernel_regularizer=regularizers.l2(0.001))(fc1)
            fc2 = Dense(24)(dense2)
            dueling_values = Dense(1,kernel_regularizer=regularizers.l2(0.001))(fc2)

            def dueling_operator(duel_input):
                duel_v = duel_input[0]
                duel_a = duel_input[1]
                return (duel_v + (duel_a - K.mean(duel_a, axis = 1, keepdims = True)))

            policy = Lambda(dueling_operator, name = 'policy')([dueling_values, dueling_actions])
            model = Model(inputs=[input_layer], outputs=[policy])
            model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
            return(model)
        else:
            # Architecture for the Neural Net in Deep-Q learning Model (also Double version)
            input_layer = Input(shape = self.state_size )
            dense1 = Dense(48, activation= 'relu', kernel_regularizer=regularizers.l2(0.001))(input_layer)
            dense2 = Dense(48, activation= 'relu', kernel_regularizer=regularizers.l2(0.001))(dense1)
            dense3 = Dense(48, activation= 'relu', kernel_regularizer=regularizers.l2(0.001))(dense2)
            dense4 = Dense(self.action_size, activation='linear', kernel_regularizer=regularizers.l2(0.01))(dense3)

            model = Model(inputs=[input_layer], outputs=[dense4])
            
            
            #model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
            model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
            return model
    
    # Add memory on the right, if over memory limit, pop leftmost item
    def remember(self, state, action, reward, next_state, done):
        '''
        This method operate in a different manner depending on whether PER memory is active or not.
            PER active  : arrange sarsd into an array and store it in the tree.
            PER inactive: append sarsd into the right of a deque item, if the item is full, pop item on the leftmost position.
        '''
        if self.PER_activated:
            experience = np.array([state, action, reward, next_state, done])
            self.memory.store(experience)

            self.episode_memory.append([state, action, reward, next_state, done])
            self.episode_reward.append(reward)
        else:
            self.memory.append([state, action, reward, next_state, done])

            self.episode_memory.append([state, action, reward, next_state, done])
            self.episode_reward.append(reward)

    def reset(self):
        self.episode_memory = []
        self.episode_reward = []

    
    def choose_action(self, state):
        '''
        This method chooses an action using an epsilon-greedy method.
            Input : State as an array.
            Output: Action as an integer.
        '''
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
            #print('Chosen Random Action {}'.format(action+1))
        else:
            act_values = self.model.predict(state)
            action = np.argmax(act_values[0])
            #print('Chosen Not-Random Action {}'.format(action+1))
        return action
    
    def learn_batch(self, batch_size, episode):
        '''
        Sample a batch of "batch_size" experiences. 
        Perform 1 step of gradient descent on all of them simultaneously.
        Update priority weights in the memory tree
        '''
        state_vector = []
        target_f_vector = []
        absolute_errors = [] 

        if self.PER_activated:
            tree_idx, minibatch, ISWeights_mb = self.memory.sample(batch_size)
        else:
            idx = np.random.randint(len(self.memory), size=batch_size, dtype=int)
            minibatch = np.array(self.memory)[idx]
        
        
        state, action, reward, next_state = np.concatenate(minibatch[:,0], axis=0 ), minibatch[:,1].astype('int32') ,minibatch[:,2].reshape(batch_size,1), np.concatenate( minibatch[:,3] , axis=0 )
        
        
        if self.DoubleDQN:
            next_action = np.argmax(self.model.predict(next_state), axis=1)
            target = reward + self.gamma * self.target_model.predict(next_state)[np.arange(batch_size),next_action].reshape(batch_size,1)
        else:
            # Fixed Q-Target
            target = reward + self.gamma * np.max(self.target_model.predict(next_state),axis=1).reshape(batch_size,1)
            
        # This section incorporates the reward into the prediction and calculates the absolute error between old and new
        target_f = self.model.predict(state)
        
        absolute_errors = np.abs(target_f[np.arange(batch_size),action].reshape(batch_size,1)-target)
        
        target_f[np.arange(batch_size),action] = target.reshape(batch_size)
        
        self.model.fit(state, target_f, epochs=1, verbose=2, batch_size = batch_size)
        
        self.loss.append(self.model.history.history['loss'][0])

        if self.PER_activated:
            #Update priority
            self.memory.batch_update(tree_idx, absolute_errors)

    def copy_weights(self):
        ''' 
        This method copies the weights from the model to the target model.
        '''
        self.target_model.set_weights(self.model.get_weights())
        print("Weights succesfully copied to Target model for Agent {}.".format(self.ID))  


import numpy as np

class SumTree(object):
    """
    This SumTree code is modified version of Morvan Zhou:
    https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/blob/master/contents/5.2_Prioritized_Replay_DQN/RL_brain.py
    """


    """
    This SumTree code is a modified version and the original code is from:
    https://github.com/jaara/AI-blog/blob/master/SumTree.py
    Story data with its priority in the tree.
    """
    data_pointer = 0

    def __init__(self, capacity):
        self.capacity = capacity  # for all priority values
        self.tree = np.zeros(2 * capacity - 1)
        # [--------------Parent nodes-------------][-------leaves to recode priority-------]
        #             size: capacity - 1                       size: capacity
        self.data = np.zeros(capacity, dtype=object)  # for all transitions
        # [--------------data frame-------------]
        #             size: capacity

    def add(self, p, data):
        tree_idx = self.data_pointer + self.capacity - 1
        self.data[self.data_pointer] = data  # update data_frame
        self.update(tree_idx, p)  # update tree_frame

        self.data_pointer += 1
        if self.data_pointer >= self.capacity:  # replace when exceed the capacity
            self.data_pointer = 0

    def update(self, tree_idx, p):
        change = p - self.tree[tree_idx]
        self.tree[tree_idx] = p
        # then propagate the change through tree
        while tree_idx != 0:    # this method is faster than the recursive loop in the reference code
            tree_idx = (tree_idx - 1) // 2
            self.tree[tree_idx] += change

    def get_leaf(self, v):
        """
        Tree structure and array storage:
        Tree index:
             0         -> storing priority sum
            / \
          1     2
         / \   / \
        3   4 5   6    -> storing priority for transitions
        Array type for storing:
        [0,1,2,3,4,5,6]
        """
        parent_idx = 0
        while True:     # the while loop is faster than the method in the reference code
            cl_idx = 2 * parent_idx + 1         # this leaf's left and right kids
            cr_idx = cl_idx + 1
            if cl_idx >= len(self.tree):        # reach bottom, end search
                leaf_idx = parent_idx
                break
            else:       # downward search, always search for a higher priority node
                if v <= self.tree[cl_idx]:
                    parent_idx = cl_idx
                else:
                    v -= self.tree[cl_idx]
                    parent_idx = cr_idx

        data_idx = leaf_idx - self.capacity + 1
        return leaf_idx, self.tree[leaf_idx], self.data[data_idx]

    @property
    def total_p(self):
        return self.tree[0]  # the root


class Memory(object):  # stored as ( s, a, r, s_ ) in SumTree
    """
    This Memory class is modified based on the original code from:
    https://github.com/jaara/AI-blog/blob/master/Seaquest-DDQN-PER.py
    """
    epsilon = 0.01  # small amount to avoid zero priority
    alpha = 0.6  # [0~1] convert the importance of TD error to priority
    beta = 0.4  # importance-sampling, from initial value increasing to 1
    beta_increment_per_sampling = 0.001
    abs_err_upper = 1.  # clipped abs error

    def __init__(self, capacity):
        self.tree = SumTree(capacity)

    def store(self, transition):
        max_p = np.max(self.tree.tree[-self.tree.capacity:])
        if max_p == 0:
            max_p = self.abs_err_upper
        self.tree.add(max_p, transition)   # set the max p for new p

    def sample(self, n):
        b_idx, b_memory, ISWeights = np.empty((n,), dtype=np.int32), np.empty((n, self.tree.data[0].size),dtype = object), np.empty((n, 1))
        pri_seg = self.tree.total_p / n       # priority segment
        self.beta = np.min([1., self.beta + self.beta_increment_per_sampling])  # max = 1

        min_prob = np.min(self.tree.tree[-self.tree.capacity:]) / self.tree.total_p     # for later calculate ISweight
        for i in range(n):
            a, b = pri_seg * i, pri_seg * (i + 1)
            v = np.random.uniform(a, b)
            idx, p, data = self.tree.get_leaf(v)
            prob = p / self.tree.total_p
            ISWeights[i, 0] = np.power(prob/min_prob, -self.beta)
            b_idx[i] = idx
            b_memory[i, :] = data


        return b_idx, b_memory, ISWeights

    def batch_update(self, tree_idx, abs_errors):
        #print(abs_errors)
        abs_errors += self.epsilon  # convert to abs and avoid 0
        #print(abs_errors)
        clipped_errors = np.minimum(abs_errors, self.abs_err_upper)
        ps = np.power(clipped_errors, self.alpha)
        #print(ps)
        for ti, p in zip(tree_idx, ps):
            #print(p)
            self.tree.update(ti, p)

