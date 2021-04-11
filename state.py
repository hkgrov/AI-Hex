import numpy as np
from random import randint

class State:
    def __init__(self, grid, player, parent, action = None, rollout = False):
        #An array consisting of all places on the board and if they are taken by a player (1 / -1)
        self.grid = grid
        #The player that should take the next move
        self.player = player
        #The parent state of this state 
        self.parent_state = parent
        self.children = []
        self.rollout = rollout
        self.action = action
        self.num_visits = 0
        self.total_wins = 0



    def add_child(self, child):
        self.children.append(child)

    
    def get_available_actions(self):
        return [v for v in range(len(self.grid)) if self.grid[v] == 0]
        #return np.where(np.array(self.grid) == 0)

    
    def get_random_move(self):
        available_actions = self.get_available_actions()
        random_move = randint(0,len(available_actions)-1)
        action = available_actions[random_move]
        return action
    
    def change_rollout(self):
        self.rollout = True
    

    def add_visits_and_win(self, value):
        self.num_visits += 1
        self.total_wins += value


    