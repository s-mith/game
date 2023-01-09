import pygame
import time

delta_time = 20

# Initialize pygame
pygame.init()

# Set the window size
window_size = (400, 400)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Keydown Example")

# Run the game loop
running = True
# standard miliseconds time thing
last_time = time.time()
while running:
    
    
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif last_time + delta_time > time.time():
            # print all the keys that are pressed
            keys = pygame.key.get_pressed()
            # turn keys into a string seperated by commas
            keys = ','.join(str(key) for key in keys)
            print(keys)
            last_time = time.time()

    # Update the game state

    # Render the screen
    pygame.display.flip()

# Close the window and quit pygame
pygame.quit()





