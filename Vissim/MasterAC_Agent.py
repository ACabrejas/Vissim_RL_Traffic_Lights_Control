


class Master_agent():
	"""
	A Master class agent containing the other agents.

	"""

	def __init__(self,model_name, vissim_working_directory, sim_length, Model_dictionnary,\
				timesteps_per_second = 1, mode = 'training', delete_results = True, verbose = True):

		self.Model_dictionnary = Model_dictionnary


					
