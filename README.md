# 🏓 Pong Game

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0.0%2B-green.svg)

A modern implementation of the classic Pong arcade game built with Pygame, featuring customizable visuals, power-ups, and various game modes.

![Pong Game Screenshot](https://via.placeholder.com/800x400?text=Pong+Game+Screenshot)

## ✨ Features

- **Game Modes**
  - Single-player vs AI with four difficulty levels (Easy, Medium, Hard, Impossible)
  - Two-player local multiplayer
  
- **Customization**
  - Multiple paddle colors (White, Red, Blue, Green, Yellow, Purple, Orange, Cyan)
  - Selectable background themes
  
- **Advanced Gameplay**
  - Dynamic power-up system (Speed boost, Size increase, Ball slow-down)
  - Realistic ball physics with paddle spin effects
  - Progressive difficulty with ball speed increasing during rallies
  
- **User Experience**
  - Clean menu interface
  - In-game pause functionality
  - Game state tracking (menus, paused, gameplay, winner announcement)

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pong-game.git
cd pong-game

# Install required dependencies
pip install pygame

# Run the game
python pong.py
```

## 📁 Project Structure

Make sure to create the following structure for the game to work properly:

```
pong-game/
├── pong.py                 # Main game file
├── README.md               # This file
├── images/                 # Background and power-up images folder
│   ├── Red&Blue.png/jpg    # Background option
│   ├── Black&White.png/jpg # Background option
│   ├── Pink&Purple.png/jpg # Background option
│   ├── OnePiece.png/jpg    # Background option
│   ├── Speed_Up.jpg        # Power-up image
│   ├── Size_UP.png         # Power-up image
│   └── slow_down.png       # Power-up image
├── paddle.wav              # Sound effect (optional)
├── wall.wav                # Sound effect (optional)
└── score.wav               # Sound effect (optional)
```

## 🎮 How to Play

### Controls

| Action | Player 1 (Left) | Player 2 (Right) |
|--------|----------------|------------------|
| Move Up | W | ↑ (Up Arrow) |
| Move Down | S | ↓ (Down Arrow) |
| Cheat (Add Score) | Z | N/A |

### Game Controls
- **P**: Pause/Unpause
- **ESC**: Return to menu (when paused)
- **Space**: Restart game (after a win)
- **Mouse**: Navigate menus

### Gameplay Rules
- First player to reach 10 points wins
- The ball speeds up with each hit
- Hit different parts of the paddle to change ball trajectory
- Collect power-ups for temporary advantages

## 🔧 Configuration

The game has several configurable constants near the top of the `pong.py` file:

```python
# Game dimensions
WIDTH, HEIGHT = 1000, 800

# Difficulty settings
MAX_SCORE = 10  # Points needed to win

# AI settings
AI_EASY = 4      # Higher number = slower reactions
AI_MEDIUM = 2    # Default setting
AI_HARD = 1      # Very responsive
AI_IMPOSSIBLE = 0 # Perfect tracking
```

## 🌟 Power-ups

| Power-up | Effect | Duration |
|----------|--------|----------|
| Speed Boost | Increases paddle movement speed | 10 seconds |
| Size Increase | Makes paddle larger | 10 seconds |
| Ball Slow | Reduces ball speed | 10 seconds |

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. Add new features (more power-ups, new game modes)
2. Fix bugs
3. Improve the code
4. Enhance documentation

Please feel free to submit a pull request or open an issue.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Pygame](https://www.pygame.org/) - The game library
- Atari's original Pong game for inspiration
