# add folder up to gain enviroments above
import sys
sys.path.append('../')

import Vissim_env_class as Env

# Allow for reload of key modules
# for debugging purposes
from imp import reload

import win32com.client as com
import os

# Dispatch works better than dynamoc dispatch
#Vissim = com.Dispatch("Vissim.Vissim")

# # MANUAL LOAD (part 1)
# for _ in range(5):
#     try:
#         Vissim = com.Dispatch("Vissim.Vissim")
#         print('success!')
#         break
#     except:
#         print('fail')
        
# # MANUAL LOAD (part 2)
# input_file = 'C:\\Users\\nwalton\\OneDrive - The Alan Turing Institute\\Documents\\MLforFlowOptimisation\\Vissim\\Vissim_Networks\\Single_Cross_Straight\\Single_Cross_Straight.inpx'
# Vissim.LoadNet(input_file)

# vissim env class
import numpy as np
from NParser import NetworkParser
from Vissim_SCU_class import Signal_Control_Unit
import win32com.client
import os

from time import time


# The environment class , 
class vissim_env():

    """
    -Load the model
        - it need the controller actions to be defined by hand
    -Deploy the SCU
    -
    """

    def __init__(self,\
                 controllers_actions,\
                 model_name=None,\
                 vissim_working_directory=None,\
                 sim_length=3601, \
                 Vissim = None,\
                 timesteps_per_second = 1,\
                 mode = 'training',\
                 delete_results = True,\
                 verbose = True,\
                 green_time = 5):

        # Model parameters
        self.model_name = model_name
        self.vissim_working_directory = vissim_working_directory
        self.controllers_actions = controllers_actions


        # Simulation parameters
        self.sim_length = sim_length
        self.global_counter = 0

        self.mode = mode
        self.timesteps_per_second = timesteps_per_second
        self.green_time = green_time

        # Evaluation parameters
        self.delete_results = delete_results
        self.verbose = verbose

        # ComServerDisp
        if Vissim is None:
            self.Vissim, _, _, _ = COMServerDispatch(model_name, vissim_working_directory, self.sim_length,\
            self.timesteps_per_second, delete_results = self.delete_results, verbose = self.verbose)
        # Hand over open Vissim
        else:
            self.Vissim = Vissim
            self.Vissim.Simulation.Stop()
            self.Vissim.Simulation.SetAttValue('SimPeriod', sim_length)
            if delete_results == True:
                # Delete all previous simulation runs first:
                for simRun in Vissim.Net.SimulationRuns:
                    self.Vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)

        self.done = False

        # The parser can be a methode of the environment
        self.npa = NetworkParser(self.Vissim) 

        self.select_mode()

        # Simulate one step and give the control to COM
        for _ in range(self.timesteps_per_second):
            self.Vissim.Simulation.RunSingleStep()
            self.global_counter += 1


        for SC in self.npa.signal_controllers_ids:
            for group in self.npa.signal_groups[SC]:
                group.SetAttValue('ContrByCOM',1)


        # Create a dictionnary of SCUs each scu control a signal controller


        tic = time()
        self._Load_SCUs()
        tac = time()
        #print(tac-tic)

    '''
    _Load_SCUs :
        provides a dictionary with at the SCUs
        # Need to find later a way to give different green / yellow time to each SCUs
    '''
    def _Load_SCUs(self):

        self.SCUs = dict()

        for idx, sc in enumerate(self.npa.signal_controllers):
            self.SCUs[idx] = Signal_Control_Unit(\
                         self.Vissim,\
                         sc,\
                         self.controllers_actions[idx],\
                         Signal_Groups = None,\
                         green_time = self.green_time,\
                         redamber_time = 1,\
                         amber_time = 3, \
                         red_time = 1\
                        )



    # -Function to get the SCUs to later deploy agent on them
    def get_SCU(self):
        return(self.SCUs)

    # does a step in the simulator
    # INPUT a dictionary of action
    # return a dictionnary of (state, action, reward, next_state , done) the key will be the SCU's key
    def step(self, actions):
        self.Vissim.Simulation.RunSingleStep()
        self.global_counter += 1
        if self.global_counter > (self.sim_length-1) * self.timesteps_per_second:
            self.done = True
            self.global_counter = 0
        else :
            self.done = False

        if not self.Vissim.Simulation.AttValue('IsRunning') :
            self.Vissim.Simulation.RunSingleStep()
        
        Sarsd = dict()

        for idx, scu in self.SCUs.items():
            if scu.action_required :
                tic = time()
                scu.action_update(actions[idx])
                tac = time()
                #print('action_update')
                #print(tac-tic)

            #tic = time()
            if not self.done :
                scu.update()
            #tac = time()
            #print('update')
            #print(tac-tic)

            if scu.action_required or self.done :
                Sarsd[idx] = scu.sars()+[self.done]


        if len(Sarsd) > 0 :
            return True, Sarsd
        else:
            return False, None


    # reset the environnement
    def reset(self):
        ## Connecting the COM Server => Open a new Vissim Window:
        # Server should only be dispatched in first run. Otherwise reload model.
        # Setting Working Directory


        COMServerReload(self.Vissim, self.model_name, self.vissim_working_directory, self.sim_length, self.timesteps_per_second, self.delete_results)
        self.npa = NetworkParser(self.Vissim) 
        self.select_mode()

        # Simulate one step and give the control to COM
        for _ in range(self.timesteps_per_second):
            self.Vissim.Simulation.RunSingleStep()

        for SC in self.npa.signal_controllers_ids:
            for group in self.npa.signal_groups[SC]:
                group.SetAttValue('ContrByCOM', 1)

        self._Load_SCUs()
        self.done = False



    # Set mode to training, demo, debugging
    def select_mode(self):
        
        self.Vissim.Simulation.Stop()
        # Select the mode for the metric collection 

        # In test mode all the data is stored (The simulation will be slow)
        if self.mode == 'test' :
            #This select quickmode and simulation resolution
            #self.timesteps_per_second = 10
            self.Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
            Vissim.ResumeUpdateGUI(False)
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
            
            Vissim.ResumeUpdateGUI(True)
            Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",0)
            
            #This select the simulation resolution
            #self.timesteps_per_second = 10
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
            #self.timesteps_per_second = 1
            self.Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
            Vissim.ResumeUpdateGUI(False)
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












def COMServerDispatch(model_name, vissim_working_directory, sim_length, timesteps_per_second, delete_results = True, verbose = True):
    for _ in range(5):
        try:
            ## Connecting the COM Server => Open a new Vissim Window:
            # Server should only be dispatched in first run. Otherwise reload model.
            # Setting Working Directory
            if verbose:
                print ('Working Directory set to: ' + vissim_working_directory)
                # Check Chache
                print ('Generating Cache...')

            # Vissim = win32com.client.gencache.EnsureDispatch("Vissim.Vissim") 
            #Vissim = win32com.client.dynamic.Dispatch("Vissim.Vissim") 
            Vissim = win32com.client.Dispatch("Vissim.Vissim")

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
                print ('Load process successful')

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

            #Pre-fetch objects for stability
            Simulation = Vissim.Simulation
            if verbose:
                print ('Fetched and containerized Simulation Object')
            Network = Vissim.Net

            if verbose:
                print ('Fetched and containerized Network Object \n')
                print ('*******************************************************')
                print ('*                                                     *')
                print ('*                 SETUP COMPLETE                      *')
                print ('*                                                     *')
                print ('*******************************************************\n')
            else:
                print('Server Dispatched.')
            return(Vissim, Simulation, Network, cache_flag)
        # If loading fails
        except:
            if _ != 4:
                print("Failed load attempt " +str(_+1)+ "/5. Re-attempting.")
            elif _ == 4:
                raise Exception("Failed 5th loading attempt. Please restart program. TERMINATING NOW.")


def COMServerReload(Vissim, model_name, vissim_working_directory, simulation_length, timesteps_per_second, delete_results):
    ## Connecting the COM Server => Open a new Vissim Window:
    # Server should only be dispatched in first run. Otherwise reload model.
    # Setting Working Directory
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
                #print ('Results from Previous Simulations: Deleted. Fresh Start Available.')

            #Pre-fetch objects for stability

            #print('Reloading complete. Executing new episode...')
            return()
        # If loading fails
        except:
            if _ != 4:
                print("Failed load attempt " +str(_+1)+ "/5. Re-attempting.")
            elif _ == 4:
                raise Exception("Failed 5th loading attempt. Please restart program. TERMINATING NOW.")
                quit()
                
# SCU Class
import numpy as np
import time as t


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
                 green_time = 10,\
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
        self.next_state = None
        self.reward = self.calculate_reward()  

        self.compatible_actions = compatible_actions

        self.time_steps_per_second = self.Vissim.Simulation.AttValue('SimRes')

        self.green_time = green_time * self.time_steps_per_second # the green time is in step
        self.redamber_time = redamber_time * self.time_steps_per_second
        self.amber_time = amber_time * self.time_steps_per_second
        self.red_time = red_time * self.time_steps_per_second

        # implement 1st action to start
        self.action_key = 0   # dict key of current action (we start with 0) 
        self.next_action_key = 0

        self.action_required = False # used to requests an action from agent
        self.update_counter = 1
        self.intermediate_phase = True # tracks when initiating a new action
        self.action_update(self.action_key)    


        self.stage = "Green" # tracks the stage particularly when in intermediate phase.
                             # Stages appear in order: "Amber" -> "Red" -> "RedAmber" -> "Green"


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

                # Comment this out because it slow they are not implemented yet and are very slow

                #self.next_state = self.calculate_state()
                #self.reward = self.calculate_reward()

            # if during a change
            # then make the change
            if self.intermediate_phase is True : 
                self.action_required = False

                # Get light color right for each signal group
                for sg in self.signal_groups :

                    ID = sg.AttValue('No')-1
                    #tic = t.time()
                    self._color_changer(sg, self.new_colors[ID], self.stage)
                    #tac = t.time()
                    #print('_color_changer')
                    #print(tac-tic)

                # change the current stage and get time the stage last for
                time = self._stage_changer(self.stage)
                self.update_counter = time

                # if full transition (Amber->Red->RedAmber-Green) to green done  
                if self.stage == "Green" :
                    self.intermediate_phase = False # record current action is implemented   


    '''
    sars :
    returns state, id of action, reward, next state
    '''     
    def sars(self):

        self.next_state = self.calculate_state()
        self.reward = self.calculate_reward(self.next_state)
        
        sars =  [self.state, self.action_key, self.reward, self.next_state]

        self.state = self.next_state
        self.action = self.next_action_key

        return(sars)


    '''
    calculate_state:
    Alvaro's reward function needs to be more general
    '''
    def calculate_state(self, length = None, verbose = False):

        # mesure the time taken to do this action
        #tic = t.time()

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

        #tac = t.time()
        #print(tac-tic)

        return (state)


    '''
    calculate_reward:
    Alvaro's reward function needs to be more general
    '''
    def calculate_reward(self,state=None):
        if state is None:
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
    def _color_changer(self,signal_group,new_color,stage):
        #Get the current color

        #print('current_color')
        #tic = t.time()
        current_color = self._color_convert(signal_group.AttValue("SigState"))
        #tac = t.time()
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


        # what is this red stage ? a stage where all the light are red ?
        elif stage == "Red" :
            time = self.redamber_time
            self.stage = "RedAmber"

        # want green but currently redamber
        elif stage == "RedAmber" :
            time = self.green_time
            self.stage = "Green"

        return time


# Raymond Agent II
from collections import deque


#Code adapted from http://inoryy.com/post/tensorflow2-deep-reinforcement-learning/

import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as kl
import tensorflow.keras.losses as kls
import tensorflow.keras.optimizers as ko


from collections import deque


#Code adapted from http://inoryy.com/post/tensorflow2-deep-reinforcement-learning/

import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as kl
import tensorflow.keras.losses as kls
import tensorflow.keras.optimizers as ko


class ProbabilityDistribution(tf.keras.Model):
    def call(self, logits):
        # sample a random categorical action from given logits
        return tf.squeeze(tf.random.categorical(logits, 1), axis=-1)

class Model(tf.keras.Model):
    def __init__(self, num_actions):
        super().__init__('mlp_policy')
        # no tf.get_variable(), just simple Keras API

        self.core1 = kl.Dense(32, activation='relu')
        
        self.value1 = kl.Dense(42, activation='relu', name='value1') #64
        self.value2 = kl.Dense(42, activation='relu', name='value2')
        self.value3 = kl.Dense(1, name='value3')
        # logits are unnormalized log probabilities


        self.logits1 = kl.Dense(42, activation='relu', name='policy_logits1')
        self.logits2 = kl.Dense(42, activation='relu', name='policy_logits2')
        self.logits3 = kl.Dense(num_actions, name='policy_logits3')

        self.dist = ProbabilityDistribution()

    def call(self, inputs):
        # inputs is a numpy array, convert to Tensor
        x = tf.convert_to_tensor(inputs, dtype=tf.float32)

        # This it the core of the model
        x = self.core1(x)
        
        # separate hidden layers from the core
        hidden_logs = self.logits1(x)
        hidden_logs = self.logits2(hidden_logs)

        hidden_vals = self.value1(x)
        hidden_vals = self.value2(hidden_vals)

        return self.logits3(hidden_logs), self.value3(hidden_vals)

    def action_value(self, obs):
        # executes call() under the hood
        logits, value = self.predict(obs)
        action = self.dist.predict(logits)
        # a simpler option, will become clear later why we don't use it
        # action = tf.random.categorical(logits, 1)
        return action , value


# An working model training with entropy = 0.00001 en nstep = 32 and learn every step lr = 0.000065 gama = 0.99 
class Modelsave1(tf.keras.Model):
    def __init__(self, num_actions):
        super().__init__('mlp_policy')

        # no tf.get_variable(), just simple Keras API
        self.hidden1 = kl.Dense(42, activation='relu')
        self.hidden2 = kl.Dense(42, activation='relu')
        self.value = kl.Dense(1, name='value')
        # logits are unnormalized log probabilities
        self.logits = kl.Dense(num_actions, name='policy_logits')
        self.dist = ProbabilityDistribution()

    def call(self, inputs):
        # inputs is a numpy array, convert to Tensor
        x = tf.convert_to_tensor(inputs, dtype=tf.float32)

        # This it the core of the model
       
        # separate hidden layers from the core
        hidden_logs = self.hidden1(x)
        hidden_vals = self.hidden2(x)
        return self.logits(hidden_logs), self.value(hidden_vals)

    def action_value(self, obs):
        # executes call() under the hood
        logits, value = self.predict(obs)
        action = self.dist.predict(logits)
        # a simpler option, will become clear later why we don't use it
        # action = tf.random.categorical(logits, 1)
        return action , value
  
    
class ACAgent_II:

    def __init__(self,\
                 state_size,\
                 action_size,\
                 #ID,\
                 #state_type,\
                 #npa,\
                 n_step_size =32,\
                 gamma = 0.99,\
                 alpha = 0.000065,\
                 entropy = 0.00001 ):
                    #Vissim):


        print("Deploying instance of Actor_Critic Agent(s) !!! TENSORFLOW 2 IS NEEDED !!! ")
        # agent type flag 
        self.type = 'AC'



        #just temporary
        self.epsilon = 0

        self.trainstep = 0

        # Model
        # hyperparameters for loss terms and Agent
        self.params = {'value': 0.5, 'entropy': entropy, 'gamma': gamma}
        self.model = Modelsave1(action_size)
        self.model.compile(
            optimizer=ko.RMSprop(lr=alpha),
            # define separate losses for policy logits and value estimate
            loss=[self._logits_loss, self._value_loss]
        )

#         # Agent Junction ID and Controller ID
#         self.signal_id = ID
#         self.signal_controller = npa.signal_controllers[self.signal_id]
#         self.signal_groups = npa.signal_groups[self.signal_id]

        # Number of states, action space and memory
        self.state_size = state_size
        self.action_size = action_size

        # Potential actions (compatible phases) and transitions
        self.update_counter = 1                                 # Timesteps until next update
        if self.action_size == 2:
            self.compatible_actions = [[0,1,0,1],[1,0,1,0]]         # Potential actions (compatible phases), 1 means green
        elif self.action_size == 8:
            self.compatible_actions = [[1,1,1,0,0,0,0,0,0,0,0,0],
                                        [0,0,0,1,1,1,0,0,0,0,0,0],
                                        [0,0,0,0,0,0,1,1,1,0,0,0],
                                        [0,0,0,0,0,0,0,0,0,1,1,1],
                                        [1,0,0,0,0,0,1,0,0,0,0,0],
                                        [0,0,0,1,0,0,0,0,0,1,0,0],
                                        [0,1,1,0,0,0,0,1,1,0,0,0],
                                        [0,0,0,0,1,1,0,0,0,0,1,1]]
        else:
            raise Exception("ERROR: Wrong Action Size. Please review master settings and RLAgents.py")
        # Internal State Traffic Control Variables
        self.intermediate_phase = False                         # Boolean indicating an ongoing green-red or red-green transition
        self.transition_vector = []                             # Vector that will store the transitions between updates


        # Initial Setup of S, A, R, S_
        self.state = np.zeros((1,state_size))
        self.newstate = np.zeros((1,state_size))
        self.action = 0
        self.newaction = 0
        self.reward = 0

        # Metrics Storage Initialization
        self.episode_reward = []
        self.loss = []
        self.queues_over_time = [[0,0,0,0]]
        self.accumulated_delay= [0]


        # The memory will store (state , action , reward, next_state) in a batch
        self.memory = deque(maxlen=n_step_size)
        self.n_step_size = n_step_size

    # Add memory on the right, if over memory limit, pop leftmost item
    def remember(self, state, action, reward, next_state):
        self.memory.append([state, action, reward, next_state])

    # Update the Junction IDs for the agent
    def update_IDS(self, ID, npa):
        self.signal_id = ID
        self.signal_controller = npa.signal_controllers[self.signal_id]
        self.signal_groups = npa.signal_groups[self.signal_id]

    # Need to test before loading to build the graph (surely an other way to do it ...)
    def test(self):
        _,_ = self.model.action_value(np.empty((1,self.state_size)))


    def _value_loss(self, returns, value):
        # value loss is typically MSE between value estimates and returns
        return self.params['value']*kls.mean_squared_error(returns, value)

    def _logits_loss(self, acts_and_advs, logits):
        # a trick to input actions and advantages through same API
        actions, advantages = tf.split(acts_and_advs, 2, axis=-1)
        # sparse categorical CE loss obj that supports sample_weight arg on call()
        # from_logits argument ensures transformation into normalized probabilities
        weighted_sparse_ce = kls.SparseCategoricalCrossentropy(from_logits=True)
        # policy loss is defined by policy gradients, weighted by advantages
        # note: we only calculate the loss on the actions we've actually taken
        actions = tf.cast(actions, tf.int32)
        policy_loss = weighted_sparse_ce(actions, logits, sample_weight=advantages)
        # entropy loss can be calculated via CE over itself
        entropy_loss = kls.categorical_crossentropy(logits, logits, from_logits=True)
        # here signs are flipped because optimizer minimizes
        return policy_loss - self.params['entropy']*entropy_loss

    def _returns_advantages(self, rewards, values, next_value):
        # next_value is the bootstrap value estimate of a future state (the critic)
        returns = np.append(np.zeros_like(rewards), next_value, axis=-1)
        # returns are calculated as discounted sum of future rewards
        for t in reversed(range(rewards.shape[0])):
            returns[t] = rewards[t] + self.params['gamma'] * returns[t+1]
        returns = returns[:-1]
        # advantages are returns - baseline, value estimates in our case
        advantages = returns - values
        return returns, advantages

    def choose_action(self, state):
        action, _ = self.model.action_value(state)
        return np.squeeze(action, axis=-1)

    #Performing step of gradient descent on the agent memory
    def learn(self):


        Sample = np.array(self.memory)

        states, actions, rewards, next_state  = np.concatenate(Sample[:,0], axis=0), Sample[:,1].astype('int32'), Sample[:,2], np.concatenate(Sample[:,3], axis=0)



        _, values = self.model.action_value(states)
        values = values.squeeze()

        _, next_value  = self.model.action_value(next_state)

        next_value = next_value[-1]



        returns, advs = self._returns_advantages(rewards, values, next_value)

        # a trick to input actions and advantages through same API

        acts_and_advs = np.concatenate([actions[:, np.newaxis], advs[:, np.newaxis]], axis=-1)

        # performs a full training step on the collected batch
        # note: no need to mess around with gradients, Keras API handles it
        losses = self.model.train_on_batch(states, [acts_and_advs, returns])

        #print(losses)



    # def train(self, env, batch_sz=32, updates=1000):
    #     # storage helpers for a single batch of data
    #     actions = np.empty((batch_sz,), dtype=np.int32)
    #     rewards, dones, values = np.empty((3, batch_sz))
    #     observations = np.empty((batch_sz,) + env.observation_space.shape)
    #     # training loop: collect samples, send to optimizer, repeat updates times
    #     ep_rews = [0.0]
    #     next_obs = env.reset()
    #     for update in range(updates):
    #         for step in range(batch_sz):
    #             observations[step] = next_obs.copy()
    #             actions[step], values[step] = self.model.action_value(next_obs[None, :])
    #             next_obs, rewards[step], dones[step], _ = env.step(actions[step])

    #               ep_rews[-1] += rewards[step]
    #             if dones[step]:
    #                 ep_rews.append(0.0)
    #                 next_obs = env.reset()

    #           _, next_value = self.model.action_value(next_obs[None, :])
    #         returns, advs = self._returns_advantages(rewards, dones, values, next_value)
    #         # a trick to input actions and advantages through same API
    #         acts_and_advs = np.concatenate([actions[:, None], advs[:, None]], axis=-1)
    #         # performs a full training step on the collected batch
    #         # note: no need to mess around with gradients, Keras API handles it
    #         losses = self.model.train_on_batch(observations, [acts_and_advs, returns])
    #     return ep_rews
    

AC = ACAgent_II(4,2)

# Load up environment
Controllers_Actions =\
{\
    0 : {   0 : [1, 0, 1, 0],
            1 : [0, 1, 0, 1],
        },
}

env = vissim_env(controllers_actions=Controllers_Actions,\
                 Vissim=Vissim,\
                 timesteps_per_second=1,\
                 green_time = 3\
                )

env.timesteps_per_second

env.mode = 'training'
env.select_mode()

# picks up first key from each controller
actions = dict()
for key, val in Controllers_Actions.items():
    actions[key] = next(iter(val)) 
    
AC.test()

t=0
av_reward = 0

for _ in range(100000):
    action_required, SARSDs = env.step(actions)
    if action_required :
        #print(action_required, (toc-tuc) - (toc-tic) )
        s,a,r,ns,d = SARSDs[0]
        #print(d)
        #tic =  time()
        AC.remember(s,a,r,ns)
        #tac =  time()
        actions[0]=int(AC.choose_action(ns))
        #toc =  time()
        AC.learn()
        # This could be internalized
        if d :
            print(av_reward)
            t=0
            av_reward = 0
            env.Vissim.Simulation.Stop()
            for _ in range(10):
                env.Vissim.Simulation.RunSingleStep()
            env.done = False
        else:
            t +=1 
            av_reward += ( r - av_reward ) / t
        
        #print(tac-tic,toc-tac,tuc-toc)
        #print(action_required, toc-tic, tuc-toc)