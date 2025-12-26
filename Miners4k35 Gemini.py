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
pygame.display.set_caption("Miners4K - Fixed Camera & World Clamping")
SCREEN_WIDTH, SCREEN_HEIGHT = 1344, 756
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
    
    zoom = 1.5
    cam_x, cam_y = 0, 0
    prev_mouse_pos = (0, 0)
    
    runningRound = True
    while runningRound:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningRound, running = False, False
            if event.type == pygame.MOUSEWHEEL:
                # Zoom centered on mouse
                old_zoom = zoom
                zoom = max(1.5, min(zoom + event.y * 0.2, 5.0))
                # Adjust camera to keep mouse over same world spot
                cam_x += (mouse_pos[0] / old_zoom) - (mouse_pos[0] / zoom)
                cam_y += (mouse_pos[1] / old_zoom) - (mouse_pos[1] / zoom)

        # 1. CAMERA CLAMPING
        # Prevents scrolling past the world boundaries
        max_cam_x = max(0, WORLD_WIDTH - (SCREEN_WIDTH / zoom))
        max_cam_y = max(0, WORLD_HEIGHT - (SCREEN_HEIGHT / zoom))
        cam_x = max(0, min(cam_x, max_cam_x))
        cam_y = max(0, min(cam_y, max_cam_y))

        # Coordinate Conversion (Now with clamping protection)
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
        
        if mouse_btns[1]:
            cam_x -= (mouse_pos[0] - prev_mouse_pos[0]) / zoom
            cam_y -= (mouse_pos[1] - prev_mouse_pos[1]) / zoom

        # --- LOGIC (35 FPS) ---
        if logic_tick_counter % LOGIC_DIVIDER == 0:
            anim_timer = (anim_timer + 1) % 4
            if numberOfMiners > 0 and anim_timer == 0:
                miners.append([1, -10, random.randint(20, 80), 1, 1, 0, 0, 1])
                numberOfMiners -= 1

            for m in miners:
                if not m[M_ALIVE]: continue
                mx, my, facing = m[M_X], m[M_Y], m[M_FACING]
                cx, cy = mx + 2, my + 10

                # Gold Pickup (Simplified for Logic)
                if not m[M_GOLD]:
                    found_gold = False
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

                # Physics & Collision
                try:
                    if m[M_STATE] == 1:
                        if level[cy + 1][cx][0] != 0: m[M_STATE] = 0
                        else: m[M_Y] += 1
                    elif m[M_STATE] == 0:
                        if level[cy][cx + facing][0] == 0: m[M_X] += facing
                        elif level[cy - 1][cx + facing][0] == 0: m[M_X], m[M_Y] = mx+facing, my-1
                        else:
                            m[M_FACING] *= -1
                            if random.random() < 0.2: m[M_STATE] = 18
                        if level[cy + 1][cx][0] == 0:
                            if random.random() < 0.5: m[M_STATE] = 18
                            else: m[M_STATE] = 1
                    else: # Jumping
                        nx, ny = mx, my
                        if m[M_STATE] > 10: ny, nx = my - 1, mx + facing
                        elif m[M_STATE] > 6: nx = mx + facing
                        else: ny, nx = my + 1, mx + facing

                        if 0 <= ny < WORLD_HEIGHT - 11 and 0 <= nx < WORLD_WIDTH - 5:
                            if level[ny + 10][nx + 2][0] == 0:
                                m[M_X], m[M_Y] = nx, ny
                                m[M_STATE] -= 1
                            else: m[M_STATE] = 1
                        else: m[M_STATE] = 1
                        if m[M_STATE] < 2: m[M_STATE] = 1
                except IndexError: m[M_ALIVE] = 0

                if m[M_STATE] == 0 and anim_timer == 0:
                    m[M_ANIM] += m[M_ANIM_DIR]
                    if m[M_ANIM] >= 4 or m[M_ANIM] <= 0: m[M_ANIM_DIR] *= -1

        # --- DRAWING ---
        myDisplay.fill((20, 20, 20))
        
        # Determine what part of the world to show
        view_rect = pygame.Rect(int(cam_x), int(cam_y), int(SCREEN_WIDTH / zoom), int(SCREEN_HEIGHT / zoom))
        world_clip = view_rect.clip(world.get_rect())
        
        if world_clip.width > 0 and world_clip.height > 0:
            sub_world = world.subsurface(world_clip)
            scaled_world = pygame.transform.scale(sub_world, (int(world_clip.width * zoom), int(world_clip.height * zoom)))
            # Offset the world blit if the camera is viewing "empty space" (though clamped now)
            blit_x = (world_clip.x - cam_x) * zoom
            blit_y = (world_clip.y - cam_y) * zoom
            myDisplay.blit(scaled_world, (blit_x, blit_y))

        # Miner Drawing with same offset logic
        for m in miners:
            if not m[M_ALIVE]: continue
            smx = (m[M_X] - cam_x) * zoom
            smy = (m[M_Y] - cam_y) * zoom
            if -10 < smx < SCREEN_WIDTH and -10 < smy < SCREEN_HEIGHT:
                idx = (2 if m[M_STATE] > 1 else m[M_ANIM]) + (5 if m[M_GOLD] else 0) + (10 if m[M_FACING] == -1 else 0)
                s = minerSprites[idx]
                scaled_s = pygame.transform.scale(s, (int(5 * zoom), int(11 * zoom)))
                myDisplay.blit(scaled_s, (smx, smy))

        prev_mouse_pos = mouse_pos
        score_txt = myfont.render(f"Gold: {goldScore} | Zoom: {zoom:.1f}x | Cam: {int(cam_x)},{int(cam_y)}", True, (255, 255, 255))
        myDisplay.blit(score_txt, (15, 10))
        pygame.display.flip()
        logic_tick_counter += 1
        clock.tick(TARGET_FPS)

pygame.quit()