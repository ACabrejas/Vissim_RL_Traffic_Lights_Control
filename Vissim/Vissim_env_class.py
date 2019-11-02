import numpy as np
from NParser import NetworkParser
from Vissim_SCU_class import Signal_Control_Unit
import win32com.client
import os
import pickle

from time import time


# The environment class , 
class environment():
	"""
	This is an python environnement on top of VISSIM simulation software.

	-Load the model
		- It needs the Model info to be defined by hand
		- Deploy the SCU
	
	"""
	def __init__(self, model_name, vissim_working_directory, sim_length, Model_dictionary, actions_set, \
				 Random_Seed, timesteps_per_second = 1, mode = 'training', delete_results = True, verbose = True, vissim = False):
					

		# Model parameters
		self.model_name = model_name
		self.vissim_working_directory = vissim_working_directory
		self.Model_dictionary = Model_dictionary
		self.actions_set =  actions_set
		self.vehicle_demand = self.Model_dictionary['demand']['default']

		# Simulation parameters
		self.sim_length = sim_length
		self.global_counter = 0
		self.action_required = False

		self.mode = mode
		self.timesteps_per_second = timesteps_per_second

		# Evaluation parameters
		self.delete_results = delete_results
		self.verbose = verbose

		# Dispatach the COM server
		if not vissim :
			self.Vissim, _ = COMServerDispatch(model_name, vissim_working_directory, self.sim_length,\
											self.timesteps_per_second, delete_results = self.delete_results, verbose = self.verbose)
		else :
			self.Vissim = vissim

		# Setting Random Seed
		self.Vissim.Simulation.SetAttValue('RandSeed', Random_Seed)
		print ('Random seed set in simulator. Random Seed = '+str(Random_Seed))
		
		self.done = False

		# The parser can be a methode of the environment
		print("Deploying Network Parser...")
		self.npa = NetworkParser(self.Vissim, Model_dictionary)
		self.Vehicle_Inputs = list(self.Vissim.Net.VehicleInputs)
		print("Successful Network Crawl: Identified SignalControllers, Links, Lanes and Vehicle Inputs.\n")

		print("Setting Simulation mode to: " + self.mode)
		self.select_mode()

		# Simulate three steps and give the control to COM
		# The reason to simulate 3 steps is to synchronize decisions and data logging
		for _ in range(3*self.timesteps_per_second):
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
		# Version without using a network dictionary. 
		# Here signal controllers are directly inherited from the model
		# This prevents an error below where the node is created with an enumerate idx rather than its intersection ID
		#
		# This solution doesnt work well.
		# Right one needs to create the partial dictionaries directly without hacking the key in the top cells of notebook
		controller_ids_in_vissim = list(self.Model_dictionary["junctions"].keys())

		for idx, signal_controller in enumerate(self.npa.signal_controllers):
			current_vissim_id = controller_ids_in_vissim[idx]
			self.SCUs[idx] = Signal_Control_Unit(\
						 self.Vissim,\
						 signal_controller,\
						 self.Model_dictionary["junctions"][current_vissim_id],\
						 self.actions_set,\
						 idx,\
						 self.npa,\
						 current_vissim_id,\
						 Signal_Groups = None\
						)

	# retrun the state of the environnement as a dictionary
	def get_state(self):
		"""
		Get the state of the environment

		"""
		state = {}
		for idx, scu in self.SCUs.items(): 
			if scu.controled_by_com :
				state[idx] = scu.state

		return state

	def get_queues(self):
		"""
		Get the queues of each junction of the environement
		"""
		queues = {}
		for idx, scu in self.SCUs.items(): 
			queues[idx] = scu.calculate_queues()
		return queues

	def get_delays(self):
		"""
		Get the delay of each junction of the environement
		"""

		delays = {}
		for idx, scu in self.SCUs.items(): 
			delays[idx] = scu.calculate_delay()
		return delays

	def get_stop_delays(self):
		"""
		Get the delay of each junction of the environement
		"""

		delays = {}
		for idx, scu in self.SCUs.items(): 
			delays[idx] = scu.calculate_stop_delay()
		return delays


	def get_delay_timestep(self):
		"""
		Get the delay of all the cars in the network

		Get the delay of each junctions
		"""

		delay_this_timestep = self.Vissim.Net.VehicleNetworkPerformanceMeasurement.AttValue('DelayTot(Current, Last, All)')
		return (0 if delay_this_timestep is None else delay_this_timestep)

	def get_stop_delay_timestep(self):
		"""
		Get the delay of all the cars in the network

		Get the delay of each junctions
		"""

		stop_delay_this_timestep = self.Vissim.Net.VehicleNetworkPerformanceMeasurement.AttValue('DelayStopTot(Current, Last, All)')
		return (0 if stop_delay_this_timestep is None else stop_delay_this_timestep)

	
	def step(self, actions, green_time = None):
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
		Sarsd = dict()
		self.action_required = False # By default no action are needed

		# Update the action of all the junction that needded one
		# This function evaluates which SCUs require an action via whether SCUs[idx].action_required is TRUE.
		# Once started, it sets intermediate_phase to TRUE, and adds 1 to the update_counter so intermediate_phase is evaluated in SCU.update()
		# Set  next_acton_key to action_key
		# Increase green time and set_action_required to False.
		[scu.action_update(actions[idx] , green_time = green_time ) for idx, scu in self.SCUs.items() if scu.action_required]
		
		# Udapte all the SCUs nearly simutaneously
		# This functions reduces the update counter of SCUs by 1 each time it is called.
		# Once the counter reaches zero, two things can happen:
		# 1 - If we aren't making a phase change, set action_required to TRUE (request action)
		# 2 - If we are in the middle of a phase change, set action_required to FALSE and change color to finish transition
		[scu.update() for idx,scu in self.SCUs.items()]

		# not a nice way of doing this, 
		# creating the dictionary of all state, action, reward, next_state
		# Of the junctions that need a new action for the next time step.
		

		for i in range(self.timesteps_per_second):
			self.Vissim.Simulation.RunSingleStep()
		# increase the update counter by one each step (until reach simulation length)
		self.global_counter += 1
		if self.global_counter > (self.sim_length-3):
			self.done = True

		[to_dictionary(Sarsd,idx,scu.sars()+[self.done]) for idx,scu in self.SCUs.items() if scu.action_required ]

		if len(Sarsd) > 0 or self.done :
			self.action_required = True
		
		return Sarsd # return the empty dictionary is no action is required
		 
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

	def test(self):
		"""
		Testing function for external system controle. Have to set the environment to test mode
		-Mova (Have PC Mova set up and all the scu's controle by com set to false)

		Compute and return the queues over time
		"""

		# Counter to change the demande during test
		demand_counter = 0
		self.change_demand(self.vehicle_demand[demand_counter])

		#Initialisation of the metrics
		Episode_Queues = {} # 
		Cumulative_Episode_Delays = {} # Delay at each junction
		Cumulative_Episode_stop_Delays = {} # Delay at each junction

		Cumulative_Totale_network_delay = [0]
		Cumulative_Totale_network_stop_delay = [0]

		queues = self.get_queues()
		for idx, junction_queues in queues.items():
				Episode_Queues[idx] = [junction_queues]

		delays = self.get_delays()
		for idx, junction_delay in delays.items():
			Cumulative_Episode_stop_Delays[idx] = [junction_delay]

		stop_delays = self.get_stop_delays()
		for idx, junction_stop_delay in stop_delays.items():
			Cumulative_Episode_Delays[idx] = [junction_stop_delay]

		
		actions = {}

		while not self.done :

			SARSDs = self.step(actions)

			# At each steps get the metrics store
			queues = self.get_queues()
			for idx, junction_queues in queues.items():
				Episode_Queues[idx].append(junction_queues)

			delays = self.get_delays()
			for idx, junction_delay in delays.items():
				Cumulative_Episode_Delays[idx].append(Cumulative_Episode_Delays[idx][-1]+junction_delay)

			stop_delays = self.get_stop_delays()
			for idx, junction_stop_delay in stop_delays.items():
				Cumulative_Episode_stop_Delays[idx].append(Cumulative_Episode_stop_Delays[idx][-1]+junction_stop_delay)

			Cumulative_Totale_network_delay.append(Cumulative_Totale_network_delay[-1]+self.get_delay_timestep())
			Cumulative_Totale_network_stop_delay.append(Cumulative_Totale_network_stop_delay[-1]+self.get_stop_delay_timestep())

			if self.global_counter% 360 == 0:
					demand_counter += 1
					self.change_demand(self.vehicle_demand[demand_counter])

		# Stop the simulation without erasing the database
		self.Stop_Simulation(delete_results = False)
		
		return(Episode_Queues, Cumulative_Episode_Delays,Cumulative_Episode_stop_Delays, Cumulative_Totale_network_delay,Cumulative_Totale_network_stop_delay)

	def Stop_Simulation(self , delete_results = True):

	 ## Stop the simulation and delete the results
		self.Vissim.Simulation.Stop()

		if delete_results == True:
			# Delete all previous simulation runs first:
			for simRun in self.Vissim.Net.SimulationRuns:
				self.Vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)

	def reset(self):
		"""
		Reset the environment by reloading the map
		End simulation and write results to database file (*.db) while deleting them from VISSIM itself
		Increase Random Seed
		Set simulator configuration
		Simulate one step and give the control to COM
		Redeploy SCUs
		"""
		# Reset the time counter
		self.global_counter = 0
	
		# End simulation and write results to database file (*.db) while deleting them from VISSIM itself
		self.Stop_Simulation(delete_results = self.delete_results)

		# Increase Random Seed
		new_random_seed = self.Vissim.Simulation.AttValue('RandSeed')+1
		self.Vissim.Simulation.SetAttValue('RandSeed', new_random_seed)
		print("Random Seed Set to {}".format(new_random_seed))

		# Set simulator configuration
		self.select_mode()

		# Simulate one step and give the control to COM
		for _ in range(self.timesteps_per_second):
			self.Vissim.Simulation.RunSingleStep()
			self.global_counter += 1

		# Redeploy SCUs
		self._Load_SCUs()
		self.done = False


	# This function has to be changed into something more flexible
	def change_demand(self, demand_list):
		"""
		Change the demand and the number of vehicle inputs in the model
		-input Level is a factor or a string that indicate the a level of demand.
		Or the number of time of the default demand in the dictionary. 

		"""
		for idx, V_input in enumerate(self.Vehicle_Inputs):
			V_input.SetAttValue('Volume(1)', demand_list[idx])

		

		pass 


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
			self.timesteps_per_second = 1
			self.Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
			self.Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode", 1)
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
			self.Vissim.Evaluation.SetAttValue('NodeResCollectData', True)
			self.Vissim.Evaluation.SetAttValue('NodeResInterval', 3)
			
			# set the queues mesurement 
			self.Vissim.Evaluation.SetAttValue('QueuesCollectData', True)
			self.Vissim.Evaluation.SetAttValue('QueuesInterval', 3)
			
			# set the vehicles perf mesurement 
			self.Vissim.Evaluation.SetAttValue('VehNetPerfCollectData', True)
			self.Vissim.Evaluation.SetAttValue('VehNetPerfInterval', 3)
			
			# set the vehicles travel time mesurement 
			self.Vissim.Evaluation.SetAttValue('VehTravTmsCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehTravTmsInterval', 99999)
			
		# In demo mode we only use the queue counter for the moment
		elif self.mode == 'demo' :

			#This select the simulation resolution
			self.timesteps_per_second = 10
			self.Vissim.Simulation.SetAttValue('SimRes', self.timesteps_per_second)
			self.Vissim.ResumeUpdateGUI()
			
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
			self.Vissim.Evaluation.SetAttValue('NodeResCollectData', True)
			self.Vissim.Evaluation.SetAttValue('NodeResInterval', 3)
			
			
			# set the queues mesurement 
			self.Vissim.Evaluation.SetAttValue('QueuesCollectData', True)
			self.Vissim.Evaluation.SetAttValue('QueuesInterval', 3)
			
			# set the vehicles perf mesurement 
			self.Vissim.Evaluation.SetAttValue('VehNetPerfCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehNetPerfInterval', 99999)
			
			# set the vehicles travel time mesurement 
			self.Vissim.Evaluation.SetAttValue('VehTravTmsCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehTravTmsInterval', 99999)
			
		# In training mode we only use the queue counter and the delay counter for the moment    
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
			self.Vissim.Evaluation.SetAttValue('NodeResCollectData', True)
			self.Vissim.Evaluation.SetAttValue('NodeResInterval', 3)
				
			# set the queues mesurement 
			self.Vissim.Evaluation.SetAttValue('QueuesCollectData', True)
			self.Vissim.Evaluation.SetAttValue('QueuesInterval', 3)
			
			# set the vehicles perf mesurement 
			self.Vissim.Evaluation.SetAttValue('VehNetPerfCollectData', True)
			self.Vissim.Evaluation.SetAttValue('VehNetPerfInterval', 3)
			
			# set the vehicles travel time mesurement 
			self.Vissim.Evaluation.SetAttValue('VehTravTmsCollectData', False)
			self.Vissim.Evaluation.SetAttValue('VehTravTmsInterval', 99999)

		# In debug mode we only use the queue counter and the delay counter for the moment    
		elif self.mode == 'debug' :

			#This select quickmode and simulation resolution
			self.timesteps_per_second = 1
			self.Vissim.Simulation.SetAttValue('UseMaxSimSpeed', False)
			self.Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",0)
			self.Vissim.Simulation.SetAttValue('SimRes', self.timesteps_per_second)
			self.Vissim.ResumeUpdateGUI()

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
			self.Vissim.Evaluation.SetAttValue('NodeResCollectData', True)
			self.Vissim.Evaluation.SetAttValue('NodeResInterval', 3)
			
			# set the queues mesurement 
			self.Vissim.Evaluation.SetAttValue('QueuesCollectData', True)
			self.Vissim.Evaluation.SetAttValue('QueuesInterval', 3)
			
			# set the vehicles perf mesurement 
			self.Vissim.Evaluation.SetAttValue('VehNetPerfCollectData', True)
			self.Vissim.Evaluation.SetAttValue('VehNetPerfInterval', 3)
			
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

