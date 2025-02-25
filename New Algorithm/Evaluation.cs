package engine;

/**
 * Evaluation.java
 *
 * A simple material+piece-square-based evaluation function.
 * Real engines have much more sophisticated evaluation.
 */
public class Evaluation {

    // Piece values
    private static final int PAWN_VALUE   = 100;
    private static final int KNIGHT_VALUE = 300;
    private static final int BISHOP_VALUE = 300;
    private static final int ROOK_VALUE   = 500;
    private static final int QUEEN_VALUE  = 900;

    public int evaluate(Board board) {
        // Basic: just sum up piece counts
        int score = 0;
        score += PAWN_VALUE   * Long.bitCount(board.WP);
        score += KNIGHT_VALUE * Long.bitCount(board.WN);
        score += BISHOP_VALUE * Long.bitCount(board.WB);
        score += ROOK_VALUE   * Long.bitCount(board.WR);
        score += QUEEN_VALUE  * Long.bitCount(board.WQ);

        score -= PAWN_VALUE   * Long.bitCount(board.BP);
        score -= KNIGHT_VALUE * Long.bitCount(board.BN);
        score -= BISHOP_VALUE * Long.bitCount(board.BB);
        score -= ROOK_VALUE   * Long.bitCount(board.BR);
        score -= QUEEN_VALUE  * Long.bitCount(board.BQ);

        // Return from White's perspective
        // If board.whiteToMove, we keep it as is.
        // If it's black to move, we might slightly shift the sign or not.
        // Typically we just keep it from White's perspective.
        return score;
    }
}
