import pygame, sys
from board import Board
from state import State
import numpy as np
from statemanager import Stateman
from mcts import Mcts
from plotter import decision_tree_plot as tree_plot
from neural_network import hex_neural_network
import csv
from time import sleep

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (198, 226, 255)
COLORS = [WHITE, GREEN, LIGHT_BLUE, BLUE, RED]

PLAYER_COLORS = [GREEN, RED]

class Game:
    def __init__(self, size = 10, play_type = 1, start_player = 1, plotter = True, simulations = 1000, visualization = True):
        self.train_x = []
        self.train_y = []
        self.visualization = visualization
        if visualization:
            self.board = Board(size)
        self.simulations = simulations
        self.plotter = plotter
        self.size = size
        self.current_player = start_player
        self.n_x_n = [0]*(size*size)
        self.current_state = State(self.n_x_n, start_player, None)
        self.current_state.change_rollout()
        self.stateman = Stateman(state = self.current_state, size = size, grid = self.n_x_n, player = start_player)


    def manual_play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    valid, index = self.board.place_tile(COLORS[self.current_player])
                    if(valid):
                        self.n_x_n[index] = self.current_player
                        print(self.n_x_n)
                        self.mirror_board(self.n_x_n)
                        if self.stateman.is_terminal(self.n_x_n, self.current_player):
                            print(str(self.current_player) + " vant!!")
                            #self.print_state_tree()
                            sys.exit()
                        self.current_player = self.current_player * -1
                        self.current_state = self.stateman.change_state(self.n_x_n, self.current_state, self.current_player)


    def neural_play(self):
        hex_nn_agent = hex_neural_network(len(self.n_x_n))
        hex_nn_agent.load_model()
        taken_actions = []
        while not self.stateman.is_terminal(self.current_state.grid, self.current_player*-1):
            grid_copy = self.current_state.grid.copy()
            grid_copy.append(self.current_player)
            print(grid_copy)
            prediction = hex_nn_agent.predict([grid_copy])
            for action in taken_actions:
                prediction[action] = 0
            print(prediction)
            if self.current_player == 1:
                action = np.argmax(prediction)
            else:
                action = np.argmin(prediction)
            taken_actions.append(action)
            print(action)
            self.n_x_n[action] = self.current_player
            if self.visualization:
                self.board.auto_place_tile(action, self.current_player)
            self.current_player *= -1
            self.current_state = State(self.n_x_n, self.current_player, self.current_state, action)
            sleep(2)


    def ai_play(self):
        while not self.stateman.is_terminal(self.current_state.grid, self.current_player*-1):
            test = Mcts(self.stateman, self.current_state, self.simulations)
            self.train_x.append(self.current_state.grid)

            new_state, train_y = test.run()
            self.train_y.append(train_y)
            
            print(new_state.action)
            #self.n_x_n[new_state.action] = self.current_player
            if self.visualization:
                self.board.auto_place_tile(new_state.action, self.current_player)
            self.current_player *= -1
            self.current_state = new_state
        
        
        for i in range(len(self.train_x)):
            print(str(self.train_x[i]) + " = " + str(self.train_y[i]))


        #model = hex_neural_network(np.array(self.train_x), np.array(self.train_y), len(self.n_x_n))
        #model.train()

        if(self.plotter):
            tree_plot(self.current_state)

    def create_dataset(self, number_of_games):
        state_dict = {-1: State(self.n_x_n, -1, None), 1: State(self.n_x_n, 1, None)}
        current_state = state_dict[self.current_player]
        current_player = self.current_player
        for i in range(number_of_games):
            while not self.stateman.is_terminal(current_state.grid, self.current_player*-1):
                mcts_runner = Mcts(self.stateman, current_state, self.simulations)
                if self.current_player == -1:
                    self.train_x.append(self.mirror_board(current_state.grid))
                    #self.train_x[-1].append(1)
                else:
                    self.train_x.append(current_state.grid.copy())
                    #self.train_x[-1].append()

                new_state, train_y = mcts_runner.run()
                if self.current_player == -1:
                    self.train_y.append(self.mirror_board(train_y))
                else:
                    self.train_y.append(train_y)

                self.current_player *= -1
                current_state = new_state
            current_player *= -1
            current_state = state_dict[current_player]
            self.current_player = current_player
            

        with open("hex_dataset_x"+str(self.size)+".csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.train_x)

        with open("hex_dataset_y"+str(self.size)+".csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.train_y)
        
        #tree_plot(root_state)


        

    def train_neural_network(self, number_of_games):
        for i in range(number_of_games):
            while not self.stateman.is_terminal(self.current_state.grid, self.current_player*-1):
                mcts_runner = Mcts(self.stateman, self.current_state, self.simulations)
                self.train_x.append(self.current_state.grid)

                new_state, train_y = test.run()
                self.train_y.append(train_y)

                self.current_player *= -1
                self.current_state = new_state
        
        
        for i in range(len(self.train_x)):
            print(str(self.train_x[i]) + " = " + str(self.train_y[i]))


        model = hex_neural_network(np.array(self.train_x), np.array(self.train_y), len(self.n_x_n))
        model.train()

        if(self.plotter):
            tree_plot(test.current_state)


    def reset_game(self, state, player):
        self.current_player = player
        self.current_state = state


    def mirror_board(self, grid):
        new_grid = grid.copy()
        for i in range(len(grid)):
            row = int(i/self.size)
            column = self.size*(i - (self.size*row))
            new_grid[row+column] = grid[i] * -1
        return new_grid
            



#[0  01 02 03 04]        [0 5 10 15 20]
#[5  06 07 08 09]        [1 6 11 16 21]
#[10 11 12 13 14]    =   [2 7 12 17 22]
#[15 16 17 18 19]        [3 8 13 18 23]
#[20 21 22 23 24]        [4 9 14 19 24]

#     def play(self):    
#         going = True
#         while(True):
#             while(going):                                 
#                 mcts = Mcts(self.current_node, self.manager, self.board_size, self.simulations, self.epsilon, self.anet)
#                 action, self.current_node = mcts.run()
                
#                 if(self.visualize):
#                     action = self.manager.to_multi(action)
#                     self.n_x_n[action[0]][action[1]] = self.current_node.player*-1
#                     self.draw_game(self.n_x_n)
#                     ev = pygame.event.get()
#                     #time.sleep(1)

#                 if(self.manager.is_terminal(self.current_node)):
#                     #print("Player " + str(self.current_node.player*-1) + " Won")
#                     #return (self.current_node.player*-1)
#                     going = False
                
                
#             if(self.visualize):
#                 time.sleep(3)
#                 return (self.current_node.player*-1)
                
#             else:
#                 return (self.current_node.player*-1)



#     def rand_play(self, net_1, name_game, player):
#         going = True
#         while(True):
                         
#             while(going):                                 
#                 if(self.current_node.player == player):
#                     case = self.manager.to_network_board(self.current_node.grid, self.current_node.player)
#                     action = net_1.predict(case, self.current_node.grid)
#                 else:
#                     action = self.manager.get_random_move(self.current_node)
                
#                 self.current_node = self.manager.get_next_state(self.current_node, action)
                    
                    
#                 action = self.manager.to_multi(action)
#                 self.n_x_n[action[0]][action[1]] = self.current_node.player*-1

#                 self.draw_game(self.n_x_n)

#                 if(self.manager.is_terminal(self.current_node)):
#                     going = False
#                 ev = pygame.event.get()
#                 time.sleep(0.7)
                
#             if(self.visualize):
#                 print("The winner is: Player" + str(self.current_node.player*-1))
#                 pygame.image.save(self.screen, name_game)
#                 time.sleep(5)
#                 return (self.current_node.player*-1)
    
    
    
    
#     def network_play(self, net_1, net_2, name_game, player):
#         self.player = player
#         going = True
#         while(True):
                         
#             while(going):                                 
#                 case = self.manager.to_network_board(self.current_node.grid, self.current_node.player)
#                 if(self.current_node.player == player):
#                     action = net_1.predict(case, self.current_node.grid)
#                 else:
#                     action = net_2.predict(case, self.current_node.grid)
                    
#                 self.current_node = self.manager.get_next_state(self.current_node, action)
                

#                 action = self.manager.to_multi(action)
#                 self.n_x_n[action[0]][action[1]] = self.current_node.player*-1

#                 self.draw_game(self.n_x_n)

#                 if(self.manager.is_terminal(self.current_node)):
#                     going = False
#                 ev = pygame.event.get()
# #!!!!!!!time.sleep(0.7)
                
#             if(self.visualize):
#                 if (self.current_node.player*-1 == self.player):
#                     print("The winner is: Player 1")
#                 else:    
#                     print("The winner is: Player 2")
#                 pygame.image.save(self.screen, name_game)
#                 #time.sleep(1)
#                 return (self.current_node.player*-1)


if __name__ == "__main__":
    new_game = Game(size = 5, play_type = 2, start_player = -1, plotter = False, simulations = 10000, visualization=True)
    #new_game.manual_play()
    #new_game.ai_play()
    new_game.create_dataset(number_of_games = 1)
    #new_game.neural_play()