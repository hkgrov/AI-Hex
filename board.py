import pygame, math, sys



BLACK = (0,0,0)
WHITE = (255,255,255)
OFF_WHITE = (255, 255, 254)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (198, 226, 255)
COLORS = [WHITE, GREEN, LIGHT_BLUE, BLUE, RED]

class Board:
    def __init__(self, size, caption="My Game"):
        
        self.screen_size = [int(640*(1+(size-5)/8)), int(640*(1+(size-5)/8))]
        self.board_size = size
        pygame.init()
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()        
        self.n_x_n = [[0]*size]*size
        self.dot_positions, self.dot_keys = self.draw_game(self.n_x_n)
        self.padding = [self.screen_size[0]/2 - 50 * (size + 1), self.screen_size[1]/2 - 50 * (size + 1)]
        ev = pygame.event.get()

    def draw_game(self, grid):
        dot_positions = []
        dot_keys = {}
        start_x = int(self.screen_size[0]/2)
        start_y = int(self.screen_size[1]/2) - (50 * (self.board_size - 1))
        for rows in range(len(grid)):
            dot_positions.append([])
            y_pos = start_y + rows*50
            x_pos = start_x - rows*50
            for column in range(len(grid[rows])):
                y_pos = y_pos + math.ceil(column/len(grid))*50
                x_pos = x_pos + math.ceil(column/len(grid))*50
                dot_positions[rows].append((x_pos, y_pos))
                dot_keys[(x_pos, y_pos)] = ((rows * self.board_size) + column)
        self.draw_lines(dot_positions)
        self.draw_circles(dot_positions)

        pygame.draw.lines(self.screen, RED, False, [(start_x - ((self.board_size  - 1) * 50), start_y + (50 * (self.board_size - 2))), ((self.screen_size[0]/2 - 50), start_y)], 5)
        pygame.draw.lines(self.screen, GREEN, False, [((start_x + 50), start_y), (start_x + ((self.board_size  - 1) * 50), start_y + (50 * (self.board_size - 2)) ) ], 5)


        pygame.draw.lines(self.screen, GREEN, False, [(start_x - ((self.board_size  - 1) * 50), start_y + (50 * (self.board_size))), ((self.screen_size[0]/2 - 50), start_y + (50 * ((self.board_size - 1)* 2)))], 5)
        pygame.draw.lines(self.screen, RED, False, [((start_x + 50), start_y + (50 * ((self.board_size - 1)* 2))), (start_x + ((self.board_size  - 1) * 50), start_y + (50 * (self.board_size)))], 5)
        
    
        #pygame.draw.lines(self.screen, GREEN, False, [100, 150], 1)

        pygame.display.update()
        return dot_positions, dot_keys
        
    def draw_circle(self, pos, color):
        pygame.draw.circle(self.screen, color, pos, 10)
    
    def draw_line(self, arr):
        pygame.draw.lines(self.screen, OFF_WHITE, False, arr, 1)

    def auto_place_tile(self, action, player):
        pos1 = int(action / self.board_size)
        pos2 = action - (pos1 * self.board_size)
        pos = self.dot_positions[pos1][pos2]
        self.draw_circle(pos, COLORS[player])
        pygame.display.update()
        print(pos1, pos2)
    

    def place_tile(self, color):
        pos = pygame.mouse.get_pos()
        click = self.screen.get_at(pos) == WHITE
        if(click):
            new_pos = (round(pos[0], self.padding[0]), round(pos[1], self.padding[1]))
            self.draw_circle(new_pos, color)
            pygame.display.update()
            return True, self.dot_keys[new_pos]
        else:
            return False, 0    

    def draw_lines(self, array):
        for row in range(len(array)):
            for column in range(len(array[row]) - 1):
                stop_hor = array[row][column]
                start_hor = array[row][column + 1]
                
                stop_ver = array[column][row]
                start_ver = array[column + 1][row]
                
                self.draw_line([start_hor,stop_hor])
                self.draw_line([start_ver, stop_ver])
                self.draw_line([stop_hor, stop_ver])
    
    def draw_circles(self, dot_positions):
        for i in range(len(dot_positions)):
            for pos in range(len(dot_positions[i])):
                color = COLORS[self.n_x_n[i][pos]]
                self.draw_circle(dot_positions[i][pos], color)

    def draw_game_state(self, grid):
        pos = 0
        for key in self.dot_keys.keys():
            self.draw_circle(key, COLORS[grid[pos]])
            pos += 1
        pygame.display.update()


def round( n , padding):
 
    # Smaller multiple
    a = (n // 50) * 50
     
    # Larger multiple
    b = a
     
    # Return of closest of two
    return (b + padding if n - a > b - n else a + padding)

if __name__ == "__main__":
    size = 5 
    game_board = Board(size = size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                game_board.place_tile(GREEN)
                

        