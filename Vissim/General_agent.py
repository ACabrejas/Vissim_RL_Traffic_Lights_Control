import os
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
import pickle
import numpy as np

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
		self.memory = None
		
		# for the training
		self.loss = []
		self.episode_memory = []
		self.episode_reward = []
		self.best_reward = -10000000

		self.reward_storage = []

	# Save agents
	def save_agent(self, vissim_working_directory, model_name, agent_type, Session_ID, episode):

		# Chech if suitable folder exists
		folder =  os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID)
		if not os.path.exists(folder):
			os.makedirs(folder)
		

		if self.type == 'AC':
			Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Weights'+'.h5')
			Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Optimizer'+'.h5')
			print('Saving architecture, weights, optimizer state for agent-{}'.format(self.ID))

			symbolic_weights = getattr(self.model.optimizer, 'weights')
			weight_values = K.batch_get_value(symbolic_weights)
			with open(Optimizer_Filename, 'wb') as f:
				pickle.dump(weight_values, f)

			# little change to save weight instead of the all agent
			self.model.save_weights(Weights_Filename)

		else :
			Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'.h5')
			print('Saving architecture, weights and optimizer state for agent-{}'.format(self.ID))
			self.model.save(Filename)

		Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Memory'+'.p')
		print('Dumping agent-{} memory into pickle file'.format(self.ID))
		pickle.dump(self.memory, open(Memory_Filename, 'wb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Train'+'.p')
		print('Dumping Training Results into pickle file.')
		pickle.dump(self.reward_storage, open(Training_Progress_Filename, 'wb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Loss'+'.p')
		print('Dumping Loss Results into pickle file.')
		pickle.dump(self.loss, open(Loss_Filename, 'wb'))



	# Reload agents
	def load_agent(self, vissim_working_directory, model_name, agent_type, Session_ID, episode, best = True):
		
		print('Loading Pre-Trained Agent {}, Architecture, Optimizer and Memory.'.format(self.ID))
		if self.type == 'AC':
			if best:
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'_Optimizer'+'.h5')

			else :
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) + 'Agent'+str(self.ID)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+ str(self.ID)+'_Optimizer'+'.h5')

			# this is to build the network (to be corrected) 
			self.test()
			self.model.load_weights(Weights_Filename)

			self.model._make_train_function()
			with open(Optimizer_Filename, 'rb') as f:
				weight_values = pickle.load(f)
			self.model.optimizer.set_weights(weight_values)
			
		
		else :
			if best:
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'.h5')
			else :
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'.h5')
			print(Filename)
			self.model = load_model(Filename)

		if best:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'_Memory'+'.p')
		else:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Memory'+'.p')
		self.memory = pickle.load(open(Memory_Filename, 'rb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Train'+'.p')
		self.reward_storage = pickle.load(open(Training_Progress_Filename, 'rb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Loss'+'.p')
		self.loss = pickle.load(open(Loss_Filename, 'rb'))
			
		print('Items successfully loaded.')
		

	def best_agent(self, vissim_working_directory, model_name, agent_type, Session_ID):

		# Chech if suitable folder exists
		folder =  os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID)
		if not os.path.exists(folder):
			os.makedirs(folder)

		if self.average_reward >= np.max(self.reward_storage):
			
			best_agent_memory = self.memory
			print('Saving architecture, weights, optimizer state for best agent-{}'.format(self.ID))
			if self.type == 'AC' :
				best_agent_weights = self.model.get_weights()
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'_Optimizer'+'.h5')
			
				symbolic_weights = getattr(self.model.optimizer, 'weights')
				weight_values = K.batch_get_value(symbolic_weights)
				with open(Optimizer_Filename, 'wb') as f:
					pickle.dump(weight_values, f)

				self.model.save_weights(Weights_Filename)
			else : 
				best_agent_weights = self.model
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'.h5')
				self.model.save(Filename)

			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'BestAgent'+str(self.ID)+'_Memory'+'.p')
			pickle.dump(best_agent_memory, open(Memory_Filename, 'wb'))
			#print("New best agent found. Saved in {}".format(Memory_Filename))
			Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Agent'+str(self.ID)+'_Train'+'.p')
			#print('Dumping Training Results into pickle file.')
			Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,'Agent'+str(self.ID)+'_Loss'+'.p')
			#print('Dumping Loss Results into pickle file.')
			pickle.dump(self.loss, open(Loss_Filename, 'wb'))

		#return(best_agent_weights, best_agent_memory)

	# Save agents
	def save_integrated_agent(self, vissim_working_directory, model_name, agent_type, Session_ID, episode):

		if self.type == 'AC':
			Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Weights'+'.h5')
			Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Optimizer'+'.h5')
			print('Saving architecture, weights, optimizer state for agent-{}'.format(self.ID))

			symbolic_weights = getattr(self.model.optimizer, 'weights')
			weight_values = K.batch_get_value(symbolic_weights)
			with open(Optimizer_Filename, 'wb') as f:
				pickle.dump(weight_values, f)

			# little change to save weight instead of the all agent
			self.model.save_weights(Weights_Filename)

		else :
			folder =  os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID, "Agent{}".format(self.ID))
			if not os.path.exists(folder):
				os.makedirs(folder)
			Filename = os.path.join(folder,'Episode'+ str(episode) +'Agent'+str(self.ID)+'.h5')
			print('Saving architecture, weights and optimizer state for agent-{}'.format(self.ID))
			self.model.save(Filename)

		Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Memory'+'.p')
		print('Dumping agent-{} memory into pickle file'.format(self.ID))
		pickle.dump(self.memory, open(Memory_Filename, 'wb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Train'+'.p')
		print('Dumping Training Results into pickle file.')
		pickle.dump(self.reward_storage, open(Training_Progress_Filename, 'wb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Loss'+'.p')
		print('Dumping Loss Results into pickle file.')
		pickle.dump(self.loss, open(Loss_Filename, 'wb'))



	# Reload individually trained agents jointly into balance
	def load_isolated_agent(self, vissim_working_directory, model_name, agent_type, Session_ID, episode, best = True):
		
		# Junctions 11 and 12 train together, so they need same loading ID when loading fresh
		if self.ID == 11:
			load_id = 10
		else:
			load_id = self.ID

		print('Independently Pre-Trained Agent {}, Architecture, Optimizer and Memory.'.format(self.ID))
		if self.type == 'AC':
			if best:
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'BestAgent'+str(load_id)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'BestAgent'+str(load_id)+'_Optimizer'+'.h5')

			else :
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) + 'Agent'+str(load_id)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+ str(load_id)+'_Optimizer'+'.h5')

			# this is to build the network (to be corrected) 
			self.test()
			self.model.load_weights(Weights_Filename)

			self.model._make_train_function()
			with open(Optimizer_Filename, 'rb') as f:
				weight_values = pickle.load(f)
			self.model.optimizer.set_weights(weight_values)
			
		else :
			if best:
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID, "Agent{}".format(self.ID),'BestAgent'+str(load_id)+'.h5')
			else :
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(load_id)+'.h5')
			
			self.model = load_model(Filename)

		if best:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'BestAgent'+str(load_id)+'_Memory'+'.p')
		else:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(load_id)+'_Memory'+'.p')
		self.memory = pickle.load(open(Memory_Filename, 'rb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(load_id)+'_Train'+'.p')
		self.reward_storage = pickle.load(open(Training_Progress_Filename, 'rb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_source", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(load_id)+'_Loss'+'.p')
		self.loss = pickle.load(open(Loss_Filename, 'rb'))
			
		print('Success.')

# Reload agents that have already worked together in Balance from Agents_results folder
	def load_integrated_agent(self, vissim_working_directory, model_name, agent_type, Session_ID, episode, best = True):
		
		print('Loading Integrated Agent {}, Architecture, Optimizer and Memory.'.format(self.ID))
		if self.type == 'AC':
			if best:
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'BestAgent'+str(self.ID)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'BestAgent'+str(self.ID)+'_Optimizer'+'.h5')

			else :
				Weights_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) + 'Agent'+str(self.ID)+'_Weights'+'.h5')
				Optimizer_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+ str(self.ID)+'_Optimizer'+'.h5')

			# this is to build the network (to be corrected) 
			self.test()
			self.model.load_weights(Weights_Filename)

			self.model._make_train_function()
			with open(Optimizer_Filename, 'rb') as f:
				weight_values = pickle.load(f)
			self.model.optimizer.set_weights(weight_values)
			
		
		else :
			if best:
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID, "Agent{}".format(self.ID),'BestAgent'+str(self.ID)+'.h5')
			else :
				Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'.h5')
			
			self.model = load_model(Filename)

		if best:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'BestAgent'+str(self.ID)+'_Memory'+'.p')
		else:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Memory'+'.p')
		self.memory = pickle.load(open(Memory_Filename, 'rb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Train'+'.p')
		self.reward_storage = pickle.load(open(Training_Progress_Filename, 'rb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, "Agents_Results", agent_type, Session_ID,"Agent{}".format(self.ID),'Episode'+ str(episode) +'Agent'+str(self.ID)+'_Loss'+'.p')
		self.loss = pickle.load(open(Loss_Filename, 'rb'))
			
		print('Items successfully loaded.')