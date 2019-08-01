import os
import tensorflow.keras.backend as K
import pickle

class RLAgent():
	"""
	This will be the general agent class:

	-Atributes
		- memory : a list of state action reward next state or a PER memory
		- episode reward : 
		- episode memory : 
		- best_reward best average reward for an episode
		- type AC , DQN 
		- ID to wich singnal controler the agent is talking to.

	-Methods
		- load
		- save
		- best_agent
		- average_reward

	"""

	def __init__(self,ID):
		self.ID = ID

		# To be defined by the init of the child class
		self.type = None
		self.model = None
		


		# for the training
		self.loss = []
		self.episode_memory = []
		self.episode_reward = []
		self.best_reward = -1000

		self.reward_storage = []




	# To be defined in subclass
	def train(self):
		"""
		One of the subclass method
		"""
		pass


	
	def remenber(self):
		"""
		One of the subclass method
		"""
		pass


	# Save agents
	def save_agent(self, vissim_working_directory, model_name, Session_ID):

		# Chech if suitable folder exists
		folder =  os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID)
		if not os.path.exists(folder):
			os.makedirs(folder)
		

		if self.type == 'AC':
			Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Weights'+'.h5')
			Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Optimizer'+'.h5')
			print('Saving architecture, weights, optimizer state for agent-{}'.format(self.ID))

			symbolic_weights = getattr(self.model.optimizer, 'weights')
			weight_values = K.batch_get_value(symbolic_weights)
			with open(Optimizer_Filename, 'wb') as f:
				pickle.dump(weight_values, f)

			# little change to save weight instead of the all agent
			self.model.save_weights(Weights_Filename)

		else :
			Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'.h5')
			print('Saving architecture, weights and optimizer state for agent-{}'.format(self.ID))
			self.model.save(Filename)

		Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Memory'+'.p')
		print('Dumping agent-{} memory into pickle file'.format(self.ID))
		pickle.dump(self.memory, open(Memory_Filename, 'wb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Train'+'.p')
		print('Dumping Training Results into pickle file.')
		pickle.dump(self.reward_storage, open(Training_Progress_Filename, 'wb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Loss'+'.p')
		print('Dumping Loss Results into pickle file.')
		pickle.dump(self.loss, open(Loss_Filename, 'wb'))



	# Reload agents
	def load_agent(self, vissim_working_directory, model_name , Session_ID, best = True):
		
		
		if self.type == 'AC':
			print('Loading Pre-Trained Agent, Architecture and Memory.')
			if best:
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'_Optimizer'+'.h5')

			else :
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Optimizer'+'.h5')

			# this is to build the network (to be corrected) 
			self.test()
			self.model.load_weights(Weights_Filename)

			self.model._make_train_function()
			with open(Optimizer_Filename, 'rb') as f:
				weight_values = pickle.load(f)
			self.model.optimizer.set_weights(weight_values)
			
		
		else :
			print('Loading Pre-Trained Agent, Architecture, Optimizer and Memory.')
			if best:
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'.h5')
			else :
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'.h5')
			
			self.model = load_model(Filename)

		if best:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'_Memory'+'.p')
		else:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Memory'+'.p')
		self.memory = pickle.load(open(Memory_Filename, 'rb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Train'+'.p')
		self.reward_storage = pickle.load(open(Training_Progress_Filename, 'rb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Loss'+'.p')
		self.Loss = pickle.load(open(Loss_Filename, 'rb'))
			
		print('Items successfully loaded.')
		

	def best_agent(self, vissim_working_directory, model_name, Session_ID):

		# Chech if suitable folder exists
		folder =  os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID)
		if not os.path.exists(folder):
			os.makedirs(folder)
		if self.average_reward >= np.max(self.reward_storage):
			for self.ID, agent in enumerate(Agents):
				best_agent_memory = agent.memory
				print('Saving architecture, weights, optimizer state for best agent-{}'.format(self.ID))
				if agent.type == 'AC' :
					best_agent_weights = agent.model.get_weights()
					Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'_Weights'+'.h5')
					Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'_Optimizer'+'.h5')
				
					symbolic_weights = getattr(agent.model.optimizer, 'weights')
					weight_values = K.batch_get_value(symbolic_weights)
					with open(Optimizer_Filename, 'wb') as f:
						pickle.dump(weight_values, f)

					agent.model.save_weights(Weights_Filename)
				else : 
					best_agent_weights = agent.model
					Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'.h5')
					agent.model.save(Filename)

				Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'BestAgent'+str(self.ID)+'_Memory'+'.p')
				pickle.dump(best_agent_memory, open(Memory_Filename, 'wb'))
				print("New best agent found. Saved in {}".format(Memory_Filename))
				Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Train'+'.p')
				print('Dumping Training Results into pickle file.')
				Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", Session_ID,'Agent'+str(self.ID)+'_Loss'+'.p')
				print('Dumping Loss Results into pickle file.')
				pickle.dump(agent.loss, open(Loss_Filename, 'wb'))

		return(best_agent_weights, best_agent_memory)