import win32com.client
import os

def COMServerDispatch(model_name, vissim_working_directory, sim_length, Start_Fresh, reset_flag, verbose):
    ## Connecting the COM Server => Open a new Vissim Window:
    # Server should only be dispatched in first run. Otherwise reload model.
    # Setting Working Directory
    
    if verbose:
        print ('Working Directory set to: ' + vissim_working_directory)
        # Check Chache
        print ('Generating Cache...')
    
#    Vissim = win32com.client.gencache.EnsureDispatch("Vissim.Vissim") 
    Vissim = win32com.client.dynamic.Dispatch("Vissim.Vissim") 

    if verbose:
        print ('Cache generated.\n')
    cache_flag = True

    if verbose:
        print ('****************************')
        print ('*   COM Server dispatched  *')
        print ('****************************\n')
    
    ## Load the Network:
    Filename = os.path.join(vissim_working_directory, model_name, (model_name+'.inpx'))
    
    if verbose:
        print ('Loading Model File: ' + model_name+'.inpx ...')
    
    Vissim.LoadNet(Filename)
    
    if verbose:
        print ('Load process successful')

    ## Setting Simulation End
    Vissim.Simulation.SetAttValue('SimPeriod', sim_length)
    
    if verbose:
        print ('Simulation length set to '+str(sim_length/10) + ' seconds.')
    
    ## If a fresh start is needed
    if reset_flag == True:
        if Start_Fresh == True:
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
        print('Sever Redispatched.')
    return(Vissim, Simulation, Network, cache_flag)

def COMServerReload(Vissim, model_name, vissim_working_directory, simulation_length, Start_Fresh, reset_flag):
    ## Connecting the COM Server => Open a new Vissim Window:
    # Server should only be dispatched in first run. Otherwise reload model.
    # Setting Working Directory

    ## Load the Network:
    Filename = os.path.join(vissim_working_directory, model_name, (model_name+'.inpx'))

    Vissim.LoadNet(Filename)

    ## Setting Simulation End
    Vissim.Simulation.SetAttValue('SimPeriod', simulation_length)
    ## If a fresh start is needed
    if reset_flag == True:
        if Start_Fresh == True:
            # Delete all previous simulation runs first:
            for simRun in Vissim.Net.SimulationRuns:
                Vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)
            #print ('Results from Previous Simulations: Deleted. Fresh Start Available.')

    
    #Pre-fetch objects for stability
    Simulation = Vissim.Simulation
    Network = Vissim.Net
    #print('Reloading complete. Executing new episode...')
    return(Simulation,Network)