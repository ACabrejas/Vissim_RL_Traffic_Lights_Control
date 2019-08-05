
from Actor_Critic_Class import ACAgent
from Vissim_env_class import environment

class MasterAC_Agent():
	"""
	A Master class agent containing the other agents.

	"""

	def __init__(self, model_name, vissim_working_directory, sim_length, Model_dictionnary, n_step_size, gamma, alpha, entropy, value, \
				timesteps_per_second = 1, verbose = True, horizon = 100, \
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


		# For saving Put here all relevent information
		self.Session_ID = "Actor_critic" 
		

		# for the monitoring only for AC
		self.horizon = horizon
		self.n_sample = n_sample

		self.Agents = {}

		for idx, info in Model_dictionnary['junctions'].items():
				acts = info['default_actions']
				if info['controled_by_com'] :
					Agents['idx'] = ACAgent(info['state_size'], len(acts), idx, self.n_step_size, self.gamma, self.alpha, self.entropy, self.value)
				

	def train(self, number_of_steps):
		self.env = environment(self.model_name, self.vissim_working_directory, self.sim_length, self.Model_dictionnary,\
			timesteps_per_second = self.timesteps_per_second, mode = 'training', delete_results = True, verbose = True)

		start_state = self.env.get_state()
		actions = {}
		for idx, s in start_state.items():
					actions[idx] = int(self.Agents[idx].choose_action(s))

		for i in range(number_of_steps):
			SARSDs = self.env.step_to_next_action(actions)

			actions = dict()
			for idx , sarsd in SARSDs.items():
				s,a,r,ns,d = sarsd
				
				#print(sarsd)
				self.Agents[idx].remember(s,a,r,ns,d)
				if len(self.Agents[idx].memory) >= self.Agents[idx].n_step_size :
					self.Agents[idx].learn() 
				
				# in order to find the next action you need to evaluate the "next_state" because it is the current state of the simulator
				actions[idx] = int(self.Agents[idx].choose_action(ns))
				#print(actions)
				
				
			# For the saving , monitoring of the agent 
			if self.env.done :
				self.env.reset()

				
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
							
				actions = {}
				for idx, s in start_state.items():
					actions[idx] = Agents[idx].choose_action(s)

	# Do a run test and save all the metrics
	def test(self):
		pass

	def save(self):
		for idx, agent in enumerate(self.Agents):
			agent.save_agent(self.vissim_working_directory, self.model_name, self.Session_ID)


	def load(self, best = True):
		for idx, agent in enumerate(self.Agents):
			agent.load_agent(self.vissim_working_directory, self.model_name , self.Session_ID, best = best)



					
