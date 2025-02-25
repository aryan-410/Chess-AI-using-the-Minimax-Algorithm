package engine;

import java.util.Arrays;

/**
 * TranspositionTable.java
 *
 * Stores entries keyed by Zobrist hash:
 * - depth
 * - score
 * - node type (exact, alpha, beta)
 * - best move
 */
public class TranspositionTable {

    public static enum NodeType {
        EXACT, ALPHA, BETA
    }

    static class TTEntry {
        long key;
        int depth;
        int score;
        NodeType type;
        Move bestMove;
        int age;
    }

    private TTEntry[] table;
    private int size;
    private int age;

    public TranspositionTable(int sizeMB) {
        // Rough approach: each entry ~some bytes. We'll just do a fixed size for demonstration.
        // For example, size = 1<<20 => ~1 million entries
        // We'll do smaller for demo if you want
        size = 1 << 20; // about 1 million
        table = new TTEntry[size];
        this.age = 0;
    }

    private int index(long key) {
        // typical approach: key mod size
        return (int)(key & (size - 1));
    }

    public void newSearch() {
        age++;
    }

    public TTEntry probe(long key) {
        int i = index(key);
        TTEntry e = table[i];
        if (e != null && e.key == key) {
            return e;
        }
        return null;
    }

    public void store(long key, int depth, int score, NodeType type, Move bestMove) {
        int i = index(key);
        TTEntry e = table[i];
        if (e == null) {
            e = new TTEntry();
            table[i] = e;
        }
        e.key = key;
        e.depth = depth;
        e.score = score;
        e.type = type;
        e.bestMove = bestMove;
        e.age = age;
    }
}
