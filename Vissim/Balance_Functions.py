def balance_dictionary(agent_type):
#####################################
## SCHEMATIC LAYOUT OF THE NETWORK ##
#####################################
#
# THE NUMBERS SHOWING ARE THE INTERSECTION IDS
#
#                       |              |
#                       |              |
#                  ---- 10------------ 8 ----
#                       |              |
#              |        |              |
#              |   ---- 9 ------------ 7 ----       ___
#              |        |              |           /
#              |        |     /-       |          /
#              |        |     |        |          |
# ------------ 1 ------ 2 --- 14 ----- 3 -------- 4 ---- 5 -----
#              |        |              |          |     /
#              |        |              \          |    /
#              |        |               \         6 --/
#              |        |                |    __ /
#        ----- 11------ 12--------------13---/              
#              |        |                |
#              |        |                |
#              |        |                |

################################
## DICTIONARY FOR THE NETWORK ##
################################
	balance_dictionary =\
		{\
		# Controller SC01 
	   'junctions' : \
		{0 : {'default_actions' : {     0 : [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], # StraightRight from sides
										1 : [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],  # Turn Left sides
										2 : [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]}, # North + South
			 
			 'all_actions' : {          0 : [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
										1 : [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
										2 : [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
										3 : [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # StraightRightLeft from East
										4 : [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]}, # StraightRightLeft from West
			 
			 'link' : [2, 40, 7, 38],
			 'lane' : ['2-1', '2-2', '2-3', '40-1', '7-1', '7-2', '7-3', '38-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [8],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             # Counterclockwise, starting by Inner, West.
             'queues_counter_ID' : [1, 2, 3, 11, 4, 5, 6, 10],
			 'agent_type' : agent_type
			},
		# Controller SC02
		1 : {'default_actions' : {      0 : [1, 0, 0, 1, 0, 0, 0, 0],
										1 : [0, 0, 1, 0, 0, 1, 0, 0],
										2 : [0, 1, 0, 0, 1, 0, 1, 1]},

			 'all_actions' : {          0 : [1, 0, 0, 1, 0, 0, 0, 0],
										1 : [0, 1, 0, 0, 1, 0, 1, 1],
										2 : [0, 0, 1, 0, 0, 1, 0, 0],
										3 : [1, 1, 0, 0, 0, 0, 0, 0], 
										4 : [0, 0, 0, 1, 1, 0, 0, 0]},
			 
			 'link' : [5, 48, 70, 46],
			 'lane' : ['5-1', '5-2', '5-3', '48-1', '70-1', '70-2', '70-3', '46-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [8],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [13, 14, 15, 16, 9, 8, 7, 12],
			 'agent_type' : agent_type
			},
		# Controller SC03
		2 : {'default_actions' : {      0 : [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										1 : [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										2 : [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
										3 : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
			 
			 'all_actions' :        {   0 : [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										1 : [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										2 : [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
										3 : [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										4 : [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										5 : [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										6 : [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										7 : [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]},
			 
			 'link' : [73, 100, 84, 95],
			 'lane' : ['73-1', '73-2', '73-3', '100-1', '100-2', '100-3', '100-4',\
					  '84-1', '84-2', '84-3', '95-1', '95-2', '95-3', '95-4'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [14],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [48, 49, 50, 51, 52, 53, 54, 41, 42, 43, 44, 45, 46 ,47],
			 'agent_type' : agent_type
			},
		# Controller SC04
		3 : {'default_actions' : {      0 : [1, 0, 0, 1, 0, 0, 1, 0],
										1 : [0, 0, 1, 0, 0, 1, 0, 1],
										2 : [0, 1, 0, 0, 1, 0, 1, 0]},

			 'all_actions' :        {   0 : [1, 0, 0, 1, 0, 0, 1, 0],
										1 : [0, 1, 0, 0, 1, 0, 1, 0],
										2 : [0, 0, 1, 0, 0, 1, 0, 1],
										3 : [1, 1, 0, 0, 0, 0, 1, 0],
										4 : [0, 0, 0, 1, 1, 0, 0, 1]},
			 
			 'link' : [87, 36, 10, 34],
			 'lane' : ['87-1', '87-2', '87-3', '36-1', '10-1', '10-2', '10-3', '34-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [8],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [59, 60, 61, 62, 55, 56, 57, 58],
			 'agent_type' : agent_type
			},
		# Controller SC05 
		4 : {'default_actions' :    {   #0 : [0, 1, 1, 0, 1],
										#1 : [1, 1, 0, 0, 0],
										#2 : [0, 0, 0, 1, 0]},

                                        0 : [0, 1, 1, 0, 1],
                                        1 : [1, 1, 0, 0, 0],
                                        2 : [0, 0, 0, 1, 0]},

			 'all_actions' :        {   0 : [0, 1, 1, 0, 0],
										1 : [1, 1, 0, 0, 0],
										2 : [0, 0, 0, 1, 0]},

			 'link' : [8, 24, 13],
			 'lane' : ['8-1', '8-2', '24-1', '13-1', '13-2', '13-3'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [6],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [66, 67, 68, 63, 64, 65],
			 'agent_type' : agent_type
			},
		# Controller SC06
		5 : {'default_actions' :    {   0 : [1, 0, 1, 0, 1, 0],
										1 : [0, 1, 0, 1, 0, 1]},

			 'all_actions' :        {   0 : [1, 0, 1, 0, 1, 0],
										1 : [0, 1, 0, 1, 0, 1]},

			 'link' : [26, 23, 35],
			 'lane' : ['26-1', '23-1', '35-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [3],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [27, 25, 26],
			 'agent_type' : agent_type
			},
		# Controller SC07
		6 : {'default_actions' :    {   0 : [0, 1, 0, 1, 1, 1],
										1 : [1, 0, 1, 0, 0, 0]},

			 'all_actions' :        {   0 : [0, 1, 0, 1, 1, 1],
										1 : [1, 0, 1, 0, 0, 0]},

			 'link' : [51, 92, 64, 19],
			 'lane' : ['51-1', '92-1', '92-2', '64-1', '19-1', '19-2'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [6],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [79, 80, 81, 76, 77, 78],
			 'agent_type' : agent_type
			},
		# Contoller SC08
		7 : {'default_actions' :    {   0 : [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
										1 : [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
										2 : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},

			 'all_actions' :        {   0 : [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
										1 : [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
										2 : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										3 : [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
										4 : [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]},

			 'link' : [18, 66, 16],
			 'lane' : ['18-1', '18-2', '18-3', '66-1', '16-1', '16-2', '16-3'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [7],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [86, 87, 88, 82, 83, 84, 85],
			 'agent_type' : agent_type
			},
		# Controller SC09
		8 : {'default_actions' :    {   0 : [1, 0, 1, 0, 0, 0, 0],
										1 : [0, 1, 0, 0, 0, 0, 0]},

			 'all_actions' :        {   0 : [1, 0, 1, 0, 0, 0, 0],
										1 : [0, 1, 0, 0, 0, 0, 0]},

			 'link' : [62, 45, 44],
			 'lane' : ['62-1', '45-1', '44-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [3],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [29, 30, 28],
			 'agent_type' : agent_type
			},
		# Controller SC10
		9 : {'default_actions' :    {   0 : [0, 1, 0, 1, 1, 0, 1, 0],
										1 : [1, 0, 1, 0, 0, 1, 0, 1]},

			 'all_actions' :        {   0 : [0, 1, 0, 1, 1, 0, 1, 0],
										1 : [1, 0, 1, 0, 0, 1, 0, 1]},

			 'link' : [60, 43, 55, 58],
			 'lane' : ['60-1', '43-1', '55-1', '58-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [4],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [33, 34, 31, 32],
			 'agent_type' : agent_type
			},
		# Controller SC11
		10 : {'default_actions' :    {  0 : [1, 0, 1, 0, 0, 1, 0, 1],
										1 : [0, 1, 0, 1, 1, 0, 1, 0]},

			 'all_actions' :         {  0 : [1, 0, 1, 0, 0, 1, 0, 1],
										1 : [0, 1, 0, 1, 1, 0, 1, 0]},

			 'link' : [32, 42, 30, 39],
			 'lane' : ['32-1', '42-1', '30-1', '39-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [4],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [19, 20, 17, 18],
			 'agent_type' : agent_type
			},
		# Controller SC12
		11 : {'default_actions' :     { 0 : [1, 0, 1, 0, 0, 1, 0, 1],
										1 : [0, 1, 0, 1, 1, 0, 1, 0]},

			 'all_actions' :          { 0 : [1, 0, 1, 0, 0, 1, 0, 1],
										1 : [0, 1, 0, 1, 1, 0, 1, 0]},

			 'link' : [29, 50, 28, 47],
			 'lane' : ['29-1', '50-1', '28-1', '47-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [4],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [24, 21, 22, 23],
			 'agent_type' : agent_type
			},
		# Controller SC13
		12 : {'default_actions' :     { 0 : [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
										1 : [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1],
										2 : [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
										3 : [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]},
			 
			 'all_actions' :          { 0 : [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
										1 : [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1],
										2 : [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
										3 : [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]},

			 'link' : [27, 268, 269, 25, 265, 266, 267],
			 'lane' : ['27-1', '22-1', '22-2', '22-3', '25-1', '77-1', '77-2'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [7],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [72, 73, 74, 75, 69, 70, 71],
			 'agent_type' : agent_type
				
			},
		# Controller SC14 
		13 : {'default_actions' :     { 0 : [1, 0, 0, 1, 0, 0, 1, 0, 0],
										1 : [0, 0, 1, 1, 0, 1, 0, 0, 0],
										2 : [0, 1, 0, 0, 1, 1, 0, 1, 1]},

			 'all_actions' :          { 0 : [1, 0, 0, 1, 0, 0, 1, 0, 0],
										1 : [0, 0, 1, 1, 0, 1, 0, 0, 0],
										2 : [0, 1, 0, 0, 1, 1, 0, 1, 1]},
			 'link' : [68, 71, 75],
			 'lane' : ['68-1', '68-2', '68-3', '71-1', '71-2', '75-1'],
			 
			 'controled_by_com' : True,
			 'green_time' : 6,
			 'redamber_time' : 0,
			 'amber_time' : 3, 
			 'red_time' : 0,
			 'state_size' : [6],
			 'state_type' : 'Queues',
			 'reward_type' : 'Queues',
             'queues_counter_ID' : [38, 39, 40, 35, 36, 37],
			 'agent_type' : agent_type
			}
		},
		"demand" : { "default" : [125, 505, 54, 39, 34, 654, 604, 198, 165, 164, 972, 124, 48, 43, 203, 76] }
	}
	return(balance_dictionary)