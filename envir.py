import numpy as np

class Environment():

    def __init__(self):
        self.current_soc = 0.6
        self.efficiency = self.data_get_efficiency()
        self.time_step = 0
        self.soc_drop = self.data_get_soc_drop()
        self.basic_trip_length = len(self.soc_drop[0])  #1797
        self.reset()
        
    def data_get_efficiency(self):
        temp=[]
        with open("energy_efficiency.txt") as f:
            for line in f:
                temp.append([float(x) for x in line.split()])
        return temp

    def data_get_soc_drop(self):
        temp=[]
        with open("west_soc_drop.txt") as f:
            for line in f:
                temp.append([float(x) for x in line.split()])
        return temp

    def reset(self):
        self.current_soc = 0.6
        #self.state = [np.random.randint(self.powdemand[0][self.time_step % self.basic_trip_length] - 1, 24)/100.0, self.current_soc]
        self.state = [(self.time_step % self.basic_trip_length) /1000.0, self.current_soc]
        
        return np.array(self.state)
        
    def step(self, action):
        done = False
        state = self.state
        reward_penalty = 0
        action_idx =  action.tolist().index(max(action))
        #print action_idx
        self.current_soc = round(self.current_soc - self.soc_drop[self.time_step % self.basic_trip_length][action_idx], 4)
        ice_output = self.icepower(action_idx)
        print self.current_soc
        if abs(self.current_soc - 0.5) > 0.3:
            reward_penalty = 30000000.0 * (abs(self.current_soc - 0.5) + 0.7)
        reward = -(reward_penalty + ice_output) / 100000.0
        self.time_step = self.time_step + 1
        reward += 50
        #self.state = [np.random.randint(self.powdemand[0][self.time_step % self.basic_trip_length] - 1, 24)/100.0, self.current_soc]
        if self.current_soc < 0.2 or self.current_soc > 0.8: done = True
		
        self.state = [(self.time_step % self.basic_trip_length) /1000.0, self.current_soc]
        return np.array(self.state), reward, done, {}
        
    def icepower(self, action):
        if action == 0:
            ice_output = 0
        else:
            ice_output = (action * 10000.0 + 9500.0) / self.efficiency[0][action]
        return ice_output
    

