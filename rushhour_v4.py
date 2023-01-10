import pygame, random

class Car():
    def __init__(self, filename: str):
        self.id = filename[0]
        self.main = f"{filename[0]}1"
        self.object = pygame.image.load(filename)
        self.height = (self.object).get_height() // 100
        self.width = (self.object).get_width() // 100
        self.move_dir = "horizontal" if self.width > self.height else "vertical"
        



class Rush_hour():
    def __init__(self):
        pygame.init()
        #The game grid
        self.grid = [[0, 0, 0, "o1", "o2", "y1"],
                     [0, 0, 0, 0, 0, "y2"],
                     ["r1", "r2", 0, 0, 0, "y3"],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, "b1", "b2"]]

        #Car PNGs
        red = Car("red2x1.png")
        blue = Car("blue2x1.png")
        orange = Car("orange2x1.png")
        yellow = Car("yellow1x3.png")
        self.cars = [red, blue, orange, yellow]

        #Status parameters
        self.solved = False
        self.drag = False
        self.held_car = ""
        self.held_car_movement = ""
        self.held_car_width = ""
        self.held_car_height = ""
        self.held_car_coords = (0, 0)
        self.held_car_start_coords = (0, 0)
        self.pointer_current_coords = (0, 0)
        self.x_diff = 0
        self.y_diff = 0

        #Screen
        self.height = 6
        self.width = 6
        self.scale = 100
        screen_height = self.scale * self.height
        screen_width = self.scale * self.width
        self.screen = pygame.display.set_mode((screen_width + 300, screen_height + 300))

        #Window title
        pygame.display.set_caption("Rush Hour")
        
        #Run loop
        self.game_loop()


    #Main game loop
    def game_loop(self):
        while True:
            self.find_events()
            self.draw_screen()
        

    def find_events(self):
        for event in pygame.event.get():
            #If the user wants to close window
            if event.type == pygame.QUIT:
                exit()
            
            #If puzzle isn't solved
            if self.solved == False:

                # If a car is clicked, write down relevant car info
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pointer_x, pointer_y = event.pos
                    clicked_square_x = (pointer_x - 100) // 100
                    clicked_square_y = (pointer_y - 100) // 100
                    if 0 <= clicked_square_x < 7 and 0 <= clicked_square_y < 7:
                        clicked_square = self.grid[clicked_square_y][clicked_square_x]
                        if clicked_square != 0:
                            self.drag = True
                            for car in self.cars:
                                if car.id == clicked_square[0]:
                                    self.held_car = car.main
                                    self.held_car_movement = car.move_dir
                                    self.held_car_width = car.width
                                    self.held_car_height = car.height
                                    for y in range(self.height):
                                        for x in range(self.width):
                                            square = self.grid[y][x]
                                            if square == car.main:
                                                self.held_car_coords = (x * self.scale + 100, y * self.scale + 100)
                                                self.held_car_start_coords = (x * self.scale + 100, y * self.scale + 100)                                            
                                                self.x_diff = pointer_x - self.held_car_coords[0]
                                                self.y_diff = pointer_y - self.held_car_coords[1]

                #If 'mouse1' hasn't been unpressed, change the car coordinates according to mouse movement
                if self.drag:
                    if event.type == pygame.MOUSEMOTION:          
                        pointer_x, pointer_y = event.pos
                        #If held car is the red one
                        if self.held_car == "r1":
                            car_start_square = (self.held_car_start_coords[0] // 100, self.held_car_start_coords[1] // 100)
                            squares_needed = 6 - (car_start_square[0] + 1) 
                            free_space = self.calculate_space(self.held_car)
                            left_space = free_space[0] * 100
                            right_space = free_space[1] * 99
                            #Let it go outside the frame if there are no cars blocking it
                            if round(right_space/100) >= squares_needed:
                                if pointer_x - self.x_diff > self.held_car_start_coords[0] - left_space and pointer_x - self.x_diff < self.held_car_start_coords[0] + self.held_car_width + right_space + 200:
                                    self.held_car_coords = (pointer_x - self.x_diff, self.held_car_start_coords[1])
                            #Else limit the movement inside the frame
                            elif pointer_x - self.x_diff > self.held_car_start_coords[0] - left_space and pointer_x - self.x_diff < self.held_car_start_coords[0] + self.held_car_width + right_space:
                                self.held_car_coords = (pointer_x - self.x_diff, self.held_car_start_coords[1])
                        #If held car moves horizontally, change only the x value within free space
                        elif self.held_car_movement == "horizontal":
                            free_space = self.calculate_space(self.held_car)
                            left_space = free_space[0] * 100
                            right_space = free_space[1] * 99
                            if pointer_x - self.x_diff > self.held_car_start_coords[0] - left_space and pointer_x - self.x_diff < self.held_car_start_coords[0] + self.held_car_width + right_space:
                                self.held_car_coords = (pointer_x - self.x_diff, self.held_car_start_coords[1])
                        #If held car moves vertically, change only the y value within free space
                        elif self.held_car_movement == "vertical":
                            free_space = self.calculate_space(self.held_car)
                            up_space = free_space[0] * 100
                            down_space = free_space[1] * 99
                            if pointer_y - self.y_diff > self.held_car_start_coords[1] - up_space and pointer_y - self.y_diff < self.held_car_start_coords[1] + self.held_car_height + down_space:
                                self.held_car_coords = (self.held_car_coords[0], pointer_y - self.y_diff)

                #If 'mouse1' is unpressed, replace the car in the grid and delete relevant car info from memory
                if event.type == pygame.MOUSEBUTTONUP:
                    car_squares = int(self.held_car_width) if self.held_car_movement == "horizontal" else int(self.held_car_height)
                    index = 1
                    car_squares_list = []
                    #create a list of values needing to be placed on the grid
                    for i in range(car_squares):
                        car_squares_list.append(f"{self.held_car[0]}{index}")
                        index += 1
                    #Delete held car values from the grid
                    self.clear_held_car()
                    current_car_line = self.held_car_coords[1] / 100 - 1
                    current_car_col = self.held_car_coords[0] / 100 - 1
                    #Rounds to the closest square
                    if current_car_line % 1 < 0.5:
                        current_car_line = int(current_car_line // 1)
                    else:
                        current_car_line = int(current_car_line //1 + 1)
                    if current_car_col % 1 < 0.5:
                        current_car_col = int(current_car_col // 1)
                    else:
                        current_car_col = int(current_car_col // 1 + 1)
                    #If the red car is outside the frame, set state to solved
                    if self.held_car == "r1" and current_car_col == 6:
                        self.solved = True
                    #Place car values on a line
                    elif self.held_car_movement == "horizontal":
                        index = 0
                        for i in range(car_squares):
                            self.grid[current_car_line][current_car_col] = car_squares_list[index]
                            index += 1
                            current_car_col += 1
                    #Place car values in a column
                    elif self.held_car_movement == "vertical":
                        index = 0
                        for i in range(car_squares):
                            self.grid[current_car_line][current_car_col] = car_squares_list[index]
                            index += 1
                            current_car_line += 1
                    #Delete relevant info
                    self.held_car = ""
                    self.drag = False
                    self.x_diff = 0
                    self.y_diff = 0

            #If puzzle is solved
            if self.solved == True:

                # If the next level button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pointer_x, pointer_y = event.pos
                    if 300 < pointer_x < 500 and 784 < pointer_y < 854:
                        print("Next level")


        pygame.draw.rect(self.screen, (0, 0, 0), (300, 784, 200, 70))
        pygame.draw.rect(self.screen, (255, 255, 255), (302, 786, 196, 66))
                    

    #Main function for drawing the screen
    def draw_screen(self):
        self.draw_board()
        self.draw_red()
        self.draw_blue()
        self.draw_orange()
        self.draw_yellow()
        if self.solved:
            self.draw_end_window()

        pygame.display.flip()


    #Draw the board as a background
    def draw_board(self):
        self.screen.fill((255, 255, 255))
        #Frame
        if self.solved:
            pygame.draw.rect(self.screen, (0, 150, 0), (84, 84, 632, 632))
            pygame.draw.polygon(self.screen, (160, 255, 160), [(84, 84), (714, 84), (84, 714)], 0)
            pygame.draw.rect(self.screen, (0, 220, 0), (88, 88, 624, 624))
            pygame.draw.rect(self.screen, (160, 255, 160), (93, 93, 614, 614))
            pygame.draw.polygon(self.screen, (0, 150, 0), [(93, 93), (706, 93), (93, 706)], 0)
            pygame.draw.rect(self.screen, (50, 50, 50), (98, 98, 604, 604))
        else:
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
        #Goal gate
        if self.solved:
            pygame.draw.rect(self.screen, (255, 255, 255), (702, 302, 100, 96))
            pygame.draw.rect(self.screen, (210, 255, 210), (707, 398, 5, 5))
            pygame.draw.polygon(self.screen, (210, 255, 210), [(706, 398), (702, 398), (706, 402)], 0)
            pygame.draw.polygon(self.screen, (210, 255, 210), [(712, 398), (715, 398), (712, 401)], 0)
            pygame.draw.rect(self.screen, (0, 100, 0), (707, 298, 5, 5))
            pygame.draw.polygon(self.screen, (0, 100, 0), [(706, 302), (702, 302), (706, 298)], 0)
            pygame.draw.polygon(self.screen, (0, 100, 0), [(712, 302), (715, 302), (712, 299)], 0)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (702, 302, 100, 96))
            pygame.draw.rect(self.screen, (255, 210, 210), (707, 398, 5, 5))
            pygame.draw.polygon(self.screen, (255, 210, 210), [(706, 398), (702, 398), (706, 402)], 0)
            pygame.draw.polygon(self.screen, (255, 210, 210), [(712, 398), (715, 398), (712, 401)], 0)
            pygame.draw.rect(self.screen, (100, 0, 0), (707, 298, 5, 5))
            pygame.draw.polygon(self.screen, (100, 0, 0), [(706, 302), (702, 302), (706, 298)], 0)
            pygame.draw.polygon(self.screen, (100, 0, 0), [(712, 302), (715, 302), (712, 299)], 0)
    
    #Draw the window below the frame after a win
    def draw_end_window(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (83, 730, 634, 140))
        pygame.draw.rect(self.screen, (255, 255, 255), (87, 734, 626, 132))
        font_title = pygame.font.SysFont("Arial", 30)
        text_title = font_title.render("Congratulations!", True, (0, 0, 0))
        width_title = text_title.get_width()
        self.screen.blit(text_title, ((900 - width_title) / 2 - 50, 740))
        pygame.draw.rect(self.screen, (0, 0, 0), (300, 784, 200, 70))
        pygame.draw.rect(self.screen, (255, 255, 255), (302, 786, 196, 66))
        font_again = pygame.font.SysFont("Arial", 28)
        text_again = font_again.render("Next level", True, (0, 0, 0))
        width_again = text_again.get_width()
        self.screen.blit(text_again, ((900 - width_title) / 2 - 5, 800))


    #Draw the 2x1 red car
    def draw_red(self):
        if self.solved == False:
            if self.held_car == "r1":
                self.screen.blit(self.cars[0].object, (self.held_car_coords))
            else:
                for y in range(self.height):
                    for x in range(self.width):
                        square = self.grid[y][x]
                        if square == "r1":
                            self.screen.blit(self.cars[0].object, (x * self.scale + 100, y * self.scale + 100))
        else:
            self.screen.blit(self.cars[0].object, (700, 300))
    
    #Draw the 2x1 blue car
    def draw_blue(self):
        if self.held_car == "b1":
            self.screen.blit(self.cars[1].object, (self.held_car_coords))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    square = self.grid[y][x]
                    if square == "b1":
                        self.screen.blit(self.cars[1].object, (x * self.scale + 100, y * self.scale + 100))

    #Draw the 2x1 orange car
    def draw_orange(self):
        if self.held_car == "o1":
            self.screen.blit(self.cars[2].object, (self.held_car_coords))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    square = self.grid[y][x]
                    if square == "o1":
                        self.screen.blit(self.cars[2].object, (x * self.scale + 100, y * self.scale + 100))

    #Draw the 1x3 yellow car
    def draw_yellow(self):
        if self.held_car == "y1":
            self.screen.blit(self.cars[3].object, (self.held_car_coords))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    square = self.grid[y][x]
                    if square == "y1":
                        self.screen.blit(self.cars[3].object, (x * self.scale + 100, y * self.scale + 100))

    #Calculates free space aronud the held car
    def calculate_space(self, car_id: str):
        space_left = 0
        space_right = 0
        car_found = False
        #For horizontal cars
        if self.held_car_movement == "horizontal":
            for line in self.grid:
                if self.held_car in line:
                    #Adds up free space just before held car, and then free space just after held car
                    for value in line:
                        if value == self.held_car:
                            car_found = True
                        elif car_found == False and value == 0:
                            space_left += 1
                        elif car_found == False and value != 0:
                            space_left = 0
                        elif car_found == True and str(value)[0] == self.held_car[0]:
                            pass
                        elif car_found == True and value == 0:
                            space_right += 1
                        elif car_found == True and str(value)[0] != self.held_car[0]:
                            break
            return (space_left, space_right)
        #For vertical cars
        elif self.held_car_movement == "vertical":
            free_above = 0
            free_below = 0
            car_square = (int(self.held_car_start_coords[0] / 100) - 1, int(self.held_car_start_coords[1] / 100) - 1)
            squares_above = car_square[1]
            squares_below = 6 - car_square[1] - self.held_car_height
            #Free space above
            index = 1
            while index <= squares_above:
                if self.grid[car_square[1] - index][car_square[0]] == 0:
                    free_above += 1
                index += 1
            #Free space above
            index = 1
            while index <= squares_below:
                if self.grid[car_square[1] + self.held_car_height - 1 + index][car_square[0]] == 0:
                    free_below += 1
                index += 1
            return(free_above, free_below)
            
    #Resets grid squares containing car info to 0
    def clear_held_car(self):
        y = 0
        x = 0
        for line in self.grid:
            for value in line:
                if self.held_car[0] == str(value)[0]:
                    self.grid[y][x] = 0
                x += 1
            y += 1
            x = 0





if __name__ == "__main__":
    Rush_hour()


    