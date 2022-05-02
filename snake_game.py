import pygame
import random
from enum import Enum
from collections import namedtuple


# Initialise pygame modules correctly
pygame.init()
font = pygame.font.SysFont('arial', 25) # Can be inefficient on boot, loading a font directly from disk is quicker.


# Python has an Enum Class!
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Similar to the Point class in C#
Point = namedtuple('Point', 'x, y')

# Constants
SNAKE_BLOCK_SIZE = 20
INITIAL_SPEED = 10
SPEED_INCREASE = 5
# Add Header for Displays
HEADER_THICKNESS = 100

# Colour RGBs
BLACK = (0, 0, 0)
PALE_BOARD = (0, 100, 150)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN1 = (0, 255, 0)
GREEN2 = (200, 255, 0)


class SnakeGame():

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Snake Game - Brent Vidler")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        self.snake_speed = INITIAL_SPEED

        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, 
                    Point(self.head.x-SNAKE_BLOCK_SIZE, self.head.y),
                    Point(self.head.x-(2*SNAKE_BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        # Generate integer positions as multiples of the block size
        # Added
        x = random.randint(0, (self.width-SNAKE_BLOCK_SIZE) // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        y = random.randint(HEADER_THICKNESS//SNAKE_BLOCK_SIZE, (self.height-SNAKE_BLOCK_SIZE) // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE

        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def _update_ui(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, PALE_BOARD, pygame.Rect(0, HEADER_THICKNESS, self.width, self.height-HEADER_THICKNESS))

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x+4, pt.y+4, 12, 12)) # Draw the inner square

        # Draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
        pygame.draw.rect(self.display, WHITE, pygame.Rect(self.food.x+4, self.food.y+4, 12, 12))

        # Draw food
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    
    def _move(self):
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += SNAKE_BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= SNAKE_BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += SNAKE_BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= SNAKE_BLOCK_SIZE
        
        self.head = Point(x, y)

    def _is_collision(self):
        # hits the boundaries
        if self.head.x > self.width - SNAKE_BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - SNAKE_BLOCK_SIZE or self.head.y < 0 + HEADER_THICKNESS:
            return True
        
        # hits itself

        if self.head in self.snake[1:]:
            return True
        
        return False

    def play_step(self):
        #1. Get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        #2. Move

        self._move() # update the head
        self.snake.insert(0, self.head)

        #3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        #4. place new food or finalise the movement
        if (self.head == self.food):
            self.score+=1
            self._place_food()
            # Increase speed
            self.snake_speed += SPEED_INCREASE
        else:
            # Remove last element
            self.snake.pop()

        #5. update ui and clock
        self._update_ui()
        self.clock.tick(self.snake_speed)
        #6. return game over and score
        game_over = False
        return game_over, self.score

if __name__=='__main__':
    game = SnakeGame()


    # game loop
    while True:
        game_over, score = game.play_step()

        # break when gameover
        if game_over:
            game.reset()

