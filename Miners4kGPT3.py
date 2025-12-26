import pygame
import random

class Miner:
    def __init__(self, x, y):
        self.alive = True
        self.x = x
        self.y = y
        self.state = 1
        self.facing = -1
        self.animation = 1
        self.carrying_gold = 0

    def update(self, level):
        if self.alive:
            # Handle miner logic based on attributes
            if self.state == 1:
                # Handle miner falling logic
                self.animation = 0
                if level[self.y + 11][self.x + 2][0] != 0:  # If there is ground directly below
                    self.state = 0  # Set state to grounded
                else:  # Otherwise, continue falling down
                    self.y += 1

            elif self.state == 0:  # If the miner is grounded
                if level[self.y + 10][self.x + 2 + 2 * self.facing][0] == 0:  # If there is empty space in front of the miner's feet
                    self.x += self.facing  # Move miner forward
                elif level[self.y + 9][self.x + 2 + 2 * self.facing][0] == 0:  # If there is empty space one step ahead and one step up
                    self.x += self.facing  # Move miner forward
                    self.y -= 1  # Move miner up
                elif level[self.y + 8][self.x + 2 + 2 * self.facing][0] == 0:  # If there is empty space one step ahead and two steps up
                    self.x += self.facing  # Move miner forward
                    self.y -= 2  # Move miner up
                else:
                    self.facing *= -1 # Reverse miner's facing direction
                    pass
                # Handle other miner behavior based on state and conditions
                pass
            elif self.state > 9:
                if level[self.y + 9][self.x + 2 + self.facing][0] == 0:  # If there is empty space one step ahead and one step up
                    self.y -= 1  # Move miner up
                    self.x += self.facing  # Move miner forward
                elif level[self.y + 10][self.x + 2 + self.facing][0] == 0:  # If there is empty space in front of the miner's feet
                    self.x += self.facing  # Move miner forward
                elif level[self.y + 9][self.x + 2][0] == 0:  # If there is empty space one step ahead
                    self.y -= 1  # Move miner up
                else:
                    self.state = 1
                self.animation = 2

            elif self.state > 5:
                if level[self.y + 10][self.x + 2 + self.facing][0] == 0:  # If there is empty space in front of the miner's feet
                    self.x += self.facing  # Move miner forward
                else:
                    self.state = 1
                self.animation = 2

            else:
                if level[self.y + 11][self.x + 2 + self.facing][0] == 0:
                    self.y += 1  # Move miner down
                    self.x += self.facing  # Move miner forward
                self.animation = 0
                self.state -= 1

class Game:
    def __init__(self):
        self.running = True
        self.screen_width = 640
        self.screen_height = 500
        self.level = None
        self.world = None
        self.miners = []
        self.gold_score = 0
        self.gold_left_platform = 1
        self.origin = None
        self.gold_current = None
        self.running_round = True
        self.gold_target = 200
        self.number_of_miners = 100
        self.message = "Gold: "

        pygame.init()
        pygame.display.set_caption("Miners4K")
        self.clock = pygame.time.Clock()
        self.sprite = pygame.image.load("sprite.png")
        self.my_font = pygame.font.SysFont('Times New Roman', 20)
        self.world = pygame.Surface((self.screen_width, self.screen_height))
        self.my_display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.circle_radius = 5
        self.circle = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2))
        self.circle.fill((0, 0, 0))
        pygame.draw.circle(self.circle, (255, 255, 255), (self.circle_radius, self.circle_radius), self.circle_radius)
        self.circle_list = []
        for y in range(self.circle_radius * 2):
            for x in range(self.circle_radius * 2):
                if self.circle.get_at((x, y)) == (255, 255, 255):
                    self.circle_list.append([y, x])
        self.miner_sprite = []
        for i in range(20):
            self.miner_sprite.append(self.sprite.subsurface(i * 5, 0, 5, 11))

    def spawn_miner(self):
        if len(self.miners) < 1:
            miner = Miner(10, 120)
            self.miners.append(miner)

    def update_miners(self):
        for miner in self.miners:
            miner.update(self.level)
            self.world.blit(self.miner_sprite[miner.animation], (miner.x, miner.y))

    def create_map(self):
        self.level = []
        border_size = 10
        platform_width = 100
        platform_level = 150
        platform_height = 6
        for y in range(self.screen_height):
            self.level.append([])
            for x in range(self.screen_width):
                self.level[y].append([0, (0, 0, 0)])  # Start with full array
                if x < border_size or x > self.screen_width - border_size:
                    self.level[y][x] = [1, (140, 140, 140)]  # Create stone border
                elif platform_level < y < platform_level + platform_height:
                    if border_size <= x < border_size + platform_width or self.screen_width - border_size - platform_width < x <= self.screen_width - border_size:
                        self.level[y][x] = [2, (140, 140, 140)]  # Create platform
                    else:
                        self.level[y][x] = [3, (80, 140, 30)]  # Create grass
                elif y > self.screen_height - border_size:
                    self.level[y][x] = [2, (140, 140, 140)]
                elif y < platform_level + platform_height:
                    self.level[y][x] = [0, (0, 0, 0)]
                else:
                    colors = ((135, 119, 52), (133, 107, 62), (124, 101, 47))
                    self.level[y][x] = [4, random.choice(colors)]  # Create dirt

        for y in range(400, 420):
            for x in range(400, 420):
                self.level[y][x] = [5, (255, 255, 0)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.running_round = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.running_round = False

    def update(self):
        self.my_display.fill((0, 0, 0))
        for y, row in enumerate(self.level):
            for x, (tile_type, color) in enumerate(row):
                pygame.draw.rect(self.world, color, (x, y, 1, 1))
        self.update_miners()
        self.my_display.blit(self.world, (0, 0))
        score_message = self.message + str(self.gold_score) + "/" + str(self.gold_target)
        text_surface = self.my_font.render(score_message, False, (255, 255, 255))
        self.my_display.blit(text_surface, (10, 10))
        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(35)

        pygame.quit()
        
game = Game()
game.create_map()
game.spawn_miner()
game.main_loop()