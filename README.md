# Tetris-AI

We built a bot to play online tetris _better than we ever could_, and this bot won a few dollars.

The bot works with screen information and emulates key presses,
thus, it can be adapted to _any_ tetris game.

After reading the screen, it uses an algorithm to determine the best piece placement and executes it.

The algorithm has various modes, for example, focusing on getting a _tetris_,
which is clearing 4 lines with a single piece.

### Gameplay demonstration
Bot playing in mode 1

![demo mode 1](https://media.giphy.com/media/kg1Ng8ZXTUQ2efOpUk/giphy.gif)

Bot playing in mode 2, in another game

![demo mode 2](https://user-images.githubusercontent.com/27450370/147476623-7acc036e-7195-409b-a2ec-d24e489aadf2.gif)


## Usage guide

### How to run
1. Take a screenshot of your Tetris game
2. Go to `config.py` and define a `DisplayConsts` instance
3. Set 'display consts' in `CONFIG` to your instance
4. If necessary, define a `colors` array with piece colors for recognition of the next piece
5. Set other config parameters
6. Run `src/main.py`
7. Switch to the Tetris window

### Runtime tuning
You can control how the bot plays while the game is going.

This is only checked when a new piece appears, so you need to hold the key.

    Piece dropping speed
    1 - the fastest speed, always hard drop
    2 - no hard drop
    3 - let the piece land on its own, the bot is always scared
    Number of computing paths for the next piece:
    z, x, c - 1, 4, 8
    n - try to clean the field
    m - disable cleaning mode (focus on getting tetrises)
