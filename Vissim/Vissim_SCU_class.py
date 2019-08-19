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
				 Identificator, npa,
				 Signal_Groups = None,\
				):
		#####################################
		# Set basic information for the SCU # 
		#####################################

		# ID so it can be matched with "env.SCUs[ID]"
		self.ID = Identificator

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
		
		#################################
		# Fetch Objects operated by SCU # 
		#################################

		# Signal Controller
		self.signal_controller = Signal_Controller_Object
		# Signal Groups
		if Signal_Groups is None :
			self.signal_groups = npa.signal_groups[self.ID]
			#self.signal_groups = self.signal_controller.SGs
		else :
			self.signal_groups = Signal_Groups
		self.signal_heads  = npa.signal_heads[self.ID]
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
		self.Node = Vissim.Net.Nodes.ItemByKey(self.ID+1) #To be corrected Vissim object count object begin at 1

		# Transform the movements into a python list (hacky technique to be because the list[-1] doesnt work with Vissim list)
		movements = list(self.Node.Movements)

		self.junction_movement = movements[-1] #The last one is the movement of the whole intersection
		self.lanes_movement = movements[1:]  # The other movement are the lane movement





		# Only for surtrac (Can be adapted to make it more modulable)
		if self.state_type == 'Surtrac' :
			self.Vissim = Vissim


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
			self.action_key = 0
			self.next_action_key = 0
			# Initiate Action on the SCU
			self.action_update(self.action_key)  

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
			self.queue_state  =\
			[0. if movement.AttValue('QLen(Current, Last)') is None else movement.AttValue('QLen(Current, Last)') for movement in self.lanes_movement]
			state = np.array(self.queue_state)[np.newaxis,:]

		elif self.state_type == "QueuesSig":
			self.queue_state  =\
			[0. if movement.AttValue('QLen(Current, Last)') is None else movement.AttValue('QLen(Current, Last)') for movement in self.lanes_movement]
			state = np.array(self.queue_state+[self.next_action_key])[np.newaxis,:]
		
		elif self.state_type == 'Surtrac':
			state = Clustering(self.Vissim)
			self.queue_state  =\
			[0. if movement.AttValue('QLen(Current, Last)') is None else movement.AttValue('QLen(Current, Last)') for movement in self.lanes_movement]

		return(state)

	def calculate_queues(self):
		"""
		Only conpute the queues at this intersection

		"""
		queues =  [0. if movement.AttValue('QLen(Current, Last)') is None else movement.AttValue('QLen(Current, Last)') for movement in self.lanes_movement]
		return queues  

	def calculate_reward(self):
		'''
		Compute the Reward of the last update cycle for the SCU.
		'''
		if self.reward_type == 'Queues':
			reward = -np.sum(self.queue_state)
		return(reward)

	def calculate_delay(self):
		delay_this_timestep = 0 if self.junction_movement.AttValue('VehDelay(Current, Last, All)') is None else self.junction_movement.AttValue('VehDelay(Current, Last, All)')
		return delay_this_timestep

	def calculate_stop_delay(self):
		delay_this_timestep = 0 if self.junction_movement.AttValue('StopDelay(Current, Last, All)') is None else self.junction_movement.AttValue('StopDelay(Current, Last, All)')
		return delay_this_timestep
 
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
					self.intermediate_phase = False
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


"""
This is a quick hack to make Surtrac working on single cross straight.
This is a very non modulable way of doing the clustering. 
But with a bit of work can be adapted to multiple junctions and model



"""


from copy import deepcopy
import numpy as np


# Creating a python class for vehicles to add some properties

# The time nedded for a car to cross the intersection.
# This have to be estimated
time_to_cross = 2

def Get_Signal_Positions(Signal_Groups):
    Signal_Positions = dict()
    for SG in Signal_Groups:
        for SH in SG.SigHeads:
            Lane = SH.AttValue('Lane')
            Position = SH.AttValue('Pos')
            Signal_Positions[Lane] = Position
    return Signal_Positions

# We have to decide when to round before or after the clustering. It may be better to do it after the clustering because :
# Here we actually lose a lot of precision
class Vehicle():
    def __init__(self, VISSIM_Vehicle,Signal_Positions, rounding=1.):
        self.VISSIM_vehicle = VISSIM_Vehicle



        #To work only for our particuliar intersection
        signalgroupdict={'1-1' : 0,'5-1' : 0,'3-1': 1,'7-1': 1 }

        # Importing and creating properties for our vehicle object
        # Converting km/h into m/s
        self.speed = VISSIM_Vehicle.AttValue('Speed')/3.6
        self.pos = VISSIM_Vehicle.AttValue('Pos')
        self.lane = VISSIM_Vehicle.AttValue('Lane')
        self.signal_group = signalgroupdict[self.lane]
        self.inqueue = VISSIM_Vehicle.AttValue('InQueue')
        self.distfromhead = Signal_Positions[self.lane]-self.pos

        # Will have to change those estimation by reading Sharma and al 2007 and Mirchandani 2001
        if  self.inqueue:
            self.arr = 0.
        else :

            # a better estimation can be done
            self.arr = int(self.distfromhead/self.speed/rounding)*rounding
        self.dep=self.arr+time_to_cross




class Cluster():
    """
    # Creating a Cluster class with arrival, departure and duration

    """


    def __init__(self,list_of_vehicles):
        # SFR is the saturation flow rate, it is the maximum number of vehicles by second the lane can serve.
        # This have to be estimated
        self.sfr=1
        self.list_of_vehicles = list_of_vehicles
        self.size = len(list_of_vehicles)
        self.signal_group = list_of_vehicles[0].signal_group

        #Here again the estimation have to be changed
        #The arrival time is the arrival time of the first car
        self.arr = list_of_vehicles[0].arr
        #The departure time is the departure time of the last car of the list
        self.dep = list_of_vehicles[-1].dep

        if list_of_vehicles[0].inqueue:
            self.dur = self.size/self.sfr
        else :
            self.dur=self.dep-self.arr

        # According to Sharma and al
        # A parameters that estimate the starting time of the cluster.
        # This have to be estimated
        self.sult = 3


def merge(cluster1,cluster2):
    """
    # A function to merge two cluster not used here but can actually be usefull later.
    # It can also be included as a class method
    """
    return Cluster(cluster1.list_of_vehicles+cluster2.list_of_vehicles)



def Clustering(Vissim,delta=2,rounding=0.1):
    """
    # This is the clustering process for our two route network.
    # Input : -The parameters of the clustering
    #         -The Vissim object are aready imported
    # Output : - The clustering : A tuple countaining lists of clusters ordered by their time arrival.
    """   
    All_Vehicles=Vissim.Net.Vehicles.GetAll()


    # get the list of signal controllers
    # To be improved
    Signal_Controller = Vissim.Net.SignalControllers.GetAll()[0]
    Signal_Groups = Signal_Controller.SGs.GetAll()
    Signal_Positions = Get_Signal_Positions(Signal_Groups)


    # It may be preferable to iterate on the number of group pahe for a larger network
    # Could do an iteration on the number on the number of signal group
    Clusters1=[]
    Clusters2=[]

    # Groupe the vehicle by lane
    Vehilane_group1= [ Vehicle(i,Signal_Positions,rounding=rounding) for i in All_Vehicles if i.AttValue('Lane') == '1-1' or i.AttValue('Lane') == '5-1' ]
    Vehilane_group2= [ Vehicle(i,Signal_Positions,rounding=rounding) for i in All_Vehicles if i.AttValue('Lane') == '7-1' or i.AttValue('Lane') == '3-1' ]

    # Sort the vehicle by order of arrival
    Vehilane_group1.sort(key = lambda x: x.arr ) #x.distfromhead
    Vehilane_group2.sort(key = lambda x: x.arr ) #x.distfromhead

    # The queue clustering is not yet handled perfectly but more precise estimation of parameters are
    # needed

    # Creating the cluster for the first route
    # current cluster initialisation with the first vehicle
    if len(Vehilane_group1)==0: #if there is no vehicles on road 0
        Clusters1=[]
    else:
        cluster=[Vehilane_group1[0]]
        for i in range(1,len(Vehilane_group1)):
                # if the next vehicle arrives before the departure of the next vehicle +  a delta than the
                # vehicle is added
                # to the current cluster
            if cluster[-1].dep+delta > Vehilane_group1[i].arr :
                cluster.append(Vehilane_group1[i])
            else :
                # Other wise the list of vehicle is put into a cluster class and the next vehicle is the
                # first car of the next cluster
                Clusters1.append(Cluster(cluster))
                cluster=[Vehilane_group1[i]]

        Clusters1.append(Cluster(cluster))

    # Creating the cluster for the second route, same as the first route
    if len(Vehilane_group2)==0:#if there is no vehicles on road 1
        Clusters2=[]
    else:
        cluster=[Vehilane_group2[0]]
        for i in range(1,len(Vehilane_group2)):
            if cluster[-1].dep+delta > Vehilane_group2[i].arr:
                cluster.append(Vehilane_group2[i])
            else :
                Clusters2.append(Cluster(cluster))
                cluster=[Vehilane_group2[i]]

        Clusters2.append(Cluster(cluster))

    return Clusters1,Clusters2
