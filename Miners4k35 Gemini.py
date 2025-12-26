import pygame
import random

# --- CONFIGURATION & CONSTANTS ---
WORLD_WIDTH = 640
WORLD_HEIGHT = 500
CIRCLE_RADIUS = 5
TARGET_FPS = 70  
LOGIC_DIVIDER = 2 

# Miner Data Indices
M_ALIVE, M_Y, M_X, M_STATE, M_FACING, M_GOLD, M_ANIM, M_ANIM_DIR = range(8)

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Miners4K - Zoomable Viewport")
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 # Larger window than the map
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
        if 0 <= ty < WORLD_HEIGHT and 0 <= tx < WORLD_WIDTH:
            if level[ty][tx][0] in valid_targets:
                level[ty][tx] = [target_val, color]
                world_surf.set_at((tx, ty), color)

# --- MAP GENERATION ---
def create_map():
    world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
    level = []
    for y in range(WORLD_HEIGHT):
        row = []
        for x in range(WORLD_WIDTH):
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
    goldScore = 0
    numberOfMiners = 1000 
    logic_tick_counter = 0
    anim_timer = 0
    
    # Zoom & Camera State
    zoom = 1.0
    cam_x, cam_y = 0, 0
    prev_mouse_pos = (0, 0)
    
    runningRound = True
    while runningRound:
        # 1. INPUT & ZOOM HANDLING
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningRound, running = False, False
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0: zoom = min(zoom + 0.5, 5.0)
                if event.y < 0: zoom = max(zoom - 0.5, 1.0)

        # Convert Screen Mouse to World Coordinates
        world_mx = int((mouse_pos[0] / zoom) + cam_x)
        world_my = int((mouse_pos[1] / zoom) + cam_y)
        prev_world_mx = int((prev_mouse_pos[0] / zoom) + cam_x)
        prev_world_my = int((prev_mouse_pos[1] / zoom) + cam_y)

        mouse_btns = pygame.mouse.get_pressed(num_buttons=3)
        if mouse_btns[0] or mouse_btns[2]:
            mode = "erase" if mouse_btns[0] else "draw"
            dx, dy = world_mx - prev_world_mx, world_my - prev_world_my
            dist = max(abs(dx), abs(dy))
            for i in range(dist + 1):
                ix = prev_world_mx + int(i * dx / dist) if dist > 0 else world_mx
                iy = prev_world_my + int(i * dy / dist) if dist > 0 else world_my
                apply_brush(ix, iy, level, world, mode)
        
        # Camera Pan (Middle click or right click + ctrl, etc)
        if mouse_btns[1]:
            cam_x -= (mouse_pos[0] - prev_mouse_pos[0]) / zoom
            cam_y -= (mouse_pos[1] - prev_mouse_pos[1]) / zoom

        # 2. LOGIC (35 FPS)
        is_logic_frame = (logic_tick_counter % LOGIC_DIVIDER == 0)
        if is_logic_frame:
            anim_timer = (anim_timer + 1) % 4
            if numberOfMiners > 0 and anim_timer == 0:
                miners.append([1, -10, random.randint(20, 80), 1, 1, 0, 0, 1])
                numberOfMiners -= 1

            for m in miners:
                if not m[M_ALIVE]: continue
                mx, my, facing = m[M_X], m[M_Y], m[M_FACING]

                # Diameter 7 Pickup
                if not m[M_GOLD]:
                    cx, cy, found_gold = mx + 2, my + 10, False
                    for ry in range(-3, 4):
                        for rx in range(-3, 4):
                            tx, ty = cx + rx, cy + ry
                            if 0 <= ty < WORLD_HEIGHT and 0 <= tx < WORLD_WIDTH:
                                if level[ty][tx][0] == 5:
                                    m[M_GOLD], found_gold = 1, True
                                    level[ty][tx] = [0, (0, 0, 0)]
                                    world.set_at((tx, ty), (0, 0, 0)); break
                        if found_gold: break
                elif my < 160 and (mx < 110 or mx > 530):
                    m[M_GOLD], goldScore = 0, goldScore + 1

                # Physics
                try:
                    if m[M_STATE] == 1:
                        if level[my + 11][mx + 2][0] != 0: m[M_STATE] = 0
                        else: m[M_Y] += 1
                    elif m[M_STATE] == 0:
                        if level[my+10][mx+2+facing][0] == 0: m[M_X] += facing
                        elif level[my+9][mx+2+facing][0] == 0: m[M_X], m[M_Y] = mx+facing, my-1
                        else:
                            m[M_FACING] *= -1
                            if random.random() < 0.2: m[M_STATE] = 18
                        if level[my+11][mx+2][0] == 0:
                            if random.random() < 0.5: m[M_STATE] = 18
                            else: m[M_STATE] = 1
                    else:
                        if m[M_STATE] > 10: m[M_Y], m[M_X] = my-1, mx+facing
                        elif m[M_STATE] > 6: m[M_X] += facing
                        else: m[M_Y], m[M_X] = my+1, mx+facing
                        m[M_STATE] -= 1
                        if m[M_STATE] < 2: m[M_STATE] = 1
                except IndexError: m[M_ALIVE] = 0

                if m[M_STATE] == 0 and anim_timer == 0:
                    m[M_ANIM] += m[M_ANIM_DIR]
                    if m[M_ANIM] >= 4 or m[M_ANIM] <= 0: m[M_ANIM_DIR] *= -1

        # 3. DRAWING & ZOOMING
        myDisplay.fill((30, 30, 30)) # Clear background
        
        # Scale the world surface to match zoom
        scaled_world = pygame.transform.scale(world, (int(WORLD_WIDTH * zoom), int(WORLD_HEIGHT * zoom)))
        myDisplay.blit(scaled_world, (-cam_x * zoom, -cam_y * zoom))

        # Scale and draw miners
        for m in miners:
            if not m[M_ALIVE]: continue
            # Frustum Culling: Only draw if on screen
            screen_mx = (m[M_X] - cam_x) * zoom
            screen_my = (m[M_Y] - cam_y) * zoom
            if -50 < screen_mx < SCREEN_WIDTH and -50 < screen_my < SCREEN_HEIGHT:
                s_idx = (2 if m[M_STATE] > 1 else m[M_ANIM]) + (5 if m[M_GOLD] else 0) + (10 if m[M_FACING] == -1 else 0)
                # Scale the specific sprite
                s = minerSprites[s_idx]
                scaled_s = pygame.transform.scale(s, (int(5 * zoom), int(11 * zoom)))
                myDisplay.blit(scaled_s, (screen_mx, screen_my))

        prev_mouse_pos = mouse_pos
        score_txt = myfont.render(f"Gold: {goldScore} | Zoom: {zoom}x | Middle-Click to Pan", True, (255, 255, 255))
        myDisplay.blit(score_txt, (15, 10))
        pygame.display.flip()
        logic_tick_counter += 1
        clock.tick(TARGET_FPS)

pygame.quit()