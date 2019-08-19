import numpy as np
from copy import deepcopy

# A class to handle the state space search
# Input : -Clusters ie 2 lists of clusters (one for each road)
#       : -ic the index of the current green phase (the start)
#       : -greedymode, this class has 2 modes, one that keep all the schedule that are not dominated (non-greedy mode)
#        one that keep only one schedule the one that has the less delay at each stage

class State_manager():
    def __init__(self,C,ic,greedymode=True):
        self.greedymode=greedymode
        self.C=C
        #initialisation of the schedule state and the state group
        self.schedule_state=[]
        self.state_group={}

        #Creating all the schedule state space possible as a list
        for i in range(len(C[0])+1):
            for j in range(len(C[1])+1):
                self.schedule_state.append([i,j])

        # Creating all the state_group possible as a dictionnary. Initialising the time and delay at +infinite to be replaced
        self.state_group[(0,0),ic]=[[0,0,[]]]
        for i in self.schedule_state[1:] :
            for j in range(len(C)):
                # it is impossible to have for exemple X = (0,1) and s = 0 because no cluster left on route 0 with this schedule state
                if not i[j]== 0 :
                    self.state_group[tuple(i),j] = [[float('+Infinity'),float('+Infinity'),[]]]


    # This is the function that add a schedule in the schedule state groupe
    # input : - X the schedule state
    #       : - s the index of the cluster last added s=S0[-1]
    #       : - t,d the time and delay of the partial schedule
    #       : - S0 the partial schedule
    def add(self,X,s,t,d,S0):
        #print(X)


        # greedy mode
        if self.greedymode:
            # if the delay of the previous schedule is less than the one we want to add.
            # The schedule is not add and discarded
            if self.state_group[tuple(X),s][0][1] < d:
                return
            else :
            # Other wise the previous schedule is replaced with the new one
                self.state_group[tuple(X),s][0][0],self.state_group[tuple(X),s][0][1] = t,d
                self.state_group[tuple(X),s][0][2]=S0+[s]

        # not greedy mode
        else :

            # We compare our schedule to be added with all the schedule of the state groupe.
            for tprime,dprime,Sprime in self.state_group[tuple(X),s]:
                # our schedule is dominated, We discard him
                if  tprime < t and dprime < d:
                    return
                # our shedule dominate another schedule. We add our schedule and we discard the dominated schedule
                if tprime > t and dprime > d:
                    self.state_group[tuple(X),s].append([t,d,S0+[s]])
                    self.state_group[tuple(X),s].remove([tprime,dprime,Sprime])
                    return
            # The schedule is not dominated nor dominate, thus it is added to the schedule state groupe
            self.state_group[tuple(X),s].append([t,d,S0+[s]])

# input : -sk is the index of the previous route (or phase). The last cluster left on route sk.
#       : -t is the time at this point of the schedule
#       : -d is the total delay at this point of the schedule
#       : -c python object with the cluster attribute (which contains sk_next). It is the next cluster to be cleared

# output : -t,d the time and the total delay of the schedule after the cluster c is cleared


def algorithm2(sk,t,d,c):
    minimal_time_switch=[[0.,3.],[3.,0.]]
    # find the route index of the next cluster
    i=c.signal_group

    # The time after the light switched to route of the cluster
    pst=t+minimal_time_switch[sk][i]

    #The departure time of the cluster
    ast=np.maximum(c.arr,pst)

    # if the cluster has already arrived before the switching, the cluster takes a certain amount of time to start
    # which is added
    if pst >= c.arr and sk!=i:
        ast=ast+c.sult

    # The totale delay is increased by the number of cars of the cluster times the waiting.
    d_delta=c.size*np.maximum(ast-c.arr,0)
    d+=d_delta
    t = ast + c.dur

    return(t,d)


# Input : Statemanager to be updated
#       : X the schedule state
#       : s the index of the cluster last added s=S0[-1]

# Output : None, it updates the state managers and computes the next schedule state group for (X,s)

def algorithm5(state_manager,s,X):


    c=state_manager.C[s][X[s]-1]
    #print(X)

    #find the previous schedule state
    X0=deepcopy(X)
    X0[s] = X0[s]-1
    #print(X0)
    #print(s)

    # iteration on (X0,0) and (X0,1) state group
    for s0  in range(len(state_manager.C)):

        # to discard very particuliar case that should not exist
        if (tuple(X0),s0) not in state_manager.state_group.keys():
        #    print(tuple(X0),s0)
        #    print(tuple(X0),s0,'plop')
            continue
        #print(state_manager.state_group[tuple(X0),s0])

        # iteration on the previous schedule to add next cluster and computing next state group
        for t,d,S0 in state_manager.state_group[tuple(X0),s0] :
            t,d = algorithm2(s0,t,d,c)
            #print(t,d)

            # condition on the time horrizon but let's put an infinite time horrizon
            state_manager.add(X,s,t,d,S0)



class SurtracAgent():
    def __init__(self, ID,\
                   delta =2 , rounding=0.1 ):

        print("Deploying Surtrac Agent")


        #Clustering algorithm hyperparameters
        self.delta = delta
        self.rounding = rounding

        # Potential actions (compatible phases) and transitions
        self.actiontime = 1                         # Timesteps until next update it is the green time given by the surtrac algorithm
        

        
        self.action = 0
        
    def choose_action(self,C,greedy=False):
        """
         Input : -Clusters ie 2 lists of clusters (one for each road)
               : -ic the index of the current green phase (the start)
               : -greedymode, this class has 2 modes, one that keep all the schedule that are not dominated (non-greedy mode)
               : one that keep only one schedule the one that has the less delay at each stage

         Output : the optimal schedule, the one with the less total delay.
        """

        #small hack to make it work when there is no vehicle
        if len(C[0])==0:
            t = 6
            self.actiontime = round(t)
            return(1, self.actiontime)
        elif len(C[1])==0:
            t = 6
            self.actiontime = round(t)
            return(0, self.actiontime)

        #initialize the state manager with the current action
        state_manager=State_manager(C,self.action,greedymode=greedy)
        # iteration on all the clusters
        for k in range(1,len(C[0])+len(C[1])+1) :

            # find and collect the schedule state that has the number of cluster required
            for X in [ X for X in state_manager.schedule_state if sum(X) == k ] :
                for s in range(len(C)):
                    # only considering possible state groupe
                    if X[s] > 0 :
                        # performing the shedule state groupe update
                        algorithm5(state_manager,s,X)

        # finding the best shedule
        # initializing delay and schedule
        d=float('+Infinity')
        S=[]
        #print(state_manager.state_group)

        # Can do better to find the optimal solution

        # Comparing iteratively the full schedule the one with X_full and s=0 or s=1
        for s in range(len(C)):
            for L in state_manager.state_group[tuple(state_manager.schedule_state[-1]),s]:
                if L[1] < d:
                    d = L[1]
                    S = L[2]

        #Finding the clearance time of the first cluster
        #print(d,S)
        s = S[0]
        key = [[0,0],s]
        key[0][s] = 1
        key[0] = tuple(key[0])
        key = tuple(key)
        t = state_manager.state_group[key][0][0]

        #print(t)
        #print(S[0])
        self.actiontime = round(t)
        # This is the schedule with the smallest total delay
        return(S[0], self.actiontime)


