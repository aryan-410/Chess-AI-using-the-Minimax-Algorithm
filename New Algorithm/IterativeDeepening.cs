package engine;

/**
 * IterativeDeepening.java
 *
 * Simple framework to drive iterative deepening search for improved move ordering,
 * time management, etc. For demonstration, we keep it minimal.
 */
public class IterativeDeepening {

    private final Search search;

    public IterativeDeepening(Search search) {
        this.search = search;
    }

    public Move findBestMove(Board board, int maxDepth, long timeLimitMillis) {
        long startTime = System.currentTimeMillis();
        Move bestMove = null;
        for (int depth = 1; depth <= maxDepth; depth++) {
            if (System.currentTimeMillis() - startTime > timeLimitMillis) {
                break; // time's up
            }
            bestMove = search.alphaBetaSearch(board, depth, startTime, timeLimitMillis);
            // You can store bestMove for TT, etc.
        }
        return bestMove;
    }
}
