import chess
import chess.pgn
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from collections import deque

############################################
# 1) Neural Network for Board Evaluation
############################################
class ChessValueNetwork(nn.Module):
    """
    A simple feedforward neural network that takes a board representation
    and outputs a scalar in [-1, 1], representing the predicted outcome
    from White's perspective.
    """
    def __init__(self):
        super().__init__()
        # For demonstration, a small 2-layer MLP
        # Input size is based on a chosen board encoding
        # We'll do something naive: 64 squares * 12 possible piece types = 768
        # (one-hot encoding of piece type in each square).
        self.fc1 = nn.Linear(768, 256)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        # x shape: [batch_size, 768]
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # final linear
        x = torch.tanh(self.fc3(x))  # in range [-1, +1]
        return x

############################################
# 2) Board Encoding
############################################
# We'll define a function that encodes a python-chess board
# into a fixed-size (768,) vector for the network.
#
# We will do a naive "one-hot" approach:
#   For each square (0..63), check if it has a piece.
#   If it does, find which one of the 12 piece slots it belongs to.
#   Then that index in our vector = 1, rest = 0.
#
# The 12 piece slots are: 
#   [White Pawn, White Knight, White Bishop, White Rook, White Queen, White King,
#    Black Pawn, Black Knight, Black Bishop, Black Rook, Black Queen, Black King]
############################################

def encode_board(board: chess.Board) -> np.ndarray:
    # 64 squares * 12 piece types = 768
    encoded = np.zeros(768, dtype=np.float32)
    
    # List out piece types in a consistent order
    piece_map = {
        chess.PAWN:   0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK:   3,
        chess.QUEEN:  4,
        chess.KING:   5
    }

    for square in chess.SQUARES:  # 0..63
        piece = board.piece_at(square)
        if piece is not None:
            # piece_map index
            offset = piece_map[piece.piece_type]
            if piece.color == chess.BLACK:
                offset += 6  # black pieces in second half
            # set the one-hot
            index = 12 * square + offset
            encoded[index] = 1.0

    return encoded

############################################
# 3) Simple Self-Play Environment
############################################
# We'll do a simplified self-play approach:
# - On each turn, choose a random legal move (or some simple heuristic).
# - Step until the game ends in checkmate or draw.
# - The outcome is +1 for White if White won, -1 if Black won,
#   and 0 for a draw.
#
# We'll store states in a buffer, then at the end of the game
# we assign the outcome from White's perspective.
############################################

def play_one_game_random():
    """Play one game using random moves for both sides.
       Returns: (state_history, outcome)
        - state_history: list of (board_fen, is_white_turn)
        - outcome in [-1, 0, +1] from White's perspective
    """
    board = chess.Board()
    state_history = []
    
    while not board.is_game_over():
        # record the state
        state_history.append((board.fen(), board.turn))
        
        # choose a random legal move
        moves = list(board.legal_moves)
        move = random.choice(moves)
        board.push(move)
    
    result = board.result()  # e.g. "1-0", "0-1", "1/2-1/2"
    if result == "1-0":
        outcome = 1.0
    elif result == "0-1":
        outcome = -1.0
    else:
        outcome = 0.0
    
    return state_history, outcome

############################################
# 4) Replay Buffer
############################################
class ReplayBuffer:
    def __init__(self, max_size=10000):
        self.buffer = deque(maxlen=max_size)

    def push(self, state, value):
        """
        state: a fen string
        value: float in [-1,1], the outcome from White's perspective
        """
        self.buffer.append((state, value))
    
    def sample(self, batch_size=32):
        mini_batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        states = []
        targets = []
        for s, v in mini_batch:
            states.append(s)
            targets.append(v)
        return states, targets
    
    def __len__(self):
        return len(self.buffer)

############################################
# 5) Training Loop
############################################
# We'll implement a simple approach:
#  - Generate self-play games with random moves
#  - For each position in that game, store the final outcome (from White's perspective)
#  - Periodically train the neural net to predict that outcome from the board
#  - Over time, it should learn some notion of better/worse positions
############################################

def train_value_network():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = ChessValueNetwork().to(device)
    optimizer = optim.Adam(net.parameters(), lr=1e-4)
    loss_fn = nn.MSELoss()

    buffer = ReplayBuffer(max_size=20000)
    
    n_games = 1000       # Number of self-play games
    train_every = 1      # Train after every game, for example
    batch_size = 64
    print_interval = 50

    for game_idx in range(1, n_games+1):
        # 1) Play one self-play game
        states, outcome = play_one_game_random()
        
        # 2) Add all positions from that game to the buffer
        for fen, is_white_turn in states:
            # The outcome is always from White's perspective. 
            # If the position is from black's perspective, we might need to invert sign 
            # if we want "Value(s) from current side's perspective". 
            # But let's keep it from White's perspective for simplicity.
            #   => If black is to move, the outcome from White's perspective is still 'outcome'
            # This is typical in "White-centric" approaches.
            buffer.push(fen, outcome)
        
        # 3) Train
        if game_idx % train_every == 0:
            # We'll run a small number of training steps
            for _ in range(5):  # do e.g. 5 mini-batches
                states_sample, targets_sample = buffer.sample(batch_size)
                if not states_sample:
                    break

                # encode states
                encoded_states = []
                for fen in states_sample:
                    b = chess.Board(fen=fen)
                    encoded = encode_board(b)
                    encoded_states.append(encoded)
                encoded_states = np.stack(encoded_states, axis=0)  # shape [B, 768]
                encoded_states = torch.tensor(encoded_states, device=device, dtype=torch.float)

                targets = torch.tensor(targets_sample, device=device, dtype=torch.float).unsqueeze(-1)  # [B,1]
                
                # forward
                pred = net(encoded_states)
                loss = loss_fn(pred, targets)
                
                # backward
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # 4) Print progress
        if game_idx % print_interval == 0:
            print(f"Game {game_idx}/{n_games} completed. Buffer size={len(buffer)}")
    
    return net

############################################
# 6) Putting it all together
############################################
def main():
    net = train_value_network()
    print("Finished training. Let's evaluate a few positions...")

    # Evaluate some well-known opening positions
    test_fens = [
        "r1bqkbnr/1ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 2 3",  # Ruy Lopez, Berlin
        "rnbqkbnr/pppp1ppp/4p3/8/2B5/5N2/PPPP1PPP/RNBQK2R b KQkq - 1 2",      # Bishop's opening
        "r1bqkbnr/pp1n1ppp/2pb4/3pp3/2BPP3/2N2N2/PPP2PPP/R1BQK2R w KQkq - 5 5", # Typical d4 line
        chess.STARTING_FEN,  # starting position
    ]

    net.eval()
    for fen in test_fens:
        board = chess.Board(fen=fen)
        enc = encode_board(board)
        x = torch.tensor(enc, dtype=torch.float).unsqueeze(0)
        with torch.no_grad():
            val = net(x).item()
        print(f"FEN: {fen}")
        print(f"Evaluation (from White's perspective) ~ {val:.3f}")
        print("")

if __name__ == "__main__":
    main()
