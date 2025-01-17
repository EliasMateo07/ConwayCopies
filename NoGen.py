"""Dev Notes: my version of Conway's game of life has the same rules but each cell 
automatically updates to what it sees in order of a list, making them have their own 
minds and more of a virus while Conway's is more of an intelligent lifeform"""
                                
def surroundings(main_square, all_squares):
    square_coords = main_square.rect.x, main_square.rect.y
    list = []
    for square in all_squares:
        if square != main_square:
            if (abs(square.rect.x - square_coords[0]) <= 25 and
                abs(square.rect.y - square_coords[1]) <= 25):
                list.append(square)
    population(main_square, list)

def population(main_square, surrounding_squares):
    alive_count = 0
    for square in surrounding_squares:
        if square.alive == True:
            alive_count += 1
    ### RULES
    if alive_count < 2 or alive_count > 3: ### Rule 1, underpopulation, Rule 2, overpopulation
        main_square.alive = False
    elif alive_count == 3: ### Rule 3, reproduction
        main_square.alive = True
                                    ### GAME SETUP ###
import pygame, sys, random
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (75,75,75)
pygame.init()

class Square(pygame.sprite.Sprite):
    def __init__(self, square_rect, color=BLACK):
        super().__init__()
        self.image = pygame.Surface(square_rect)
        self.value = 0
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.alive = False 

(SCREEN_WIDTH, SCREEN_HEIGHT) = 1000, 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Elias's Game of Life")
game_grid = pygame.sprite.Group()

squares = []
players = []
grid = (40, 40)
square_rect = (25,25)
for column in range(grid[0]):
    for row in range(grid[1]):
        outer = Square(square_rect,GRAY)
        square = Square((23,23))
        outer.rect.x = (column * 25)
        outer.rect.y = (row * 25)
        square.rect.center = outer.rect.center
        squares.append(outer)
        squares.append(square)
        players.append(square)
game_grid.add(squares)

starting_squares = random.sample(players, 100)
for square in starting_squares:
    square.alive = True
                                     ### GAME LOOP ###
def gameloop():
    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                        
                    else:
                        paused = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if paused:
                        for square in players:
                            if square.rect.collidepoint(event.pos):
                                if not square.alive:
                                    square.alive = True
                                else:
                                    square.alive = False
        for square in players:
            if square.alive:
                square.image.fill(WHITE)
            else:
                square.image.fill(BLACK)                        
            if not paused:
                surroundings(square, players)
        screen.fill(WHITE)
        game_grid.draw(screen)
        pygame.display.update()
gameloop()