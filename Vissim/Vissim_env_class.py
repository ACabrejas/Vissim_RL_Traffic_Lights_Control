import numpy as np
from NParser import NetworkParser
from Vissim_SCU_class import Signal_Control_Unit
import win32com.client
import os

from time import time


# The environment class , 
class env():

    """
    -Load the model
        - it need the controller actions to be defined by hand
    -Deploy the SCU
    -
    """

    def __init__(self, controllers_actions, model_name=None, vissim_working_directory=None, sim_length=3601, \
                     Vissim = None, timesteps_per_second = 1, mode = 'training', delete_results = True, verbose = True):

        # Model parameters
        self.model_name = model_name
        self.vissim_working_directory = vissim_working_directory
        self.controllers_actions = controllers_actions


        # Simulation parameters
        self.sim_length = sim_length
        self.global_counter = 0

        self.mode = mode
        self.timesteps_per_second = timesteps_per_second

        # Evaluation parameters
        self.delete_results = delete_results
        self.verbose = verbose

        # ComServerDisp
        if Vissim is None:
            self.Vissim, _, _, _ = COMServerDispatch(model_name, vissim_working_directory, self.sim_length,\
            self.timesteps_per_second, delete_results = self.delete_results, verbose = self.verbose)
        else:
            self.Vissim = Vissim

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
                         green_time = 50,\
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

        Sarsd = dict()

        for idx, scu in self.SCUs.items():
            if scu.action_required :
                tic = time()
                scu.action_update(actions[idx])
                tac = time()
                #print('action_update')
                #print(tac-tic)

            tic = time()
            scu.update()
            tac = time()
            #print('update')
            #print(tac-tic)

            if scu.action_required :
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
        # Select the mode for the metric collection 

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









