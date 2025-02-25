import chess
import gym
import numpy as np
from gym import spaces
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

###############################################################################
# 1) Chess Environment for PPO Training
###############################################################################
class ChessEvaluationEnv(gym.Env):
    """
    Custom Gym Environment where PPO learns to evaluate chess positions.
    """
    def __init__(self):
        super(ChessEvaluationEnv, self).__init__()
        self.board = chess.Board()
        
        # Observation: 8x8x12 board representation
        self.observation_space = spaces.Box(low=0, high=1, shape=(8, 8, 12), dtype=np.float32)
        
        # Action space: Continuous value [-1, 1] representing evaluation
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)

    def reset(self):
        """Resets the board and returns an observation."""
        self.board.reset()
        return self._get_observation()

    def _get_observation(self):
        """Encodes the board into a tensor representation."""
        planes = np.zeros((8, 8, 12), dtype=np.float32)
        piece_map = {
            "P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5,
            "p": 6, "n": 7, "b": 8, "r": 9, "q": 10, "k": 11
        }
        for square in range(64):
            piece = self.board.piece_at(square)
            if piece:
                row, col = divmod(square, 8)
                planes[row, col, piece_map[piece.symbol()]] = 1
        return planes

    def step(self, action):
        """Executes a random legal move and assigns rewards based on the game outcome."""
        legal_moves = list(self.board.legal_moves)
        if len(legal_moves) == 0:
            return self._get_observation(), -1, True, {}  # Loss if no moves left
        
        self.board.push(np.random.choice(legal_moves))  # Simulated move
        
        # Reward system: Win = +1, Loss = -1, Draw = 0, small -0.01 per move
        if self.board.is_checkmate():
            reward = 1 if self.board.turn == chess.BLACK else -1
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            reward = 0  # Draw
        else:
            reward = -0.01  # Small penalty to encourage faster wins
        
        done = self.board.is_game_over()
        return self._get_observation(), reward, done, {}

    def render(self, mode="human"):
        print(self.board)

    def close(self):
        pass

###############################################################################
# 2) Train PPO for Board Evaluation
###############################################################################
def train_ppo_evaluation():
    """
    Trains PPO to learn an evaluation function for chess positions.
    """
    env = ChessEvaluationEnv()
    vec_env = make_vec_env(lambda: env, n_envs=4)  # Parallel training

    model = PPO("CnnPolicy", vec_env, verbose=1)
    model.learn(total_timesteps=500000)  # Train for 500,000 steps

    model.save("ppo_chess_evaluation")
    return model

###############################################################################
# 3) PPO-Based Board Evaluation Function
###############################################################################
def evaluate_position(board, model):
    """
    Uses the trained PPO model to evaluate a board position.
    Returns a float in [-1, 1], indicating game advantage.
    """
    obs = ChessEvaluationEnv()._get_observation()
    obs = obs.reshape((1, 8, 8, 12))  # Add batch dimension
    value = model.predict(obs)[0]  # PPO model evaluates board
    
    return value

###############################################################################
# 4) Minimax Algorithm with PPO Evaluation
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
                break
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
                break
        return value, best_move

###############################################################################
# 5) Hybrid Chess Bot (Minimax + PPO Evaluation)
###############################################################################
def play_chess():
    # Load trained PPO model or train if not available
    try:
        ppo_model = PPO.load("ppo_chess_evaluation")
    except:
        print("No trained model found. Training PPO now...")
        ppo_model = train_ppo_evaluation()

    # Start a chess game
    board = chess.Board()

    while not board.is_game_over():
        _, best_move = alpha_beta_search(board, depth=3, alpha=float('-inf'), beta=float('inf'), is_maximizing=board.turn == chess.WHITE, model=ppo_model)
        board.push(best_move)

    # Print final game result
    print("\nFinal Board State:")
    print(board)
    print("Game Result:", board.result())

if __name__ == "__main__":
    play_chess()
