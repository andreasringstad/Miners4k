import pygame
import random

# --- CONFIGURATION & CONSTANTS ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 500
CIRCLE_RADIUS = 5
FPS = 35

# Miner Data Indices
M_ALIVE = 0
M_Y = 1
M_X = 2
M_STATE = 3  # 0:ground, 1:falling, >5:jumping
M_FACING = 4 # 1:right, -1:left
M_GOLD = 5   # 0:no, 1:yes
M_ANIM = 6
M_ANIM_DIR = 7

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Miners4K - Gemini Edition")
myDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Times New Roman', 20)

# Load Sprites
try:
    sprite_sheet = pygame.image.load("sprite.png").convert_alpha()
    minerSprites = [sprite_sheet.subsurface(i * 5, 0, 5, 11) for i in range(20)]
except:
    minerSprites = [pygame.Surface((5, 11)) for _ in range(20)]
    [s.fill((255, 0, 255)) for s in minerSprites]

# --- BRUSH SETUP ---
circle_surf = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2))
circle_surf.fill((0, 0, 0))
pygame.draw.circle(circle_surf, (255, 255, 255), (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
circle_offsets = []
for y in range(CIRCLE_RADIUS * 2):
    for x in range(CIRCLE_RADIUS * 2):
        if circle_surf.get_at((x, y)) == (255, 255, 255, 255):
            circle_offsets.append((y - CIRCLE_RADIUS, x - CIRCLE_RADIUS))

def apply_brush(x, y, level, world_surf, mode):
    if mode == "erase":
        target_val, color, valid_targets = 0, (0, 0, 0), [3, 4]
    else:
        target_val, color, valid_targets = 4, (124, 91, 68), [0]

    for off_y, off_x in circle_offsets:
        ty, tx = y + off_y, x + off_x
        if 0 <= ty < SCREEN_HEIGHT and 0 <= tx < SCREEN_WIDTH:
            if level[ty][tx][0] in valid_targets:
                level[ty][tx] = [target_val, color]
                world_surf.set_at((tx, ty), color)

# --- MAP GENERATION ---
def create_map():
    world = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    level = []
    platformWidth = 100
    borderSize = 10
    platformLevel = 150
    platformHeight = 6

    for y in range(SCREEN_HEIGHT):
        row = []
        for x in range(SCREEN_WIDTH):
            if x < borderSize or x > SCREEN_WIDTH - borderSize:
                cell = [1, (140, 140, 140)]
            elif platformLevel < y < platformLevel + platformHeight:
                if borderSize <= x < borderSize + platformWidth or SCREEN_WIDTH - borderSize - platformWidth < x <= SCREEN_WIDTH - borderSize:
                    cell = [2, (140, 140, 140)]
                else:
                    cell = [3, (80, 140, 30)]
            elif y > SCREEN_HEIGHT - borderSize:
                cell = [2, (140, 140, 140)]
            elif y < platformLevel + platformHeight:
                cell = [0, (0, 0, 0)]
            else:
                cell = [4, random.choice(((135, 119, 52), (133, 107, 62), (124, 101, 47)))]
            row.append(cell)
            world.set_at((x, y), cell[1])
        level.append(row)
    
    for y in range(400, 420):
        for x in range(400, 420):
            level[y][x] = [5, (255, 255, 0)]
            world.set_at((x, y), (255, 255, 0))
    return level, world

# --- MAIN LOOP ---
running = True
while running:
    level, world = create_map()
    miners = []
    px, py = [0, 0], [0, 0]
    mouse_btns = [0, 0, 0]
    prev_btns = [0, 0, 0]
    goldScore = 0
    goldTarget = 200
    numberOfMiners = 10000 # Reduced for clearer viewing of behavior
    anim_timer = 0
    runningRound = True

    while runningRound:
        anim_timer = (anim_timer + 1) % 4
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningRound = False
                running = False

        # Input & Interpolated Brush
        px[1], py[1] = px[0], py[0]
        prev_btns = mouse_btns
        mouse_btns = pygame.mouse.get_pressed(num_buttons=3)
        px[0], py[0] = pygame.mouse.get_pos()

        active_mode = None
        if mouse_btns[0]: active_mode = "erase"
        elif mouse_btns[2]: active_mode = "draw"

        if active_mode:
            dx, dy = px[0] - px[1], py[0] - py[1]
            dist = max(abs(dx), abs(dy))
            if dist > 0 and (prev_btns[0] or prev_btns[2]):
                for i in range(dist + 1):
                    ix = px[1] + int(i * dx / dist)
                    iy = py[1] + int(i * dy / dist)
                    apply_brush(ix, iy, level, world, active_mode)
            else:
                apply_brush(px[0], py[0], level, world, active_mode)

        # Spawn
        if numberOfMiners > 0 and anim_timer == 0:
            miners.append([1, -10, random.randint(15, 85), 1, 1, 0, 0, 1])
            numberOfMiners -= 1

        # Render
        myDisplay.blit(world, (0, 0))

        # Miner Logic
        for m in miners:
            if m[M_ALIVE] == 0: continue
            
            cx = m[M_X] + 2
            cy = m[M_Y] + 10
            facing = m[M_FACING]

            # 1. MINING LOGIC (Increased Reach)
            if m[M_GOLD] == 0:
                # Priority list of offsets: Front, Above, Center, Behind, Below
                reach_offsets = [
                    (0, facing), (-1, 0), (0, 0), (0, -facing), (1, 0)
                ]
                
                for ry, rx in reach_offsets:
                    target_y, target_x = cy + ry, cx + rx
                    # Boundary check
                    if 0 <= target_y < SCREEN_HEIGHT and 0 <= target_x < SCREEN_WIDTH:
                        if level[target_y][target_x][0] == 5: # Found Gold!
                            m[M_GOLD] = 1
                            level[target_y][target_x] = [0, (0, 0, 0)]
                            world.set_at((target_x, target_y), (0, 0, 0))
                            break # Only pick up one at a time

            # 2. PHYSICS & MOVEMENT
            try:
                ground_val = level[cy + 1][cx][0]
                front_val = level[cy][cx + facing][0]
            except IndexError:
                m[M_ALIVE] = 0
                continue

            # Return Gold to platform
            if m[M_GOLD] == 1:
                if m[M_Y] < 160 and (m[M_X] < 110 or m[M_X] > 530):
                    m[M_GOLD] = 0
                    goldScore += 1

            # State Machine
            if m[M_STATE] == 1: # Fall
                if ground_val != 0: m[M_STATE] = 0
                else: m[M_Y] += 1
            elif m[M_STATE] == 0: # Walk
                if front_val == 0: 
                    m[M_X] += facing
                elif level[cy - 1][cx + facing][0] == 0: # Step up 1
                    m[M_X] += facing
                    m[M_Y] -= 1
                else: 
                    m[M_FACING] *= -1 # Turn around
                
                if ground_val == 0: m[M_STATE] = 1

            # 3. ANIMATE & BLIT
            if anim_timer == 0:
                m[M_ANIM] += m[M_ANIM_DIR]
                if m[M_ANIM] >= 4 or m[M_ANIM] <= 0: m[M_ANIM_DIR] *= -1

            sprite_idx = m[M_ANIM]
            if m[M_GOLD]: sprite_idx += 5
            if m[M_FACING] == -1: sprite_idx += 10
            myDisplay.blit(minerSprites[sprite_idx], (m[M_X], m[M_Y]))

        # UI
        score_txt = myfont.render(f"Gold: {goldScore}/{goldTarget}", True, (255, 255, 255))
        myDisplay.blit(score_txt, (12, 5))
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()