from collections import deque
import numpy as np
import random
import PER

import tensorflow as tf
from keras import backend as K
from keras.models import load_model, Sequential, Model
from keras.layers import merge, Dense, Input, Lambda
from keras.layers.core import Activation, Flatten
from keras.optimizers import Adam

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

        # Model and target networks
        self.copy_weights_frequency = copy_weights_frequency    # Frequency to copy weights to target network
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.target_model.set_weights(self.model.get_weights())

        # Potential actions (compatible phases) and transitions
        self.update_counter = 1                                 # Timesteps until next update
        self.compatible_actions = [[1,0,1,0],[0,1,0,1]]         # Potential actions (compatible phases), 1 means green

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
        self.state = np.reshape([0,0,0,0], [1,state_size])
        self.newstate = np.reshape([0,0,0,0], [1,state_size])
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
            dense1 = Dense(12, input_dim=self.state_size, activation='relu')(input_layer)
            #dense2 = Dense(48, activation='relu')(dense1)
            #flatten = Flatten()(dense2)
            fc1 = Dense(24)(dense1)
            dueling_actions = Dense(self.action_size)(fc1)
            fc2 = Dense(24)(dense1)
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
            model.add(Dense(12, input_dim=self.state_size, activation='relu'))
            model.add(Dense(24, activation='relu'))
            model.add(Dense(self.action_size, activation='linear'))
            model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
            return model
    
    # Add memory on the right, if over memory limit, pop leftmost item
    def remember(self, state, action, reward, next_state):
        if self.PER_activated:
            experience = (state, action, reward, next_state)
            self.memory.store(experience)
        else:
            self.memory.append((state, action, reward, next_state))
    
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
    
    def replay_single(self, batch_size, episode):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state in minibatch:

            if self.DoubleDQN:
                next_action = np.argmax(self.target_model.predict(np.reshape(next_state,(1,self.state_size))), axis=1)
                target = reward + self.gamma * self.target_model.predict(np.reshape(next_state,(1,self.state_size)))[0][next_action][0]
            else:
                target = reward + self.gamma * np.max(self.target_model.predict(np.reshape(next_state,(1,self.state_size))))
                # No fixed targets version
                #target = reward + self.gamma * np.max(self.model.predict(np.reshape(next_state,(1,self.state_size))))

            target_f = self.model.predict(state)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)
            self.loss.append(self.model.history.history['loss'][0])

        # Exploration rate decay
        if self.epsilon > self.epsilon_min:
            self.epsilon += self.epsilon_decay
        # Copy weights every 5 episodes
        if (episode+1) % self.copy_weights_frequency == 0 and episode != 0:
            self.copy_weights()   
   
    def replay_batch(self, batch_size, episode):
        state_vector = []
        target_f_vector = []
        absolute_errors = [] 

        if self.PER_activated:
            tree_idx, minibatch, ISWeights_mb = self.memory.sample(batch_size)
            minibatch = [item[0] for item in minibatch]
            #print(minibatch)
            #return(minibatch)
        else:
            minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state in minibatch:
            if self.DoubleDQN:
                next_action = np.argmax(self.model.predict(np.reshape(next_state,(1,self.state_size))), axis=1)
                target = reward + self.gamma * self.target_model.predict(np.reshape(next_state,(1,self.state_size)))[0][next_action][0]
            else:
                # Fixed Q-Target
                target = reward + self.gamma * np.max(self.target_model.predict(np.reshape(next_state,(1,self.state_size))))
                # No fixed targets version
                #target = reward + self.gamma * np.max(self.model.predict(np.reshape(next_state,(1,self.state_size))))

            # This section incorporates the reward into the prediction and calculates the absolute error between old and new
            target_f = self.model.predict(state)
            absolute_errors.append(abs(target_f[0][action] - target))
            target_f[0][action] = target

            state_vector.append(state[0])
            target_f_vector.append(target_f[0])

        state_matrix = np.asarray(state_vector)
        target_f_matrix = np.asarray(target_f_vector)

        self.model.fit(state_matrix, target_f_matrix, epochs=1, verbose=0)
        self.loss.append(self.model.history.history['loss'])

        if self.PER_activated:
            #Update priority
            self.memory.batch_update(tree_idx, absolute_errors)

        # Copy weights every "copy_weights_frequency" episodes
        if (episode+1) % self.copy_weights_frequency == 0 and episode != 0:
            self.copy_weights()   

    # Copy weights function
    def copy_weights(self):
        self.target_model.set_weights(self.model.get_weights())
        print("Weights succesfully copied to Target model.")  
