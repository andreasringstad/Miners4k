import pygame
import random

# Constants for game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
FRAMERATE = 60  # Target frame rate for smooth mouse interaction
MINER_MOVE_RATE = 30  # Miner movement updates per second

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Miners4K Simplified")
clock = pygame.time.Clock()

# Load miner sprites from a single image
sprite_sheet = pygame.image.load("sprite.png").convert_alpha()
miner_sprites = [sprite_sheet.subsurface(i*5, 0, 5, 11) for i in range(20)]

# Miner class
class Miner:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.facing = 1  # 1 for right, -1 for left
        self.state = "falling"  # "grounded", "falling", "jump1", "jump2", "jump 3", "jump4", 
        self.hasGold = False
        self.sprites = sprites  # A list of sprites for different animations
        self.frame = 0  # Current frame of the animation

    def update(self):
        if self.state == "falling":
            if level[self.y + 1][self.x][0] == 'air':
                self.y += 1
            else:
                self.state = "grounded"
        elif self.state == "grounded":
            if level[self.y + 1][self.x][0] == 'air':
                self.state = "falling"
                self.y += 1
            elif level[self.y][self.x + self.facing][0] == 'air':
                self.x += self.facing
            else:
                self.facing *= -1
                if random.random() < 0.5:
                    self.state = "jump1"
                    self.y -= 1
                    self.x += self.facing


        self.x += 1
        self.frame = (self.frame + 1) % len(self.sprites)  # Cycle through the sprites
        # Here you can add logic to change the current_sprite based on the miner's state or actions

    def draw(self, screen):
        # Draw the miner using the current sprite
        screen.blit(self.sprites[self.frame], (self.x-2, self.y-10))


# Function to create the level
        
# level: 0 ground type: 0 air, 1 stone, 2 platform, 3 grass, 4 dirt, 5 gold, 6 surfacegold, 7 dropplatform
# color: air-black(0,0,0), stone-gray(140,140,140), filled-dirt(102,68,12), gold(255,255,0), surfacegold(255,255,0)
def create_level():
    level = []
    platformWidth = 100
    borderSize = 10
    platformLevel = 150
    platformHeight = 6
    
    for y in range(SCREEN_HEIGHT):
        row = []
        for x in range(SCREEN_WIDTH):
            # Stone border
            if x < borderSize or x > SCREEN_WIDTH - borderSize:
                row.append(('border', (140, 140, 140)))
            # Platform level handling
            elif platformLevel <= y < platformLevel + platformHeight:
                if borderSize <= x < borderSize + platformWidth or SCREEN_WIDTH - borderSize - platformWidth < x <= SCREEN_WIDTH - borderSize:
                    # Platform
                    row.append(('platform', (140, 140, 140)))
                else:
                    # Grass above the platform
                    row.append(('grass', (80, 140, 30)))
            # Ground below the platform
            elif y >= platformLevel + platformHeight:
                # Randomize dirt tiles
                dirt_color = random.choice([(135, 119, 52), (133, 107, 62), (124, 101, 47)])
                row.append(('dirt', dirt_color))
            else:
                # Air for everything else
                row.append(('air', (0, 0, 0)))
        level.append(row)
    
    # Adding gold
    for y in range(400, 420):
        for x in range(400, 420):
            level[y][x] = ('gold', (255, 255, 0))  # Gold area

    return level

# Draw the level
def draw_level(screen, level):
    
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            screen.set_at((x, y), tile[1])

# Create level
level = create_level()
worldSurface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
draw_level(worldSurface, level)

# List to store miners
miners = []

# Timing for miner movement updates
move_timer = 0
move_interval = 1000 // MINER_MOVE_RATE  # Milliseconds between miner updates

# Game loop
running = True
while running:
    dt = clock.tick(FRAMERATE)  # Delta time in milliseconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn a new miner at a random position
    if random.random() < 0.05:
        miners.append(Miner(random.randint(10, SCREEN_WIDTH - 10), random.randint(10, 20), miner_sprites) )

    # Update miner positions at a controlled rate
    move_timer += dt
    if move_timer >= move_interval:
        for miner in miners:
            miner.update()
        move_timer %= move_interval  # Reset timer, keep the remainder to avoid drift

    # Drawing
    screen.fill((0, 0, 0))  # Clear screen with black or another background drawing function
    screen.blit(worldSurface, (0, 0))  # Draw the level
    for miner in miners:
        miner.draw(screen)  # Draw each miner with their current sprite

    pygame.display.flip()  # Update the display

pygame.quit()