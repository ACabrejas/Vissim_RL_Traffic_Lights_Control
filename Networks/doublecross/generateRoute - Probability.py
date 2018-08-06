from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3000  # number of time steps
    # demand per second from different directions
    p1 = 1. / 20
    p3 = 1. / 20
    p5 = 1. / 20
    p6 = 1. / 20
    p7 = 1. / 20
    p8 = 1. / 20
    p9 = 1. / 20

    with open("newRoute.rou.xml", "w") as routes:
        print("""<routes>
    <vTypeDistribution id="vehtypedist1">
        <vType id="car" accel="0.8" length="5" maxSpeed="70" probability="0.75"/>
        <vType id="scooter" accel="1.8" length="2" maxSpeed="100" probability="0.1"/>
        <vType id="lorry" accel="1.8" length="15" maxSpeed="50" probability="0.1"/>
        <vType id="bus" accel="1.8" length="15" maxSpeed="70" probability="0.05"/>
    </vTypeDistribution>

    <routeDistribution id="routeFrom1">
        <route id="1-2-5" color="1,1,0" edges="A1 -A2 -A5" probability="0.33"/>
        <route id="1-2-6" color="1,1,0" edges="A1 -A2 -A6" probability="0.33"/>
        <route id="1-3" color="1,1,0" edges="A1 -A3" probability="0.33"/>
        <route id="1-4-7" color="1,1,0" edges="A1 -A4 -A7" probability="0.33"/>
        <route id="1-4-8" color="1,1,0" edges="A1 -A4 -A8" probability="0.33"/>
        <route id="1-4-9" color="1,1,0" edges="A1 -A4 -A9" probability="0.33"/>
    </routeDistribution>

    <routeDistribution id="routeFrom3">
        <route id="3-1" color="1,1,0" edges="A3 -A1" probability="0.33"/>
        <route id="3-2-5" color="1,1,0" edges="A3 -A2 -A5" probability="0.33"/>
        <route id="3-2-6" color="1,1,0" edges="A3 -A2 -A6" probability="0.33"/>
        <route id="3-4-7" color="1,1,0" edges="A3 -A4 -A7" probability="0.33"/>
        <route id="3-4-8" color="1,1,0" edges="A3 -A4 -A8" probability="0.33"/>
        <route id="3-4-9" color="1,1,0" edges="A3 -A4 -A9" probability="0.33"/>
    </routeDistribution>

    <routeDistribution id="routeFrom5">
        <route id="5-6" color="1,1,0" edges="A5 -A6" probability="0.33"/>
        <route id="5-2-1" color="1,1,0" edges="A5 A2 -A1" probability="0.33"/>
        <route id="5-2-3" color="1,1,0" edges="A5 A2 -A3" probability="0.33"/>
        <route id="5-2-4-7" color="1,1,0" edges="A5 A2 -A4 -A7" probability="0.33"/>
        <route id="5-2-4-8" color="1,1,0" edges="A5 A2 -A4 -A8" probability="0.33"/>
        <route id="5-2-4-9" color="1,1,0" edges="A5 A2 -A4 -A9" probability="0.33"/>
    </routeDistribution>

    <routeDistribution id="routeFrom6">
        <route id="6-2-1" color="1,1,0" edges="A6 A2 -A1" probability="0.33"/>
        <route id="6-2-3" color="1,1,0" edges="A6 A2 -A3" probability="0.33"/>
        <route id="6-5" color="1,1,0" edges="A6 -A5" probability="0.33"/>
        <route id="6-2-4-7" color="1,1,0" edges="A6 A2 -A4 -A7" probability="0.33"/>
        <route id="6-2-4-8" color="1,1,0" edges="A6 A2 -A4 -A8" probability="0.33"/>
        <route id="6-2-4-9" color="1,1,0" edges="A6 A2 -A4 -A9" probability="0.33"/>
    </routeDistribution>

    <routeDistribution id="routeFrom7">
        <route id="7-4-1" color="1,1,0" edges="A7 A4 -A1" probability="0.33"/>
        <route id="7-4-3" color="1,1,0" edges="A7 A4 -A3" probability="0.33"/>
        <route id="7-4-2-5" color="1,1,0" edges="A7 A4 -A2 -A5" probability="0.33"/>
        <route id="7-4-2-6" color="1,1,0" edges="A7 A4 -A2 -A6" probability="0.33"/>
        <route id="7-8" color="1,1,0" edges="A7 -A8" probability="0.33"/>
        <route id="7-9" color="1,1,0" edges="A7 -A9" probability="0.33"/>
    </routeDistribution>

    <routeDistribution id="routeFrom8">
        <route id="8-4-1" color="1,1,0" edges="A8 A4 -A1" probability="0.33"/>
        <route id="8-4-3" color="1,1,0" edges="A8 A4 -A3" probability="0.33"/>
        <route id="8-4-2-5" color="1,1,0" edges="A8 A4 -A2 -A5" probability="0.33"/>
        <route id="8-4-2-6" color="1,1,0" edges="A8 A4 -A2 -A6" probability="0.33"/>
        <route id="8-7" color="1,1,0" edges="A8 -A7" probability="0.33"/>
        <route id="8-9" color="1,1,0" edges="A8 -A9" probability="0.33"/>
    </routeDistribution>

    <routeDistribution id="routeFrom9">
        <route id="9-4-1" color="1,1,0" edges="A9 A4 -A1" probability="0.33"/>
        <route id="9-4-3" color="1,1,0" edges="A9 A4 -A3" probability="0.33"/>
        <route id="9-4-2-5" color="1,1,0" edges="A9 A4 -A2 -A5" probability="0.33"/>
        <route id="9-4-2-6" color="1,1,0" edges="A9 A4 -A2 -A6" probability="0.33"/>
        <route id="9-7" color="1,1,0" edges="A9 -A7" probability="0.33"/>
        <route id="9-8" color="1,1,0" edges="A9 -A8" probability="0.33"/>
    </routeDistribution>

        """, file=routes)
        lastVeh = 0
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < p1:
                print('    <vehicle id="1_%i" type="vehtypedist1" route="routeFrom1" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < p3:
                print('    <vehicle id="3_%i" type="vehtypedist1" route="routeFrom3" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < p5:
                print('    <vehicle id="5_%i" type="vehtypedist1" route="routeFrom5" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i

            if random.uniform(0, 1) < p6:
                print('    <vehicle id="6_%i" type="vehtypedist1" route="routeFrom6" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < p7:
                print('    <vehicle id="7_%i" type="vehtypedist1" route="routeFrom7" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < p8:
                print('    <vehicle id="8_%i" type="vehtypedist1" route="routeFrom8" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i
            if random.uniform(0, 1) < p9:
                print('    <vehicle id="9_%i" type="vehtypedist1" route="routeFrom9" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
                lastVeh = i                
        print("</routes>", file=routes)
print("Success")
