from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import optparse
import subprocess
import random
import pdb
import xmltodict
import re
import numpy as np

os.getcwd()
__file__=os.getcwd()

try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "../tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "../test_tools"))  # tutorial in docs
    from sumolib import checkBinary
    import traci
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

def keywithmaxval(d):                   #Function used in Example control algorithm
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

def getEdgeData(edgeIDs):
    #Edge data order (type: double / integer): [CO2, CO, Hydrocarbons, NOx, PMx, Noise,
    #mean Vehicle Length, mean Speed,occupancy, number of vehicles (integer),
    #estimated travel time, Waiting time]
    #http://sumo.dlr.de/daily/pydoc/traci._edge.html 
    data = []

    for i in range(0,len(edgeIDs)):
        data.append(traci.edge.getCO2Emission(edgeIDs[i]))
        data.append(traci.edge.getCOEmission(edgeIDs[i]))
        data.append(traci.edge.getHCEmission(edgeIDs[i]))
        data.append(traci.edge.getNOxEmission(edgeIDs[i]))
        data.append(traci.edge.getPMxEmission(edgeIDs[i]))
        data.append(traci.edge.getNoiseEmission(edgeIDs[i]))
        data.append(traci.edge.getLastStepLength(edgeIDs[i]))
        data.append(traci.edge.getLastStepMeanSpeed(edgeIDs[i]))
        data.append(traci.edge.getLastStepOccupancy(edgeIDs[i]))
        data.append(traci.edge.getLastStepVehicleNumber(edgeIDs[i]))
        data.append(traci.edge.getTraveltime(edgeIDs[i]))
        data.append(traci.edge.getWaitingTime(edgeIDs[i]))
    return data

def getInductionLoopData(inductionLoopIDs):
    #Inductive Loop data order (type: double / integer): [mean Vehicle Length,
    #mean Speed, occupancy, number of vehicles (integer)]
    #http://sumo.dlr.de/daily/pydoc/traci._inductionloop.html 
    data = []

    for i in range(0,len(inductionLoopIDs)):
        data.append(traci.inductionloop.getLastStepLength(inductionLoopIDs[i]))
        data.append(traci.inductionloop.getLastStepMeanSpeed(inductionLoopIDs[i]))
        data.append(traci.inductionloop.getLastStepOccupancy(inductionLoopIDs[i]))
        data.append(traci.inductionloop.getLastStepVehicleNumber(inductionLoopIDs[i]))
    return data

def getLaneData(laneIDs):
    #Lane data order (type: double / integer): [CO2, CO, Hydrocarbons, NOx, PMx, Noise,
    #mean Vehicle Length, mean Speed, occupancy, number of vehicles (integer),
    #estimated travel time, Waiting time]
    #http://sumo.dlr.de/daily/pydoc/traci._lane.html 
    data = []

    for i in range(0,len(laneIDs)):
        data.append(traci.lane.getCO2Emission(laneIDs[i]))
        data.append(traci.lane.getCOEmission(laneIDs[i]))
        data.append(traci.lane.getHCEmission(laneIDs[i]))
        data.append(traci.lane.getNOxEmission(laneIDs[i]))
        data.append(traci.lane.getPMxEmission(laneIDs[i]))
        data.append(traci.lane.getNoiseEmission(laneIDs[i]))
        data.append(traci.lane.getLastStepLength(laneIDs[i]))
        data.append(traci.lane.getLastStepMeanSpeed(laneIDs[i]))
        data.append(traci.lane.getLastStepOccupancy(laneIDs[i]))
        data.append(traci.lane.getLastStepVehicleNumber(laneIDs[i]))
        data.append(traci.lane.getTraveltime(laneIDs[i]))
        data.append(traci.lane.getWaitingTime(laneIDs[i]))
    return data

def getLaneAreaData(laneAreaIDs):
    #Lane area characteristic order (type: double / integer): [jam length (m), jam length (no. vehicles),
    #mean Speed, occupancy, number of vehicles (integer)]
    #http://sumo.dlr.de/daily/pydoc/traci._lanearea.html 
    data = []
    
    for i in range(0,len(laneAreaIDs)):
        data.append(traci.lanearea.getJamLengthMeters(laneAreaIDs[i]))
        data.append(traci.lanearea.getJamLengthVehicle(laneAreaIDs[i]))
        data.append(traci.lanearea.getLastStepMeanSpeed(laneAreaIDs[i]))
        data.append(traci.lanearea.getLastStepOccupancy(laneAreaIDs[i]))
        data.append(traci.lanearea.getLastStepVehicleNumber(laneAreaIDs[i]))
    return data

def getMultiEntryExitData(multiEntryExitIDs):
    #Multi entry exit detection area data order (type: double / integer):
    #mean Speed, number of vehicles (integer)]
    #http://sumo.dlr.de/daily/pydoc/traci._multientryexit.html 
    data = []

    for i in range(0,len(multiEntryExitIDs)):
        data.append(traci.multientryexit.getLastStepMeanSpeed(multiEntryExitIDs[i]))
        data.append(traci.multientryexit.getLastStepVehicleNumber(multiEntryExitIDs[i]))
    return data

def getSimulationData():
    #Simulation data order (type: double):
    #[current time, number of vehicles entering the network]
    #http://sumo.dlr.de/daily/pydoc/traci._simulation.html
    data = []

    data.append(traci.simulation.getCurrentTime())
    data.append(traci.simulation.getDepartedNumber())
    return data

def getTrafficLightData(trafficLightIDs):
    #Traffic light data = [current phase ID, phase duration,
    #current traffic phase]
    #http://sumo.dlr.de/daily/pydoc/traci._trafficlights.html 
    data = []

    for i in range(0,len(trafficLightIDs)):
        data.append(traci.trafficlight.getPhase(trafficLightIDs[i]))
        data.append(traci.trafficlight.getPhaseDuration(trafficLightIDs[i])) #this will reference the fixed time
        data.append(traci.trafficlight.getRedYellowGreenState(trafficLightIDs[i]))
    return data

def getVehicleData(vehicleIDs):
    #Individual vehicle data = [CO2, CO, Hydrocarbons, NOx, PMx, Noise,
    #emission class, total distance travelled (odometer), length,
    #list of upcoming traffic lights [(tlsID, tlsIndex, distance, state), ...], position (m,m),
    #vehicle route (edge IDs),current Speed, Vehicle Class, Waiting Time (below 0.1m/s)]
    #http://sumo.dlr.de/daily/pydoc/traci._vehicle.html 
    data = []

    for i in range(0,len(vehicleIDs)):
        data.append(traci.vehicle.getCO2Emission(vehicleIDs[i]))
        data.append(traci.vehicle.getCOEmission(vehicleIDs[i]))
        data.append(traci.vehicle.getHCEmission(vehicleIDs[i]))
        data.append(traci.vehicle.getNOxEmission(vehicleIDs[i]))
        data.append(traci.vehicle.getPMxEmission(vehicleIDs[i]))
        data.append(traci.vehicle.getNoiseEmission(vehicleIDs[i]))
        data.append(traci.vehicle.getEmissionClass(vehicleIDs[i]))
        data.append(traci.vehicle.getDistance(vehicleIDs[i]))
        data.append(traci.vehicle.getLength(vehicleIDs[i]))
        data.append(traci.vehicle.getNextTLS(vehicleIDs[i]))
        data.append(traci.vehicle.getPosition(vehicleIDs[i]))
        data.append(traci.vehicle.getRoute(vehicleIDs[i]))
        data.append(traci.vehicle.getSpeed(vehicleIDs[i]))
        data.append(traci.vehicle.getVehicleClass(vehicleIDs[i]))
        data.append(traci.vehicle.getWaitingTime(vehicleIDs[i]))
    return data

def getStaticLaneData(laneIDs):
    #Static lane data = [Lane Length, Max Speed]
    #http://sumo.dlr.de/daily/pydoc/traci._lane.html
    data = []

    #Get lane characteristics
    for i in range(0,len(laneIDs)):
        data.append(traci.lane.getLength(laneIDs[i]))
        data.append(traci.lane.getMaxSpeed(laneIDs[i]))
    return data

def getStaticTrafficLightData(trafficLightIDs):
    #Static traffic light data = [lanes controlled by traffic lights, links controlled
    #by traffic lights, ]
    #http://sumo.dlr.de/daily/pydoc/traci._trafficlights.html 
    data = []

    for i in range(0,len(trafficLightIDs)):
        data.append(traci.trafficlight.getControlledLanes(trafficLightIDs[i]))
        data.append(traci.trafficlight.getControlledLinks(trafficLightIDs[i]))
    return data

class NetworkParser:

    def __init__(self, file_path):
        self.junctions = dict()
        self.junction_lights = dict()

        with open(file_path) as f:
            self.file = xmltodict.parse(f.read())

    def get_lane_ids(self):
        for junction in self.file['net']['junction']:
            if junction['@type'] == 'traffic_light':
                self.junctions[junction['@id']] = junction['@incLanes'].split(' ')
        return self.junctions

    # Given a LaneID it returns the traffic light ID
    def get_trafficlights_by_laneID(self, laneID):
        for connection in self.file['net']['connection']:
            if connection['@from'] == laneID.split('_')[0] and '@tl' in connection:
                return connection['@tl']

    def get_junction_trafficlights(self):
        if not self.junctions:
            self.get_lane_ids()
        for junctionID in self.junctions.keys():
            for lane in self.junctions[junctionID]:
                traffic_light = self.get_trafficlights_by_laneID(lane)
                if traffic_light in self.junction_lights and lane not in self.junction_lights[traffic_light]:
                    self.junction_lights[traffic_light].append(lane)
                else:
                    self.junction_lights[traffic_light] = []
        return self.junction_lights

    def get_traffic_light(self, laneID):
        if not self.junction_lights:
            self.get_junction_trafficlights()
        for traffic_light, lanes in self.junction_lights.iteritems():
            if laneID in lanes:
                return traffic_light

    def get_phases(self, traffic_light):
        phases = []
        for tls in self.file['net']['tlLogic']:
            if tls['@id'] == traffic_light:
                for tls_phase in tls['phase']:
                    phases.append(tls_phase)
        return phases

class Qlearner:
    def __init__(self,TLid,lanes,phases):
        self.jid     = TLid
        self.TLid    = TLid
        self.laneids = lanes
        self.Nlanes  = len(self.laneids)                                #len(nodes.junctions[self.jid])
        self.phases  = range(0, phases)                            #traci.trafficlights.getallPhases
        self.green_phases = [0, 2, 4, 6]
        num_phases = len(self.phases)
        self.Qm      = np.zeros(((2**self.Nlanes)*num_phases, num_phases))

        self.state   = 0
        self.action  = 0

    
    def set_action(self,action):
        traci.trafficlights.setPhase(self.jid, self.phases[action])

    def get_reward(self):
        return sum([traci.lane.getNOxEmission(lane_id) for lane_id in self.laneids])
 

    def get_state(self,threshold_l=3):
        current_phase = traci.trafficlights.getPhase(self.jid)
        NOXlanes=[int(traci.lane.getNOxEmission(lane_id)>threshold_l) for lane_id in self.laneids]

        state = current_phase*(2**len(NOXlanes)) + sum([x*y for x,y in zip(NOXlanes, 2**np.arange(len(NOXlanes)) )])

        return(state)

    def update(self,gamma=0.8,alpha=0.95,epsilon=0.025):
        state    = self.state
        action   = self.action
        newstate = self.get_state()
        reward   = self.get_reward()

        self.Qm[state, action] = self.Qm[state, action]*(1-alpha) + alpha*(reward + gamma*np.max(self.Qm[newstate,:]))
        
        r=np.random.rand(1)


        if r > epsilon :
            newaction = np.argmax(self.Qm[state,:])
        else:
            newaction = np.random.randint(0, len(self.phases))
        
        self.state = newstate
        self.action = newaction
        self.set_action(newaction)
        # print(newaction)

def run(learners = []):
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for learner in learners:
            learner.update()


    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# def main():
options = get_options()

if options.nogui:
    sumoBinary = checkBinary('sumo')
else:
    sumoBinary = checkBinary('sumo-gui')

npa = NetworkParser('cityNetwork.net.xml')

nodes = npa.get_junction_trafficlights()
phase_list = [len(npa.get_phases(k)) for k in npa.get_junction_trafficlights().keys()]

traci.start([sumoBinary, "-c", "cityNetwork.sumocfg",
                         "--tripinfo-output", "tripinfo.xml"])

learners=[Qlearner(ID,lan,p) for ID, lan, p in zip(nodes.keys(),nodes.values(),phase_list)]
run(learners)

traci.close()
