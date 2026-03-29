# Minecraft Clone - 3D Voxel Game

A basic Minecraft-like game with 3D graphics, block placement/removal, and procedural textures.

## Features

- **3D Voxel World**: Explore a procedurally generated 3D world
- **Block Building**: Place and remove blocks to build structures
- **Multiple Block Types**: Grass, Dirt, Stone, Wood, and Leaves
- **Procedural Textures**: Automatically generated textures for each block type
- **First-Person Camera**: Smooth camera controls with mouse look
- **Tree Generation**: Random trees spawn in the world

## Installation

### Windows

1. Make sure you have Python 3.8+ installed from [python.org](https://www.python.org/)
2. Double-click `Minecraft.bat` to install dependencies and launch the game

OR manually:
```bash
pip install pygame PyOpenGL numpy
python src/minecraft.py
```

### Linux/Mac

1. Make sure you have Python 3.8+ installed
2. Run the launcher script:
```bash
chmod +x Minecraft.sh
./Minecraft.sh
```

OR manually:
```bash
pip3 install pygame PyOpenGL numpy
python3 src/minecraft.py
```

## Controls

| Key/Action | Function |
|------------|----------|
| **W** | Move forward |
| **A** | Move left |
| **S** | Move backward |
| **D** | Move right |
| **Mouse** | Look around |
| **Left Click** | Remove block |
| **Right Click** | Place block |
| **1** | Select Grass block |
| **2** | Select Dirt block |
| **3** | Select Stone block |
| **4** | Select Wood block |
| **5** | Select Leaves block |
| **Space** | Move up (fly) |
| **Shift** | Move down (fly) |
| **ESC** | Release mouse cursor |

## Requirements

- Python 3.8 or higher
- pygame
- PyOpenGL
- numpy
- OpenGL-capable graphics card

## Folder Structure

```
GAME/
├── Minecraft.bat      # Windows launcher (installs libs + runs game)
├── Minecraft.sh       # Linux/Mac launcher
├── README.md          # This file
├── src/
│   └── minecraft.py   # Main game source code
├── assets/
│   └── textures/      # (Textures are generated procedurally)
└── lib/               # (Dependencies installed here by pip)
```

## How to Play

1. Launch the game using the appropriate launcher for your system
2. Click to lock your mouse cursor and enable camera control
3. Use WASD to move around the world
4. Press 1-5 to select different block types
5. Left-click to remove blocks
6. Right-click to place blocks
7. Press ESC to release the mouse cursor when needed

## Technical Details

- **World Size**: 32x16x32 blocks
- **Rendering**: OpenGL with immediate mode rendering
- **Texture Generation**: Procedural noise-based textures
- **Mesh Generation**: Only visible faces are rendered for performance
- **Camera**: First-person with 6DOF movement (fly mode)

## Troubleshooting

### Game won't start
- Make sure Python is installed and in your PATH
- Install dependencies manually: `pip install pygame PyOpenGL numpy`

### Black screen or no blocks visible
- Make sure your graphics card supports OpenGL
- Try updating your graphics drivers

### Controls not working
- Click in the game window to lock the mouse cursor
- Press ESC to release the cursor if needed

## License

This is a fan-made Minecraft clone created for educational purposes.
Minecraft is a trademark of Mojang Synergies AB.
