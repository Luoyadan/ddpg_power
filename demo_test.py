from ddpg import *
import numpy as np
import tensorflow as tf
from envir import Environment      # Environment class
from collections import deque
import random
import time
EPISODES = 500
STEP = 1800
INITIAL_EPSILON = 0.5
FINAL_EPSILON = 0.01
REPLAY_SIZE = 2000
BATCH_SIZE = 32
TEST = 5

def main():
	env = Environment()
	agent = DDPG(env)
	reward_track = []
	power_track = []
    

	for episode in xrange(EPISODES):
		state = env.reset()
		print "episode:",episode
        # Train
		for step in xrange(STEP):
			action = agent.noise_action(state)
			next_state,reward,done,_ = env.step(action)
			#print "step:",step
			reward_track.append(reward)
			agent.perceive(state,action,reward,next_state,done)
			state = next_state
			if done:
				break
        # Testing:
		if episode % 5 == 0:
			total_reward = 0
			power = 0.0
			for i in xrange(TEST):
				state = env.reset()
				for j in xrange(1800):
					#env.render()
					action = agent.action(state) # direct action for test
					power = power + env.icepower(action.tolist().index(max(action)))
					#print power, action.tolist().index(max(action))
					state,reward,done,_ = env.step(action)
					total_reward += reward
					if done:
						print j
						break
			ave_reward = total_reward/5.0
			print 'episode: ',episode,'Evaluation Average Reward:',ave_reward
			ave_power = power / 5.0
			power_track.append(ave_power)
			print 'episode: ', episode, 'Power:' , ave_power
			time.sleep(1) 
			
			
	f = file("DDPG_reward_reply.txt", 'w')
	print >> f, reward_track
	f.close()
    
	#f = file("DDPG_loss_100.txt", 'w')
	#print >> f, loss_track
	#f.close()
    
	f = file("DDPG_reply_power.txt", 'w')
	print >> f, power_track
	f.close()
	print("finished")
    

if __name__ == '__main__':
	main()
