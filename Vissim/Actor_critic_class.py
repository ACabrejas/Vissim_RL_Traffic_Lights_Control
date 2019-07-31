from collections import deque

import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as kl
import tensorflow.keras.losses as kls
import tensorflow.keras.optimizers as ko
import tensorflow.keras.backend as K
from tensorflow.keras.activations import relu


###
#leaky relu
lrelu = lambda x : relu(x, alpha =0.01)

###

class ProbabilityDistribution(tf.keras.Model):
	def call(self, logits):
		# sample a random categorical action from given logits
		return tf.squeeze(tf.random.categorical(logits, 1), axis=-1)



# An working model training with entropy = 0.00001 en nstep = 32 and learn every step lr = 0.000065 gamma = 0.99 
class Model(tf.keras.Model):
	def __init__(self, num_actions):
		super().__init__('mlp_policy')

		# no tf.get_variable(), just simple Keras API
		self.hidden1 = kl.Dense(128, activation='relu')
		self.hidden2 = kl.Dense(128, activation='relu')
		self.value = kl.Dense(1, name='value')
		# logits are unnormalized log probabilities
		self.logits = kl.Dense(num_actions, name='policy_logits')
		self.dist = ProbabilityDistribution()

	def call(self, inputs):
		# inputs is a numpy array, convert to Tensor
		x = tf.convert_to_tensor(inputs, dtype=tf.float32)

		# This it the core of the model
	   
		# separate hidden layers from the core
		hidden_logs = self.hidden1(x)
		hidden_vals = self.hidden2(x)
		return self.logits(hidden_logs), self.value(hidden_vals)

	def action_value(self, obs):
		# executes call() under the hood
		logits, value = self.predict(obs)
		action = self.dist.predict(logits)
		# a simpler option, will become clear later why we don't use it
		# action = tf.random.categorical(logits, 1)
		return action , value

class Model2(tf.keras.Model):
	def __init__(self, num_actions):
		super().__init__('mlp_policy')
		# no tf.get_variable(), just simple Keras API

		#self.core1 = kl.Dense(60, activation='relu')
		
		self.value1 = kl.Dense(64, activation='relu', name='value1') #64
		self.value2 = kl.Dense(64, activation='relu', name='value2')
		self.value3 = kl.Dense(42, activation='relu', name='value3')

		self.value = kl.Dense(1, name='value')
		# logits are unnormalized log probabilities


		self.logits1 = kl.Dense(42, activation='relu', name='policy_logits1')
		self.logits2 = kl.Dense(42, activation='relu', name='policy_logits2')
		self.logits3 = kl.Dense(42, activation='relu', name='policy_logits3')

		self.logits = kl.Dense(num_actions, name='policy_logits')

		self.dist = ProbabilityDistribution()

	def call(self, inputs):
		# inputs is a numpy array, convert to Tensor
		x = tf.convert_to_tensor(inputs, dtype=tf.float32)

		# This it the core of the model
		#x = self.core1(x)
		
		# separate hidden layers from the core
		hidden_logs = self.logits1(x)
		hidden_logs = self.logits2(hidden_logs)
		hidden_logs = self.logits3(hidden_logs)

		hidden_vals = self.value1(x)
		hidden_vals = self.value2(hidden_vals)
		hidden_vals = self.value3(hidden_vals)

		return self.logits(hidden_logs), self.value(hidden_vals)

	def action_value(self, obs):
		# executes call() under the hood
		logits, value = self.predict(obs)
		action = self.dist.predict(logits)
		# a simpler option, will become clear later why we don't use it
		# action = tf.random.categorical(logits, 1)
		return action , value


class ACAgent:

	def __init__(self, state_size, action_size, ID, n_step_size, gamma, alpha, entropy, value):


		print("Deploying instance of Actor_Critic Agent(s) !!! TENSORFLOW 2 IS NEEDED !!! ")
		# agent type flag 
		self.type = 'AC'


		# Model
		# hyperparameters for loss terms and Agent
		self.params = {'value': value, 'entropy': entropy, 'gamma': gamma, 'lr' : alpha}
		self.model = Model2(action_size)
		self.model.compile(
			optimizer=ko.RMSprop(lr = self.params['lr']),
			# define separate losses for policy logits and value estimate
			loss=[self._logits_loss, self._value_loss]
		)

		self.trainstep = 0
		self.predicted_value = 0
		self.true_value = 0 


		# Agent Junction ID and Controller ID
		self.signal_id = ID
		

		# Number of states, action space and memory
		self.state_size = state_size
		self.action_size = action_size


		# The memory will store (state , action , reward, next_state) in a batch
		self.memory = deque(maxlen=n_step_size)
		self.episode_memory = []
		self.episode_reward = []
		self.n_step_size = n_step_size

		self.test()

	# Add memory on the right, if over memory limit, pop leftmost item
	def remember(self, state, action, reward, next_state, done):
		self.memory.append([state, action, reward, next_state, done])
		self.episode_memory.append([state, action, reward, next_state, done])
		self.episode_reward.append(reward)


	# Flush the memory for the next episode 
	def reset(self):
		self.episode_memory = []
		self.memory = []

	# Update the Junction IDs for the agent
	def update_IDS(self, ID, npa):
		self.signal_id = ID
		self.signal_controller = npa.signal_controllers[self.signal_id]
		self.signal_groups = npa.signal_groups[self.signal_id]

	def reduce_entropy(self):
		"""
		Function to reduce entropy, a very hacky way to rebuild the train_function with new loss
		"""
		self.params['entropy'] = self.params['entropy']*0.1

		self.model.compile(optimizer = ko.RMSprop(lr=self.params['lr']),
		  	# define separate losses for policy logits and value estimate
			loss = [self._logits_loss, self._value_loss])
		self.model.summary()


	# Need to test before loading to build the graph (surely an other way to do it ...)
	def test(self):
		_,_ = self.model.action_value(np.empty(self.state_size)[np.newaxis,:]) 
		self.model.summary()
		print('To be corrected')

	# A function to check if the predicted value of a state is converging or near the actual return.
	# horizon : the number of steps used to compute the return
	# n_step, the number of sample
	def value_check(self, horizon, n_sample):

		if len(self.episode_memory) < horizon :
			raise Exception("Episode_memory too small ")

		# random indexes to sample the value function
		indexes = np.random.choice(len(self.episode_memory) - horizon, size = n_sample)
		predicted_values = []
		true_values = []
		probas = []

		state0 = np.zeros(self.state_size)[np.newaxis,:]
		logit0, _ = self.model.predict(state0)
		proba0 = np.round(tf.nn.softmax(logit0).numpy().squeeze(axis = 0), decimals = 2)


		
		# We could find a way to vectorize this but it is not worth it
		for index in indexes:

			# Compute the predicted value by the model
			state = self.episode_memory[index][0]
			logit, predicted_value = self.model.predict(state)
			predicted_value = predicted_value.squeeze(axis = 0)
			predicted_value = np.round(predicted_value[0])
			predicted_values.append(predicted_value)

			proba = list(np.round(tf.nn.softmax(logit).numpy().squeeze(axis = 0), decimals = 2))
			probas.append(proba)

			# Compute the return 
			true_value = np.sum(np.array(self.episode_reward[index: index+horizon]) * (self.params['gamma'] * np.ones(horizon))**np.arange(horizon))
			true_values.append(round(true_value))

		return predicted_values, true_values, proba0, probas



	def _value_loss(self, returns, value):
		# value loss is typically MSE between value estimates and returns
		return self.params['value']*kls.mean_squared_error(returns, value)

	def _logits_loss(self, acts_and_advs, logits):
		# a trick to input actions and advantages through same API
		actions, advantages = tf.split(acts_and_advs, 2, axis=-1)
		# sparse categorical CE loss obj that supports sample_weight arg on call()
		# from_logits argument ensures transformation into normalized probabilities
		weighted_sparse_ce = kls.SparseCategoricalCrossentropy(from_logits=True)
		# policy loss is defined by policy gradients, weighted by advantages
		# note: we only calculate the loss on the actions we've actually taken
		actions = tf.cast(actions, tf.int32)
		policy_loss = weighted_sparse_ce(actions, logits, sample_weight=advantages)
		# entropy loss can be calculated via CE over itself
		entropy_loss = kls.categorical_crossentropy(tf.nn.softmax(logits), logits, from_logits=True)
		# here signs are flipped because optimizer minimizes
		return policy_loss - self.params['entropy']*entropy_loss

	def _returns_advantages(self, rewards, values, next_value):
		# next_value is the bootstrap value estimate of a future state (the critic)
		returns = np.append(np.zeros_like(rewards), next_value, axis=-1)
		# returns are calculated as discounted sum of future rewards
		for t in reversed(range(rewards.shape[0])):
			returns[t] = rewards[t] + self.params['gamma'] * returns[t+1]
		returns = returns[:-1]
		# advantages are returns - baseline, value estimates in our case
		advantages = returns - values
		return returns, advantages

	def choose_action(self, state):
		action, _ = self.model.action_value(state)
		return np.squeeze(action, axis=-1)

	#Performing step of gradient descent on the agent memory
	def learn(self):


		Sample = np.array(self.memory)

		states, actions, rewards, next_state  = np.concatenate(Sample[:,0], axis=0), Sample[:,1].astype('int32'), Sample[:,2], np.concatenate(Sample[:,3], axis=0)[-1]

		_, values = self.model.action_value(states)
		values = values.squeeze()

		_, next_value  = self.model.action_value(next_state[np.newaxis,:])

		next_value = next_value.squeeze(axis = 0)

		returns, advs = self._returns_advantages(rewards, values, next_value)

		# a trick to input actions and advantages through same API

		acts_and_advs = np.concatenate([actions[:, np.newaxis], advs[:, np.newaxis]], axis=-1)

		# performs a full training step on the collected batch
		# note: no need to mess around with gradients, Keras API handles it
		losses = self.model.train_on_batch(states, [acts_and_advs, returns])

	#def save_agent(self)


### The next functions differentiate the type of the agent : if it is a DQN the all model with optimisier is saved, otherwise only the weight of the model is saved
# Reload agents
def load_agents(vissim_working_directory, model_name, Agents, Session_ID, best):
	
	for index, agent in enumerate(Agents):
		if agent.type == 'AC':
			print('Loading Pre-Trained Agent, Architecture and Memory.')
			if best:
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'_Optimizer'+'.h5')

			else :
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Optimizer'+'.h5')

			# this is to build the network (to be corrected) 
			agent.test()
			agent.model.load_weights(Weights_Filename)

			agent.model._make_train_function()
			with open(Optimizer_Filename, 'rb') as f:
				weight_values = pickle.load(f)
			agent.model.optimizer.set_weights(weight_values)
			
		
		else :
			print('Loading Pre-Trained Agent, Architecture, Optimizer and Memory.')
			if best:
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'.h5')
			else :
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'.h5')
			
			agent.model = load_model(Filename)

		if best:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'_Memory'+'.p')
		else:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Memory'+'.p')
		agent.memory = pickle.load(open(Memory_Filename, 'rb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Train'+'.p')
		reward_storage = pickle.load(open(Training_Progress_Filename, 'rb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Loss'+'.p')
		agent.Loss = pickle.load(open(Loss_Filename, 'rb'))
		
	print('Items successfully loaded.')
	return(Agents, reward_storage)

# Save agents
def save_agents(vissim_working_directory, model_name, Agents, Session_ID, reward_storage):

	# Chech if suitable folder exists
	folder =  os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID)
	if not os.path.exists(folder):
		os.makedirs(folder)
	for index, agent in enumerate(Agents):

		if agent.type == 'AC':
			Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Weights'+'.h5')
			Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Optimizer'+'.h5')
			print('Saving architecture, weights, optimizer state for agent-{}'.format(index))

			symbolic_weights = getattr(agent.model.optimizer, 'weights')
			weight_values = K.batch_get_value(symbolic_weights)
			with open(Optimizer_Filename, 'wb') as f:
				pickle.dump(weight_values, f)

			# little change to save weight instead of the all agent
			agent.model.save_weights(Weights_Filename)

		else :
			Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'.h5')
			print('Saving architecture, weights and optimizer state for agent-{}'.format(index))
			agent.model.save(Filename)

		Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Memory'+'.p')
		print('Dumping agent-{} memory into pickle file'.format(index))
		pickle.dump(agent.memory, open(Memory_Filename, 'wb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Train'+'.p')
		print('Dumping Training Results into pickle file.')
		pickle.dump(reward_storage, open(Training_Progress_Filename, 'wb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Loss'+'.p')
		print('Dumping Loss Results into pickle file.')
		pickle.dump(agent.loss, open(Loss_Filename, 'wb'))

######################################################
##### THIS DOESNT WORK FOR MULTIPLE AGENTS. FIX!!!!
# Save the agent producing best reward
def best_agent(reward_storage, average_reward, best_agent_weights, best_agent_memory, vissim_working_directory, model_name, Agents, Session_ID):

	# Chech if suitable folder exists
	folder =  os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID)
	if not os.path.exists(folder):
		os.makedirs(folder)
	if average_reward == np.max(reward_storage):
		for index, agent in enumerate(Agents):
			best_agent_memory = agent.memory
			print('Saving architecture, weights, optimizer state for best agent-{}'.format(index))
			if agent.type == 'AC' :
				best_agent_weights = agent.model.get_weights()
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'_Optimizer'+'.h5')
			
				symbolic_weights = getattr(agent.model.optimizer, 'weights')
				weight_values = K.batch_get_value(symbolic_weights)
				with open(Optimizer_Filename, 'wb') as f:
					pickle.dump(weight_values, f)

				agent.model.save_weights(Weights_Filename)
			else : 
				best_agent_weights = agent.model
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'.h5')
				agent.model.save(Filename)

			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(index)+'_Memory'+'.p')
			pickle.dump(best_agent_memory, open(Memory_Filename, 'wb'))
			print("New best agent found. Saved in {}".format(Memory_Filename))
			Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Train'+'.p')
			print('Dumping Training Results into pickle file.')
			Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(index)+'_Loss'+'.p')
			print('Dumping Loss Results into pickle file.')
			pickle.dump(agent.loss, open(Loss_Filename, 'wb'))

	return(best_agent_weights, best_agent_memory)