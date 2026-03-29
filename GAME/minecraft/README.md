# 🎮 Minecraft Clone

A 3D voxel-based Minecraft clone built with Python, Pygame, and OpenGL.

## 📁 Folder Structure
```
minecraft/
├── Minecraft.bat      # Windows launcher (installs libs + runs game)
├── Minecraft.sh       # Linux/Mac launcher
├── README.md          # This file
├── src/
│   └── minecraft.py   # Main game source code
├── assets/
│   └── textures/      # Texture folder (textures generated procedurally)
└── lib/               # Dependencies folder
```

## 🚀 How to Run

### Windows
1. Double-click `Minecraft.bat`
2. The launcher will automatically install required libraries
3. Game will start automatically

### Linux/Mac
```bash
chmod +x Minecraft.sh
./Minecraft.sh
```

## 🎯 Controls

| Key | Action |
|-----|--------|
| **W** | Move Forward |
| **A** | Move Left |
| **S** | Move Backward |
| **D** | Move Right |
| **Mouse** | Look Around (click to lock cursor) |
| **Left Click** | Remove Block |
| **Right Click** | Place Block |
| **1** | Select Grass Block |
| **2** | Select Dirt Block |
| **3** | Select Stone Block |
| **4** | Select Wood Block |
| **5** | Select Leaves Block |
| **6** | Select Sand Block |
| **7** | Select Snow Block |
| **Space** | Fly Up |
| **Shift** | Fly Down |
| **ESC** | Release Mouse / Exit |

## 🎨 Features

- **Procedural 3D World**: 48x48x32 block terrain with hills, valleys, and water
- **8 Block Types**: Grass, Dirt, Stone, Wood, Leaves, Sand, Water, Snow
- **High-Quality Textures**: Procedurally generated noisy textures for each block type
- **Tree Generation**: Random trees spawn throughout the world
- **First-Person Camera**: Smooth mouse look and WASD movement
- **Block Building**: Left-click to remove, right-click to place blocks
- **Fly Mode**: Space to go up, Shift to go down
- **Collision Detection**: Player collides with blocks
- **Optimized Rendering**: Distance culling and occlusion culling

## 🛠️ Requirements

The launcher will automatically install:
- Python 3.x
- pygame
- PyOpenGL
- numpy

## 🎮 Gameplay Tips

1. **First Launch**: Click the screen to capture the mouse
2. **Building**: Select a block type (1-7), right-click to place
3. **Mining**: Left-click to remove blocks
4. **Exploration**: Use WASD to move, mouse to look around
5. **Flying**: Hold Space to fly up, Shift to fly down
6. **Exit**: Press ESC to release mouse, press again to exit

## 🌍 World Generation

The world features:
- Rolling hills and valleys
- Beach areas with sand near water
- Snow-capped mountains at high elevations
- Lakes and oceans at sea level
- Randomly generated trees

## ⚠️ Troubleshooting

**Game won't start?**
- Make sure you have OpenGL drivers installed
- Update your graphics card drivers
- Check that Python is installed correctly

**Low FPS?**
- The render distance can be adjusted in the source code
- Reduce world size for better performance

**Mouse not working?**
- Click the game window to capture the mouse
- Press ESC to release if needed

Enjoy building your Minecraft world! 🎉
