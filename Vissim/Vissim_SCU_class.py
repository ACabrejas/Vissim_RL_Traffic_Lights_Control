import numpy as np
import time as t
 #SCU


'''
Signal_Control_Unit :
	
	interfaces between a signal controller (at a junction) and actions (provided by an agent)
	
	inputs:
	-- Vissim
	-- Signal_Controller - a Vissim, signal controller
	-- compatible_actions - a dictionary taking IDs to vectors non-conflicting signal groups
	-- green_time = 10   (times are in seconds but converted to simulation steps)
	-- redamber_time = 1
	-- amber_time = 3
	-- red_time = 1
	 
	methods :
	-- action_update():
			initiates the change to a new action
			
			inputs:
			-- action_key 
			-- green_time 
	-- update():
			ensures each signal is correct at each simulation step
'''
class Signal_Control_Unit:
	
	def __init__(self,\
				 Vissim,\
				 Signal_Controller,\
				 Intersection_info,\
				 Signal_Groups = None,\
				):

		# To be read derectly inside the model on inside a specified dictionnary
		# created by hand for each model
		self.state_type = Intersection_info['state_type']
		self.state_size = Intersection_info['state_size']
		self.reward_type = Intersection_info['reward_type']
		self.compatible_actions = Intersection_info['compatible_actions']

		# Those are for the moment not Vissim object
		self.Lanes_names = Intersection_info['lane']
		self.Links_names = Intersection_info['link']

		# Time of the different stage, and the minimal green time
		self.time_steps_per_second = Vissim.Simulation.AttValue('SimRes')
		self.green_time = Intersection_info['green_time'] * self.time_steps_per_second # the green time is in step
		self.redamber_time = Intersection_info['redamber_time'] * self.time_steps_per_second
		self.amber_time = Intersection_info['amber_time'] * self.time_steps_per_second
		self.red_time = Intersection_info['red_time'] * self.time_steps_per_second

		#Controle by com ?
		self.controled_by_com = Intersection_info['controled_by_com']
		
		
		# Those are Vissim objects (Do we need to work on the networkparser ?)
		# or do we get rid of it completely
		# get Vissim, signal controller and its signal groups
		self.signal_controller = Signal_Controller
		if Signal_Groups is None :
			self.signal_groups = self.signal_controller.SGs
		else :
			self.signal_groups = Signal_Groups


		# Give the controle to com or not

		if self.controled_by_com:
			for group in self.signal_groups:
				group.SetAttValue('ContrByCOM',1)
			#self.action_required = False # used to requests an action from agent
			self.update_counter = 1
			# implement 1st action to start
			self.action_key = 0   # dict key of current action (we start with 0)
			self.action = self.compatible_actions[self.action_key] 

			self.next_action_key = 0
			self.next_action = self.compatible_actions[self.next_action_key] 



			self.action_update(self.action_key)    
			self.stage = "Green" # tracks the stage particularly when in intermediate phase.
								 # Stages appear in order: "Amber" -> "Red" -> "RedAmber" -> "Green"

		else :
			self.action_required = False

		self.Vissim_Links = []
		self.Vissim_Lanes = []
		for link in self.Links_names:
			self.Vissim_Links.append(Vissim.Net.Links.ItemByKey(link))

		for link in self.Links_names:
			for lane in Vissim.Net.Links.ItemByKey(link).Lanes:
				self.Vissim_Lanes.append(lane)
		
		
			
		# get state and reward parameters
		self.state = self.calculate_state()
		self.next_state = None
		self.reward = self.calculate_reward()  
	   
		
	'''
	sars :
	returns state, id of action, reward, next state
	'''     
	def sars(self):
	
		sars =  [self.state, self.action_key, self.reward, self.next_state]

		self.state = self.next_state
		self.action = self.next_action_key

		return(sars)

	# Those two functions could be and should be methode of the class (when we will agree on a good methode)
	def calculate_state(self):
		if self.state_type == 'Queues':
			state = [get_queue(lane) for lane in self.Vissim_Lanes]

		state = np.array(state)[np.newaxis,:]
		
		return(state)


	# 	return reward
	def calculate_reward(self):
		if self.reward_type == 'Queues':
			reward = -np.sum(self.state)
		return(reward)
 

	'''
	action_update :
	initiates a new action
		inputs:
		-- id of action
		-- green_time, if specified by agent (in seconds)
	'''    
	def action_update(self, action, green_time=None):
		self.intermediate_phase = True # initate intermediate_phase
		self.update_counter = 1 # set update counter zero (will get reset at self.update())
		self.next_action_key = action

		self.next_action = self.compatible_actions[action] 
		
		
		if green_time is not None:
			self.green_time = green_time * self.time_steps_per_second

		self.action_required = False
		

	# internal helper function
	# red = 0, amber/redamber = 1 and green = 2
	def _color_convert(self,color):

		if color == "RED" :
			return 0
		elif color == "GREEN" :
			return 2
		else :
			return 1

		
	'''
	_color_changer :
	Internal function
	Changes color of a signal group
		inputs:
		-- signal group
		-- new_color : 2 = green / 0 = red
		-- stage : what stage all lights in the controller are.
	'''          
	def _color_changer(self):
		#Get the current color

		current_color =  [2*val for val in self.action]
		next_color = [2*val for val in self.next_action_key] 

		transition_vector = np.subtract()

		change = np.subtract(self.new_colors, self.current_color)
		
		# want green but currently red
		


		# want red but currently amber
		# if just gone red need on second before green change
		


		
		# want green but currently red 
		

				
		# want green but currently redamber
		

		
		# if both red or green pass (i.e. no change keep green)
		

	

	'''
	_stage_changer :
	Internal function
	
	Track controllers stage (in the stages of Amber->Red->RedAmber-Green) 
	and time for each transtion
	
	TO DO :
	-Find a way to skip a stage if it's allocated time is 0 for exemple if we don't want redamber or red time.
	
		inputs:
		-- stage
		
	Nb. stage is a controller method while color is a sg property
	'''
	def _stage_changer(self,stage):
		
		if stage == "Green" :
			time = self.amber_time
			self.stage = "Amber" 
	
		elif stage == "Amber" :
			if self.red_time == 0:
				time = self.redamber_time
				self.stage = "RedAmber"

				if self.redamber_time == 0:
					time = self.green_time
					self.stage = "Green"

			else :
				time = self.red_time
				self.stage = "Red"
		

		# what is this red stage ? a stage where all the light are red ?
		elif stage == "Red" :

			if self.redamber_time == 0:
				time = self.green_time
				self.stage = "Green"

			else :
				time = self.redamber_time
				self.stage = "RedAmber"
				
		# want green but currently redamber
		elif stage == "RedAmber" :
			time = self.green_time
			self.stage = "Green"
		
		return time
				
		
	'''
	update :
	
	returns True if action required (otherwise is None)
	
	implements cycle at each signal group
	and updates the stage of the controllers.
	
	(writen so multiple controllers can be updated in parallel)
	(Computational Overhead should be lower than before)
	
	'''   
	def update(self):

		if not self.controled_by_com :
			pass
		else :
			self.update_counter -= 1
			# These 'if' clauses mean update computation only happens if needed
			if self.update_counter == 0. :
				# if update counter just went zero 
				# then ask for an action 
				if self.intermediate_phase is False :
					self.action_required = True 

					self.next_state = self.calculate_state()
					self.reward = self.calculate_reward()
						
				# if during a change
				# then make the change
				if self.intermediate_phase is True : 
					self.action_required = False
					
					# Get light color right for each signal group


					self._color_changer()
					
					# for sg in self.signal_groups :
						
					# 	ID = sg.AttValue('No')-1
					# 	tic = t.time()
					# 	self._color_changer(sg, self.new_colors[ID], self.stage)
					# 	tac = t.time()
					# 	#('_color_changer')
					# 	#print(tac-tic)
							
					# change the current stage and get time the stage last for
					time = self._stage_changer(self.stage)
					self.update_counter = time
						
					# if full transition (Amber->Red->RedAmber-Green) to green done  
					if self.stage == "Green" :
						self.intermediate_phase = False # record current action is implemented





#Fonction to compute the queue in a lane

def get_queue(lane):

	vehicles_in_lane = lane.Vehs
	queue_in_lane = np.sum([vehicle.AttValue('InQueue') for vehicle in vehicles_in_lane])

	return(queue_in_lane)



# For one intersection here is the state and reward computation methode

# We should script those function later because it is only for the basic intersection here
# ID will be the ID / number of the intersection 
def calculate_state(Vissim, state_type, state_size, action, ID):
	if state_type == 'Queues':
		#Obtain Queue Values (average value over the last period)
		West_Queue  = Vissim.Net.QueueCounters.ItemByKey(1).AttValue('QLen(Current,Last)')
		South_Queue = Vissim.Net.QueueCounters.ItemByKey(2).AttValue('QLen(Current,Last)')
		East_Queue  = Vissim.Net.QueueCounters.ItemByKey(3).AttValue('QLen(Current,Last)')
		North_Queue = Vissim.Net.QueueCounters.ItemByKey(4).AttValue('QLen(Current,Last)')
		state = [West_Queue, South_Queue, East_Queue, North_Queue]
		state = [0. if state is None else state for state in state]
		state = np.reshape(state, state_size)[np.newaxis,:]
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
		pre_state = [0. if state is None else state for state in pre_state]
		state = [pre_state[0]*pre_state[4], pre_state[1]*pre_state[5], pre_state[2]*pre_state[6], pre_state[3]*pre_state[7]]
		state = np.reshape(state, state_size)[np.newaxis,:]
		return(state)
	
	elif state_type == 'QueuesSig':
		#Obtain Queue Values (average value over the last period)
		West_Queue  = Vissim.Net.QueueCounters.ItemByKey(1).AttValue('QLen(Current,Last)')		
		South_Queue = Vissim.Net.QueueCounters.ItemByKey(2).AttValue('QLen(Current,Last)')		
		East_Queue  = Vissim.Net.QueueCounters.ItemByKey(3).AttValue('QLen(Current,Last)')
		North_Queue = Vissim.Net.QueueCounters.ItemByKey(4).AttValue('QLen(Current,Last)')
		
		# Obtain the signal state  We only need 2 out of 4 for our basic intersection in fact we only need 1 out of 4
		
		
		state = [West_Queue, South_Queue, East_Queue, North_Queue, action]
		state = [0. if state is None else state for state in state]
		state = np.reshape(state, state_size)[np.newaxis,:]
		
		
		return(state)
		
	elif state_type == 'CellsSpeedSig':
		Detectors = Vissim.Net.Detectors.GetAll()
		state = [0 for i in range(len(Detectors)+1)]
		for index , Detector in enumerate(Detectors):
			state[index] = Detector.AttValue('VehSpeed') 

		
		state[-1] = action

		state = [-1. if state is None else state for state in state]
		state = np.reshape(state, state_size)[np.newaxis,:]
	
		return(state)

	elif state_type == 'CellsSpeedOccSig':
		Detectors = Vissim.Net.Detectors.GetAll()
		state = [0 for i in range(2*len(Detectors)+1)]
		for index , Detector in enumerate(Detectors):
			state[2*index] = Detector.AttValue('VehSpeed') 
			state[2*index+1] = Detector.AttValue('OccupRate') 

		
		state[-1] = action

		state = [-1. if state is None else state for state in state]
		state = np.reshape(state, state_size)[np.newaxis,:]
		#print(state)

		return(state)

	elif state_type == 'CellsOccSig':
		Detectors = Vissim.Net.Detectors.GetAll()
		state = [0 for i in range(len(Detectors)+1)]
		for index , Detector in enumerate(Detectors):
			state[index] = Detector.AttValue('OccupRate') 

		
		state[-1] = agent.action

		state = [-1. if state is None else state for state in state]
		state = np.reshape(state, state_size)[np.newaxis,:]

		return(state)

	elif state_type == 'CellsT':
		Detectors = Vissim.Net.Detectors.GetAll()
		Occupancy = [0 for i in range(len(Detectors))]
		Speed = [0 for i in range(len(Detectors))]
		for index , Detector in enumerate(Detectors):
			Speed[index] = Detector.AttValue('VehSpeed') 
			Occupancy[index] = Detector.AttValue('OccupRate') 

		Occupancy = [-1. if occ is None else occ for occ in Occupancy]
		Speed = [-1. if sp is None else sp for sp in Speed]

		Occupancy = np.reshape(Occupancy, state_size[1:])[np.newaxis, :]
		Speed = np.reshape(Speed, state_size[1:])[np.newaxis, :]

		state = np.concatenate([Occupancy, Speed], axis=0)

		state = np.reshape(state, state_size)[np.newaxis,:]

		return(state)

	elif state_type == 'QueuesCellsSpeedOccSig':
		Detectors = Vissim.Net.Detectors.GetAll()
		state = [0 for i in range(2*len(Detectors)+1+4)]
		for index , Detector in enumerate(Detectors):
			state[2*index] = Detector.AttValue('VehSpeed') 
			state[2*index+1] = Detector.AttValue('OccupRate') 

		state[-1] = action
		state[-2]  = Vissim.Net.QueueCounters.ItemByKey(1).AttValue('QLen(Current,Last)')		
		state[-3] = Vissim.Net.QueueCounters.ItemByKey(2).AttValue('QLen(Current,Last)')		
		state[-4]  = Vissim.Net.QueueCounters.ItemByKey(3).AttValue('QLen(Current,Last)')
		state[-5] = Vissim.Net.QueueCounters.ItemByKey(4).AttValue('QLen(Current,Last)')

		state = [-1. if state is None else state for state in state]
		state = np.reshape(state, state_size)[np.newaxis,:]
		
		return(state)	
	elif state_type == 'MaxFlow':
		pass
	elif state_type == 'FuelConsumption':
		pass
	elif state_type == 'NOx':
		pass
	elif state_type == "COM":
		pass
# For the moment We only work on a particuliar junction    
	elif state_type == "Clusters":
		return(Vp.Clustering(Vissim))

# The calculate reward is now separate from the agent state (this can cause the simulation to be slower)
def calculate_reward(Vissim, reward_type, ID):
	if reward_type == 'Queues':
		#Obtain Queue Values (average value over the last period)
		West_Queue  = Vissim.Net.QueueCounters.ItemByKey(1).AttValue('QLen(Current,Last)')
		South_Queue = Vissim.Net.QueueCounters.ItemByKey(2).AttValue('QLen(Current,Last)')
		East_Queue  = Vissim.Net.QueueCounters.ItemByKey(3).AttValue('QLen(Current,Last)')
		North_Queue = Vissim.Net.QueueCounters.ItemByKey(4).AttValue('QLen(Current,Last)')
		state = [West_Queue, South_Queue, East_Queue, North_Queue]
		state = [0. if state is None else state for state in state]
		state = np.reshape(state, [1,len(state)])
		pass
		
		
	elif reward_type == 'Delay':
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
		state = np.reshape(state, [1,len(state)])
		pass
		
	elif reward_type == 'MaxFlow':
		pass
	elif reward_type == 'FuelConsumption':
		pass
	elif reward_type == 'NOx':
		pass
	elif reward_type == "COM":
		pass
		
	# For the moment We only work on a particuliar junction    	
	if reward_type == 'Queues':
		reward = -np.sum([0. if state is None else state for state in state[0]])
		#print(reward)
	if reward_type == 'QueuesDifference':
		current_queue_sum = -np.sum([0. if state is None else state for state in state[0]])
		previous_queue_sum =  -np.sum([0. if state is None else state for state in state[0]])
		reward = previous_queue_sum - current_queue_sum
		
	return reward