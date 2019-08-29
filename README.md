# MLforFlowOptimisation


## How to run
Open Jupyter Notebook. Currently in the middle of some major code rearrangement, so everything needs to be run from Env_Ray.ipynb.
The controller architecture works in the following way:
 ![Controller Architecture](./md_pics/Interface2.pdf)


There are currently 3 maps:
 - Cross Single Straight (2 phases) - Focus on asymmetric demand. Can be run using programs or phases. No turning.
 ![Single Cross Straight map](./md_pics/Single_straight_cross.PNG)

 - Cross Single Triple (4 phases) - Focus on single intersection complex control. Only the first 4 phases in the diagram below.
 - Cross Single Triple (8 phases) - Same with more complexity on the actions side.
 ![Cross Single Triple map](./md_pics/Single_cross_triple.PNG)
 ![Phases in 8 actions setup](./md_pics/Triple_phase.PNG)
 
 - Five Intersection (8 phases) - Combination of 5 complex intersections in cross, s.t. the incoming cars to the middle intersection have at least gone through one of the outer ones.
 ![Five Intersection map](./md_pics/Five_intersection.PNG)
 
 - Balance (14 intersections) - Currently training.
  ![Balance Network map](./md_pics/Balance.PNG)

 Several agents can be deployed:
 - DQN
 - Double DQN
 - Duelling DQN
 - Duelling Double DQN
 - Actor Critic
 
 Commercial approaches can be used:
 - MOVA
 - Surtrac

## Results
Currently under construction

### Single Cross Straight
 ![Single Cross Straight Early Results](./md_pics/SCS_Delay.png)
 ![Single Cross Straight Early Results](./md_pics/SCS_Stop_Delay.png)
Single_straight_cross.PNG)

### Cross Single Triple
 ![Cross Single Triple Early Results](./md_pics/SCT_Delay.png)
 ![Cross Single Triple Early Results](./md_pics/SCT_Stop_Delay.png)

### Five Intersection
 ![Five Intersection Early Results](./md_pics/FI_Delay2.png)
 ![Five Intersection Early Results](./md_pics/FI_Stop_Delay2.png)


