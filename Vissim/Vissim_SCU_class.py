import numpy as np
import time as t
 #SCU



class Signal_Control_Unit:
	"""
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
	"""
	
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

		# Those are for the moment not Vissim objects, it is the index of object located in the simulator
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


		# Give the controle to com or not in case we want to do cavitation.
		# The update function doas nothing in this case 
		if self.controled_by_com:
			for group in self.signal_groups:
				group.SetAttValue('ContrByCOM',1)
			#self.action_required = False # used to requests an action from agent
			self.update_counter = 1
			# implement 1st action to start
			self.action_key = 0   # dict key of current action (we start with 0)
			

			# Next Action and action key.
			self.next_action_key = 0
			

			self.action_update(self.action_key)   

			# tracks the stage particularly when in intermediate phase.
			# Stages appear in order: "Amber" -> "Red" -> "RedAmber" -> "Green"
			# It is used to change the light of the signal group in _color_changer
			self.stage = "Green"

		else :
			self.action_required = False



		# Gather / Reference Vissim lanes and links for the intersection controled by this SCU as internal object 
		self.Vissim_Links = []
		self.Vissim_Lanes = []
		for link in self.Links_names:
			self.Vissim_Links.append(Vissim.Net.Links.ItemByKey(link))

		for link in self.Links_names:
			for lane in Vissim.Net.Links.ItemByKey(link).Lanes:
				self.Vissim_Lanes.append(lane)
		
		
			
		# initialize state and reward parameters
		self.state = self.calculate_state()
		self.next_state = None
		self.reward = self.calculate_reward()  
	   
		
	     
	def sars(self):
		"""
		sars :
		returns state, id of action, reward, next state
		THIS function actualy change the object. (There should be a better way...). Or we can duplicate
		the function in case we only want the state, action ,reward, next_state without changing the SCU
		"""
	
		sars =  [self.state, self.action_key, self.reward, self.next_state]

		self.state = self.next_state
		self.action_key = self.next_action_key

		return(sars)

	# Those two functions could be and should be methode of the class (when we will agree on a good methode)
	def calculate_state(self):
		"""
		Compute the state of the SCU. More type of state can be added
		"""
		if self.state_type == 'Queues':
			state = [get_queue(lane) for lane in self.Vissim_Lanes]
			state = np.array(state)[np.newaxis,:]
		
		return(state)


	# 	return reward
	def calculate_reward(self):
		if self.reward_type == 'Queues':
			reward = -np.sum(self.state)
		return(reward)
 


	# This function could be improve to make it more intuitive
	def action_update(self, action_key, green_time = None):
		"""
		action_update :
		initiates a new action
			inputs:
			-- id of action
			-- green_time, if specified by agent (in seconds)
		"""

		self.intermediate_phase = True # initate intermediate_phase
		self.update_counter = 1 # set update counter zero (will get reset at self.update())
		self.next_action_key = action_key

		if green_time is not None:
			self.green_time = green_time * self.time_steps_per_second

		self.action_required = False
		

	
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
		if self.next_action_key == self.action_key :
			# If the next action is the same as the current action nothing is done
			# The update counter is set to the minimal greeen time.
			self.stage = "Green"
			self.update_counter =  self.green_time
			self.intermediate_phase = False
			#print('green_stay_green')
			return

		elif  self.next_action_key != self.action_key :
			# If the next action is not the same then some light as to be changed

			if self.stage == "Green":
				#print('green to amber')
				current_colors =  self.compatible_actions[self.action_key]
				next_colors = self.compatible_actions[self.next_action_key]

				# This is the transition vector. It is the difference between the action
				# -1 then the groups was GREEN and need to be turn red
				# 0 then the groups was GREEN and stays GREEN or the group was RED and stays red, 
				# no change has to be made on this group
				# 1 The group was red and need to be turn green  
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
					# if the red time is not 0 then switch all the light to RED

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
				pass	
	   
	def update(self):
		"""
		
		Update the state of the SCU. Decrease the update counter until an action is needed
		it then computes the state. 
		OR until a transition has to be made :
		- Updates the stage of the controllers
		- Change the light in the simulato
		
		(writen so multiple controllers can be updated in parallel)
		(Computational Overhead should be lower than before)
	
		"""

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

					#Compute the state for the RL agent to find the next best agent 
					self.next_state = self.calculate_state()
					self.reward = self.calculate_reward()
						
				# if during a change
				# then make the change
				if self.intermediate_phase is True : 
					self.action_required = False
					

					self._color_changer() #Make the change in the Simulator
					



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
	Compute the queues size of a lane
	-input lane, It is a Vissim object
	"""
	vehicles_in_lane = lane.Vehs

	# Collecte the attribute in lane of the vehicle of the lane and sum them
	queue_in_lane = np.sum([vehicle.AttValue('InQueue') for vehicle in vehicles_in_lane])

	return(queue_in_lane)

