import pygame, random

class Car():
    def __init__(self, filename: str):
        name = filename.split(".")
        self.first_square = f"{filename[0]}1"
        self.object = pygame.image.load(filename)
        self.height = (self.object).get_height() // 100
        self.width = (self.object).get_width() // 100
        self.move_dir = "horizontal" if self.width > self.height else "vertical"
        



class Rush_hour():
    def __init__(self):
        pygame.init()
        #The game grid
        self.grid = [[0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, "b1", "b2", 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
        #Car PNGs
        self.blue = Car("blue2x1.png")
        self.orange = Car("orange2x1.png")
        self.yellow = Car("yellow1x3.png")

        #Status parameters
        self.solved = False
        self.dragging = False
        self.held_item = ""
        self.held_item_coords = (0, 0)
        self.held_item_start_coords = (0, 0)
        self.pointer_current_coords = (0, 0)
        self.x_diff = 0
        self.y_diff = 0
        #Screen
        self.height = 6
        self.width = 6
        self.scale = 100
        screen_height = self.scale * self.height
        screen_width = self.scale * self.width
        self.screen = pygame.display.set_mode((screen_width + 200, screen_height + 200))
        #Window title
        pygame.display.set_caption("Rush Hour")
        #Run loop
        self.game_loop()


    #Game loop that is repeated
    def game_loop(self):
        while True:
            self.find_events()
            self.draw_screen()
            self.debug()
        

    def find_events(self):
        for event in pygame.event.get():
            #If the user wants to close window
            if event.type == pygame.QUIT:
                exit()
            
            #If the puzzle is not solved, track these events
            if self.solved == False:

                #If the board is clicked, check whether a car is clicked and write down the relevant info
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    clicked_square_x = (x - 100) // 100
                    clicked_square_y = (y - 100) // 100
                    if 0 <= clicked_square_x < 7 and 0 <= clicked_square_y < 7:
                        if self.grid[clicked_square_y][clicked_square_x] != 0:
                            self.dragging = True
                            held_item_id = self.grid[clicked_square_y][clicked_square_x]
                            if held_item_id[0] == "b":
                                self.held_item = self.blue
                                selected_car = self.blue
                            self.held_item_coords = self.find_car_coords(selected_car.first_square)
                            self.x_diff = x - self.held_item_coords[0]
                            self.y_diff = y - self.held_item_coords[1]



                #If a car was clicked and the user is still holding mouse 1 start tracking mouse coords
                if self.dragging:
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        self.pointer_current_coords = (x, y)

                        #If held car moves horizontally
                        if self.held_item.move_dir == "horizontal":
                            self.held_item_coords = (x - self.x_diff, self.held_item_start_coords[1])
                            #Left limit
                            if self.held_item_coords[0] < 100:
                                self.held_item_coords = (100, self.held_item_start_coords[1])
                            #right limit
                            if self.held_item_coords[0] > 500:
                                self.held_item_coords = (500, self.held_item_start_coords[1])



                #If the user lets go of mouse 1, 
                if event.type == pygame.MOUSEBUTTONUP:
                    dropped_square_x = (self.held_item_coords[0] - 50) // 100
                    dropped_square_y = (self.held_item_start_coords[1] - 100) // 100
                    self.clear_selected_item(self.held_item)                                                      ########################################
                    if self.held_item.isupper():
                        self.grid[item_y][item_x] = self.held_item
                        self.grid[item_y][item_x +1] = self.held_item.lower()
                    else:
                        self.grid[item_y][item_x + 1] = self.held_item
                        self.grid[item_y][item_x] = self.held_item.upper()
                    self.held_item = ""
                    self.dragging = False
                    self.x_diff = 0

    def find_car_coords(self, car_letter: str):
        car_id = f"{car_letter}1"
        for y in range(self.height):
            for x in range(self.width):
                square = self.grid[y][x]
                try:
                    if car_id == square[0]:
                        return (x * self.scale + 100, y * self.scale + 100)
                except:
                    pass

    
    def calculate_x_space(held_item: str):
        pass


    #Main function for drawing the screen
    def draw_screen(self):
        self.draw_board()
        self.draw_blue()
        self.draw_orange()
        self.draw_yellow()

        pygame.display.flip()

    #Draw the board as a background
    def draw_board(self):
        self.screen.fill((255, 255, 255))
        #Frame
        pygame.draw.rect(self.screen, (150, 0, 0), (84, 84, 632, 632))
        pygame.draw.polygon(self.screen, (255, 160, 160), [(84, 84), (714, 84), (84, 714)], 0)
        pygame.draw.rect(self.screen, (220, 0, 0), (88, 88, 624, 624))
        pygame.draw.rect(self.screen, (255, 160, 160), (93, 93, 614, 614))
        pygame.draw.polygon(self.screen, (150, 0, 0), [(93, 93), (706, 93), (93, 706)], 0)
        pygame.draw.rect(self.screen, (50, 50, 50), (98, 98, 604, 604))
        #Squares
        for y in range(self.height):
            for x in range(self.width):
                square = self.grid[y][x]
                pygame.draw.rect(self.screen, (160, 160, 160), (x * self.scale + 102, y * self.scale + 102, 96, 96))
                pygame.draw.polygon(self.screen, (240, 240, 240), [(x * self.scale + 102, y * self.scale + 102), (x * self.scale + 102, y * self.scale + 196), (x * self.scale + 196, y * self.scale + 102)], 0)
                pygame.draw.rect(self.screen, (200, 200, 200), (x * self.scale + 110, y * self.scale + 110, 80, 80))
                
    #Draw the 2x1 blue car
    def draw_blue(self):
        if self.held_item == "b1":
            self.screen.blit(self.blue.object, (self.held_item_coords))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    square = self.grid[y][x]
                    if square == "b1":
                        self.screen.blit(self.blue.object, (x * self.scale + 100, y * self.scale + 100))

    #Draw the 2x1 orange car
    def draw_orange(self):
        item = self.held_item
        if item.upper() == "O":
            if self.held_item == "O":
                self.screen.blit(self.orange.object, (self.held_item_coords))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    square = self.grid[y][x]
                    if square == "O":
                        self.screen.blit(self.orange.object, (x * self.scale + 100, y * self.scale + 100))


    #Draw the 1x3 yellow car
    def draw_yellow(self):
        item = self.held_item
        if item.upper() == "Y":
            if self.held_item == "Y":
                self.screen.blit(self.yellow.object, (self.held_item_coords))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    square = self.grid[y][x]
                    if square == "Y":
                        self.screen.blit(self.yellow.object, (x * self.scale + 100, y * self.scale + 100))


    def debug(self):
        pass
    
    def laske_erotus(self, x_coord: int):
        erotus = (x_coord -100) % 100
        return erotus


    def clear_selected_item(self, item: str):
        for y in range(self.height):
            for x in range(self.width):
                square = self.grid[y][x]
                if square == item or square == item.lower():
                    self.grid[y][x] = 0






if __name__ == "__main__":
    Rush_hour()


    