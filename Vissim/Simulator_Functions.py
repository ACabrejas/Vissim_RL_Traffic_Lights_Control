import numpy as np
import os
import pickle
from keras.models import load_model

# Set Fastest Mode in Simulator
def Set_Quickmode(Vissim):
	# Set speed parameters in Vissim
    Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
    Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",1)
    Vissim.SuspendUpdateGUI()  

# Run a Single Episode for a set simulation length
def run_simulation_episode(Agents, Vissim, state_type, state_size, simulation_length, Demo_Mode, PER_activated):
	cycle_t = 0
	Vissim.Simulation.SetAttValue('SimRes', 1)
	#Vissim.Simulation.RunContinuous()
	for time_t in range(simulation_length):
		if cycle_t == 900:
			for agent in Agents:

				agent.newstate = agent.get_state(state_type, state_size, Vissim)
				agent.reward   = agent.get_reward()
				agent.remember(agent.state, agent.action, agent.reward, agent.newstate)
				agent.action = agent.act(agent.newstate)
				if Demo_Mode:
					print('Agent Reward in this cycle is : {}'.format(round(agent.reward,2)))

				agent.state    = agent.newstate

			cycle_t = 0
		else:
			cycle_t += 1
            
		# Advance the game to the next frame based on the action.
		Vissim.Simulation.RunSingleStep()
	# Stop the simulation    
	Vissim.Simulation.Stop()

def PER_prepopulate_memory(Agents, Vissim, state_type, state_size, memory_size, vissim_working_directory, model_name):
	memory = []
	# Chech if suitable file exists
	PER_prepopulation_filename =  os.path.join(vissim_working_directory, model_name, 'PER_Prepopulation_length_'+ str(memory_size) +'.p')
	PER_prepopulation_exists = os.path.isfile(PER_prepopulation_filename)
	# If it does, process it into the memory
	if PER_prepopulation_exists:
		print("Previous Experience Found")
		for agent in Agents:
			memory = pickle.load(open(PER_prepopulation_filename, 'rb'))
			for s,a,r,s_ in memory:
				agent.remember(s,a,r,s_)
	# Otherwise generate random data, store it in the agent and generate the file above
	else:
		memory_full = False
		cycle_t = 0
		while not memory_full:
			if cycle_t == 900:
				for agent in Agents:
					agent.newstate = agent.get_state(state_type, state_size, Vissim)
					agent.reward   = agent.get_reward()
	
					memory.append((agent.state, agent.action, agent.reward, agent.newstate))
					agent.remember(agent.state, agent.action, agent.reward, agent.newstate)
	
					agent.action   = agent.act(agent.newstate)
					agent.state    = agent.newstate
					if len(memory) == memory_size:
						memory_full = True
				cycle_t = 0
			else:
				cycle_t += 1
 	         
			# Advance the game to the next frame based on the action.
			Vissim.Simulation.RunSingleStep()
		# Dump random transitions into pickle file for later prepopulation of PER
		pickle.dump(memory, open(PER_prepopulation_filename, 'wb'))
		# Stop the simulation   
		Vissim.Simulation.Stop()
	return(memory)

# Average reward across agents after an episode
def average_reward(reward_storage, Agents, episode, episodes):
	average_reward = []
	for agent in Agents:
		average_agent_reward = np.average(agent.episode_reward)
		average_reward.append(average_agent_reward)
	average_reward = np.average(average_reward)
	reward_storage.append(average_reward)
    
	if len(Agents)>1:
			# Print the score and break out of the loop
			print("Episode: {}/{}, Epsilon:{}, Average reward: {}".format(episode+1, episodes, np.round(Agents[0].epsilon,2),np.round(average_reward,2)))
			print("Prediction for [5000,0,5000,0] is: {}".format(Agents[0].model.predict(np.reshape([5000,0,5000,0], [1,4]))))
			for agent in enumerate(Agents):
				print("Agent {}, Average agent reward: {}".format(agent, average_reward[index]))
	else:
		print("Episode: {}/{}, Epsilon:{}, Average reward: {}".format(episode+1, episodes, np.round(Agents[0].epsilon,2), np.round(average_reward,2)))
		print("Prediction for [500,0,500,0] is: {}".format(Agents[0].model.predict(np.reshape([500,0,500,0], [1,4]))))
	return(reward_storage, average_reward)

# Reload agents
def load_agents(vissim_working_directory, model_name, Agents, Session_ID, best):
	print('Loading Pre-Trained Agent, Architecture, Optimizer and Memory.')
	for index, agent in enumerate(Agents):
		Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'.h5')
		agent.model = load_model(Filename)
		if best:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_BestAgent'+str(index)+'_Memory'+'.p')
		else:
			Memory_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'_Memory'+'.p')
		agent.memory = pickle.load(open(Memory_Filename, 'rb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'_Training'+'.p')
		agent.memory = pickle.load(open(Training_Progress_Filename, 'rb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'_Loss'+'.p')
		agent.Loss = pickle.load(open(Loss_Filename, 'rb'))
		
	print('Items successfully loaded.')
	return(Agents)

# Save agents
def save_agents(vissim_working_directory, model_name, Agents, Session_ID, reward_storage):
	for index,agent in enumerate(Agents):    
		Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'.h5')
		print('Saving architecture, weights and optimizer state for agent-{}'.format(index))
		agent.model.save(Filename)
		Memory_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'_Memory'+'.p')
		print('Dumping agent-{} memory into pickle file'.format(index))
		pickle.dump(agent.memory, open(Memory_Filename, 'wb'))
		Training_Progress_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'_Training'+'.p')
		print('Dumping Training Results into pickle file.')
		pickle.dump(reward_storage, open(Training_Progress_Filename, 'wb'))
		Loss_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_Agent'+str(index)+'_Loss'+'.p')
		print('Dumping Loss Results into pickle file.')
		pickle.dump(agent.loss, open(Loss_Filename, 'wb'))

# Save the agent producing best reward
def best_agent(reward_storage, average_reward, best_agent_weights, vissim_working_directory, model_name, Agents, Session_ID):
	if average_reward == np.max(reward_storage):
		for index, agent in enumerate(Agents):
			best_agent_weights = agent.memory
			Memory_Filename = os.path.join(vissim_working_directory, model_name, model_name+'_'+ Session_ID + '_BestAgent'+str(index)+'_Memory'+'.p')
			pickle.dump(agent.memory, open(Memory_Filename, 'wb'))
			print("New best agent found. Saved in {}".format(Memory_Filename))
	return(best_agent_weights)