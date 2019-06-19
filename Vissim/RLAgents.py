from collections import deque
import numpy as np
import random
import PER

import tensorflow as tf
from tensorflow.python.keras import backend as k
from tensorflow.keras.models import load_model, Sequential, Model
from tensorflow.keras.layers import Dense, Input, Lambda
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.losses as kls
from tensorflow.keras import regularizers

######################################################################################
## Deep Q Learning Agent (Use DoubleDQN flag to swap to DDQN)
######################################################################################

class DQNAgent:
    def __init__(self, state_size, action_size, ID, state_type, npa, memory_size, gamma, epsilon, alpha, copy_weights_frequency, Vissim, PER_activated, DoubleDQN, Dueling):
        
        # Agent Junction ID and Controller ID
        self.signal_id = ID
        self.signal_controller = npa.signal_controllers[self.signal_id]
        self.signal_groups = npa.signal_groups[self.signal_id]

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

        # Potential actions (compatible phases) and transitions
        self.update_counter = 1                                 # Timesteps until next update
        if self.action_size == 2:
            self.compatible_actions = [[0,1,0,1],[1,0,1,0]]         # Potential actions (compatible phases), 1 means green
        elif self.action_size == 8:
            self.compatible_actions = [[1,1,1,0,0,0,0,0,0,0,0,0],
                                        [0,0,0,1,1,1,0,0,0,0,0,0],
                                        [0,0,0,0,0,0,1,1,1,0,0,0],
                                        [0,0,0,0,0,0,0,0,0,1,1,1],
                                        [1,0,0,0,0,0,1,0,0,0,0,0],
                                        [0,0,0,1,0,0,0,0,0,1,0,0],
                                        [0,1,1,0,0,0,0,1,1,0,0,0],
                                        [0,0,0,0,1,1,0,0,0,0,1,1]]
        else:
            raise Exception("ERROR: Wrong Action Size. Please review master settings and RLAgents.py")

        # Internal State Traffic Control Variables
        self.intermediate_phase = False                         # Boolean indicating an ongoing green-red or red-green transition
        self.transition_vector = []                             # Vector that will store the transitions between updates

        # Architecture Debug Messages
        if self.DoubleDQN:
            if self.Dueling:
                print("Deploying instance of Dueling Double Deep Q Learning Agent(s)")
            else:
                print("Deploying instance of Double Deep Q Learning Agent(s)")
        else:
            if self.Dueling:
                print("Deploying instance of Dueling Deep Q Learning Agent(s)")
            else:
                print("Deploying instance of Standard Deep Q Learning Agent(s)")

        # Initial Setup of S, A, R, S_
        self.state = np.zeros((1,state_size))
        self.newstate = np.zeros((1,state_size))
        self.action = 0
        self.newaction = 0
        self.reward = 0
        
        # Metrics Storage Initialization
        self.episode_reward = []
        self.loss = []

        if self.PER_activated:
            # If PER_activated spawn BinaryTree and Memory object to store priorities and experiences
            self.memory = PER.Memory(memory_size)
        else:
            # Else use the deque structure to only store experiences which will be sampled uniformly
            self.memory = deque(maxlen=memory_size)

    # Update the Junction IDs for the agent
    def update_IDS(self, ID, npa):
        self.signal_id = ID
        self.signal_controller = npa.signal_controllers[self.signal_id]
        self.signal_groups = npa.signal_groups[self.signal_id]
    
    # Agent Neural Network definition
    def _build_model(self):
        if self.Dueling:
            # Architecture for the Neural Net in the Dueling Deep Q-Learning Model
            #model = Sequential()
            input_layer = Input(shape = (self.state_size,))
            dense1 = Dense(8, input_dim=self.state_size, activation='relu')(input_layer)
            #dense2 = Dense(48, activation='relu')(dense1)
            #flatten = Flatten()(dense2)
            fc1 = Dense(16)(dense1)
            dueling_actions = Dense(self.action_size)(fc1)
            fc2 = Dense(16)(dense1)
            dueling_values = Dense(1)(fc2)

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
            model = Sequential()
            model.add(Dense(42, input_dim=self.state_size, activation='relu',kernel_regularizer=regularizers.l2(0.01)))
            model.add(Dense(42, activation='relu',kernel_regularizer=regularizers.l2(0.01)))
            model.add(Dense(42, activation='relu',kernel_regularizer=regularizers.l2(0.01)))
            model.add(Dense(self.action_size, activation='linear',kernel_regularizer=regularizers.l2(0.01)))
            
            #model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
            model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate, epsilon =1.5*10**-4))
            return model
    
    # Add memory on the right, if over memory limit, pop leftmost item
    def remember(self, state, action, reward, next_state):
        if self.PER_activated:
            experience = np.array([state, action, reward, next_state])
            self.memory.store(experience)
        else:
            self.memory.append([state, action, reward, next_state])
    
    # Choosing actions
    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
            #print('Chosen Random Action {}'.format(action+1))
        else:
            act_values = self.model.predict(state)
            action = np.argmax(act_values[0])
            #print('Chosen Not-Random Action {}'.format(action+1))
        return action
    
    
    
    # Sample a batch of "batch_size" experiences and perform 1 step of gradient descent on all of them simultaneously
    def learn_batch(self, batch_size, episode):
        state_vector = []
        target_f_vector = []
        absolute_errors = [] 

        if self.PER_activated:
            tree_idx, minibatch, ISWeights_mb = self.memory.sample(batch_size)
        else:
            idx = np.random.randint(len(self.memory), size=batch_size,dtype=int)
            minibatch = np.array(self.memory)[idx]
        
        
        state, action, reward, next_state = np.concatenate(minibatch[:,0], axis=0 ), minibatch[:,1].astype('int32') ,minibatch[:,2].reshape(batch_size,1), np.concatenate( minibatch[:,3] , axis=0 )
        
        
        
        if self.DoubleDQN:
            next_action = np.argmax(self.model.predict(np.reshape(next_state,(batch_size,self.state_size))), axis=1)
            target = reward + self.gamma * self.target_model.predict(np.reshape(next_state,(batch_size,self.state_size)))[np.arange(batch_size),next_action].reshape(batch_size,1)
        else:
            # Fixed Q-Target
            target = reward + self.gamma * np.max(self.target_model.predict(np.reshape(next_state,(batch_size,self.state_size))),axis=1)
            # No fixed targets version
            # target = reward + self.gamma * np.max(self.model.predict(np.reshape(next_state,(1,self.state_size))))    
        
            
        # There should be a way to vectorize this
        #for state, action, reward, next_state in minibatch:
        #    if self.DoubleDQN:
        #        next_action = np.argmax(self.model.predict(np.reshape(next_state,(1,self.state_size))), axis=1)
        #        target = reward + self.gamma * self.target_model.predict(np.reshape(next_state,(1,self.state_size)))[0][next_action][0]
        #    else:
                # Fixed Q-Target
        #        target = reward + self.gamma * np.max(self.target_model.predict(np.reshape(next_state,(1,self.state_size))))
                # No fixed targets version
                # target = reward + self.gamma * np.max(self.model.predict(np.reshape(next_state,(1,self.state_size))))

        # This section incorporates the reward into the prediction and calculates the absolute error between old and new
        target_f = self.model.predict(state)
        
        absolute_errors = np.abs(target_f[np.arange(batch_size),action].reshape(batch_size,1)-target)
        
        #absolute_errors.append(abs(target_f[0][action] - target))
        
        target_f[np.arange(batch_size),action] = target.reshape(batch_size)
        
        
        #self.model.fit(state_matrix, target_f_matrix, epochs=1, verbose=0)
        self.model.fit(state, target_f, epochs=1, verbose=2,batch_size=batch_size)
        
        self.loss.append(self.model.history.history['loss'])

        if self.PER_activated:
            #Update priority
            self.memory.batch_update(tree_idx, absolute_errors)

        # Copy weights every "copy_weights_frequency" episodes
        #if (episode+1) % self.copy_weights_frequency == 0 and episode != 0:
        #    self.copy_weights()   

    # Copy weights function
    def copy_weights(self):
        self.target_model.set_weights(self.model.get_weights())
        print("Weights succesfully copied to Target model.")  



