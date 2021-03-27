from state import State
import numpy as np
from random import randint


class Stateman:
    def __init__(self, state, size, grid, player):
        self.current_state = state
        self.current_player = player
        self.board_size = size
        self.grid = grid
        self.neighbors = {}
        self.get_neighbors()
        self.indices = {-1: ([i * size for i in range(size)], [(i * size) + (size - 1) for i in range(size)]), 1: ([i for i in range(size)], [i for i in range(size * (size - 1), size * size)])}
        

    def change_state(self, grid, state, player):
        new_state = State(grid.copy(), player, state)
        state.add_child(new_state)
        return new_state


    def print_state_tree(self):
        state = self.current_state
        while(state.parent_state != None):
            print("State")
            print(state.grid)
            print(state.player)
            print("------------------------------\n")
            state = state.parent_state

    def intersection(self, a, b):
        A = set(a)
        B = set(b)
        return (A & B)


    def to_one(self, arr):
        if(arr[0] < 0 or arr[1] < 0 or arr[0] > (self.board_size-1) or arr[1] > (self.board_size-1)):
            return -100
        return (self.board_size*arr[0] + arr[1])


    def get_neighbors(self): 
        neighbors = []
        allowed_neighbors = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                allowed_neighbors.append(self.to_one([r,c]))
                neighbors.append([self.to_one([r-1,c]), self.to_one([r-1, c+1]), self.to_one([r, c+1]), self.to_one([r+1, c]), self.to_one([r+1, c-1]), self.to_one([r, c-1])])


        for i in range(self.board_size*self.board_size):
            self.neighbors[i] = (self.intersection(allowed_neighbors, neighbors[i]))

    def is_terminal(self, grid, player):
        start_indices, end_indices = self.indices[player]
        explore = []
        visited = []
        
        
        for i in start_indices:
            if(grid[i] == player):
                explore.append(i)
        
        while len(explore) != 0:
            current_node = explore.pop()
            if(current_node in end_indices):
                #print("The winner is player: " + str(player))
                return True
            
            if(current_node in visited):
                continue
            for neigh in self.neighbors[current_node]:
                if(grid[neigh] == player):
                    explore.append(neigh)
                    
            visited.append(current_node)
        
        return False


    
    def get_available_actions(self, grid):
        return np.where(np.array(grid) == 0)

    
    def get_random_move(self, grid):
        available_actions = self.get_available_actions(grid)[0]
        random_move = randint(0,len(available_actions)-1)
        action = available_actions[random_move]
        return action