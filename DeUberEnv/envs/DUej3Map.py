import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from random import randint

class FSej3(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.map =[
            [1,1,0,0,0],
            [1,0,0,1,0],
            [1,0,1,1,1],
            [1,0,0,0,1],
            [0,0,1,0,1]]
        self.t = 0
        x,y = 0,0
        self.cars = [1,1]
        self.map[1][1] = 2
        self.map[1][4] = 3
        self.action_space = spaces.Discrete(4)
        pass

    def _step(self, action):
        self._take_action(action)
        reward = self._get_reward()
        episode_over = False
        if(reward<0 or self.t>50):
            episode_over = True
        self.t+=1
        return np.array(self.map).flatten().reshape((1, 25)), reward, episode_over, {}

    def _reset(self):
        self.t = 0
        self.map =[
            [1,1,0,0,0],
            [1,0,0,1,0],
            [1,0,1,1,1],
            [1,0,0,0,1],
            [0,0,1,0,1]]
        x,y = 0,0
        while(self.map[y][x]==1):
            x,y = randint(0,len(self.map[0])-1), randint(0,len(self.map)-1)
        self.cars = [1,1]
        self.map[1][1] = 2
        self.map[1][4] = 3
        return np.array(self.map).flatten().reshape((1, 25))

    def _render(self, mode='human', close=False):
        pass
    
    def _seed(self):
        pass

    def _take_action(self, action):
        action+=1
        val_x_n,val_y_n  = self.cars
        self.map[val_y_n][val_x_n] = 0
        if(action%2==1):
            val_y_n += (2*(action%2)-((action*action*action)%4))
        else:
            if(action==2):
                val_x_n += 1
            else:
                val_x_n -= 1
        self.cars = [val_x_n,val_y_n]
        if(not(val_x_n< 0 or val_x_n >= len(self.map[0]) or val_y_n < 0 or val_y_n >= len(self.map))):
            if(self.map[val_y_n][val_x_n]==0):
                self.map[val_y_n][val_x_n] = 2


    def _get_reward(self):

        x,y = self.cars
        #print(f"El coche esta en {x}:{y}, con valor {self.map[y][x]}")
        if(x< 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map)):
            return -1
        if self.map[y][x]==2:
            return 0.01
        elif(x==4 and y==1):
            return 2
        else:
            return -1