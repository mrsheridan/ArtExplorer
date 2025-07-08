import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, screen_width, screen_height):
        super().__init__()  # Call the parent class (Sprite) constructor
        self.image = pygame.image.load(image)  # Load the image
        self.rect = self.image.get_rect()  # Get the rectangular area of the image
        self.rect.topleft = (x, y)  # Set the position of the sprite
        self.speed = 5  # Set speed to 1 for slower movement
        self.screen_width = screen_width  # Store the screen width
        self.screen_height = screen_height  # Store the screen height

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed  # Move left
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed  # Move right
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed  # Move up
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed  # Move down

        # ADD BOUNDARY CHECK LOGIC HERE:

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()  # Create a clock object to control the frame rate

# Create a player instance
player = Player('player_img.png', 100, 100, screen_width, screen_height)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)  # Add the player sprite to the group

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
    player.update(keys)  # Update the player's position

    screen.fill((255, 255, 255))  # Fill the screen with white
    all_sprites.draw(screen)  # Draw all sprites in the group
    pygame.display.flip()  # Update the display

    clock.tick(60)  # Cap the frame rate at 60 FPS

pygame.quit()
