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