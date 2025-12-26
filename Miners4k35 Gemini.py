import pygame
import random

# --- CONFIGURATION & CONSTANTS ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 500
CIRCLE_RADIUS = 5
TARGET_FPS = 70
LOGIC_DIVIDER = 2

# Miner Data Indices
M_ALIVE = 0
M_Y = 1
M_X = 2
M_STATE = 3
M_FACING = 4
M_GOLD = 5
M_ANIM = 6
M_ANIM_DIR = 7

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Miners4K - Extended Reach (Diameter 7)")
myDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Arial', 20)

# Load Sprites
try:
    sprite_sheet = pygame.image.load("sprite.png").convert_alpha()
    minerSprites = [sprite_sheet.subsurface(i * 5, 0, 5, 11) for i in range(20)]
except:
    minerSprites = [pygame.Surface((5, 11)) for _ in range(20)]
    [s.fill((255, 0, 255)) for s in minerSprites]

# --- BRUSH SETUP ---
circle_offsets = []
for y in range(-CIRCLE_RADIUS, CIRCLE_RADIUS):
    for x in range(-CIRCLE_RADIUS, CIRCLE_RADIUS):
        if x*x + y*y <= CIRCLE_RADIUS*CIRCLE_RADIUS:
            circle_offsets.append((y, x))

def apply_brush(x, y, level, world_surf, mode):
    if mode == "erase":
        target_val, color, valid_targets = 0, (0, 0, 0), (3, 4)
    else:
        target_val, color, valid_targets = 4, (124, 91, 68), (0,)

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
    for y in range(SCREEN_HEIGHT):
        row = []
        for x in range(SCREEN_WIDTH):
            if x < 10 or x > 630 or y > 490: cell = [2, (140, 140, 140)]
            elif 150 < y < 156 and (x < 110 or x > 530): cell = [2, (140, 140, 140)]
            elif 150 < y < 156: cell = [3, (80, 140, 30)]
            elif y < 156: cell = [0, (0, 0, 0)]
            else: cell = [4, (124, 101, 47)]
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
    goldScore = 0
    numberOfMiners = 10000
    logic_tick_counter = 0
    anim_timer = 0
    runningRound = True

    while runningRound:
        # 1. HIGH-FREQUENCY INPUT (70 FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningRound, running = False, False

        px[1], py[1] = px[0], py[0]
        mouse_btns = pygame.mouse.get_pressed(num_buttons=3)
        px[0], py[0] = pygame.mouse.get_pos()

        if mouse_btns[0] or mouse_btns[2]:
            mode = "erase" if mouse_btns[0] else "draw"
            dx, dy = px[0] - px[1], py[0] - py[1]
            dist = max(abs(dx), abs(dy))
            for i in range(dist + 1):
                ix = px[1] + int(i * dx / dist) if dist > 0 else px[0]
                iy = py[1] + int(i * dy / dist) if dist > 0 else py[0]
                apply_brush(ix, iy, level, world, mode)

        # 2. LOW-FREQUENCY LOGIC (35 FPS)
        is_logic_frame = (logic_tick_counter % LOGIC_DIVIDER == 0)
        
        if is_logic_frame:
            anim_timer = (anim_timer + 1) % 4
            
            if numberOfMiners > 0 and anim_timer == 0:
                miners.append([1, -10, random.randint(20, 80), 1, 1, 0, 0, 1])
                numberOfMiners -= 1

            for m in miners:
                if not m[M_ALIVE]: continue
                mx, my, facing = m[M_X], m[M_Y], m[M_FACING]

                # --- GOLD PICKUP LOGIC (DIAMETER 7) ---
                if not m[M_GOLD]:
                    cx, cy = mx + 2, my + 10 # Base position
                    found_gold = False
                    
                    # Prioritize point directly in front of feet
                    if 0 <= cy < 500 and 0 <= cx + (facing*3) < 640:
                        if level[cy][cx + (facing*3)][0] == 5:
                            tx, ty = cx + (facing*3), cy
                            found_gold = True
                    
                    # If not found in front, check 7x7 area around feet
                    if not found_gold:
                        for ry in range(-3, 4):
                            for rx in range(-3, 4):
                                tx, ty = cx + rx, cy + ry
                                if 0 <= ty < 500 and 0 <= tx < 640:
                                    if level[ty][tx][0] == 5:
                                        found_gold = True
                                        break
                            if found_gold: break
                    
                    if found_gold:
                        m[M_GOLD] = 1
                        level[ty][tx] = [0, (0, 0, 0)]
                        world.set_at((tx, ty), (0, 0, 0))

                elif my < 160 and (mx < 110 or mx > 530):
                    m[M_GOLD], goldScore = 0, goldScore + 1

                # Physics
                try:
                    if m[M_STATE] == 1: # Falling
                        if level[my + 11][mx + 2][0] != 0: m[M_STATE] = 0
                        else: m[M_Y] += 1
                    elif m[M_STATE] == 0: # Walking
                        if level[my + 10][mx + 2 + facing][0] == 0: m[M_X] += facing
                        elif level[my + 9][mx + 2 + facing][0] == 0: m[M_X], m[M_Y] = m[M_X] + facing, m[M_Y] - 1
                        else:
                            m[M_FACING] *= -1
                            if random.random() < 0.2: m[M_STATE] = 18
                        if level[my + 11][mx + 2][0] == 0:
                            if random.random() < 0.5: m[M_STATE] = 18
                            else: m[M_STATE] = 1
                    else: # Jumping
                        if m[M_STATE] > 10: 
                            if level[my+9][mx+2+facing][0] == 0: m[M_Y], m[M_X] = my-1, mx+facing
                        elif m[M_STATE] > 6:
                            if level[my+10][mx+2+facing][0] == 0: m[M_X] += facing
                        else:
                            if level[my+11][mx+2+facing][0] == 0: m[M_Y], m[M_X] = my+1, mx+facing
                        m[M_STATE] -= 1
                        if m[M_STATE] < 2: m[M_STATE] = 1
                except IndexError:
                    m[M_ALIVE] = 0

                if m[M_STATE] == 0 and anim_timer == 0:
                    m[M_ANIM] += m[M_ANIM_DIR]
                    if m[M_ANIM] >= 4 or m[M_ANIM] <= 0: m[M_ANIM_DIR] *= -1

        # 3. DRAWING (70 FPS)
        myDisplay.blit(world, (0, 0))
        for m in miners:
            if not m[M_ALIVE]: continue
            s_idx = (2 if m[M_STATE] > 1 else m[M_ANIM]) + (5 if m[M_GOLD] else 0) + (10 if m[M_FACING] == -1 else 0)
            myDisplay.blit(minerSprites[s_idx], (m[M_X], m[M_Y]))

        score_txt = myfont.render(f"Gold: {goldScore} | FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        myDisplay.blit(score_txt, (15, 10))
        pygame.display.flip()
        
        logic_tick_counter += 1
        clock.tick(TARGET_FPS)

pygame.quit()