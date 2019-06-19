import win32com.client
import os

def COMServerDispatch(model_name, vissim_working_directory, sim_length, timesteps_per_second, delete_results, verbose):
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
            Vissim.Simulation.SetAttValue('SimPeriod', simulation_length * timesteps_per_second)
            ## If a fresh start is needed
            if delete_results == True:
                # Delete all previous simulation runs first:
                for simRun in Vissim.Net.SimulationRuns:
                    Vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)
                #print ('Results from Previous Simulations: Deleted. Fresh Start Available.')

            #Pre-fetch objects for stability
            Simulation = Vissim.Simulation
            Network = Vissim.Net
            #print('Reloading complete. Executing new episode...')
            return(Simulation,Network)
        # If loading fails
        except:
            if _ != 4:
                print("Failed load attempt " +str(_+1)+ "/5. Re-attempting.")
            elif _ == 4:
                raise Exception("Failed 5th loading attempt. Please restart program. TERMINATING NOW.")
                quit()
