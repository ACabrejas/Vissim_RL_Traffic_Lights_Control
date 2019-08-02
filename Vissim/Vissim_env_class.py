import numpy as np
from NParser import NetworkParser
from Vissim_SCU_class import Signal_Control_Unit
import win32com.client
import os

from time import time


# The environment class , 
class env():

	"""
	This is an python environnement on top of VISSIM simulation softwar.

	-Load the model
		- It needs the Model info to be defined by hand
		- Deploy the SCU
	
	"""
	def __init__(self, model_name, vissim_working_directory, sim_length, Model_dictionary,\
				 Random_Seed, mode = 'training', delete_results = True, verbose = True):

		# Model parameters
		self.model_name = model_name
		self.vissim_working_directory = vissim_working_directory
		self.Model_dictionary = Model_dictionary

		# Simulation parameters
		self.sim_length = sim_length
		self.global_counter = 0
		self.action_required = False

		self.mode = mode
		self.timesteps_per_second = None

		# Evaluation parameters
		self.delete_results = delete_results
		self.verbose = verbose

		# Dispatach the COM server
		self.Vissim, _ = COMServerDispatch(model_name, vissim_working_directory, self.sim_length,\
											self.timesteps_per_second, delete_results = self.delete_results, verbose = self.verbose)

		# Setting Random Seed
		self.Vissim.Simulation.SetAttValue('RandSeed', Random_Seed)
		print ('Random seed set in simulator. Random Seed = '+str(Random_Seed))
		
		self.done = False

		# The parser can be a methode of the environment
		print("Deploying Network Parser...")
		self.npa = NetworkParser(self.Vissim)
		print("Successful Network Crawl: Identified SignalControllers, Links and Lanes.\n")

		print("Setting Simulation mode to: " + self.mode)
		self.select_mode()
		print()

		# Simulate one step and give the control to COM
		for _ in range(self.timesteps_per_second):
			self.Vissim.Simulation.RunSingleStep()
		self.global_counter += 1

		# Deploy the SCUs and the agents
		print("Starting Deployments of Signal Control Units...")
		tic = time()
		self._Load_SCUs() # Create a dictionary of SCUs each scu control a signal controller
		tac = time()
		print("SCUs successfully deployed. Elapsed time " + str(np.round(tac-tic,2)) + " seconds.\n")
		
	def _Load_SCUs(self):
		'''
		_Load_SCUs 
			provides and create a dictionary of SCUs
		'''
		self.SCUs = dict()
		
		for idx, signal_controller in enumerate(self.npa.signal_controllers):
			self.SCUs[idx] = Signal_Control_Unit(\
						 self.Vissim,\
						 signal_controller,\
						 self.Model_dictionary[idx],\
						 idx, self.npa,\
						 Signal_Groups = None
						)

	# retrun the state of the environnement as a dictionary
	def get_state(self):
		state = {}
		for idx, scu in self.SCUs.items(): 
			state[idx] = scu.state

		return state

	def step_to_next_action(self, actions):
		"""
		Does steps until an action is required the simulator. 
		ie performs the following action
		- Advance on step time in the simulator (cars moving)
		- Change the signal group light color controled by com if needed for every intersection 
		- Compute the state of the intersections that need an action at the next time step

		Input
		- A dictionary of actions. Each action is indexed by the number of the corresponding SCU

		Return
		- if an action is required on the all network
		- a dictionary of (state, action, reward, next_state , done) the key will be the SCUs' key
		"""

		while not self.action_required:
			Sarsd = self.step(actions)

		self.action_required = False

		return Sarsd
	
	def step(self, actions):
		"""
		Does one step in the simulator. 
		ie performs the following action
		- Advance on step time in the simulator (cars moving)
		- Change the signal group light color controled by com if needed for every intersection 
		- Compute the state of the intersections that need an action at the next time step

		Input
		- A dictionary of actions. Each action is indexed by the number of the corresponding SCU

		
		Return
		- if an action is required on the all network
		- a dictionary of (state, action, reward, next_state , done) the key will be the SCUs' key
		"""
		for i in range(self.timesteps_per_second):
			self.Vissim.Simulation.RunSingleStep()
		# increase the update counter by one each step (until reach simulation length)
		self.global_counter += 1
		if self.global_counter > (self.sim_length-10):
			self.done = True

		Sarsd = dict()

		# Update the action of all the junction that needded one
		[scu.action_update(actions[idx]) for idx, scu in self.SCUs.items() if scu.action_required]
		
		# Udapte all the SCUs nearly simutaneously 
		[scu.update() for idx,scu in self.SCUs.items()]

		# not a nice way of doing this, 
		# creating the dictionary of all state, action, reward, next_state
		# Of the junctions that need a new action for the next time step.
		[to_dictionary(Sarsd,idx,scu.sars()+[self.done]) for idx,scu in self.SCUs.items() if scu.action_required ]

		if len(Sarsd) > 0 :
			self.action_required = True

		if len(Sarsd) > 0 :
			return Sarsd
		else:
			return None

	def reset(self):
		"""
		Reset the environment by reloading the map
		"""
		# Reset the time counter
		self.global_counter = 0

		# Reload the server
		COMServerReload(self.Vissim, self.model_name, self.vissim_working_directory, self.sim_length, self.timesteps_per_second, self.delete_results)
		# Update the Network Parser
		self.npa = NetworkParser(self.Vissim) 
		# Set simulator configuration
		self.select_mode()

		# Simulate one step and give the control to COM
		for _ in range(self.timesteps_per_second):
			self.Vissim.Simulation.RunSingleStep()
			self.global_counter += 1

		# Redeploy agents
		self._Load_SCUs()
		self.done = False

	def select_mode(self):
		"""
		Set mode to training, demo, debugging

		Select the mode for the metric collection 

		The metric are collected in a database located in <Model>.results
		Some metric collection are also needed for the state computation

		"""
		# In test mode all the data is stored (The simulation will be slow)
		if self.mode == 'test' :
			#This select quickmode and simulation resolution
			self.timesteps_per_second = 10
			self.Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
			self.Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode", 1)
			self.Vissim.Simulation.SetAttValue('SimRes', self.timesteps_per_second)
			self.Vissim.SuspendUpdateGUI()  
			
			# set the data mesurement
			self.Vissim.Evaluation.SetAttValue('DataCollCollectData', True)
			self.Vissim.Evaluation.SetAttValue('DataCollInterval', 1)
			
			# set the delay mesurement
			self.Vissim.Evaluation.SetAttValue('DelaysCollectData', True)
			self.Vissim.Evaluation.SetAttValue('DelaysInterval', 1)
			
			# set the data mesurement for each link
			self.Vissim.Evaluation.SetAttValue('LinkResCollectData', True)
			self.Vissim.Evaluation.SetAttValue('LinkResInterval', 1)
			
			# set the data mesurement for each node
			self.Vissim.Evaluation.SetAttValue('NodeResCollectData', True)
			self.Vissim.Evaluation.SetAttValue('NodeResInterval', 1)
			
			# set the queues mesurement 
			self.Vissim.Evaluation.SetAttValue('QueuesCollectData', True)
			self.Vissim.Evaluation.SetAttValue('QueuesInterval', 1)
			
			# set the vehicles perf mesurement 
			self.Vissim.Evaluation.SetAttValue('VehNetPerfCollectData', True)
			self.Vissim.Evaluation.SetAttValue('VehNetPerfInterval', 1)
			
			# set the vehicles travel time mesurement 
			self.Vissim.Evaluation.SetAttValue('VehTravTmsCollectData', True)
			self.Vissim.Evaluation.SetAttValue('VehTravTmsInterval', 1)
			
		# In demo mode we only use the queue counter for the moment
		elif self.mode == 'demo' :

			#This select the simulation resolution
			self.timesteps_per_second = 10
			self.Vissim.Simulation.SetAttValue('SimRes', self.timesteps_per_second)
			
			# set the data mesurement
			self.Vissim.Evaluation.SetAttValue('DataCollCollectData', False)
			self.Vissim.Evaluation.SetAttValue('DataCollInterval', 99999)
			
			# set the delay mesurement
			self.Vissim.Evaluation.SetAttValue('DelaysCollectData', False)
			self.Vissim.Evaluation.SetAttValue('DelaysInterval', 99999)
			
			# set the data mesurement for each link
			self.Vissim.Evaluation.SetAttValue('LinkResCollectData', False)
			self.Vissim.Evaluation.SetAttValue('LinkResInterval', 99999)
			
			# set the data mesurement for each node
			self.Vissim.Evaluation.SetAttValue('NodeResCollectData', False)
			self.Vissim.Evaluation.SetAttValue('NodeResInterval', 99999)
			
			
			# set the queues mesurement 
			self.Vissim.Evaluation.SetAttValue('QueuesCollectData', True)
			self.Vissim.Evaluation.SetAttValue('QueuesInterval', 3)
			
			# set the vehicles perf mesurement 
			self.Vissim.Evaluation.SetAttValue('VehNetPerfCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehNetPerfInterval', 99999)
			
			# set the vehicles travel time mesurement 
			self.Vissim.Evaluation.SetAttValue('VehTravTmsCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehTravTmsInterval', 99999)
			
		# In demo mode we only use the queue counter and the delay counter for the moment    
		elif self.mode == 'training' :

			#This select quickmode and simulation resolution
			self.timesteps_per_second = 1
			self.Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
			self.Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",1)
			self.Vissim.Simulation.SetAttValue('SimRes', self.timesteps_per_second)
			self.Vissim.SuspendUpdateGUI()  


			# set the data mesurement
			self.Vissim.Evaluation.SetAttValue('DataCollCollectData', False)
			self.Vissim.Evaluation.SetAttValue('DataCollInterval', 3)
			
			# set the delay mesurement
			self.Vissim.Evaluation.SetAttValue('DelaysCollectData', False)
			self.Vissim.Evaluation.SetAttValue('DelaysInterval', 99999)
			
			# set the data mesurement for each link
			self.Vissim.Evaluation.SetAttValue('LinkResCollectData', False)
			self.Vissim.Evaluation.SetAttValue('LinkResInterval', 99999)
			
			# set the data mesurement for each node
			self.Vissim.Evaluation.SetAttValue('NodeResCollectData', False)
			self.Vissim.Evaluation.SetAttValue('NodeResInterval', 99999)
			
			
			# set the queues mesurement 
			self.Vissim.Evaluation.SetAttValue('QueuesCollectData', True)
			self.Vissim.Evaluation.SetAttValue('QueuesInterval', 3)
			
			# set the vehicles perf mesurement 
			self.Vissim.Evaluation.SetAttValue('VehNetPerfCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehNetPerfInterval', 99999)
			
			# set the vehicles travel time mesurement 
			self.Vissim.Evaluation.SetAttValue('VehTravTmsCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehTravTmsInterval', 99999)

# That is not a clean way to do this
def to_dictionary(dictionary,idx,value):
	"""
	Assign a value to an index in a dictionary
	"""
	dictionary[idx] = value

def COMServerDispatch(model_name, vissim_working_directory, sim_length, timesteps_per_second, delete_results = True, verbose = True):
	'''
	Connecting the COM Server => Open a new Vissim Window:
	Server should only be dispatched in first run. Otherwise reload model.
	'''
	for _ in range(5):
		try:
			# Setting Working Directory
			if verbose:
				print ('Working Directory set to: ' + vissim_working_directory)
				# Check Chache
				print ('Generating Cache...')
			
			# Vissim = win32com.client.gencache.EnsureDispatch("Vissim.Vissim") 
			Vissim = win32com.client.dynamic.Dispatch("Vissim.Vissim") 
		
			if verbose:
				print ('Cache generated.\n')
				print ('****************************')
				print ('*   COM Server dispatched  *')
				print ('****************************\n')
			cache_flag = True
			
			## Load the Network:
			Filename = os.path.join(vissim_working_directory, model_name, (model_name+'.inpx'))
			
			if verbose:
				print ('Attempting to load Model File: ' + model_name+'.inpx ...')
			
			if os.path.exists(Filename):
				Vissim.LoadNet(Filename)
			else:
				raise Exception("ERROR: Could not find Model file: {}".format(Filename))
			
			if verbose:
				print ('Model File load process successful.')
		
			## Setting Simulation End
			Vissim.Simulation.SetAttValue('SimPeriod', sim_length)
			
			if verbose:
				print ('Simulation length set to '+str(sim_length) + ' seconds.')
			
			## If a fresh start is needed
			if delete_results == True:
				# Delete all previous simulation runs first:
				for simRun in Vissim.Net.SimulationRuns:
					Vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)
				if verbose:
					print ('Results from Previous Simulations: Deleted. Fresh Start Available.')
		
			##Pre-fetch objects for stability
			#Simulation = Vissim.Simulation
			#if verbose:
		#		print ('Fetched and containerized Simulation Object.')
		#	Network = Vissim.Net
		
			if verbose:
				print ('Fetched and containerized Network Object \n')
				print ('*******************************************************')
				print ('*                                                     *')
				print ('*                COM SETUP COMPLETE                   *')
				print ('*                                                     *')
				print ('*******************************************************\n')
			else:
				print('Server Dispatched.')
			#return(Vissim, Simulation, Network, cache_flag)
			return(Vissim, cache_flag)
		# If loading fails
		except:
			if _ != 4:
				print("Failed load attempt " +str(_+1)+ "/5. Re-attempting.")
			elif _ == 4:
				raise Exception("Failed 5th loading attempt. Please restart program. TERMINATING NOW.")

def COMServerReload(Vissim, model_name, vissim_working_directory, simulation_length, timesteps_per_second, delete_results):
	'''
	Connecting the COM Server => Open a new Vissim Window:
	Server should only be dispatched in first run. Otherwise reload.
	'''
	#Try 5 times
	for _ in range(5):
		try:
			## Load the Network:
			Filename = os.path.join(vissim_working_directory, model_name, (model_name+'.inpx'))
			Vissim.LoadNet(Filename)

			## Setting Simulation End
			Vissim.Simulation.SetAttValue('SimPeriod', simulation_length)
			## If a fresh start is needed
			if delete_results == True:
				# Delete all previous simulation runs first:
				for simRun in Vissim.Net.SimulationRuns:
					Vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)
			return()
		# If loading fails
		except:
			if _ != 4:
				print("Failed load attempt " +str(_+1)+ "/5. Re-attempting.")
			elif _ == 4:
				raise Exception("Failed 5th loading attempt. Please restart program. TERMINATING NOW.")
				quit()
