import numpy as np
from math import sqrt, log
from state import State
from random import randint

class Mcts:
    def __init__(self, stateman, root, simulations):
        self.stateman = stateman
        self.current_state = root
        self.simulations = simulations

    def tree_policy(self, start_state):
        current_state = start_state
        while(current_state.children):
            next_state = self.selection(current_state)
            current_state = next_state

        if(current_state.rollout):
            self.expansion(current_state)
        else:
            self.rollout(current_state, current_state.get_available_actions())

    def selection(self, state):
        poss_next_state = [0]*len(state.children)
        pos = 0

        for child in state.children:
            if(child.num_visits == 0):
                return child
            
            else:
                if(state.player == 1):
                    poss_next_state[pos] = ((child.total_wins/child.num_visits) + (4 * sqrt((log(state.num_visits))/(1+child.num_visits))))
                elif(state.player == -1):
                    poss_next_state[pos] = ((child.total_wins/child.num_visits) - (4 * sqrt((log(state.num_visits))/(1+child.num_visits))))
            pos+=1          
        if(state.player == 1):
            next_state = state.children[poss_next_state.index(max(poss_next_state))]
        elif(state.player == -1):
            next_state = state.children[poss_next_state.index(min(poss_next_state))]
        return next_state

    def expansion(self, current_state):
        actions = current_state.get_available_actions()
        if self.stateman.is_terminal(current_state.grid, current_state.player, len(actions)):
            self.backprop(current_state.player, current_state)
            return
        if not actions:
            self.backprop(0, current_state)
            return
        for action in actions:
            new_grid = current_state.grid.copy()
            new_grid[action] = current_state.player
            new_state = State(new_grid, current_state.player*-1, current_state, action)
            current_state.add_child(new_state)
        self.rollout(new_state, actions)
        

    def rollout(self, current_state, actions):
        available_actions = actions
        num_actions = len(actions)
        rollout_grid = current_state.grid.copy()
        rollout_player = current_state.player
        current_state.change_rollout()

        while not self.stateman.is_terminal(rollout_grid, rollout_player*-1, num_actions):
            if num_actions == 0:
                self.backprop(0, current_state)
                return
            random_move = randint(0,len(available_actions)-1)
            action = available_actions.pop(random_move)

            rollout_grid[action] = rollout_player
            rollout_player *= -1
            num_actions -= 1
        #print(rollout_grid)

        
        self.backprop(rollout_player*-1, current_state)

    def backprop(self, winner, current_state):
        current_state = current_state
        current_state.add_visits_and_win(winner)
        #FIXME: Have to evaluate if this is the right strategy to update
        #adding a value to the state. Either it is a win for player 1 => +1 or a win for player 2 => -1
        
        while (current_state.parent_state):
            current_state = current_state.parent_state
            current_state.add_visits_and_win(winner)
        return

    def run(self):
        for i in range(self.simulations):
            self.tree_policy(self.current_state)

        num_visits = []
        for child in self.current_state.children:
            num_visits.append(child.num_visits + child.total_wins/self.simulations)
        indeks = num_visits.index(max(num_visits))
        print(num_visits)

        child_number = 0
        action_board = []
        for placement in range(len(self.current_state.grid)):
            if(self.current_state.grid[placement] == 0):
                action_board.append(num_visits[child_number])
                child_number += 1
            else:
                action_board.append(0) 
        print(action_board)

        return self.current_state.children[indeks], action_board