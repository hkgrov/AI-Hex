import pygame, sys
from board import Board
from state import State
import numpy as np
from statemanager import Stateman
from mcts import Mcts
from plotter import decision_tree_plot as tree_plot

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (198, 226, 255)
COLORS = [WHITE, GREEN, LIGHT_BLUE, BLUE, RED]

PLAYER_COLORS = [GREEN, RED]

class Game:
    def __init__(self, size = 4, play_type = 2, start_player = 1):
        self.board = Board(size)
        self.size = size
        self.current_player = start_player
        self.n_x_n = [0]*(size*size)
        #self.game_state_board = [-1, -1, 1, 1, -1, -1, 1, 0, 0, 1, 1, -1, 0, -1, 1, 1]
        #self.board.draw_game_state(self.game_state_board)
        self.current_state = State(self.n_x_n, start_player, None)
        self.current_state.change_rollout()
        self.stateman = Stateman(state = self.current_state, size = size, grid = self.n_x_n, player = start_player)
        if play_type == 1:
            self.manual_play()
        
        if play_type == 2:
            self.ai_play()


    def manual_play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    valid, index = self.board.place_tile(COLORS[self.current_player])
                    if(valid):
                        self.n_x_n[index] = self.current_player
                        
                        if self.stateman.is_terminal(self.n_x_n, self.current_player):
                            print(str(self.current_player) + " vant!!")
                            #self.print_state_tree()
                            sys.exit()
                        self.current_player = self.current_player * -1
                        self.current_state = self.stateman.change_state(self.n_x_n, self.current_state, self.current_player)


    def ai_play(self):
        test = Mcts(self.stateman, self.current_state, 2000)
        test.run()
        #tree_plot(test.current_state)




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
    Game()