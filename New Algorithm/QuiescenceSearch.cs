package engine;

import java.util.List;

/**
 * QuiescenceSearch.java
 *
 * A minimal quiescence search that only searches capture moves to stabilize positions.
 */
public class QuiescenceSearch {

    private final Evaluation eval;
    private final MoveGenerator moveGen;

    public QuiescenceSearch(Evaluation eval, MoveGenerator moveGen) {
        this.eval = eval;
        this.moveGen = moveGen;
    }

    public int quiescence(Board board, int alpha, int beta) {
        int standPat = eval.evaluate(board);
        if (standPat >= beta) {
            return beta;
        }
        if (standPat > alpha) {
            alpha = standPat;
        }

        // Generate captures
        List<Move> moves = moveGen.generateAllMoves(board);
        // Filter to captures only (or checks, but let's do captures for simplicity)
        // We'll do a quick check: if move.to has an opponent's piece or is en passant
        moves.removeIf(m -> !isCapture(board, m));

        // Evaluate each
        for (Move m : moves) {
            // Save board
            m.savedBoard = new Board(board);
            board.makeMove(m);

            int score = -quiescence(board, -beta, -alpha);

            board.unmakeMove(m);

            if (score >= beta) {
                return beta;
            }
            if (score > alpha) {
                alpha = score;
            }
        }

        return alpha;
    }

    private boolean isCapture(Board board, Move m) {
        // If there's an opponent piece on 'm.to' or if isEnPassant
        if (m.isEnPassant) return true;
        boolean color = board.whiteToMove; // the color that just moved in makeMove, but here check prior
        // Actually, we must check the board *before* the move:
        // Identify piece at 'm.to' for the opposite color
        boolean oppColor = !color;
        int captured = board.identifyPieceAt(m.to, oppColor);
        return (captured != 0);
    }
}
