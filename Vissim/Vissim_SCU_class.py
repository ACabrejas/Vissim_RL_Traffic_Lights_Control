import numpy as np
import time as time
import pickle

class Signal_Control_Unit():
	"""
	Signal_Control_Unit :
	Interfaces between a signal controller (which operates the junction) and the agents (which provide the actions to implement).
	
	Inputs:
	-- Vissim
	-- Signal_Controller - a Vissim, signal controller
	-- compatible_actions - a dictionary taking IDs to vectors non-conflicting signal groups
	-- green_time = 10   (times are in seconds but converted to simulation steps)
	-- redamber_time = 1
	-- amber_time = 3
	-- red_time = 1
	 
	Methods :
	-- action_update():
			Initiates the change to a new action.

			Inputs:
			-- action_key 
			-- green_time

	-- update():
			ensures each signal is correct at each simulation step
	"""
	
	def __init__(self,\
				 Vissim,\
				 Signal_Controller_Object,\
				 Intersection_info,\
				 actions_set,\
				 Identificator,\
				 npa,\
				 Vissim_ID,\
				 Signal_Groups = None\
				):
		#####################################
		# Set basic information for the SCU # 
		#####################################

		# ID so it can be matched with "env.SCUs[ID]"
		self.ID = Identificator
		self.Vissim_ID = Vissim_ID

		## Read information from "Intersection Info" dictionary. These will be names and values.
		## Objects as such are imported in the section below.
		self.state_type = Intersection_info['state_type']
		self.state_size = Intersection_info['state_size']
		self.reward_type = Intersection_info['reward_type']
		self.compatible_actions = Intersection_info['default_actions']
		self.all_actions = Intersection_info['all_actions']
		# Those are for the moment not Vissim objects, it is the index of object located in the simulator
		self.Lanes_names = Intersection_info['lane']
		self.Links_names = Intersection_info['link']
		# Time of the different stage, and the minimal green time
		self.time_steps_per_second = Vissim.Simulation.AttValue('SimRes')
		self.green_time = Intersection_info['green_time'] # the green time is in step
		self.redamber_time = Intersection_info['redamber_time'] 
		self.amber_time = Intersection_info['amber_time'] 
		self.red_time = Intersection_info['red_time']

		# Controlled by com?
		self.controled_by_com = Intersection_info['controled_by_com']

		# Default actions or all available actions?
		self.compatible_actions = Intersection_info[actions_set]
	
		#################################
		# Fetch Objects operated by SCU # 
		#################################

		# Queue counters for this intersection, dictionnary has to countain the queue counters ID
		self.queues_counter_ID = Intersection_info['queues_counter_ID']
		# Put the simulation objects in Vissim in a list
		self.queues_counters = [ Vissim.Net.QueueCounters.ItemByKey(i) for i in self.queues_counter_ID]

		# Signal Controller
		self.signal_controller = Signal_Controller_Object
		# Signal Groups
		if Signal_Groups is None :
			self.signal_groups = npa.signal_groups[self.ID]
			#self.signal_groups = self.signal_controller.SGs
		else :
			self.signal_groups = Signal_Groups
		#self.signal_heads  = npa.signal_heads[self.ID]
		# Links operated
		self.Vissim_Links = []
		for link in self.Links_names:
			self.Vissim_Links.append(Vissim.Net.Links.ItemByKey(link))
		# Lanes operated
		self.Vissim_Lanes = []
		for link in self.Links_names:
			for lane in Vissim.Net.Links.ItemByKey(link).Lanes:
				self.Vissim_Lanes.append(lane)
	
		# Node of this intersection (could be in the network Parser)
		self.Node = Vissim.Net.Nodes.ItemByKey(self.Vissim_ID+1) #To be corrected Vissim object count object begin at 1
		# Vehicle Network Performance Measurement Object
		self.VehNetPerformance = Vissim.Net.VehicleNetworkPerformanceMeasurement
		# Transform the movements into a python list (hacky technique to be because the list[-1] doesnt work with Vissim list)
		movements = list(self.Node.Movements)

		self.junction_movement = movements[-1] #The last one is the movement of the whole intersection
		self.lanes_movement = movements[:-1]  # The other movement are the lane movement


		#####################################
		# Pass Traffic Light Control to COM #
		#####################################

		# Set the Signal Control to be exclusively controlled by COM
		if self.controled_by_com:
			# Set COM Control
			for group in self.signal_groups:
				group.SetAttValue('ContrByCOM',1)
			# Set initial time to update SCUs
			self.update_counter = 1
			# Set initial action and next action 

			#### MAKE SURE THIS IS CORRECTLY IMPLEMENTED
			self.action_key = 0
			self.next_action_key = 0
			# Initiate Action on the SCU
			self.action_update(self.action_key)
			self.force_safe_colors(self.compatible_actions[self.action_key])  

			# Initialize state and reward variables
			self.state = self.calculate_state()
			self.next_state = None
			self.reward = self.calculate_reward() 
			# "stage" tracks the stage particularly when in intermediate phase.
			# Stages appear in order: "Amber" -> "Red" -> "RedAmber" -> "Green"
			# It is used to change the light of the signal group in _color_changer
			self.stage = "Green"
		else :
			self.action_required = False
	
	def force_safe_colors(self, target_colors):
		'''
		Only to be used in "Not intermediate phases".
		This means all lights should be either GREEN OR RED and no changes can be happening.
		This function ensures the correct initial configuration of colors.
		It forces all Signal Groups in the Signal Controller to be set to the action taken as input.
		'''
		for idx, value in enumerate(target_colors):
			if value == 1:
				self.signal_groups[idx].SetAttValue("SigState", "GREEN")
				#print("Set Forced Green in SG{}".format(idx))
			elif value == 0:
				self.signal_groups[idx].SetAttValue("SigState", "RED")
				#print("Set Forced Red in SG{}".format(idx))
			else:
				raise ValueError("Unexpected value found in Target Colors in \"force_safe_colors\" method in the SCU class.")

	   
	def sars(self):
		"""
		sars :
		returns state, id of action, reward, next state
		THIS function actualy change the object. (There should be a better way...). Or we can duplicate
		the function in case we only want the state, action ,reward, next_state without changing the SCU
		"""

		#Compute the state for the RL agent to find the next best action
		self.next_state = self.calculate_state()
		self.reward = self.calculate_reward()

		sars =  [self.state, self.action_key, self.reward, self.next_state]

		self.state = self.next_state
		self.action_key = self.next_action_key
		return(sars)

	def calculate_state(self):
		"""
		Compute the state of the SCU.
		"""
		if self.state_type == 'Queues':
			#self.queue_state  =\
			#[0. if movement.AttValue('QLen(Current, Last)') is None else movement.AttValue('QLen(Current, Last)') for movement in self.lanes_movement]

			self.queue_state  =\
			[0. if queue.AttValue('QLen(Current, Last)') is None else queue.AttValue('QLen(Current, Last)') for queue in self.queues_counters]

			state = np.array(self.queue_state)[np.newaxis,:]

		if self.state_type == "QueuesSig":

			self.queue_state  =\
			[0. if queue.AttValue('QLen(Current, Last)') is None else queue.AttValue('QLen(Current, Last)') for queue in self.queues_counters]

			state = np.array(self.queue_state+[self.next_action_key])[np.newaxis,:]
	
		return(state)

	def calculate_queues(self):
		"""
		Only conpute the queues at this intersection

		"""
		#queues = [get_queue(lane) for lane in self.Vissim_Lanes]
		
		queues = [0. if queue.AttValue('QLen(Current, Last)') is None else queue.AttValue('QLen(Current, Last)') for queue in self.queues_counters]
		return queues  

	def calculate_reward(self):
		'''
		Compute the Reward of the last update cycle for the SCU.
		'''
		if self.reward_type == 'Queues':
			reward = -np.sum(self.queue_state)
		elif self.reward_type == 'Queues_with_incentive':
			queues_incentive = [-10. if queue == 0. else queue for queue in self.queue_state]
			reward = -np.sum(queues_incentive)
		elif self.reward_type == "Delay":
			delay = self.VehNetPerformance.AttValue('DelayTot(Current, Last, All)')
			if delay is None:
				reward = 0
			else:
				reward = -delay
		elif self.reward_type == "Queues_squared":
			queues_squared = [queue ** 2 for queue in self.queue_state]
			reward = -np.sum(queues_squared)
		return(reward)

	def calculate_delay(self):
		delay_this_timestep = 0 if self.junction_movement.AttValue('VehDelay(Current, Last, All)') is None else self.junction_movement.AttValue('VehDelay(Current, Last, All)')
		return delay_this_timestep

	def calculate_stop_delay(self):
		delay_this_timestep = 0 if self.junction_movement.AttValue('StopDelay(Current, Last, All)') is None else self.junction_movement.AttValue('StopDelay(Current, Last, All)')
		return delay_this_timestep
		
	# This function can be improved to make it truly parallel	        
	def _color_changer(self):
		"""
		_color_changer :
		Internal function
		This method change the color of lights in the Vissim simulator.
		
		Following the stage orded :
		GREEN --> AMBER --> RED --> REDAMBER --> GREEN

		But other order can be follow if the time attributed to intermediate phase is 0
		GREEN --> AMBER --> REDAMBER --> GREEN
		GREEN --> AMBER --> GREEN
		GREEN --> AMBER --> RED --> GREEN
		"""   
		# In the case in which the new action is the same as the current action:
		if self.next_action_key == self.action_key :
			# At least one light will remain green.
			self.stage = "Green"
			# The update counter is set to the minimal greeen time.
			self.update_counter =  self.green_time
			self.intermediate_phase = False
			#print('green_stay_green')
			return
		
		# If the next action is not the same, then some light has to be changed
		elif  self.next_action_key != self.action_key :

			if self.stage == "Green":
				#print('green to amber')
				current_colors =  self.compatible_actions[self.action_key]
				next_colors = self.compatible_actions[self.next_action_key]

				# This is a security option to make sure the colors are changed.
				# However it will negatively impact on the network performance.
				#self.force_safe_colors(current_colors)  

				# This is the transition vector. It is the difference between the actions:
				# -1 The group was GREEN and need to be turn red
				# 0 The group was GREEN and stays GREEN or the group was RED and stays red, 
				# no change has to be made on this group.
				# 1 The group was red and need to be turn green.  
				self.change_vector = np.subtract(next_colors, current_colors)

				# Performs the changes on Vissim in a nearly parallel way
				[self.signal_groups[idx].SetAttValue("SigState", "AMBER") \
								for idx,value in enumerate(self.change_vector) if value == -1]

				# Set the internal stage to AMBER which is an intermediate stage
				self.stage = "Amber"
				self.update_counter = self.amber_time
				self.intermediate_phase = True
				return

			elif self.stage == "Amber":
				#print("Amber")
				if self.red_time != 0:
					# If the red time is not 0 then switch all the light to RED
					[self.signal_groups[idx].SetAttValue("SigState", "RED") \
								for idx,value in enumerate(self.change_vector) if value == -1]
					self.update_counter = self.red_time
					self.stage = "Red"
					self.intermediate_phase = True
					return
				
				elif self.red_time == 0:
					# Skip the red stage and go directly to red amber
					if self.redamber_time != 0:
						[self.signal_groups[idx].SetAttValue("SigState", Amber_to_Redamber(value)) \
									for idx,value in enumerate(self.change_vector) if value != 0]

						self.update_counter = self.redamber_time
						self.stage = "RedAmber"
						self.intermediate_phase = True
						return

					elif  self.redamber_time == 0:
						# Skip the red stage and the reamber stage
						[self.signal_groups[idx].SetAttValue("SigState", Amber_to_Green(value)) \
									for idx,value in enumerate(self.change_vector) if value != 0]

						self.update_counter = self.green_time
						self.stage = "Green"
						self.intermediate_phase = False
						return
				
			elif self.stage == "Red":
				if self.redamber_time != 0 :
					# Go to red amber stage
					[self.signal_groups[idx].SetAttValue("SigState", "REDAMBER") \
									for idx,value in enumerate(self.change_vector) if value == 1]

					self.update_counter = self.redamber_time
					self.stage = "RedAmber"
					self.intermediate_phase = True
					return

				elif self.redamber_time == 0 :
					# skip the red amber stage
					[self.signal_groups[idx].SetAttValue("SigState", "GREEN") \
									for idx,value in enumerate(self.change_vector) if value == 1]

					self.update_counter = self.green_time
					self.stage = "Green"
					self.intermediate_phase = True
					return

			elif self.stage == "RedAmber":
				# Switch to green stage
				[self.signal_groups[idx].SetAttValue("SigState", "GREEN") \
									for idx,value in enumerate(self.change_vector) if value == 1]
				
				self.update_counter = self.green_time
				# This is not an intermediate stage which means that an action will be needed at
				#  the end of the stage
				self.stage = "Green"
				self.intermediate_phase = False

				### HERE AGAIN  NEW COLORS###
				# This is a security option to make sure the colors are changed.
				# However it will negatively impact on the network performance.
				#self.force_safe_colors(next_colors)
				pass	

	def action_update(self, action_key, green_time = None):
		"""
		action_update :
		Initiates a new action.
			Inputs:
			-- id of action
			-- green_time, if specified by agent (in seconds)
		"""
		self.intermediate_phase = True # initate intermediate_phase
		self.update_counter = 1 # set update counter zero (will get reset at self.update())
		self.next_action_key = action_key

		if green_time is not None:
			self.green_time = green_time 

		self.action_required = False
	   
	def update(self):
		"""
		
		Update the state of the SCU. Decrease the update counter until an action is needed
		it then computes the state. 
		OR until a transition has to be made :
		- Updates the stage of the controllers
		- Change the light in the simulator
		
		"""
		# If being controlled by COM
		if self.controled_by_com :
			# Substract 1 from the update counter
			self.update_counter -= 1
			# If the update counter reaches zero
			if self.update_counter == 0. :
				# then ask for an action 
				if self.intermediate_phase is False :
					self.action_required = True 
						
				# if during a change
				# then make the change
				if self.intermediate_phase is True : 
					self.action_required = False
					self._color_changer() #Make the change in the Simulator
		else :
			pass				

def Amber_to_Redamber(val):
	"""
	Used to convert the transition vector to color in the Amber_to_Redamber stage transition
	"""
	if val == 1 :
		return "REDAMBER"
	elif val == -1:
		return "RED"

def Amber_to_Green(val):
	"""
	Used to convert the transition vector to color in the Amber_to_Green stage transition
	"""
	if val == 1 :
		return "GREEN"
	elif val == -1:
		return "RED"

# This function can be rethink to be a method of the SCU to make it faster
def get_queue(lane):
	"""
	Compute the queues size of a lane.
	-Input lane as a Vissim object
	"""
	vehicles_in_lane = lane.Vehs
	# Collecte the attribute in lane of the vehicle of the lane and sum them
	queue_in_lane = np.sum([vehicle.AttValue('InQueue') for vehicle in vehicles_in_lane])
	return(queue_in_lane)

