import pygame 
import random
import time

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

PI = 3.141592653

screen_width = 500
screen_height = 700

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Draw the ellipse
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
    def reset_pos(self):
        # """ Reset position to the top of the screen, at a random x location.
        # Called by update() or the main program loop if there is a collision.
        # """
        self.rect.y = random.randrange(0, 200)
        self.rect.x = random.randrange(0, screen_width)        
 
    def update(self):
        # """ Called each frame. """
 
        # Move block down one pixel
        self.rect.y += 3
         
        # If block is too far down, reset to top of screen.
        if self.rect.y > 700:
            self.reset_pos()

# def draw_car(screen, x = 0, y = 0): A better looking car 
#         pygame.draw.rect(screen,WHITE,[225 + x,550 + y,50,100],0)
#         pygame.draw.ellipse(screen, BLACK, [217.5 + x,560 + y,10,20], 0)
#         pygame.draw.ellipse(screen, BLACK, [273.5 + x,560 + y, 10,20], 0)
#         pygame.draw.ellipse(screen, BLACK, [217.5 + x,625 + y,10,20], 0)
#         pygame.draw.ellipse(screen, BLACK, [273.5 + x,625 + y,10,20], 0)

class Player(pygame.sprite.Sprite):
    # Speed in pixels per frame
    
    def __init__(self, color, width, height):
        self.x_speed = 0
        self.y_speed = 0
 
        # Current position
        self.x_coord = 0
        self.y_coord = 0
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.rect(self.image, color, [0,0,width,height],0)
        
        self.rect = self.image.get_rect()

    def update(self):
        # User pressed down on a key
        if event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                self.x_speed = -10
            if event.key == pygame.K_RIGHT:
                self.x_speed = 10
        if event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT:
                self.x_speed = 0
            if event.key == pygame.K_RIGHT:
                self.x_speed = 0
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

pygame.init()

# This is a list of 'sprites.' Each block in the program is
# added to this list.
# The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
 
# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(10):
    # This represents a block
    block = Block(BLACK, 20, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(0, 500)
 
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a player block
player = Player(BLUE, 50, 100)
player.rect.x = 225
player.rect.y = 550
all_sprites_list.add(player)
size = (500, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Motion Sickness")

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0
health = 10 
game_over = False
timer = 0

# -------- Main Program Loop -----------
while not done:

    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
 
    # --- Game logic should go here
    
    # --- Drawing code should go here
 
    
    # First, clear the screen to green.
    screen.fill(GREEN)
    
    if game_over == False:
        # Calls update() method on every sprite in the list
        all_sprites_list.update()
      
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)  
      
    # Check the list of collisions.
    for block in blocks_hit_list:
        health -= 1
        if health == 0:
            game_over = True
        # Reset block to the top of the screen to fall again.
        block.reset_pos() 
          
    # Draw all the spites
    if game_over == False:
        all_sprites_list.draw(screen)
        
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 25, True, False)
 
    # Render the text. "True" means anti-aliased text. 
    # Black is the color. This creates an image of the 
    # letters, but does not put it on the screen
    if game_over == True:
        game_over_text = font.render("GameOver", True, BLACK)
        # Put the image of the text on the screen at 250x250
        screen.blit(game_over_text, [200, 250])
    score_text = font.render("Score: " + str(score), True, BLACK)
    lives_text = font.render("Lives: " + str(health), True, BLACK)
 
    screen.blit(score_text, [0, 500])
    screen.blit(lives_text, [0, 400])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(60)
    if timer == 60:
        timer = 0
        if game_over == False:
            score += 1
    else:
        timer += 1