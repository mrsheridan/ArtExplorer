import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self, keys, controls, screen_width, screen_height):
        # controls = dictionary with keys for movement: left, right, up, down
        if keys[controls['left']]:
            self.rect.x -= self.speed
        if keys[controls['right']]:
            self.rect.x += self.speed
        if keys[controls['up']]:
            self.rect.y -= self.speed
        if keys[controls['down']]:
            self.rect.y += self.speed

        # Boundary logic
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Create player instances
player1 = Player('player_img.png', 100, 100)
player2 = Player('player2.png', 300, 200)

# Create sprite group and add both players
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# Define control mappings
player1_controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN
}

player2_controls = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s
}

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player1.update(keys, player1_controls, screen_width, screen_height)
    player2.update(keys, player2_controls, screen_width, screen_height)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
