import numpy as np
from time import time
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
		
		# get Vissim, signal controller and its signal groups
		self.Vissim = Vissim
		self.signal_controller = Signal_Controller
		
		if Signal_Groups is None :
			self.signal_groups = self.signal_controller.SGs
		else :
			self.signal_groups = Signal_Groups
			
		# get stae and reward parameters
		self.state = self.calculate_state()
		self.reward = self.calculate_reward()  
	   
		self.compatible_actions = compatible_actions
		  
		self.time_steps_per_second = self.Vissim.Simulation.AttValue('SimRes')
		
		self.green_time = green_time * self.time_steps_per_second # the green time is in step
		self.redamber_time = redamber_time * self.time_steps_per_second
		self.amber_time = amber_time * self.time_steps_per_second
		self.red_time = red_time * self.time_steps_per_second
	
		# implement 1st action to start
		self.action_key = 0   # dict key of current action (we start with 0) 
		self.action_required = False # used to requests an action from agent
		self.update_counter = 0
		self.intermediate_phase = True # tracks when initiating a new action
		self.action_update(self.action_key)    
		

		self.stage = "Green" # tracks the stage particularly when in intermediate phase.
							 # Stages appear in order: "Amber" -> "Red" -> "RedAmber" -> "Green"

			
	'''
	sars :
	returns state, id of action, reward
	'''     
	def sar(self):
		self.state = self.calculate_state()
		self.reward = self.calculate_reward()
		
		return self.state, self.action_key, self.reward

	
	'''
	calculate_state:
	Alvaro's reward function needs to be more general
	'''
	def calculate_state(self, length = None, verbose = False):

		tic = time()
		
		Queues = []
		Lanes = []
		for sg in self.signal_groups :
			q = 0 
			for sh in sg.SigHeads:
				if (sh.Lane.AttValue('Link'),sh.Lane.AttValue('Index')) not in Lanes :
					Lanes.append((sh.Lane.AttValue('Link'),sh.Lane.AttValue('Index')))
					for veh in sh.Lane.Vehs:
						q += veh.AttValue('InQueue')
			Queues.append(q)
			# Summarize queue size in each lane
			if verbose :
				print(self.signal_controller.AttValue('No'),sg.AttValue('No'),q)
			
		# now reshape
		if length is not None :
			state = np.reshape(Queues,[1,length])
		else :
			state = np.reshape(Queues,[1,len(Queues)])

		tac = time()
		print(tac-tic)
		
		return (state)

	
	'''
	calculate_reward:
	Alvaro's reward function needs to be more general
	'''
	def calculate_reward(self):
		state = self.calculate_state()
		reward = -np.sum(state)
		
		return reward
 

	'''
	action_update :
	initiates a new action
		inputs:
		-- id of action
		-- green_time, if specified by agent (in seconds)
	'''    
	def action_update(self, action_key, green_time=None):
		self.intermediate_phase = True # initate intermediate_phase
		self.update_counter = 1 # set update counter zero (will get reset at self.update() )
		self.action_key = action_key
		self.current_action = self.compatible_actions[action_key] 
		self.new_colors = [ 2*val for val in self.current_action] # converts action to 0,1,2 range
		
		if green_time is not None:
			self.green_time = green_time * self.time_steps_per_second
		

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
	def _color_changer(self,signal_group,new_color,stage):
		#Get the current color
		current_color = self._color_convert(signal_group.AttValue("SigState"))
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
	
		inputs:
		-- stage
		
	Nb. stage is a controller method while color is a sg property
	'''
	def _stage_changer(self,stage):
		
		if stage == "Green" :
			time = self.amber_time
			self.stage = "Amber" 
	
		elif stage == "Amber" :
			time = self.red_time
			self.stage = "Red"
		
		elif stage == "Red" :
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
		if self.update_counter == 0 :
			# if update counter just went zero 
			# then ask for an action 
			if self.intermediate_phase is False :
				self.action_required = True 
				
					
			# if during a change
			# then make the change
			if self.intermediate_phase is True : 
				self.action_reqired = False
				
				# Get light color right for each signal group
				for sg in self.signal_groups :
					ID = sg.AttValue('No')-1
					self._color_changer(sg, self.new_colors[ID], self.stage)
						
				# change the current stage and get time the stage last for
				time = self._stage_changer(self.stage)
				self.update_counter = time
					
				# if full transition (Amber->Red->RedAmber-Green) to green done  
				if self.stage == "Green" :
					self.intermediate_phase = False # record current action is implemented