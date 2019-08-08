
from Actor_Critic_Class import ACAgent
from Vissim_env_class import environment
import os

class MasterAC_Agent():
	"""
	A Master class agent containing the other agents.

	"""

	def __init__(self, model_name, vissim_working_directory, sim_length, Model_dictionnary, n_step_size, gamma, alpha, entropy, value, \
				timesteps_per_second = 1, Session_ID = 'AC' , verbose = True, horizon = 100, \
				n_sample = 10):



		# Model information
		self.Model_dictionnary = Model_dictionnary
		self.model_name = model_name
		self.sim_length = sim_length
		self.vissim_working_directory = vissim_working_directory
		self.timesteps_per_second = timesteps_per_second



		# Agent hyperparameters
		self.gamma = gamma
		self.alpha = alpha
		self.value = value
		self.entropy = entropy
		self.n_step_size = n_step_size

		self.number_of_episode = 0


		# For saving Put here all relevent information
		self.Session_ID = "Actor_critic" 
		

		# for the monitoring only for AC
		self.horizon = horizon
		self.n_sample = n_sample

		self.Agents = {}

		for idx, info in Model_dictionnary['junctions'].items():
				acts = info['default_actions']
				if info['controled_by_com'] :
					self.Agents[idx] = ACAgent(info['state_size'], len(acts), idx, self.n_step_size, self.gamma, self.alpha, self.entropy, self.value)
				

	def train(self, number_of_steps):
		self.env = environment(self.model_name, self.vissim_working_directory, self.sim_length, self.Model_dictionnary,\
			timesteps_per_second = self.timesteps_per_second, mode = 'training', delete_results = True, verbose = True)

		self.env = None
		self.env = environment(self.model_name, self.vissim_working_directory, self.sim_length, self.Model_dictionnary,\
			Random_Seed = self.Random_Seed, timesteps_per_second = self.timesteps_per_second, mode = 'training', delete_results = True, verbose = True)

		for idx, agent in self.Agents.items():
			agent.reset()

		start_state = self.env.get_state()

		while self.number_of_episode < number_of_episode:
			actions = {}
			for idx, s in start_state.items():
				actions[idx] = self.Agents[idx].choose_action(s)

			while True:
				SARSDs = self.env.step_to_next_action(actions)

				actions = dict()
				for idx , sarsd in SARSDs.items():
					s,a,r,ns,d = sarsd
					
					#print(sarsd)
					self.Agents[idx].remember(s,a,r,ns,d)

					# in order to find the next action you need to evaluate the "next_state" because it is the current state of the simulator
					actions[idx] = int(self.Agents[idx].choose_action(ns))
					
					
			# For the saving , monitoring of the agent 
			if self.env.done :
				self.env.reset()
				self.Random_Seed += 1
				self.number_of_episode += 1

				
				# if (i+1)%reduce_entropy_every == 0:
			 #        if Agents[idx].params['entropy'] >= entropy_threshold :
			 #            Agents[idx].reduce_entropy()
			 #            print ("Agent {} : Entropy reduced to {} " .format(idx, Agents[idx].params['entropy']))
				
				
				
				# Only for AC
				for idx, agent in enumerate(self.Agents):
					predicted_values, true_values, proba0, probas = agent.value_check(horizon, n_sample)
					print ("Agent {} : Predicted Values and True Return : \n {} \n {}" .format(idx, predicted_values, true_values))
					print ("Agent {} : Proba distribution on those states : \n {}" .format(idx, probas))
					print ("Agent {} : Proba distribution on the 0 state : \n {}" .format(idx, proba0))
					agent.reset()


				if self.number_of_episode%self.save_every == 0 :
						self.save(self.number_of_episode)	
							
				actions = {}
				for idx, s in start_state.items():
					actions[idx] = self.Agents[idx].choose_action(s)



	# Those methode could be in a general MAster agents				
	# Do a run test and save all the metrics
	def test(self):

		"""
		Function to test our agents on one episode with all the metrics : queues over time, delay
		Average reward of the agents.
		"""

		self.env = None
		self.env = environment(self.model_name, self.vissim_working_directory, self.sim_length, self.Model_dictionnary,\
			Random_Seed = self.Random_Seed, timesteps_per_second = self.timesteps_per_second, mode = 'test', delete_results = True, verbose = True)


		#Initialisation of the metrics
		Episode_Queues = {} # 
		Cumulative_Episode_Delays = {} # Delay at each junction
		Cumulative_Totale_network_delay = [0]

		queues = self.env.get_queues()
		for idx, junction_queues in queues.items():
				Episode_Queues[idx] = [junction_queues]

		delays = self.env.get_delays()
		for idx, junction_delay in delays.items():
			Cumulative_Episode_Delays[idx] = [junction_delay]


		for idx, agent in self.Agents.items():
			agent.reset()
			agent.epsilon = 0 #Set the exploration rate to 0

		start_state = self.env.get_state()

		actions = {}

		# Initialisation
		for idx, s in start_state.items():
				actions[idx] = self.Agents[idx].choose_action(s)
				


		while not self.env.done :

			SARSDs = self.env.step(actions)

			# At each steps get the metrics store
			queues = self.env.get_queues()
			for idx, junction_queues in queues.items():
				Episode_Queues[idx].append(junction_queues)

			delays = self.env.get_delays()
			for idx, junction_delay in delays.items():
				Cumulative_Episode_Delays[idx].append(Cumulative_Episode_Delays[idx][-1]+junction_delay)

			Cumulative_Totale_network_delay.append(Cumulative_Totale_network_delay[-1]+self.env.get_delay_timestep())


			if self.env.action_required:

				actions = dict()
				for idx , sarsd in SARSDs.items():
					s,a,r,ns,d = sarsd
					
					self.Agents[idx].remember(s,a,r,ns,d)
					# in order to find the next action you need to evaluate the "next_state" because it is the current state of the simulator
					actions[idx] = int(self.Agents[idx].choose_action(ns))


		# Stop the simulation without erasing the database
		self.env.Stop_Simulation(delete_results = False)
		self.env = None
		return(Episode_Queues, Cumulative_Episode_Delays, Cumulative_Totale_network_delay)


	def demo(self):
		"""
		Function to make a demo of our agents 
		"""

		self.env = None
		self.env = environment(self.model_name, self.vissim_working_directory, self.sim_length, self.Model_dictionnary,\
			Random_Seed = self.Random_Seed, timesteps_per_second = self.timesteps_per_second, mode = 'demo', delete_results = True, verbose = True)


		for idx, agent in self.Agents.items():
			agent.reset()
			agent.epsilon = 0 #Set the exploration rate to 0

		start_state = self.env.get_state()

		actions = {}

		# Initialisation
		for idx, s in start_state.items():
				actions[idx] = self.Agents[idx].choose_action(s)
				


		while not self.env.done :

			SARSDs = self.env.step(actions)



			if self.env.action_required:

				actions = dict()
				for idx , sarsd in SARSDs.items():
					s,a,r,ns,d = sarsd
					# in order to find the next action you need to evaluate the "next_state" because it is the current state of the simulator
					actions[idx] = int(self.Agents[idx].choose_action(ns))

		self.env.Stop_Simulation(delete_results = False)
		self.env = None

	def save(self , episode):
		"""
		Save all the agent with the number of episodes
		"""
		for idx, agent in self.Agents.items():
			agent.save_agent(self.vissim_working_directory, self.model_name, self.Session_ID, episode)


	def load(self, episode, best = True):
		"""

		"""
		for idx, agent in self.Agents.items():
			agent.load_agent(self.vissim_working_directory, self.model_name , self.Session_ID, episode, best = best)
		self.number_of_episode = episode



					
