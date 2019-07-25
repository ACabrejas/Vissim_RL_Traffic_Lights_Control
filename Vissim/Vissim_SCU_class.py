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
				 compatible_actions,\
				 Signal_Groups = None,\
				 green_time = 40,\
				 redamber_time = 1,\
				 amber_time = 3, \
				 red_time = 1\
				):

		# To be read derectly inside the model on inside a specified dictionnary
		# created by hand for each model
		self.state_type = 'QueuesSig'
		self.state_size = [5]
		self.reward_type = 'Queues'
		self.ID = 0
		
		# get Vissim, signal controller and its signal groups
		self.Vissim = Vissim
		self.signal_controller = Signal_Controller
		
		if Signal_Groups is None :
			self.signal_groups = self.signal_controller.SGs
		else :
			self.signal_groups = Signal_Groups


		# implement 1st action to start
		self.action_key = 0   # dict key of current action (we start with 0) 
		self.next_action_key = 0
			
		# get stae and reward parameters
		self.state = self.calculate_state()
		self.next_state = None
		self.reward = self.calculate_reward()  
	   
		self.compatible_actions = compatible_actions
		  
		self.time_steps_per_second = self.Vissim.Simulation.AttValue('SimRes')
		
		self.green_time = green_time * self.time_steps_per_second # the green time is in step
		self.redamber_time = redamber_time * self.time_steps_per_second
		self.amber_time = amber_time * self.time_steps_per_second
		self.red_time = red_time * self.time_steps_per_second
	
		

		self.action_required = False # used to requests an action from agent
		self.update_counter = 1
		self.intermediate_phase = True # tracks when initiating a new action
		self.action_update(self.action_key)    
		

		self.stage = "Green" # tracks the stage particularly when in intermediate phase.
							 # Stages appear in order: "Amber" -> "Red" -> "RedAmber" -> "Green"


		


			
	'''
	sars :
	returns state, id of action, reward, next state
	'''     
	def sars(self):
	
		sars =  [self.state, self.action_key, self.reward, self.next_state]

		self.state = self.next_state
		self.action = self.next_action_key

		return(sars)

	
	'''
	calculate_state:
	Alvaro's reward function needs to be more general
	'''
	# def calculate_state(self, length = None, verbose = False):

	# 	# mesure the time taken to do this action
	# 	tic = t.time()
		
	# 	Queues = []
	# 	Lanes = []
	# 	for sg in self.signal_groups :
	# 		q = 0 
	# 		for sh in sg.SigHeads:
	# 			if (sh.Lane.AttValue('Link'),sh.Lane.AttValue('Index')) not in Lanes :
	# 				Lanes.append((sh.Lane.AttValue('Link'),sh.Lane.AttValue('Index')))
	# 				for veh in sh.Lane.Vehs:
	# 					q += veh.AttValue('InQueue')
	# 		Queues.append(q)
	# 		# Summarize queue size in each lane
	# 		if verbose :
	# 			print(self.signal_controller.AttValue('No'),sg.AttValue('No'),q)
			
	# 	# now reshape
	# 	if length is not None :
	# 		state = np.reshape(Queues,[1,length])
	# 	else :
	# 		state = np.reshape(Queues,[1,len(Queues)])

	# 	tac = t.time()
	# 	#print(tac-tic)
		
	# 	return (state)



	# Those two functions could be and should be methode of the class (when we will agree on a good methode)
	def calculate_state(self):
		state = calculate_state(self.Vissim, self.state_type, self.state_size, self.next_action_key, self.ID)
		return(state)


	
	# '''
	# calculate_reward:
	# Alvaro's reward function needs to be more general
	# '''
	# def calculate_reward(self):
	# 	state = self.calculate_state()
	# 	reward = -np.sum(state)
		
	# 	return reward
	def calculate_reward(self):
		reward = calculate_reward(self.Vissim, self.reward_type, self.ID)
		return(reward)
 

	'''
	action_update :
	initiates a new action
		inputs:
		-- id of action
		-- green_time, if specified by agent (in seconds)
	'''    
	def action_update(self, next_action_key, green_time=None):
		self.intermediate_phase = True # initate intermediate_phase
		self.update_counter = 1 # set update counter zero (will get reset at self.update() )
		self.next_action_key = next_action_key
		self.current_action = self.compatible_actions[next_action_key] 
		self.new_colors = [ 2*val for val in self.current_action] # converts action to 0,1,2 range
		
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
	def _color_changer(self, signal_group, new_color, stage):
		#Get the current color

		#print('current_color')
		tic = t.time()
		current_color = self._color_convert(signal_group.AttValue("SigState"))
		tac = t.time()
		#print(tac-tic)
		change = new_color-current_color
		
		# want green but currently red
		if change == -2 and stage == "Green" :
			signal_group.SetAttValue("SigState", "AMBER")
		
		# want red but currently amber
		# if just gone red need on second before green change
		elif change == -1 and stage == "Amber" :
			signal_group.SetAttValue("SigState", "RED")
		
		# want green but currently red 
		elif change == 2 and stage == "Red" :
			signal_group.SetAttValue("SigState", "REDAMBER")
				
		# want green but currently redamber
		elif change == 1 and stage == "RedAmber":
			signal_group.SetAttValue("SigState", "GREEN")
		
		# if both red or green pass (i.e. no change keep green)
		elif change == 0 :
			pass
	

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
	
		self.update_counter -= 1
		
		# These 'if' clauses mean update computation only happens if needed
		if self.update_counter == 0. :
			# if update counter just went zero 
			# then ask for an action 
			if self.intermediate_phase is False :
				self.action_required = True 

				# Comment this out because it slow they are not implemented yet 

				self.next_state = self.calculate_state()
				self.reward = self.calculate_reward()
					
			# if during a change
			# then make the change
			if self.intermediate_phase is True : 
				self.action_required = False
				
				# Get light color right for each signal group
				for sg in self.signal_groups :
					
					ID = sg.AttValue('No')-1
					tic = t.time()
					self._color_changer(sg, self.new_colors[ID], self.stage)
					tac = t.time()
					#('_color_changer')
					#print(tac-tic)
						
				# change the current stage and get time the stage last for
				time = self._stage_changer(self.stage)
				self.update_counter = time
					
				# if full transition (Amber->Red->RedAmber-Green) to green done  
				if self.stage == "Green" :
					self.intermediate_phase = False # record current action is implemented


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