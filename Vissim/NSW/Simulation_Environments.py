import math
import numpy as np
from COMServer import COMServerDispatch

##################################
## THIS IS A GENERIC SIMULATION ##
##################################

class Simulation_Environment():
    def __init__(self,\
                 Loaded_Vissim,\
                 sim_length=3601,\
                 timesteps_per_second=12):
        
        self.Vissim = Loaded_Vissim
        self.Quick_Mode(Quick_Mode)
            
        
    def Step(self,action,sim_steps=10):
        
        state = _calculate_state(self)
        reward = _calculate_reward(self)
    
        return  state, reward, done
        
    def _calculate_state(self):
        pass
    
    def _calculate_reward(self):
        pass
    
#    def Quick_Mode(self,Quick_Mode):
#        self.Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",Quick_Mode)
        
# Queue Length Based Simulator
class Q_Sim_Env(Simulation_Environment):
    def __init__(self,\
                 Loaded_Vissim,\
                 model_name,\
                 vissim_working_directory,\
                 Lane_List = ['3-1','1-1','7-1','5-1'],\
                 sim_length=3601,\
                 timesteps_per_second=1,\
                 delete_results=True,\
                 verbose=False):
    
        # Load init from Parent Class
        super(Q_Sim_Env,self).__init__(
                 Loaded_Vissim,\
                 model_name,\
                 vissim_working_directory,\
                 sim_length,\
                 timesteps_per_second,\
                 delete_results,\
                 verbose)

    
        self.Signal_Controller = self.Vissim.Net.SignalControllers.GetAll()[0]
        self.Signal_Groups = self.Signal_Controller.SGs.GetAll()
        self.Lane_List = Lane_List

    def Step(self,action=None,Signal_Groups=None):
        if Signal_Groups is None:
            Signal_Groups = self.Signal_Groups
    # Consist of 4 steps: 
    # Greens go Amber
    # Ambers go Red
    # Reds go RedAmber
    # RedAmbers go Green

        # Initial Parameters
        Sim_Period = self.Vissim.Simulation.AttValue('SimPeriod') #End of Simulation
        Amber_Time = 4. #One second of Amber
        Red_Time = 1.
        RedAmber_Time = 1.

        # If current_state = 'GREEN' and next_state = 'RED'
        # Then go AMBER        
        for i, sg in enumerate(Signal_Groups):
            current_state = sg.AttValue("SigState")
            if current_state == "GREEN" and action[i] == 0 :
                sg.SetAttValue("SigState", "AMBER")

        # Simulate 4 seconds for Amber
        Sim_Time = self.Vissim.Simulation.AttValue('SimSec')
        Amber_Break = min(Sim_Time+Amber_Time,Sim_Period)
        self.Vissim.Simulation.SetAttValue('SimBreakAt', Amber_Break)
        self.Vissim.Simulation.RunContinuous()

        # Set the AMBER lights red
        for i, sg in enumerate(Signal_Groups):
            current_state = sg.AttValue("SigState")
            if current_state == "AMBER":
                sg.SetAttValue("SigState", "RED")

        # Simulate 1 second for Red
        Sim_Time = self.Vissim.Simulation.AttValue('SimSec')
        Red_Break = min(Sim_Time+Red_Time,Sim_Period)
        self.Vissim.Simulation.SetAttValue('SimBreakAt', Red_Break)
        self.Vissim.Simulation.RunContinuous()

        # If current state "RED" and next_state = "GREEN"
        # Then go RedAmber
        for i, sg in enumerate(Signal_Groups):
            current_state = sg.AttValue("SigState")
            if current_state == "RED" and action[i] == 1 :
                sg.SetAttValue("SigState", "REDAMBER")

        # Simulate 1 second for RedAmber
        Sim_Time = self.Vissim.Simulation.AttValue('SimSec')
        RedAmber_Break = min(Sim_Time+RedAmber_Time,Sim_Period)
        self.Vissim.Simulation.SetAttValue('SimBreakAt', RedAmber_Break)
        self.Vissim.Simulation.RunContinuous()

        # Finally set all RedAmbers to Green
        for i, sg in enumerate(Signal_Groups):
            current_state = sg.AttValue("SigState")
            if current_state == "REDAMBER":
                sg.SetAttValue("SigState", "GREEN")
                
        state = self._calculate_state()
        reward = self._calculate_reward()
        not_finished = self.Vissim.Simulation.AttValue('IsRunning')
        done = False if not_finished == 1 else True
        
        return  state, reward, done
                
    def _calculate_state(self,Lane_List=None, rounding=1.):
        # Loads globals if variables not specfied
        if Lane_List is None :
            Lane_List = self.Lane_List

        # initialize with zero queues
        Qsum = 0
        Q_sizes = dict.fromkeys(Lane_List)
        for key in Q_sizes.keys():
            Q_sizes[key]=0

        # initialize with zero numbers of non-waiting cars
        nonQsum = 0
        nonQ_sizes = dict.fromkeys(Lane_List)
        for key in nonQ_sizes.keys():
            nonQ_sizes[key]=0

        # get all Q lengths    
        All_Vehicles = self.Vissim.Net.Vehicles.GetAll() 
        for Veh in All_Vehicles:
            lane = Veh.AttValue('Lane')
            if lane in Lane_List : 
                if Veh.AttValue('InQueue') == 1 :
                    Q_sizes[lane] += 1
                else : 
                    nonQ_sizes[lane] += 1

        state = []

        for lane in Lane_List :
            state.append(math.ceil(Q_sizes[lane] / rounding))

        return np.reshape(state, [1,len(state)])
    
    def _calculate_reward(self,Q_Size=None):
        # Use global as default
        if Q_Size is None:
            Q_Size = self._calculate_state()

        return -np.sum(Q_Size)