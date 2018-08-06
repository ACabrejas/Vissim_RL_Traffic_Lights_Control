"""
@file    runnerAH.py
@author  Andy Hamilton
@date    2017-05-18
@version 0.1

Test of traffic light control via the TraCI interface.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2009-2017 DLR/TS, Germany

SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random
import traci

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

def keywithmaxval(d):                   #Function used in Example control algorithm
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]


"""
The following getXXXData functions will return relevant data relating to each of the heading types
For example, getEdgeData will return relevant metrics relating to an edge in the simulation during
the previous time step. i.e. along Edge1, the current CO2 emissions was x milligrams
"""

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

def run():
    """execute the TraCI control loop which will enable the user to implement their own
        traffic control algorithm"""

    #Single junction network model specific IDs stored as lists. 
    nodeIDs = ['0']
    laneIDs = ['A1_0','A2_0','A3_0','A4_0']
    laneAreaIDs = ['AreaDet1','AreaDet2','AreaDet3','AreaDet4']

    #Variables needed for example traffic control algorithm 
    currentSimTime = 0      #Time within the simulation
    phaseTimer = 0          #Timer for duration of current phase
    intergreenTimer = 0     #Timer for duration of inter-green phase
    currentPhase = 99       #Description of current phase number

    """The following text describes how the lanes correspond to Phases within the model.
    i.e. what phase is needed to release traffic from each lane
    Phase1 = North (A1_0)
    Phase2 = Inter-green for Phase1
    Phase3 = East (A2_0)
    Phase4 = Inter-green for Phase3
    Phase5 = South (A3_0)
    Phase6 = Inter-green for Phase5
    Phase7 = West (A4_0)
    Phase8 = Inter-green for Phase7"""
    
    #Control mechanism constraints = [Phase Number in SUMO model, Max Duration for Phase,
    #Min Duration for Phase]
    phaseConstraints = {}
    phaseConstraints['Phase1'] = [0,30,6]
    phaseConstraints['Phase3'] = [2,30,6]
    phaseConstraints['Phase5'] = [4,30,6]
    phaseConstraints['Phase7'] = [6,30,6]


    #The while loop steps through the SUMO simulation for each timestep
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        currentSimTime = traci.simulation.getCurrentTime()

        #GET LIVE DATA FROM ONE OF THE 'GETDATA' FUNCTIONS
        laneData = getLaneData(laneIDs)         #In this simple control algorithm example, we store the data in a list variable

        #This maps the Phase number to the vehicle counts associated with the phase
        phaseDict = {}
        phaseDict['Phase1'] = laneData[9]
        phaseDict['Phase3'] = laneData[21]
        phaseDict['Phase5'] = laneData[33]
        phaseDict['Phase7'] = laneData[45]

        #The highest vehicle count is returned (NB limit to code - if multiple phases have the same count value then the first key with this value will be returned via this method)
        highestCount = keywithmaxval(phaseDict)

        #selectedPhaseConstraints stores the constraints of the phase with the highest vehicle count
        selectedPhaseConstraints = phaseConstraints.get(highestCount)
        currentPhase = traci.trafficlights.getPhase(nodeIDs[0])

        """The following if statements are described in more detail in the Challenge document"""
        #This checks if the current phase exceeds maximum phase timer. If so, go to intergreen.
        if phaseTimer >= selectedPhaseConstraints[1]:
            traci.trafficlights.setPhase(nodeIDs[0], (selectedPhaseConstraints[0]+1))
            phaseTimer = 0
            intergreenTimer = 1
            #print('The phase is now* = ',(selectedPhaseConstraints[0]+1))
            
        #This checks if it is not the intergreen phase (intergreen phases are odd numbers in this example)
        #and if phase has ran for less that minimum phase timer
        elif currentPhase % 2 == 0 and phaseTimer < selectedPhaseConstraints[2]:
            pass
            #print('The phase is still** = ',currentPhase)

        #This checks if the intergreen phase has run its minimum time
        elif currentPhase % 2 == 1 and intergreenTimer < 5:
            phaseTimer = 0
            intergreenTimer +=1
            #print('The phase is still*** = ',currentPhase)

        #If intergreen period has run, then select the phase with the highest count
        elif intergreenTimer == 5:
            traci.trafficlights.setPhase(nodeIDs[0], selectedPhaseConstraints[0])
            phaseTimer = 0
            intergreenTimer = 0
            #print('The phase is now*** = ',selectedPhaseConstraints[0])

        #if current phase does not equal the desired stage then go to intergreen
        elif currentPhase != selectedPhaseConstraints[0]:
            traci.trafficlights.setPhase(nodeIDs[0], (currentPhase+1))
            intergreenTimer = 1
            phaseTimer = 0
            #print('The phase is now**** = ',(currentPhase+1))

        #if current phase is also the desired stage
        else:
            pass
            #print('The phase is still*** = ',currentPhase)
           
        phaseTimer += 1
        #print(phaseTimer)
    
    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options



"""The SUMO config file is hardcoded here - if using this script for a different model then make sure you change it"""

if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    # if individual vehicle trace is desired, then add "--fcd-output", "sumoTrace.xml" to command line input
    # if individual vehicle emissions is desired, then add "--emission-output", "emissions.xml" to command line input
    traci.start([sumoBinary, "-c", "multiRoad.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
