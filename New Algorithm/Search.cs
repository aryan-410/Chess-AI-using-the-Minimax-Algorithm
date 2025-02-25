package engine;

import java.util.List;

/**
 * Search.java
 *
 * Implements minimax search with alpha-beta pruning, using:
 *  - TranspositionTable
 *  - QuiescenceSearch
 *  - Basic time check
 */
public class Search {

    private final MoveGenerator moveGen;
    private final Evaluation eval;
    private final QuiescenceSearch quiescence;
    private final TranspositionTable tt;

    private boolean stopSearch;

    public Search(MoveGenerator moveGen, Evaluation eval, QuiescenceSearch quiescence, TranspositionTable tt) {
        this.moveGen = moveGen;
        this.eval = eval;
        this.quiescence = quiescence;
        this.tt = tt;
    }

    public Move alphaBetaSearch(Board board, int depth, long startTime, long timeLimitMillis) {
        stopSearch = false;
        tt.newSearch();

        Move bestMove = null;
        int alpha = -999999;
        int beta  =  999999;
        int bestScore = -999999;

        List<Move> moves = moveGen.generateAllMoves(board);
        // Basic move ordering: we can do a partial approach by checking if we have a TT entry
        // for best move from previous iteration, but let's keep it simpler for demonstration.

        for (Move move : moves) {
            // Save board
            move.savedBoard = new Board(board);
            board.makeMove(move);

            int score = -search(board, depth - 1, -beta, -alpha, startTime, timeLimitMillis);

            board.unmakeMove(move);

            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
            if (score > alpha) {
                alpha = score;
            }
            if (alpha >= beta) {
                break; // alpha-beta cutoff
            }
            if (System.currentTimeMillis() - startTime > timeLimitMillis) {
                // Time is up
                stopSearch = true;
                break;
            }
        }

        return bestMove;
    }

    private int search(Board board, int depth, int alpha, int beta, long startTime, long timeLimitMillis) {
        if (depth <= 0) {
            // quiescence
            return quiescence.quiescence(board, alpha, beta);
        }

        if (System.currentTimeMillis() - startTime > timeLimitMillis) {
            stopSearch = true;
            return eval.evaluate(board);
        }
        if (stopSearch) {
            return eval.evaluate(board);
        }

        // Transposition Table probe
        long key = board.getZobristKey();
        TranspositionTable.TTEntry entry = tt.probe(key);
        if (entry != null && entry.depth >= depth) {
            // We can use stored entry
            switch (entry.type) {
                case EXACT: return entry.score;
                case ALPHA:
                    if (entry.score <= alpha) return entry.score;
                    break;
                case BETA:
                    if (entry.score >= beta) return entry.score;
                    break;
            }
        }

        List<Move> moves = moveGen.generateAllMoves(board);
        if (moves.isEmpty()) {
            // checkmate or stalemate
            // If king in check => mate
            boolean kingInCheck = board.isSquareAttacked(
                getKingSquare(board, board.whiteToMove), !board.whiteToMove, moveGen);
            if (kingInCheck) {
                return -99999 + (100 - depth);
            } else {
                return 0; // stalemate
            }
        }

        int bestScore = -999999;
        Move bestMove = null;

        int originalAlpha = alpha;

        // Basic loop
        for (Move move : moves) {
            move.savedBoard = new Board(board);
            board.makeMove(move);

            int score = -search(board, depth - 1, -beta, -alpha, startTime, timeLimitMillis);

            board.unmakeMove(move);

            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
            if (score > alpha) {
                alpha = score;
            }
            if (alpha >= beta) {
                break; // alpha-beta cutoff
            }
            if (stopSearch) {
                break;
            }
        }

        // Store in TT
        TranspositionTable.NodeType type;
        if (bestScore <= originalAlpha) {
            type = TranspositionTable.NodeType.ALPHA;
        } else if (bestScore >= beta) {
            type = TranspositionTable.NodeType.BETA;
        } else {
            type = TranspositionTable.NodeType.EXACT;
        }
        tt.store(key, depth, bestScore, type, bestMove);

        return bestScore;
    }

    private int getKingSquare(Board board, boolean white) {
        long kingBB = white ? board.WK : board.BK;
        if (kingBB == 0) return -1;
        return Long.numberOfTrailingZeros(kingBB);
    }
}
