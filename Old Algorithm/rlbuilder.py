import chess
import numpy as np
import gym
from gym import spaces
import torch
import torch.nn as nn
import torch.optim as optim
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

###############################################################################
# 1) Board Representation (CNN Input)
###############################################################################
def board_to_planes(board):
    """
    Converts a chess board into an 8x8x12 tensor representation.
    - 12 channels for piece types (6 for white, 6 for black).
    - Each square is either 1 (occupied) or 0 (empty).
    """
    planes = np.zeros((8, 8, 12), dtype=np.float32)
    piece_map = {
        "P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5,
        "p": 6, "n": 7, "b": 8, "r": 9, "q": 10, "k": 11
    }
    for square in range(64):
        piece = board.piece_at(square)
        if piece:
            row, col = divmod(square, 8)
            planes[row, col, piece_map[piece.symbol()]] = 1
    return planes

###############################################################################
# 2) Custom Chess Environment for PPO Training
###############################################################################
class ChessEnv(gym.Env):
    """
    Chess environment where an agent learns by playing against itself.
    """
    def __init__(self):
        super(ChessEnv, self).__init__()
        self.board = chess.Board()

        self.observation_space = spaces.Box(low=0, high=1, shape=(8, 8, 12), dtype=np.float32)
        self.action_space = spaces.Discrete(4672)  # All legal chess moves

    def reset(self):
        self.board.reset()
        return board_to_planes(self.board)

    def step(self, action):
        legal_moves = list(self.board.legal_moves)
        if len(legal_moves) == 0:
            return board_to_planes(self.board), -1, True, {}  # Loss if no moves left
        
        move = legal_moves[action % len(legal_moves)]  # Ensure valid move
        self.board.push(move)
        
        # Reward system: Win = +1, Loss = -1, Draw = 0, small -0.01 per move
        reward = 0
        if self.board.is_checkmate():
            reward = 1 if self.board.turn == chess.BLACK else -1
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            reward = 0  # Draw
        else:
            reward = -0.01  # Small penalty to encourage faster wins
        
        done = self.board.is_game_over()
        return board_to_planes(self.board), reward, done, {}

    def render(self, mode="human"):
        print(self.board)

    def close(self):
        pass

###############################################################################
# 3) Train PPO on Self-Play Games
###############################################################################
def train_ppo():
    """
    Trains PPO on self-play games using the ChessEnv.
    """
    env = ChessEnv()
    vec_env = make_vec_env(lambda: env, n_envs=4)  # Parallel training

    model = PPO("CnnPolicy", vec_env, verbose=1)
    model.learn(total_timesteps=500000)  # Train for 500,000 steps

    model.save("ppo_chess_strong")
    return model

###############################################################################
# 4) Minimax Algorithm with PPO Integration
###############################################################################
def alpha_beta_search(board, depth, alpha, beta, is_maximizing, model):
    """
    Minimax with Alpha-Beta pruning using PPO-based evaluation.
    """
    if board.is_game_over() or depth == 0:
        return evaluate_position(board, model), None

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return evaluate_position(board, model), None

    best_move = None

    if is_maximizing:
        value = float('-inf')
        for move in legal_moves:
            board.push(move)
            new_value, _ = alpha_beta_search(board, depth - 1, alpha, beta, False, model)
            board.pop()

            if new_value > value:
                value = new_value
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return value, best_move
    else:
        value = float('inf')
        for move in legal_moves:
            board.push(move)
            new_value, _ = alpha_beta_search(board, depth - 1, alpha, beta, True, model)
            board.pop()

            if new_value < value:
                value = new_value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cutoff
        return value, best_move

###############################################################################
# 5) PPO-Based Evaluation Function
###############################################################################
def evaluate_position(board, model):
    """
    Uses the trained PPO model to evaluate a board position.
    """
    obs = board_to_planes(board)
    obs = obs.reshape((1, 8, 8, 12))  # Add batch dimension
    value = model.predict(obs)[0]  # PPO model evaluates board

    return value

###############################################################################
# 6) PPO-Based Move Selection
###############################################################################
def ppo_select_move(board, model):
    """
    Uses the trained PPO model to select the best move.
    """
    obs = board_to_planes(board)
    action, _ = model.predict(obs)  # Use PPO to select move
    legal_moves = list(board.legal_moves)

    if action >= len(legal_moves):
        action = 0  # Fallback to first move if invalid

    return legal_moves[action]  # Return the best move from PPO

###############################################################################
# 7) Hybrid Chess Bot (PPO + Minimax)
###############################################################################
def hybrid_chess_bot(board, minimax_depth=3, ppo_model=None):
    """
    Hybrid bot using PPO for early-game and Minimax for deeper calculations.
    """
    move = None

    if board.fullmove_number <= 10:  # Use PPO for early-game moves
        move = ppo_select_move(board, ppo_model)
    else:  # Use Minimax for deep calculations
        _, move = alpha_beta_search(board, minimax_depth, float('-inf'), float('inf'), board.turn == chess.WHITE, ppo_model)

    return move

###############################################################################
# 8) Run Chess Bot
###############################################################################
def main():
    # Train PPO if not already trained
    try:
        ppo_model = PPO.load("ppo_chess_strong")
    except:
        print("No trained model found. Training PPO now...")
        ppo_model = train_ppo()

    # Start a game
    board = chess.Board()

    while not board.is_game_over():
        move = hybrid_chess_bot(board, minimax_depth=3, ppo_model=ppo_model)
        board.push(move)

    # Print final game result
    print("\nFinal Board State:")
    print(board)
    print("Game Result:", board.result())

if __name__ == "__main__":
    main()
