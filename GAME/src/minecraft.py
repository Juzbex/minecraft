"""
Minecraft Clone - 3D Voxel Game
A basic Minecraft-like game with 3D graphics, block placement/removal, and procedural textures.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import os

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Minecraft Clone - 3D Voxel World")

# OpenGL setup
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

# Camera settings
camera_pos = [0, 2, 5]
camera_rot = [0, 0]
mouse_sensitivity = 0.1
move_speed = 0.1

# Block types
BLOCK_AIR = 0
BLOCK_GRASS = 1
BLOCK_DIRT = 2
BLOCK_STONE = 3
BLOCK_WOOD = 4
BLOCK_LEAVES = 5

# World settings
WORLD_SIZE = 32
WORLD_HEIGHT = 16

# Generate procedural textures
def create_texture(width, height, color_variations):
    """Create a procedural texture with noise"""
    texture_data = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            # Add noise
            noise = random.randint(-30, 30)
            base_color = random.choice(color_variations)
            r = max(0, min(255, base_color[0] + noise))
            g = max(0, min(255, base_color[1] + noise))
            b = max(0, min(255, base_color[2] + noise))
            texture_data[y, x] = [r, g, b]
    return texture_data

# Create block textures
textures = {
    BLOCK_GRASS: create_texture(16, 16, [[76, 201, 24], [66, 181, 14], [86, 221, 34]]),
    BLOCK_DIRT: create_texture(16, 16, [[139, 69, 19], [119, 49, 9], [159, 89, 29]]),
    BLOCK_STONE: create_texture(16, 16, [[128, 128, 128], [108, 108, 108], [148, 148, 148]]),
    BLOCK_WOOD: create_texture(16, 16, [[139, 90, 43], [119, 70, 23], [159, 110, 63]]),
    BLOCK_LEAVES: create_texture(16, 16, [[34, 139, 34], [24, 119, 24], [44, 159, 44]])
}

# Generate texture IDs
texture_ids = {}
for block_type, texture_data in textures.items():
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 16, 16, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    texture_ids[block_type] = texture_id

# World data structure
world = {}

def get_block(x, y, z):
    """Get block at position"""
    if 0 <= x < WORLD_SIZE and 0 <= y < WORLD_HEIGHT and 0 <= z < WORLD_SIZE:
        return world.get((x, y, z), BLOCK_AIR)
    return BLOCK_AIR

def set_block(x, y, z, block_type):
    """Set block at position"""
    if 0 <= x < WORLD_SIZE and 0 <= y < WORLD_HEIGHT and 0 <= z < WORLD_SIZE:
        if block_type == BLOCK_AIR:
            world.pop((x, y, z), None)
        else:
            world[(x, y, z)] = block_type

def generate_world():
    """Generate a simple world"""
    for x in range(WORLD_SIZE):
        for z in range(WORLD_SIZE):
            # Simple terrain generation
            height = int(4 + 2 * np.sin(x / 8) * np.cos(z / 8))
            
            for y in range(height + 1):
                if y == height:
                    set_block(x, y, z, BLOCK_GRASS)
                elif y > height - 3:
                    set_block(x, y, z, BLOCK_DIRT)
                else:
                    set_block(x, y, z, BLOCK_STONE)
            
            # Add some trees
            if random.random() < 0.02 and x > 2 and x < WORLD_SIZE - 2 and z > 2 and z < WORLD_SIZE - 2:
                tree_height = random.randint(3, 5)
                for ty in range(tree_height):
                    set_block(x, height + 1 + ty, z, BLOCK_WOOD)
                
                # Leaves
                for lx in range(-2, 3):
                    for lz in range(-2, 3):
                        for ly in range(tree_height - 1, tree_height + 1):
                            if abs(lx) + abs(lz) < 3:
                                set_block(x + lx, height + 1 + ly, z + lz, BLOCK_LEAVES)

# Mesh generation
def generate_mesh():
    """Generate vertex data for visible blocks"""
    vertices = []
    normals = []
    tex_coords = []
    indices = []
    
    vertex_count = 0
    
    for (x, y, z), block_type in world.items():
        if block_type == BLOCK_AIR:
            continue
            
        # Check which faces are visible
        faces = []
        
        # Top face (y+1)
        if get_block(x, y + 1, z) == BLOCK_AIR:
            faces.append([
                (x, y + 1, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)
            ])
            normals.extend([(0, 1, 0)] * 4)
            tex_coords.extend([(0, 0), (1, 0), (1, 1), (0, 1)])
        
        # Bottom face (y-1)
        if get_block(x, y - 1, z) == BLOCK_AIR:
            faces.append([
                (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y, z), (x, y, z)
            ])
            normals.extend([(0, -1, 0)] * 4)
            tex_coords.extend([(0, 0), (1, 0), (1, 1), (0, 1)])
        
        # Front face (z+1)
        if get_block(x, y, z + 1) == BLOCK_AIR:
            faces.append([
                (x, y, z + 1), (x, y + 1, z + 1), (x + 1, y + 1, z + 1), (x + 1, y, z + 1)
            ])
            normals.extend([(0, 0, 1)] * 4)
            tex_coords.extend([(0, 0), (1, 0), (1, 1), (0, 1)])
        
        # Back face (z-1)
        if get_block(x, y, z - 1) == BLOCK_AIR:
            faces.append([
                (x + 1, y, z), (x + 1, y + 1, z), (x, y + 1, z), (x, y, z)
            ])
            normals.extend([(0, 0, -1)] * 4)
            tex_coords.extend([(0, 0), (1, 0), (1, 1), (0, 1)])
        
        # Right face (x+1)
        if get_block(x + 1, y, z) == BLOCK_AIR:
            faces.append([
                (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x + 1, y + 1, z), (x + 1, y, z)
            ])
            normals.extend([(1, 0, 0)] * 4)
            tex_coords.extend([(0, 0), (1, 0), (1, 1), (0, 1)])
        
        # Left face (x-1)
        if get_block(x - 1, y, z) == BLOCK_AIR:
            faces.append([
                (x, y, z), (x, y + 1, z), (x, y + 1, z + 1), (x, y, z + 1)
            ])
            normals.extend([(-1, 0, 0)] * 4)
            tex_coords.extend([(0, 0), (1, 0), (1, 1), (0, 1)])
        
        for face in faces:
            for vertex in face:
                vertices.append(vertex)
                indices.append(vertex_count)
                vertex_count += 1
    
    return vertices, normals, tex_coords, indices

# Input handling
keys_pressed = set()
mouse_locked = False

def handle_input():
    """Handle keyboard input"""
    global camera_pos, camera_rot
    
    if K_w in keys_pressed:
        # Move forward
        dx = -np.sin(np.radians(camera_rot[1])) * move_speed
        dz = -np.cos(np.radians(camera_rot[1])) * move_speed
        camera_pos[0] += dx
        camera_pos[2] += dz
    
    if K_s in keys_pressed:
        # Move backward
        dx = np.sin(np.radians(camera_rot[1])) * move_speed
        dz = np.cos(np.radians(camera_rot[1])) * move_speed
        camera_pos[0] += dx
        camera_pos[2] += dz
    
    if K_a in keys_pressed:
        # Strafe left
        dx = -np.cos(np.radians(camera_rot[1])) * move_speed
        dz = np.sin(np.radians(camera_rot[1])) * move_speed
        camera_pos[0] += dx
        camera_pos[2] += dz
    
    if K_d in keys_pressed:
        # Strafe right
        dx = np.cos(np.radians(camera_rot[1])) * move_speed
        dz = -np.sin(np.radians(camera_rot[1])) * move_speed
        camera_pos[0] += dx
        camera_pos[2] += dz
    
    if K_SPACE in keys_pressed:
        # Move up
        camera_pos[1] += move_speed
    
    if K_LSHIFT in keys_pressed:
        # Move down
        camera_pos[1] -= move_speed

# Raycasting for block selection
def raycast(max_distance=5):
    """Cast a ray from the camera to find the targeted block"""
    direction = np.array([
        -np.sin(np.radians(camera_rot[1])) * np.cos(np.radians(camera_rot[0])),
        np.sin(np.radians(camera_rot[0])),
        -np.cos(np.radians(camera_rot[1])) * np.cos(np.radians(camera_rot[0]))
    ])
    direction /= np.linalg.norm(direction)
    
    step = 0.1
    for distance in np.arange(0, max_distance, step):
        pos = np.array(camera_pos) + direction * distance
        x, y, z = int(pos[0]), int(pos[1]), int(pos[2])
        
        if get_block(x, y, z) != BLOCK_AIR:
            # Return block position and previous position (for placement)
            prev_pos = np.array(camera_pos) + direction * (distance - step)
            return (x, y, z), (int(prev_pos[0]), int(prev_pos[1]), int(prev_pos[2]))
    
    return None, None

# Main game loop
def main():
    global mouse_locked
    
    generate_world()
    
    clock = pygame.time.Clock()
    selected_block = BLOCK_GRASS
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            if event.type == KEYDOWN:
                keys_pressed.add(event.key)
                
                # Block selection
                if event.key == K_1:
                    selected_block = BLOCK_GRASS
                elif event.key == K_2:
                    selected_block = BLOCK_DIRT
                elif event.key == K_3:
                    selected_block = BLOCK_STONE
                elif event.key == K_4:
                    selected_block = BLOCK_WOOD
                elif event.key == K_5:
                    selected_block = BLOCK_LEAVES
                
                # Toggle mouse lock
                if event.key == K_ESCAPE:
                    if mouse_locked:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                        mouse_locked = False
                    else:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                        mouse_locked = True
            
            if event.type == KEYUP:
                keys_pressed.discard(event.key)
            
            if event.type == MOUSEBUTTONDOWN and mouse_locked:
                if event.button == 1:  # Left click - remove block
                    block_pos, _ = raycast()
                    if block_pos:
                        set_block(*block_pos, BLOCK_AIR)
                
                if event.button == 3:  # Right click - place block
                    _, place_pos = raycast()
                    if place_pos:
                        # Don't place block inside player
                        player_box = [
                            camera_pos[0] - 0.3, camera_pos[1] - 1.5, camera_pos[2] - 0.3,
                            camera_pos[0] + 0.3, camera_pos[1] + 0.5, camera_pos[2] + 0.3
                        ]
                        block_box = [
                            place_pos[0], place_pos[1], place_pos[2],
                            place_pos[0] + 1, place_pos[1] + 1, place_pos[2] + 1
                        ]
                        
                        # Simple collision check
                        if not (player_box[0] < block_box[3] and player_box[3] > block_box[0] and
                                player_box[1] < block_box[4] and player_box[4] > block_box[1] and
                                player_box[2] < block_box[5] and player_box[5] > block_box[2]):
                            set_block(*place_pos, selected_block)
        
        # Handle mouse movement for camera rotation
        if mouse_locked:
            mouse_rel = pygame.mouse.get_rel()
            camera_rot[0] -= mouse_rel[1] * mouse_sensitivity
            camera_rot[1] -= mouse_rel[0] * mouse_sensitivity
            
            # Limit vertical rotation
            camera_rot[0] = max(-90, min(90, camera_rot[0]))
        
        # Handle input
        handle_input()
        
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.5, 0.7, 1.0, 1.0)  # Sky blue
        
        # Setup camera
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, display[0] / display[1], 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  camera_pos[0] - np.sin(np.radians(camera_rot[1])) * np.cos(np.radians(camera_rot[0])),
                  camera_pos[1] + np.sin(np.radians(camera_rot[0])),
                  camera_pos[2] - np.cos(np.radians(camera_rot[1])) * np.cos(np.radians(camera_rot[0])),
                  0, 1, 0)
        
        # Enable texturing
        glEnable(GL_TEXTURE_2D)
        
        # Generate and render mesh
        vertices, normals, tex_coords, indices = generate_mesh()
        
        if vertices:
            glBegin(GL_QUADS)
            for i, vertex in enumerate(vertices):
                glTexCoord2fv(tex_coords[i])
                glNormal3fv(normals[i])
                glVertex3fv(vertex)
            glEnd()
        
        # Render block selection highlight
        if mouse_locked:
            block_pos, _ = raycast()
            if block_pos:
                glColor4f(1.0, 1.0, 1.0, 0.3)
                glDisable(GL_TEXTURE_2D)
                glBegin(GL_LINE_LOOP)
                for vertex in [(block_pos[0], block_pos[1], block_pos[2]),
                              (block_pos[0] + 1, block_pos[1], block_pos[2]),
                              (block_pos[0] + 1, block_pos[1] + 1, block_pos[2]),
                              (block_pos[0], block_pos[1] + 1, block_pos[2])]:
                    glVertex3fv(vertex)
                glEnd()
                glEnable(GL_TEXTURE_2D)
                glColor3f(1.0, 1.0, 1.0)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    print("=" * 50)
    print("MINECRAFT CLONE - 3D VOXEL GAME")
    print("=" * 50)
    print("\nCONTROLS:")
    print("  WASD - Move")
    print("  Mouse - Look around")
    print("  Left Click - Remove block")
    print("  Right Click - Place block")
    print("  1-5 - Select block type")
    print("     1: Grass, 2: Dirt, 3: Stone, 4: Wood, 5: Leaves")
    print("  Space - Move up")
    print("  Shift - Move down")
    print("  ESC - Release mouse cursor")
    print("\nGenerating world...")
    main()
