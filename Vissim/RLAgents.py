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
    def __init__(self, state_size, action_size, ID, state_type, npa, memory_size, gamma, epsilon_start, epsilon_end, epsilon_decay, alpha, copy_weights_frequency, Vissim, PER_activated, DoubleDQN, Dueling):
        # Agent Junction ID and Controller ID
        self.signal_id = ID
        self.signal_controller = npa.signal_controllers[self.signal_id]
        
        # Number of states, action space and memory
        self.state_size = state_size
        self.action_size = action_size

        # Agent Hyperparameters
        self.gamma = gamma                    # discount rate
        self.epsilon = epsilon_start          # starting exploration rate
        self.epsilon_min = epsilon_end        # final exploration rate
        self.epsilon_decay = epsilon_decay    # decay of exploration rate
        self.learning_rate = alpha            # learning rate

        # Agent Architecture
        self.DoubleDQN = DoubleDQN            # Double Deep Q Network Flag
        self.Dueling = Dueling                # Dueling Q Networks Flag
        self.PER_activated = PER_activated    # Prioritized Experience Replay Flag

        # Model and target networks
        self.copy_weights_frequency = copy_weights_frequency    # Frequency to copy weights to target network
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.target_model.set_weights(self.model.get_weights())
        
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
    
    # Agent Neural Network definition
    def _build_model(self):
        if self.Dueling:
            # Architecture for the Neural Net in the Dueling Deep Q-Learning Model
            #model = Sequential()
            input_layer = Input(shape = (self.state_size,))
            dense1 = Dense(24, input_dim=self.state_size, activation='relu')(input_layer)
            #dense2 = Dense(48, activation='relu')(dense1)
            #flatten = Flatten()(dense2)
            fc1 = Dense(48)(dense1)
            dueling_actions = Dense(self.action_size)(fc1)
            fc2 = Dense(48)(dense1)
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
            model.add(Dense(24, input_dim=self.state_size, activation='relu'))
            model.add(Dense(48, activation='relu'))
            model.add(Dense(self.action_size, activation='linear'))
            model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
            return model
    
    # Obtain the state based on different state definitions
    def get_state(self, state_type, state_size, Vissim):
        if state_type == 'Queues':
            #Obtain Queue Values (average value over the last period)
            West_Queue  = Vissim.Net.QueueCounters.ItemByKey(1).AttValue('QLen(Current,Last)')
            South_Queue = Vissim.Net.QueueCounters.ItemByKey(2).AttValue('QLen(Current,Last)')
            East_Queue  = Vissim.Net.QueueCounters.ItemByKey(3).AttValue('QLen(Current,Last)')
            North_Queue = Vissim.Net.QueueCounters.ItemByKey(4).AttValue('QLen(Current,Last)')
            state = [West_Queue, South_Queue, East_Queue, North_Queue]
            state = np.reshape(state, [1,state_size])
            return(state)
        elif state_type == 'Delay':
            # Obtain Delay Values (average delay in lane * nr cars in queue)
            West_Delay    = Vissim.Net.DelayMeasurements.ItemByKey(1).AttValue('VehDelay(Current,Last,All)') 
            West_Stopped  = Vissim.Net.QueueCounters.ItemByKey(1).AttValue('QStops(Current,Last)')
            South_Delay   = Vissim.Net.DelayMeasurements.ItemByKey(2).AttValue('VehDelay(Current,Last,All)') 
            South_Stopped = Vissim.Net.QueueCounters.ItemByKey(2).AttValue('QStops(Current,Last)')
            East_Delay    = Vissim.Net.DelayMeasurements.ItemByKey(3).AttValue('VehDelay(Current,Last,All)') 
            East_Stopped  = Vissim.Net.QueueCounters.ItemByKey(3).AttValue('QStops(Current,Last)')
            North_Delay   = Vissim.Net.DelayMeasurements.ItemByKey(4).AttValue('VehDelay(Current,Last,All)') 
            North_Stopped = Vissim.Net.QueueCounters.ItemByKey(4).AttValue('QStops(Current,Last)')
            
            pre_state = [West_Delay, South_Delay, East_Delay, North_Delay, West_Stopped, South_Stopped, East_Stopped, North_Stopped]
            pre_state = [0 if state is None else state for state in pre_state]
            
            state = [pre_state[0]*pre_state[4], pre_state[1]*pre_state[5], pre_state[2]*pre_state[6], pre_state[3]*pre_state[7]]
            state = np.reshape(state, [1,state_size])
            return(state)
        elif state_type == 'MaxFlow':
            pass
        elif state_type == 'FuelConsumption':
            pass
        elif state_type == 'NOx':
            pass
        elif state_type == "COM":
            pass
    
    # Add memory on the right, if over memory limit, pop leftmost item
    def remember(self, state, action, reward, next_state):
        if self.PER_activated:
            experience = (state, action, reward, next_state)
            self.memory.store(experience)
        else:
            self.memory.append((state, action, reward, next_state))
    
    # Choosing actions
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size) 
            self.signal_controller.SetAttValue('ProgNo', int(action+1))
            #print('Chosen Random Action {}'.format(action+1))
            return action
        else:
            act_values = self.model.predict(state)
            action = np.argmax(act_values[0]) 
            self.signal_controller.SetAttValue('ProgNo', int(action+1))
            #print('Chosen Not-Random Action {}'.format(action+1))
            return action  # returns action
    
    def get_reward(self):
        #reward = -np.absolute((self.newstate[0][0]-self.newstate[0][2])-(self.newstate[0][1]-self.newstate[0][3])) - 
        #reward = -np.sum(Agents[0].newstate[0])
        reward = -np.sum([0 if state is None else state for state in self.newstate[0]])
        #print(reward)

        self.episode_reward.append(reward)
        return reward
    
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

        # Exploration rate decay
        if self.epsilon > self.epsilon_min:
            self.epsilon += self.epsilon_decay
        # Copy weights every 5 episodes
        if (episode+1) % self.copy_weights_frequency == 0 and episode != 0:
            self.copy_weights()   

    # Copy weights function
    def copy_weights(self):
        self.target_model.set_weights(self.model.get_weights())
        print("Weights succesfully copied to Target model.")  