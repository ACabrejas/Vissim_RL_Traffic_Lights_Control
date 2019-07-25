from collections import deque


#Code adapted from http://inoryy.com/post/tensorflow2-deep-reinforcement-learning/



import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as kl
import tensorflow.keras.losses as kls
import tensorflow.keras.optimizers as ko

from tensorflow.keras.activations import relu


###
#leaky relu
lrelu = lambda x : relu(x, alpha =0.01)

###

class ProbabilityDistribution(tf.keras.Model):
	def call(self, logits):
		# sample a random categorical action from given logits
		return tf.squeeze(tf.random.categorical(logits, 1), axis=-1)

class Model(tf.keras.Model):
	def __init__(self, num_actions):
		super().__init__('mlp_policy')
		# no tf.get_variable(), just simple Keras API

		#self.core1 = kl.Dense(60, activation='relu')
		
		self.value1 = kl.Dense(60, activation='relu', name='value1') #64
		self.value2 = kl.Dense(21, activation='relu', name='value2')
		self.value3 = kl.Dense(1, name='value3')
		# logits are unnormalized log probabilities


		self.logits1 = kl.Dense(60, activation='relu', name='policy_logits1')
		self.logits2 = kl.Dense(21, activation='relu', name='policy_logits2')
		self.logits3 = kl.Dense(num_actions, name='policy_logits3')

		self.dist = ProbabilityDistribution()

	def call(self, inputs):
		# inputs is a numpy array, convert to Tensor
		x = tf.convert_to_tensor(inputs, dtype=tf.float32)

		# This it the core of the model
		#x = self.core1(x)
		
		# separate hidden layers from the core
		hidden_logs = self.logits1(x)
		hidden_logs = self.logits2(hidden_logs)

		hidden_vals = self.value1(x)
		hidden_vals = self.value2(hidden_vals)

		return self.logits3(hidden_logs), self.value3(hidden_vals)

	def action_value(self, obs):
		# executes call() under the hood
		logits, value = self.predict(obs)
		action = self.dist.predict(logits)
		# a simpler option, will become clear later why we don't use it
		# action = tf.random.categorical(logits, 1)
		return action , value

class Modelconv(tf.keras.Model):
	"""docstring for Modelconv"""
	
	def __init__(self, num_actions):
		super().__init__('mlp_policy')

		#self.core1 = kl.Conv2D(32, (3, 3), activation=lrelu, padding='same' , name = 'core_conv1')
		#self.core2 = kl.Conv2D(32, (3, 3), activation=lrelu, padding='same' , name = 'core_conv2')
		#self.core3 = kl.Conv2D(32, (3, 3), activation=lrelu, padding='same' , name = 'core_conv3')

		self.valueconv1 = kl.Conv2D(64, (3, 4), activation=lrelu, strides = (1,2), padding = "same", name = 'value_conv1')
		self.valueconv2 = kl.Conv2D(32, (3, 4), activation=lrelu, strides = (1,2), padding = "same", name = 'value_conv2')
		self.valueconv3 = kl.Conv2D(16, (3, 4), activation=lrelu, strides = (1,2), padding = "same", name = 'value_conv3')
		self.value1 = kl.Dense(32, activation=lrelu, name='value1')
		self.value2 = kl.Dense(16, activation=lrelu, name='value2')
		self.value = kl.Dense(1, name='value_last')

		self.flat1 = kl.Flatten(name = 'value_flat') 
		# logits are unnormalized log probabilities


		self.logitsconv1 = kl.Conv2D(32, (3, 4), activation=lrelu, strides = (1,2), padding = "same", name = 'policy_conv1')
		self.logitsconv2 = kl.Conv2D(32, (3, 4), activation=lrelu, strides = (1,2), padding = "same", name = 'policy_conv2')
		self.logitsconv3 = kl.Conv2D(16, (3, 4), activation=lrelu, strides = (1,2), padding = "same", name = 'policy_conv3')
		self.logits1 = kl.Dense(32, activation=lrelu, name='policy_logits2')
		self.logits2 = kl.Dense(16, activation=lrelu, name='policy_logits3')
		self.logits = kl.Dense(num_actions, name='policy_last')

		self.flat2 = kl.Flatten(name = 'policy_flat')

		self.dist = ProbabilityDistribution()

	def call(self, inputs):
		# inputs is a numpy array, convert to Tensor
		x = tf.convert_to_tensor(inputs, dtype=tf.float32)

		# This it the core of the model
		#x = self.flat1(self.core3(self.core2(self.core1(x))))
		
		# separate hidden layers from the core
		hidden_logs = self.logitsconv1(x)
		hidden_logs = self.logitsconv2(hidden_logs)
		hidden_logs = self.logitsconv3(hidden_logs)
		hidden_logs = self.flat1(hidden_logs)
		hidden_logs = self.logits1(hidden_logs)
		hidden_logs = self.logits2(hidden_logs)

		hidden_vals = self.valueconv1(x)
		hidden_vals = self.valueconv2(hidden_vals)
		hidden_vals = self.valueconv3(hidden_vals)
		hidden_vals = self.flat2(hidden_vals)
		hidden_vals = self.value1(hidden_vals)
		hidden_vals = self.value2(hidden_vals)

		return self.logits(hidden_logs), self.value(hidden_vals)

	def action_value(self, obs):
		# executes call() under the hood
		logits, value = self.predict(obs)
		action = self.dist.predict(logits)
		# a simpler option, will become clear later why we don't use it
		# action = tf.random.categorical(logits, 1)
		return action , value
		

class Modelconvsave2(tf.keras.Model):
	"""docstring for Modelconv"""
	
	def __init__(self, num_actions):
		super().__init__('mlp_policy')

		#self.core1 = kl.Conv2D(32, (3, 3), activation='relu', padding='same' , name = 'core_conv1')
		#self.core2 = kl.Conv2D(16, (3, 3), activation='relu', padding='same' , name = 'core_conv'2)

		self.valueconv1 = kl.Conv2D(32, (3, 3), activation=lrelu, padding='same', name = 'value_conv1')
		self.valueconv2 = kl.Conv2D(32, (3, 3), activation=lrelu, padding='same', name = 'value_conv2')
		self.value1 = kl.Dense(16, activation=lrelu, name='value1')
		self.value2 = kl.Dense(16, activation=lrelu, name='value2')
		self.value = kl.Dense(1, name='value_last')

		self.flat1 = kl.Flatten(name = 'value_flat') 
		# logits are unnormalized log probabilities


		self.logitsconv1 = kl.Conv2D(32, (3, 3), activation=lrelu, padding='same', name = 'policy_conv1')
		self.logitsconv2 = kl.Conv2D(16, (3, 3), activation=lrelu, padding='same', name = 'policy_conv2')
		self.logits1 = kl.Dense(16, activation=lrelu, name='policy_logits2')
		self.logits2 = kl.Dense(8, activation=lrelu, name='policy_logits3')
		self.logits = kl.Dense(num_actions, name='policy_last')

		self.flat2 = kl.Flatten(name = 'policy_flat')

		self.dist = ProbabilityDistribution()

	def call(self, inputs):
		# inputs is a numpy array, convert to Tensor
		x = tf.convert_to_tensor(inputs, dtype=tf.float32)

		# This it the core of the model
		# x = self.core1(x)
		
		# separate hidden layers from the core
		hidden_logs = self.logitsconv1(x)
		hidden_logs = self.logitsconv2(hidden_logs)
		hidden_logs = self.flat1(hidden_logs)
		hidden_logs = self.logits1(hidden_logs)
		hidden_logs = self.logits2(hidden_logs)

		hidden_vals = self.valueconv1(x)
		hidden_vals = self.valueconv2(hidden_vals)
		hidden_vals = self.flat2(hidden_vals)
		hidden_vals = self.value1(hidden_vals)
		hidden_vals = self.value2(hidden_vals)

		return self.logits(hidden_logs), self.value(hidden_vals)

	def action_value(self, obs):
		# executes call() under the hood
		logits, value = self.predict(obs)
		action = self.dist.predict(logits)
		# a simpler option, will become clear later why we don't use it
		# action = tf.random.categorical(logits, 1)
		return action , value

class Modelconvsave1(tf.keras.Model):
	"""docstring for Modelconv"""
	
	def __init__(self, num_actions):
		super().__init__('mlp_policy')

		#self.core1 = kl.Conv2D(32, (3, 3), activation='relu', padding='same' , name = 'core_conv1')
		#self.core2 = kl.Conv2D(16, (3, 3), activation='relu', padding='same' , name = 'core_conv'2)

		self.value1 = kl.Conv2D(32, (3, 3), activation='relu', padding='same', name = 'value_conv1')
		self.value2 = kl.Dense(16, activation='relu', name='value2')
		self.value3 = kl.Dense(16, activation='relu', name='value3')
		self.value = kl.Dense(1, name='value_last')

		self.flat1 = kl.Flatten(name = 'value_flat') 
		# logits are unnormalized log probabilities


		self.logits1 = kl.Conv2D(32, (3, 3), activation='relu', padding='same', name = 'policy_conv1')
		self.logits2 = kl.Dense(16, activation='relu', name='policy_logits2')
		self.logits3 = kl.Dense(8, activation='relu', name='policy_logits3')
		self.logits = kl.Dense(num_actions, name='policy_last')

		self.flat2 = kl.Flatten(name = 'policy_flat')

		self.dist = ProbabilityDistribution()

	def call(self, inputs):
		# inputs is a numpy array, convert to Tensor
		x = tf.convert_to_tensor(inputs, dtype=tf.float32)

		# This it the core of the model
		# x = self.core1(x)
		
		# separate hidden layers from the core
		hidden_logs = self.logits1(x)
		hidden_logs = self.flat1(hidden_logs)
		hidden_logs = self.logits2(hidden_logs)
		hidden_logs = self.logits3(hidden_logs)

		hidden_vals = self.value1(x)
		hidden_vals = self.flat2(hidden_vals)
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

# An working model training with entropy = 0.00001 en nstep = 32 and learn every step lr = 0.000065 gamma = 0.99 
class Modelsave1(tf.keras.Model):
	def __init__(self, num_actions):
		super().__init__('mlp_policy')

		# no tf.get_variable(), just simple Keras API
		self.hidden1 = kl.Dense(42, activation='relu')
		self.hidden2 = kl.Dense(42, activation='relu')
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

class ACAgent:

	def __init__(self, state_size, action_size, ID, state_type, npa, n_step_size, gamma, alpha, entropy, value,  Vissim):


		print("Deploying instance of Actor_Critic Agent(s) !!! TENSORFLOW 2 IS NEEDED !!! ")
		# agent type flag 
		self.type = 'AC'

		#just temporary
		self.epsilon = 0

		# Model
		# hyperparameters for loss terms and Agent
		self.params = {'value': value, 'entropy': entropy, 'gamma': gamma}
		self.model = Modelconv(action_size)
		self.model.compile(
			optimizer=ko.RMSprop(lr=alpha),
			# define separate losses for policy logits and value estimate
			loss=[self._logits_loss, self._value_loss]
		)

		self.trainstep = 0
		self.predicted_value = 0
		self.true_value = 0 


		# Agent Junction ID and Controller ID
		self.signal_id = ID
		self.signal_controller = npa.signal_controllers[self.signal_id]
		self.signal_groups = npa.signal_groups[self.signal_id]

		# Number of states, action space and memory
		self.state_size = state_size
		self.action_size = action_size

		# Potential actions (compatible phases) and transitions
		self.update_counter = 1                                 # Timesteps until next update
		if self.action_size == 2:
			self.compatible_actions = [[0,1,0,1],[1,0,1,0]]         # Potential actions (compatible phases), 1 means green

		elif self.action_size == 4:
			self.compatible_actions = [[1,1,1,0,0,0,0,0,0,0,0,0],
										[0,0,0,1,1,1,0,0,0,0,0,0],
										[0,0,0,0,0,0,1,1,1,0,0,0],
										[0,0,0,0,0,0,0,0,0,1,1,1]]
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


		# Initial Setup of S, A, R, S_
		self.state = np.zeros(state_size)[np.newaxis,:]
		self.newstate = np.zeros(state_size)[np.newaxis,:]
		self.action = 0
		self.newaction = 0
		self.reward = 0

		# Metrics Storage Initialization
		self.episode_reward = []
		self.episode_memory = []
		self.loss = []
		self.queues_over_time = [[0,0,0,0]]
		self.accumulated_delay= [0]


		# The memory will store (state , action , reward, next_state) in a batch
		self.memory = deque(maxlen=n_step_size)
		self.n_step_size = n_step_size

	# Add memory on the right, if over memory limit, pop leftmost item
	def remember(self, state, action, reward, next_state):
		self.memory.append([state, action, reward, next_state])

	# Update the Junction IDs for the agent
	def update_IDS(self, ID, npa):
		self.signal_id = ID
		self.signal_controller = npa.signal_controllers[self.signal_id]
		self.signal_groups = npa.signal_groups[self.signal_id]

	# Need to test before loading to build the graph (surely an other way to do it ...)
	def test(self):
		_,_ = self.model.action_value(np.empty(self.state_size)[np.newaxis,:]) 
		self.model.summary()
		print('To be corected')

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

		#print(losses)



	# def train(self, env, batch_sz=32, updates=1000):
	#     # storage helpers for a single batch of data
	#     actions = np.empty((batch_sz,), dtype=np.int32)
	#     rewards, dones, values = np.empty((3, batch_sz))
	#     observations = np.empty((batch_sz,) + env.observation_space.shape)
	#     # training loop: collect samples, send to optimizer, repeat updates times
	#     ep_rews = [0.0]
	#     next_obs = env.reset()
	#     for update in range(updates):
	#         for step in range(batch_sz):
	#             observations[step] = next_obs.copy()
	#             actions[step], values[step] = self.model.action_value(next_obs[None, :])
	#             next_obs, rewards[step], dones[step], _ = env.step(actions[step])

	#               ep_rews[-1] += rewards[step]
	#             if dones[step]:
	#                 ep_rews.append(0.0)
	#                 next_obs = env.reset()

	#           _, next_value = self.model.action_value(next_obs[None, :])
	#         returns, advs = self._returns_advantages(rewards, dones, values, next_value)
	#         # a trick to input actions and advantages through same API
	#         acts_and_advs = np.concatenate([actions[:, None], advs[:, None]], axis=-1)
	#         # performs a full training step on the collected batch
	#         # note: no need to mess around with gradients, Keras API handles it
	#         losses = self.model.train_on_batch(observations, [acts_and_advs, returns])
	#     return ep_rews