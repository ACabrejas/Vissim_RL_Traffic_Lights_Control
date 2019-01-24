from TupleToList import toList
## Network Parser (Crawler) class definition
class NetworkParser:
    
    ######################################################################################################################
    ## Nested data structure:
    ## 
    ## Signal Controllers = signal_controllers[signal_controller_ids]
    ## Signal Groups      = signal_groups     [signal_controller_ids] [signal_group_id]
    ## Signal Heads       = signal_heads      [signal_controller_ids] [signal_heads_id]
    ## Lanes              = lanes             [signal_controller_ids] [signal_heads_id] [lane_id]
    ##
    ######################################################################################################################
    ##
    ## Accessing attributes:
    ##
    ## AttValue('AttName(X,Y,bla)')
    ##
    ## X = Simulation Number.      Values: 1,2,3.. 'Current' [single case], Avg, StdDev, Min, Max [over several sims]
    ## Y = Time Interval Number    Values: 1,2,3, 'Current', 'Last', Avg, StdDev, Min, Max, Total
    ## All = All vehicle classes   Values: 10, 20, All
    ######################################################################################################################

    def __init__(self, Vissim):
        ## Get all SignalControllers
        self.signal_controllers     = toList(Vissim.Net.SignalControllers.GetAll())
        self.signal_controllers_ids = range(len(self.signal_controllers)) #Vissim count starts at 1
                 
        ## Create SignalGroupContainers and unpack the SignalGroups into a list by SignalController
        self.signal_groups = [[] for _ in self.signal_controllers_ids]
        for SC in self.signal_controllers_ids:
            for SG in range(1,self.signal_controllers[SC].SGs.Count+1):
                self.signal_groups[SC].append(self.signal_controllers[SC].SGs.ItemByKey(SG))
                
        ## Create SignalHeadsCollection and unpack the SignalHeads into a list by SignalController
        self.signal_heads = [[] for _ in self.signal_controllers_ids]
        for SC in self.signal_controllers_ids:
            for SG in range(self.signal_controllers[SC].SGs.Count):
                self.signal_heads[SC].append(toList(self.signal_groups[SC][SG].SigHeads.GetAll())[0])
                
        self.lanes = [[[] for b in range(len(self.signal_heads[a])) ] for a in self.signal_controllers_ids]
        for SC in self.signal_controllers_ids:
            for SH in range(len(self.signal_heads[SC])):
                self.lanes[SC][SH].append(self.signal_heads[SC][SH].Lane)