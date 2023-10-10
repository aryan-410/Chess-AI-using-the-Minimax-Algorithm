# 🚨 IMPORTANT UPDATE 🚨
**As of 27th September 2023, the latest algorithm has been taken down due to issues in the source code and memory complications.** I apologize for any inconvenience caused. A revised and cleaner version of the code is in the works and is scheduled to be uploaded by 15th October 2023.


# 🛡️ Chess AI: Harnessing Minimax for Masterful Moves 🛡️

Welcome to the Chess AI repository! Built with precision and a keen understanding of the grand game of chess, this AI uses the Minimax algorithm to provide you with a challenging and engaging opponent. Whether you're a novice or a seasoned player, stepping onto this digital chessboard promises a game worth your mettle.

## 📖 Table of Contents
- [Board Class](#board-class)
- [Minimax Algorithm](#minimax-algorithm)
- [How to Play](#how-to-play)
- [Contributions & Feedback](#contributions--feedback)

## 📚 Board Class
Located in: `boardClass.py`

At the core of any chess game lies the board. The `boardClass.py` contains the `Board` class which serves as the foundational piece for our entire game.

### Key Features:

- **Representation**: Internally represented as an 8x8 matrix, with each cell denoting a piece or an empty space.
- **Piece Movement**: Methods for validating and executing standard chess moves.
- **Game State**: Fetch the current game state, with details like turn status, check/checkmate statuses, and available moves.

## 🔍 Minimax Algorithm
Located in: `minimaxAI.py`

Minimax is the brain behind our Chess AI. This decision-making algorithm simulates potential outcomes to choose the optimal strategy for the AI.

### How It Works:

1. **Decision Tree**: Creates a decision tree for each possible move.
2. **Evaluating Moves**: Uses a scoring system to evaluate potential outcomes.
3. **Depth-Limited Search**: Limits the depth of the search for efficiency.
4. **Optimal Strategy**: Assesses outcomes to maximize the AI's winning chances.

## 🎮 How to Play
Run the game using: `main.py`

Dive into the game by running the `main.py` file. This script provides an interactive interface to challenge our Chess AI.

### Instructions:

1. **Starting the Game**: Execute `main.py`.
2. **Making Moves**: Follow the interface prompts.
3. **Facing the AI**: After your move, the AI will counter based on the Minimax algorithm.

## 💌 Contributions & Feedback

Your feedback is invaluable! Open an issue or submit a PR if you have suggestions, bug reports, or contributions. Let's enhance this Chess AI together!

🎉 Happy gaming! 🎉
