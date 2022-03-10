from random import randint, random, sample
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


    def player_vs_ai(self):
        hex_nn_agent = hex_neural_network(self.size)
        hex_nn_agent.load_model()
        taken_actions = []
        conversion_array = [i + j  for j in range(self.size) for i in range(0, self.size*self.size, self.size)]

        while not self.stateman.is_terminal(self.current_state.grid, self.current_player*-1):
            if self.current_player == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        valid, action = self.board.place_tile(COLORS[self.current_player])
                        if(valid):
                            taken_actions.append(action)
                            self.n_x_n[action] = self.current_player
                            self.current_player = self.current_player * -1
                            self.current_state = State(self.n_x_n, self.current_player, self.current_state, action)
            else:
                new_grid = self.mirror_board(self.current_state.grid)
                #new_grid = self.mirror_board([x / 10 for x  in self.current_state.grid])
                prediction = hex_nn_agent.predict([new_grid])
                print(prediction)
                for action in taken_actions:
                    prediction[conversion_array[action]] = 0

                action = conversion_array[np.argmax(prediction)]


                taken_actions.append(action)
                self.n_x_n[action] = self.current_player
                self.board.auto_place_tile(action, self.current_player)
                self.current_player *= -1
                self.current_state = State(self.n_x_n, self.current_player, self.current_state, action)


        print(str(self.current_player) + " vant!!")
        sys.exit()

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
        hex_nn_agent = hex_neural_network(self.size)
        hex_nn_agent.load_model()
        taken_actions = []
        #conversion_array = [0, 5, 10, 15, 20, 1, 6, 11, 16, 21, 2, 7, 12, 17, 22, 3, 8, 13, 18, 23, 4, 9, 14, 19, 24]

        conversion_array = [i + j  for j in range(self.size) for i in range(0, self.size*self.size, self.size)]
        while not self.stateman.is_terminal(self.current_state.grid, self.current_player*-1):
            #grid_copy = self.current_state.grid.copy()
            #grid_copy.append(self.current_player)
            #print(grid_copy)

            if self.current_player == -1:
                new_grid = self.mirror_board(self.current_state.grid)
                #new_grid = self.mirror_board([x / 10 for x  in self.current_state.grid])
                prediction = hex_nn_agent.predict([new_grid])
                print(prediction)
                for action in taken_actions:
                    prediction[conversion_array[action]] = 0

                action = conversion_array[np.argmax(prediction)]

            else:
                prediction = hex_nn_agent.predict([self.current_state.grid])
                #prediction = hex_nn_agent.predict([[x / 10 for x in self.current_state.grid]])
                print(prediction)
                for action in taken_actions:
                    prediction[action] = 0
                
                action = np.argmax(prediction)


            
            taken_actions.append(action)
            print(action)
            self.n_x_n[action] = self.current_player
            if self.visualization:
                self.board.auto_place_tile(action, self.current_player)
            self.current_player *= -1
            self.current_state = State(self.n_x_n, self.current_player, self.current_state, action)
            sleep(2)
        if self.visualization:
            pygame.image.save(self.board.screen, "Screenshot.jpg")


    def ai_play(self):
        root = self.current_state
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
            tree_plot(root)

    def create_dataset(self, number_of_games):
        #state_dict = {-1: State(self.n_x_n, -1, None), 1: State(self.n_x_n, 1, None)}
        #current_state = state_dict[self.current_player]
        
        current_player = self.current_player
        for i in range(number_of_games):
            if(random() > 0.6):
                current_state, current_player = self.create_rand_state()
            else:
                current_state = State(self.n_x_n, self.current_player, None)
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
                    self.train_y.append(self.mirror_board_natural(train_y))
                else:
                    self.train_y.append(train_y)

                self.current_player *= -1
                current_state = new_state

            current_player *= -1
            #current_state = state_dict[current_player]
            self.current_player = current_player
            if(i % 10 == 0):
                print("Number of games finished: " + str(i))
            

        with open("hex_dataset_x_" + str(self.size)+".csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.train_x)

        with open("hex_dataset_y_" + str(self.size)+".csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.train_y)
        
        
        model = hex_neural_network(self.size)
        model.create_model()
        model.load_dataset_from_csv()
        model.preprocessing()
        model.train()
        model.save_model()


    def create_rand_state(self):
        players = [-1, 1]
        grid = self.n_x_n.copy()

        number_of_moves = randint(1, (self.size*2)-1)
        start_player = players[randint(0,1)]
        actions = sample(range(0, len(self.n_x_n)), number_of_moves)
        for action in actions:
            grid[action] = start_player
            start_player *= -1

        rand_state = State(grid, start_player, None, actions[-1])
        print(grid)
        return rand_state, start_player

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

    def mirror_board_natural(self, grid):
        new_grid = grid.copy()
        for i in range(len(grid)):
            row = int(i/self.size)
            column = self.size*(i - (self.size*row))
            new_grid[row+column] = grid[i]
        return new_grid
            



if __name__ == "__main__":
    new_game = Game(size = 5, play_type = 2, start_player = 1, plotter = False, simulations = 10000, visualization = True)
    #new_game.manual_play()
    #new_game.ai_play()
    #new_game.create_dataset(number_of_games = 1)
    new_game.player_vs_ai()