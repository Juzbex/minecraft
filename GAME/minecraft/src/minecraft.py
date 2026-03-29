"""
Minecraft Clone - 3D Voxel Game
High-quality procedural textures and smooth gameplay
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import math
import os
import sys

# Initialize Pygame
pygame.init()

# Display settings
WIDTH, HEIGHT = 1280, 720
display = (WIDTH, HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Minecraft Clone")

# Enable depth testing and face culling
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

# Projection matrix
glMatrixMode(GL_PROJECTION)
gluPerspective(45, display[0] / display[1], 0.1, 1000.0)
glMatrixMode(GL_MODELVIEW)

# World settings
WORLD_SIZE = 48
WORLD_HEIGHT = 32
CHUNK_SIZE = 16

# Block types
BLOCK_AIR = 0
BLOCK_GRASS = 1
BLOCK_DIRT = 2
BLOCK_STONE = 3
BLOCK_WOOD = 4
BLOCK_LEAVES = 5
BLOCK_SAND = 6
BLOCK_WATER = 7
BLOCK_SNOW = 8

block_names = {
    BLOCK_GRASS: "Grass",
    BLOCK_DIRT: "Dirt",
    BLOCK_STONE: "Stone",
    BLOCK_WOOD: "Wood",
    BLOCK_LEAVES: "Leaves",
    BLOCK_SAND: "Sand",
    BLOCK_WATER: "Water",
    BLOCK_SNOW: "Snow"
}

# Texture generation with noise
def generate_noise_texture(base_color, size=64, noise_amount=30):
    """Generate a textured surface with noise"""
    texture_data = np.zeros((size, size, 3), dtype=np.uint8)
    
    for y in range(size):
        for x in range(size):
            # Base color with variation
            noise = random.randint(-noise_amount, noise_amount)
            r = max(0, min(255, base_color[0] + noise))
            g = max(0, min(255, base_color[1] + noise))
            b = max(0, min(255, base_color[2] + noise))
            
            # Add some pattern variation
            pattern = int((math.sin(x * 0.1) + math.cos(y * 0.1)) * 10)
            r = max(0, min(255, r + pattern))
            g = max(0, min(255, g + pattern))
            b = max(0, min(255, b + pattern))
            
            texture_data[y, x] = [r, g, b]
    
    return texture_data.flatten()

def create_grass_texture():
    """Create grass block texture with green top and dirt sides"""
    return generate_noise_texture([76, 153, 76], noise_amount=25)

def create_dirt_texture():
    """Create dirt block texture"""
    return generate_noise_texture([139, 90, 43], noise_amount=20)

def create_stone_texture():
    """Create stone block texture with cracks"""
    base = generate_noise_texture([128, 128, 128], noise_amount=15)
    # Add some darker spots for cracks
    arr = np.frombuffer(base, dtype=np.uint8).reshape(64, 64, 3)
    for _ in range(50):
        x, y = random.randint(0, 63), random.randint(0, 63)
        size = random.randint(2, 5)
        for dy in range(-size, size+1):
            for dx in range(-size, size+1):
                if 0 <= y+dy < 64 and 0 <= x+dx < 64:
                    if random.random() < 0.3:
                        arr[y+dy, x+dx] = [max(0, arr[y+dy, x+dx][i] - 30) for i in range(3)]
    return arr.flatten()

def create_wood_texture():
    """Create wood log texture with grain"""
    texture_data = np.zeros((64, 64, 3), dtype=np.uint8)
    base_color = [101, 67, 33]
    
    for y in range(64):
        for x in range(64):
            # Wood grain pattern
            grain = int(math.sin(x * 0.3) * 15 + math.cos(y * 0.1) * 10)
            noise = random.randint(-10, 10)
            r = max(0, min(255, base_color[0] + grain + noise))
            g = max(0, min(255, base_color[1] + grain + noise))
            b = max(0, min(255, base_color[2] + grain + noise))
            texture_data[y, x] = [r, g, b]
    
    return texture_data.flatten()

def create_leaves_texture():
    """Create leaves texture with varied greens"""
    texture_data = np.zeros((64, 64, 3), dtype=np.uint8)
    
    for y in range(64):
        for x in range(64):
            # Varied green colors
            base_g = random.randint(100, 180)
            base_r = random.randint(30, 60)
            base_b = random.randint(30, 60)
            
            # Add some yellow/brown spots
            if random.random() < 0.1:
                base_r += 30
                base_g -= 20
            
            texture_data[y, x] = [base_r, base_g, base_b]
    
    return texture_data.flatten()

def create_sand_texture():
    """Create sand texture"""
    return generate_noise_texture([237, 220, 163], noise_amount=15)

def create_water_texture():
    """Create water texture with wave effect"""
    texture_data = np.zeros((64, 64, 3), dtype=np.uint8)
    
    for y in range(64):
        for x in range(64):
            # Wave animation base (static for now)
            wave = int(math.sin(x * 0.15 + y * 0.1) * 20)
            base = [65, 105, 225]
            r = max(0, min(255, base[0] + wave))
            g = max(0, min(255, base[1] + wave))
            b = max(0, min(255, base[2] + wave))
            texture_data[y, x] = [r, g, b]
    
    return texture_data.flatten()

def create_snow_texture():
    """Create snow texture"""
    return generate_noise_texture([255, 255, 255], noise_amount=8)

# Generate all textures
textures = {}
texture_ids = {}

def load_textures():
    """Load all block textures into OpenGL"""
    global texture_ids
    
    texture_data_map = {
        BLOCK_GRASS: create_grass_texture(),
        BLOCK_DIRT: create_dirt_texture(),
        BLOCK_STONE: create_stone_texture(),
        BLOCK_WOOD: create_wood_texture(),
        BLOCK_LEAVES: create_leaves_texture(),
        BLOCK_SAND: create_sand_texture(),
        BLOCK_WATER: create_water_texture(),
        BLOCK_SNOW: create_snow_texture()
    }
    
    texture_ids = {}
    
    for block_id, data in texture_data_map.items():
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 64, 64, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        texture_ids[block_id] = texture_id
    
    # Create grass side texture (dirt with grass top)
    grass_side_data = create_dirt_texture()
    arr = np.frombuffer(grass_side_data, dtype=np.uint8).reshape(64, 64, 3)
    # Add grass on top
    for y in range(20):
        for x in range(64):
            if random.random() < 0.7 or y < 5:
                arr[y, x] = [max(0, arr[y, x][i] * 0.3 + [76, 153, 76][i] * 0.7) for i in range(3)]
    
    grass_side_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, grass_side_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 64, 64, 0, GL_RGB, GL_UNSIGNED_BYTE, arr.flatten())
    texture_ids['grass_side'] = grass_side_id

# World generation
class World:
    def __init__(self):
        self.blocks = {}
        self.generate_world()
    
    def generate_world(self):
        """Generate terrain with hills, trees, and water"""
        print("Generating world...")
        
        for x in range(WORLD_SIZE):
            for z in range(WORLD_SIZE):
                # Simple height map using sine waves
                height = int(8 + 
                           math.sin(x * 0.15) * 4 + 
                           math.cos(z * 0.15) * 4 +
                           math.sin(x * 0.05 + z * 0.05) * 6)
                height = max(1, min(WORLD_HEIGHT - 5, height))
                
                for y in range(height + 1):
                    if y == height:
                        if height < 6:
                            block = BLOCK_SAND
                        elif height > 18:
                            block = BLOCK_SNOW
                        else:
                            block = BLOCK_GRASS
                    elif y > height - 4:
                        block = BLOCK_DIRT
                    else:
                        block = BLOCK_STONE
                    
                    self.blocks[(x, y, z)] = block
        
        # Generate trees
        for _ in range(40):
            tx = random.randint(2, WORLD_SIZE - 3)
            tz = random.randint(2, WORLD_SIZE - 3)
            
            # Find ground level
            for ty in range(WORLD_HEIGHT - 1, -1, -1):
                if (tx, ty, tz) in self.blocks and self.blocks[(tx, ty, tz)] == BLOCK_GRASS:
                    self.create_tree(tx, ty + 1, tz)
                    break
        
        # Add water level
        water_level = 5
        for x in range(WORLD_SIZE):
            for z in range(WORLD_SIZE):
                for y in range(water_level):
                    if (x, y, z) not in self.blocks:
                        self.blocks[(x, y, z)] = BLOCK_WATER
        
        print(f"World generated with {len(self.blocks)} blocks")
    
    def create_tree(self, x, y, z):
        """Create a simple tree"""
        # Trunk
        for i in range(5):
            self.blocks[(x, y + i, z)] = BLOCK_WOOD
        
        # Leaves
        for lx in range(x - 2, x + 3):
            for lz in range(z - 2, z + 3):
                for ly in range(y + 3, y + 6):
                    if abs(lx - x) + abs(lz - z) + abs(ly - (y + 4)) < 5:
                        if (lx, ly, lz) not in self.blocks or self.blocks[(lx, ly, lz)] == BLOCK_AIR:
                            self.blocks[(lx, ly, lz)] = BLOCK_LEAVES
    
    def get_block(self, x, y, z):
        return self.blocks.get((x, y, z), BLOCK_AIR)
    
    def set_block(self, x, y, z, block_id):
        if block_id == BLOCK_AIR:
            if (x, y, z) in self.blocks:
                del self.blocks[(x, y, z)]
        else:
            self.blocks[(x, y, z)] = block_id

# Player class
class Player:
    def __init__(self, world):
        self.world = world
        self.x = WORLD_SIZE / 2
        self.y = 20
        self.z = WORLD_SIZE / 2
        self.rot_x = 0
        self.rot_y = 0
        self.velocity = [0, 0, 0]
        self.speed = 0.15
        self.fly_speed = 0.2
        self.selected_block = BLOCK_GRASS
        self.on_ground = False
    
    def update(self, keys):
        """Update player position based on input"""
        # Rotation
        mouse_rel = pygame.mouse.get_rel()
        self.rot_y -= mouse_rel[0] * 0.15
        self.rot_x -= mouse_rel[1] * 0.15
        self.rot_x = max(-90, min(90, self.rot_x))
        
        # Movement
        move_x = 0
        move_z = 0
        move_y = 0
        
        rad_y = math.radians(self.rot_y)
        
        if keys[K_w]:
            move_x -= math.sin(rad_y) * self.speed
            move_z -= math.cos(rad_y) * self.speed
        if keys[K_s]:
            move_x += math.sin(rad_y) * self.speed
            move_z += math.cos(rad_y) * self.speed
        if keys[K_a]:
            move_x -= math.cos(rad_y) * self.speed
            move_z += math.sin(rad_y) * self.speed
        if keys[K_d]:
            move_x += math.cos(rad_y) * self.speed
            move_z -= math.sin(rad_y) * self.speed
        
        # Flying
        if keys[K_SPACE]:
            move_y += self.fly_speed
        if keys[K_LSHIFT]:
            move_y -= self.fly_speed
        
        # Apply movement with collision detection
        new_x = self.x + move_x
        new_z = self.z + move_z
        new_y = self.y + move_y
        
        # Simple collision
        if not self.check_collision(new_x, self.y, self.z):
            self.x = new_x
        if not self.check_collision(self.x, self.y, new_z):
            self.z = new_z
        if not self.check_collision(self.x, new_y, self.z):
            self.y = new_y
        else:
            self.on_ground = move_y <= 0
    
    def check_collision(self, x, y, z):
        """Check if position collides with blocks"""
        player_width = 0.3
        player_height = 1.7
        
        for dx in [-player_width, player_width]:
            for dz in [-player_width, player_width]:
                for dy in [0, player_height - 0.1]:
                    bx, by, bz = int(x + dx), int(y + dy), int(z + dz)
                    if self.world.get_block(bx, by, bz) != BLOCK_AIR:
                        return True
        return False
    
    def apply_physics(self):
        """Apply gravity if not flying"""
        if not (pygame.key.get_pressed()[K_SPACE] or pygame.key.get_pressed()[K_LSHIFT]):
            if not self.on_ground:
                self.y -= 0.01
                if self.check_collision(self.x, self.y, self.z):
                    self.y += 0.01
                    self.on_ground = True
    
    def raycast(self, max_dist=6):
        """Raycast to find block being looked at"""
        dx = -math.sin(math.radians(self.rot_y)) * math.cos(math.radians(self.rot_x))
        dy = math.sin(math.radians(self.rot_x))
        dz = -math.cos(math.radians(self.rot_y)) * math.cos(math.radians(self.rot_x))
        
        x, y, z = self.x, self.y + 1.5, self.z
        
        for i in range(int(max_dist * 20)):
            x += dx * 0.05
            y += dy * 0.05
            z += dz * 0.05
            
            bx, by, bz = int(x), int(y), int(z)
            block = self.world.get_block(bx, by, bz)
            
            if block != BLOCK_AIR:
                # Return block position and previous position for placement
                prev_x, prev_y, prev_z = int(x - dx * 0.05), int(y - dy * 0.05), int(z - dz * 0.05)
                return (bx, by, bz), (prev_x, prev_y, prev_z)
        
        return None, None

# Rendering
def draw_block(x, y, z, block_id):
    """Draw a single block with proper textures"""
    if block_id == BLOCK_AIR:
        return
    
    texture_id = texture_ids.get(block_id, texture_ids.get(BLOCK_STONE))
    
    # Special handling for grass block (different texture for top)
    if block_id == BLOCK_GRASS:
        grass_top = texture_ids[BLOCK_GRASS]
        grass_side = texture_ids['grass_side']
        grass_bottom = texture_ids[BLOCK_DIRT]
    else:
        grass_top = grass_side = grass_bottom = texture_id
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    vertices = [
        (x, y, z), (x + 1, y, z), (x + 1, y + 1, z), (x, y + 1, z),  # Front
        (x, y, z + 1), (x, y + 1, z + 1), (x + 1, y + 1, z + 1), (x + 1, y, z + 1),  # Back
        (x, y, z), (x, y + 1, z), (x, y + 1, z + 1), (x, y, z + 1),  # Left
        (x + 1, y, z), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x + 1, y + 1, z),  # Right
        (x, y + 1, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x, y + 1, z + 1),  # Top
        (x, y, z), (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y, z)   # Bottom
    ]
    
    # Texture coordinates
    texcoords = [
        (0, 0), (1, 0), (1, 1), (0, 1)
    ]
    
    # Face textures for grass
    face_textures = [grass_side, grass_side, grass_side, grass_side, grass_top, grass_bottom]
    
    glBegin(GL_QUADS)
    for i in range(6):
        tex = face_textures[i] if block_id == BLOCK_GRASS else texture_id
        glBindTexture(GL_TEXTURE_2D, tex)
        
        base = i * 4
        for j in range(4):
            glTexCoord2f(texcoords[j][0], texcoords[j][1])
            glVertex3f(vertices[base + j][0], vertices[base + j][1], vertices[base + j][2])
    glEnd()

def render_world(world, player):
    """Render visible blocks"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Apply player rotation and position
    glRotatef(player.rot_x, 1, 0, 0)
    glRotatef(player.rot_y, 0, 1, 0)
    glTranslatef(-player.x, -player.y - 1.5, -player.z)
    
    # Enable texturing
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Render blocks (optimization: only render visible blocks)
    render_range = 32
    px, py, pz = int(player.x), int(player.y), int(player.z)
    
    for (x, y, z), block_id in world.blocks.items():
        if block_id == BLOCK_AIR:
            continue
        
        # Distance culling
        if abs(x - px) > render_range or abs(y - py) > render_range or abs(z - pz) > render_range:
            continue
        
        # Simple occlusion culling
        if block_id != BLOCK_WATER:  # Always render water
            neighbors = [
                (x+1, y, z), (x-1, y, z),
                (x, y+1, z), (x, y-1, z),
                (x, y, z+1), (x, y, z-1)
            ]
            visible = False
            for nx, ny, nz in neighbors:
                if world.get_block(nx, ny, nz) == BLOCK_AIR:
                    visible = True
                    break
            if not visible:
                continue
        
        draw_block(x, y, z, block_id)
    
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)

# Main game loop
def main():
    clock = pygame.time.Clock()
    world = World()
    player = Player(world)
    load_textures()
    
    running = True
    mouse_captured = False
    
    font = pygame.font.Font(None, 36)
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if mouse_captured:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                        mouse_captured = False
                    else:
                        running = False
                elif event.key == K_1:
                    player.selected_block = BLOCK_GRASS
                elif event.key == K_2:
                    player.selected_block = BLOCK_DIRT
                elif event.key == K_3:
                    player.selected_block = BLOCK_STONE
                elif event.key == K_4:
                    player.selected_block = BLOCK_WOOD
                elif event.key == K_5:
                    player.selected_block = BLOCK_LEAVES
                elif event.key == K_6:
                    player.selected_block = BLOCK_SAND
                elif event.key == K_7:
                    player.selected_block = BLOCK_SNOW
            elif event.type == MOUSEBUTTONDOWN:
                if not mouse_captured:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    mouse_captured = True
                else:
                    # Block interaction
                    hit_pos, place_pos = player.raycast()
                    
                    if event.button == 1:  # Left click - remove block
                        if hit_pos:
                            world.set_block(*hit_pos, BLOCK_AIR)
                    elif event.button == 3:  # Right click - place block
                        if place_pos:
                            px, py, pz = place_pos
                            # Don't place block inside player
                            if not player.check_collision(px + 0.5, py + 0.5, pz + 0.5):
                                world.set_block(px, py, pz, player.selected_block)
        
        if mouse_captured:
            keys = pygame.key.get_pressed()
            player.update(keys)
            player.apply_physics()
        
        # Render
        render_world(world, player)
        
        # Draw UI
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WIDTH, HEIGHT, 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        
        # Crosshair
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(WIDTH/2 - 10, HEIGHT/2)
        glVertex2f(WIDTH/2 + 10, HEIGHT/2)
        glVertex2f(WIDTH/2, HEIGHT/2 - 10)
        glVertex2f(WIDTH/2, HEIGHT/2 + 10)
        glEnd()
        
        # Selected block indicator
        block_name = block_names.get(player.selected_block, "Unknown")
        text_surface = font.render(f"Block: {block_name} (1-7 to select)", True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGB", True)
        
        # Simple text rendering fallback
        glColor3f(1, 1, 1)
        glRasterPos2f(10, 30)
        
        glEnable(GL_DEPTH_TEST)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
