
import java.util.ArrayList;
import java.util.List;

/**
 * MoveGenerator.java
 *
 * Contains methods to generate all pseudo-legal moves:
 * - White & Black pawns
 * - Knights
 * - Bishops
 * - Rooks
 * - Queens
 * - King
 * - Special moves (en passant, castling, promotion)
 *
 * Also some helper methods (like 'isSquareAttacked(...)').
 */
public class MoveGenerator {

    // For a simpler approach, define piece indices for both colors:
    // We'll reuse piece codes from Board:
    // 1=Pawn,2=Knight,3=Bishop,4=Rook,5=Queen,6=King

    // Generate all pseudo-legal moves for the side to move
    public List<Move> generateAllMoves(Board board) {
        if (board.whiteToMove) {
            return generateWhiteMoves(board);
        } else {
            return generateBlackMoves(board);
        }
    }

    public boolean isSquareAttacked(Board board, int sq, boolean byWhite) {
        // We can do a direct approach: generate all *pseudo-legal* moves for the side
        // 'byWhite'
        // If any move's 'to' is sq, that means 'sq' is attacked.
        List<Move> moves = byWhite ? generateWhiteMoves(board) : generateBlackMoves(board);
        for (Move m : moves) {
            if (m.to == sq)
                return true;
        }
        return false;
    }

    // ========== White ================
    private List<Move> generateWhiteMoves(Board board) {
        List<Move> moves = new ArrayList<>();
        long occupancy = board.getAllPieces();
        long myPieces = board.getWhitePieces();

        // 1) Pawns
        moves.addAll(generateWhitePawnMoves(board, occupancy, myPieces));

        // 2) Knights
        long knights = board.WN;
        while (knights != 0) {
            int sq = Long.numberOfTrailingZeros(knights);
            knights &= knights - 1;
            moves.addAll(knightMoves(board, sq, myPieces));
        }

        // 3) Bishops
        long bishops = board.WB;
        while (bishops != 0) {
            int sq = Long.numberOfTrailingZeros(bishops);
            bishops &= bishops - 1;
            moves.addAll(bishopMoves(board, sq, occupancy, myPieces));
        }

        // 4) Rooks
        long rooks = board.WR;
        while (rooks != 0) {
            int sq = Long.numberOfTrailingZeros(rooks);
            rooks &= rooks - 1;
            moves.addAll(rookMoves(board, sq, occupancy, myPieces));
        }

        // 5) Queens
        long queens = board.WQ;
        while (queens != 0) {
            int sq = Long.numberOfTrailingZeros(queens);
            queens &= queens - 1;
            moves.addAll(queenMoves(board, sq, occupancy, myPieces));
        }

        // 6) King
        long kingBB = board.WK;
        if (kingBB != 0) {
            int sq = Long.numberOfTrailingZeros(kingBB);
            moves.addAll(kingMoves(board, sq, myPieces));
        }

        // Castling
        moves.addAll(generateWhiteCastling(board, occupancy));

        return moves;
    }

    // ========== Black ================
    private List<Move> generateBlackMoves(Board board) {
        List<Move> moves = new ArrayList<>();
        long occupancy = board.getAllPieces();
        long myPieces = board.getBlackPieces();

        // 1) Pawns
        moves.addAll(generateBlackPawnMoves(board, occupancy, myPieces));

        // 2) Knights
        long knights = board.BN;
        while (knights != 0) {
            int sq = Long.numberOfTrailingZeros(knights);
            knights &= knights - 1;
            moves.addAll(knightMoves(board, sq, myPieces));
        }

        // 3) Bishops
        long bishops = board.BB;
        while (bishops != 0) {
            int sq = Long.numberOfTrailingZeros(bishops);
            bishops &= bishops - 1;
            moves.addAll(bishopMoves(board, sq, occupancy, myPieces));
        }

        // 4) Rooks
        long rooks = board.BR;
        while (rooks != 0) {
            int sq = Long.numberOfTrailingZeros(rooks);
            rooks &= rooks - 1;
            moves.addAll(rookMoves(board, sq, occupancy, myPieces));
        }

        // 5) Queens
        long queens = board.BQ;
        while (queens != 0) {
            int sq = Long.numberOfTrailingZeros(queens);
            queens &= queens - 1;
            moves.addAll(queenMoves(board, sq, occupancy, myPieces));
        }

        // 6) King
        long kingBB = board.BK;
        if (kingBB != 0) {
            int sq = Long.numberOfTrailingZeros(kingBB);
            moves.addAll(kingMoves(board, sq, myPieces));
        }

        // Castling
        moves.addAll(generateBlackCastling(board, occupancy));

        return moves;
    }

    // ====================== White Pawn ========================
    private List<Move> generateWhitePawnMoves(Board board, long occupancy, long myPieces) {
        List<Move> list = new ArrayList<>();
        long pawns = board.WP;

        // Single push: (pawns << 8) & empty
        long empty = ~occupancy;
        long oneStep = (pawns << 8) & empty;
        // from => to = from + 8
        long twoStep = ((oneStep & 0x000000FF00000000L) << 8) & empty;
        // captures
        long leftCap = (pawns << 7) & (board.getBlackPieces()) & 0xFEFEFEFEFEFEFEFEL;
        long rightCap = (pawns << 9) & (board.getBlackPieces()) & 0x7F7F7F7F7F7F7F7FL;

        // Single pushes
        addWhitePawnMoves(board, oneStep, 8, list, false);
        // Double pushes
        addWhitePawnMoves(board, twoStep, 16, list, false);

        // Captures
        addWhitePawnCaptures(board, leftCap, 7, list);
        addWhitePawnCaptures(board, rightCap, 9, list);

        // En passant
        if (board.enPassantSquare != -1) {
            long epMask = 1L << board.enPassantSquare;
            long epLeft = (pawns << 7) & 0xFEFEFEFEFEFEFEFEL;
            long epRight = (pawns << 9) & 0x7F7F7F7F7F7F7F7FL;
            if ((epLeft & epMask) != 0) {
                int to = board.enPassantSquare;
                int from = to - 7;
                Move m = new Move(from, to);
                m.isEnPassant = true;
                list.add(m);
            }
            if ((epRight & epMask) != 0) {
                int to = board.enPassantSquare;
                int from = to - 9;
                Move m = new Move(from, to);
                m.isEnPassant = true;
                list.add(m);
            }
        }

        return list;
    }

    private void addWhitePawnMoves(Board board, long bitboard, int shift, List<Move> list, boolean capture) {
        while (bitboard != 0) {
            int to = Long.numberOfTrailingZeros(bitboard);
            bitboard &= bitboard - 1;
            int from = to - shift;
            // Promotion?
            if (to >= 56) {
                for (int promo : new int[] { 5, 4, 3, 2 }) {
                    Move m = new Move(from, to);
                    m.isPromotion = true;
                    m.promotionPieceCode = promo;
                    list.add(m);
                }
            } else {
                Move m = new Move(from, to);
                list.add(m);
            }
        }
    }

    private void addWhitePawnCaptures(Board board, long bitboard, int shift, List<Move> list) {
        while (bitboard != 0) {
            int to = Long.numberOfTrailingZeros(bitboard);
            bitboard &= bitboard - 1;
            int from = to - shift;
            if (to >= 56) {
                for (int promo : new int[] { 5, 4, 3, 2 }) {
                    Move m = new Move(from, to);
                    m.isPromotion = true;
                    m.promotionPieceCode = promo;
                    list.add(m);
                }
            } else {
                Move m = new Move(from, to);
                list.add(m);
            }
        }
    }

    // ====================== Black Pawn ========================
    private List<Move> generateBlackPawnMoves(Board board, long occupancy, long myPieces) {
        List<Move> list = new ArrayList<>();
        long pawns = board.BP;

        long empty = ~occupancy;
        long oneStep = (pawns >>> 8) & empty;
        long twoStep = ((oneStep & 0x0000FF0000000000L) >>> 8) & empty;
        long leftCap = (pawns >>> 9) & board.getWhitePieces() & 0x007F7F7F7F7F7F7FL;
        long rightCap = (pawns >>> 7) & board.getWhitePieces() & 0x00FEFEFEFEFEFEFEL;

        addBlackPawnMoves(board, oneStep, -8, list, false);
        addBlackPawnMoves(board, twoStep, -16, list, false);

        addBlackPawnCaptures(board, leftCap, -9, list);
        addBlackPawnCaptures(board, rightCap, -7, list);

        // En passant
        if (board.enPassantSquare != -1) {
            long epMask = 1L << board.enPassantSquare;
            long epLeft = (pawns >>> 9) & 0x007F7F7F7F7F7F7FL;
            long epRight = (pawns >>> 7) & 0x00FEFEFEFEFEFEFEL;
            if ((epLeft & epMask) != 0) {
                int to = board.enPassantSquare;
                int from = to + 9;
                Move m = new Move(from, to);
                m.isEnPassant = true;
                list.add(m);
            }
            if ((epRight & epMask) != 0) {
                int to = board.enPassantSquare;
                int from = to + 7;
                Move m = new Move(from, to);
                m.isEnPassant = true;
                list.add(m);
            }
        }

        return list;
    }

    private void addBlackPawnMoves(Board board, long bitboard, int shift, List<Move> list, boolean capture) {
        while (bitboard != 0) {
            int to = Long.numberOfTrailingZeros(bitboard);
            bitboard &= bitboard - 1;
            int from = to - shift;
            if (to < 8) {
                for (int promo : new int[] { 5, 4, 3, 2 }) {
                    Move m = new Move(from, to);
                    m.isPromotion = true;
                    m.promotionPieceCode = promo;
                    list.add(m);
                }
            } else {
                list.add(new Move(from, to));
            }
        }
    }

    private void addBlackPawnCaptures(Board board, long bitboard, int shift, List<Move> list) {
        while (bitboard != 0) {
            int to = Long.numberOfTrailingZeros(bitboard);
            bitboard &= bitboard - 1;
            int from = to - shift;
            if (to < 8) {
                for (int promo : new int[] { 5, 4, 3, 2 }) {
                    Move m = new Move(from, to);
                    m.isPromotion = true;
                    m.promotionPieceCode = promo;
                    list.add(m);
                }
            } else {
                list.add(new Move(from, to));
            }
        }
    }

    // ====================== Knights ========================
    private List<Move> knightMoves(Board board, int sq, long myPieces) {
        List<Move> list = new ArrayList<>();
        long attacks = knightAttacks(sq) & ~myPieces;
        while (attacks != 0) {
            int to = Long.numberOfTrailingZeros(attacks);
            attacks &= attacks - 1;
            list.add(new Move(sq, to));
        }
        return list;
    }

    private static long knightAttacks(int sq) {
        // Offsets approach
        long mask = 0L;
        int rank = sq / 8;
        int file = sq % 8;
        int[] dRank = { -2, -2, -1, -1, 1, 1, 2, 2 };
        int[] dFile = { -1, 1, -2, 2, -2, 2, -1, 1 };
        for (int i = 0; i < 8; i++) {
            int r2 = rank + dRank[i];
            int f2 = file + dFile[i];
            if (r2 >= 0 && r2 < 8 && f2 >= 0 && f2 < 8) {
                int sq2 = r2 * 8 + f2;
                mask |= (1L << sq2);
            }
        }
        return mask;
    }

    // ====================== Bishops (sliding) ================
    private List<Move> bishopMoves(Board board, int sq, long occ, long myPieces) {
        List<Move> list = new ArrayList<>();
        long attacks = bishopAttacks(sq, occ) & ~myPieces;
        while (attacks != 0) {
            int to = Long.numberOfTrailingZeros(attacks);
            attacks &= attacks - 1;
            list.add(new Move(sq, to));
        }
        return list;
    }

    private long bishopAttacks(int sq, long occ) {
        long mask = 0L;
        mask |= ray(sq, occ, 9);
        mask |= ray(sq, occ, 7);
        mask |= ray(sq, occ, -9);
        mask |= ray(sq, occ, -7);
        return mask;
    }

    // ====================== Rooks (sliding) ==================
    private List<Move> rookMoves(Board board, int sq, long occ, long myPieces) {
        List<Move> list = new ArrayList<>();
        long attacks = rookAttacks(sq, occ) & ~myPieces;
        while (attacks != 0) {
            int to = Long.numberOfTrailingZeros(attacks);
            attacks &= attacks - 1;
            list.add(new Move(sq, to));
        }
        return list;
    }

    private long rookAttacks(int sq, long occ) {
        long mask = 0L;
        mask |= ray(sq, occ, 1);
        mask |= ray(sq, occ, -1);
        mask |= ray(sq, occ, 8);
        mask |= ray(sq, occ, -8);
        return mask;
    }

    // ====================== Queens = Rook + Bishop ===========
    private List<Move> queenMoves(Board board, int sq, long occ, long myPieces) {
        List<Move> list = new ArrayList<>();
        long attacks = (rookAttacks(sq, occ) | bishopAttacks(sq, occ)) & ~myPieces;
        while (attacks != 0) {
            int to = Long.numberOfTrailingZeros(attacks);
            attacks &= attacks - 1;
            list.add(new Move(sq, to));
        }
        return list;
    }

    // ====================== King =============================
    private List<Move> kingMoves(Board board, int sq, long myPieces) {
        List<Move> list = new ArrayList<>();
        long attacks = kingAttacks(sq) & ~myPieces;
        while (attacks != 0) {
            int to = Long.numberOfTrailingZeros(attacks);
            attacks &= attacks - 1;
            list.add(new Move(sq, to));
        }
        return list;
    }

    private static long kingAttacks(int sq) {
        long mask = 0L;
        int rank = sq / 8;
        int file = sq % 8;
        for (int dr = -1; dr <= 1; dr++) {
            for (int df = -1; df <= 1; df++) {
                if (dr == 0 && df == 0)
                    continue;
                int rr = rank + dr;
                int ff = file + df;
                if (rr >= 0 && rr < 8 && ff >= 0 && ff < 8) {
                    mask |= (1L << (rr * 8 + ff));
                }
            }
        }
        return mask;
    }

    // ====================== Sliding Helper ===================
    private long ray(int start, long occ, int step) {
        long mask = 0L;
        int sq = start;
        while (true) {
            int next = sq + step;
            if (next < 0 || next >= 64)
                break;
            // Check wrap-around
            int rank1 = sq / 8, file1 = sq % 8;
            int rank2 = next / 8, file2 = next % 8;
            if (Math.abs(rank2 - rank1) > 1 || Math.abs(file2 - file1) > 1)
                break;
            mask |= (1L << next);
            if (((1L << next) & occ) != 0) {
                break;
            }
            sq = next;
        }
        return mask;
    }

    // ====================== Castling =========================
    private List<Move> generateWhiteCastling(Board board, long occ) {
        List<Move> list = new ArrayList<>();
        if ((board.castlingRights & 1) != 0) {
            // White king-side
            // e1=4, f1=5, g1=6
            if (((occ & (1L << 5)) == 0) && ((occ & (1L << 6)) == 0)) {
                // squares not attacked?
                if (!board.isSquareAttacked(4, false, this)
                        && !board.isSquareAttacked(5, false, this)
                        && !board.isSquareAttacked(6, false, this)) {
                    Move m = new Move(4, 6);
                    m.isCastling = true;
                    list.add(m);
                }
            }
        }
        if ((board.castlingRights & 2) != 0) {
            // White queen-side
            // e1=4, d1=3, c1=2, b1=1
            if (((occ & (1L << 3)) == 0)
                    && ((occ & (1L << 2)) == 0)
                    && ((occ & (1L << 1)) == 0)) {
                if (!board.isSquareAttacked(4, false, this)
                        && !board.isSquareAttacked(3, false, this)
                        && !board.isSquareAttacked(2, false, this)) {
                    Move m = new Move(4, 2);
                    m.isCastling = true;
                    list.add(m);
                }
            }
        }
        return list;
    }

    private List<Move> generateBlackCastling(Board board, long occ) {
        List<Move> list = new ArrayList<>();
        if ((board.castlingRights & 4) != 0) {
            // Black king-side
            // e8=60, f8=61, g8=62
            if (((occ & (1L << 61)) == 0) && ((occ & (1L << 62)) == 0)) {
                if (!board.isSquareAttacked(60, true, this)
                        && !board.isSquareAttacked(61, true, this)
                        && !board.isSquareAttacked(62, true, this)) {
                    Move m = new Move(60, 62);
                    m.isCastling = true;
                    list.add(m);
                }
            }
        }
        if ((board.castlingRights & 8) != 0) {
            // Black queen-side
            // e8=60, d8=59, c8=58, b8=57
            if (((occ & (1L << 59)) == 0)
                    && ((occ & (1L << 58)) == 0)
                    && ((occ & (1L << 57)) == 0)) {
                if (!board.isSquareAttacked(60, true, this)
                        && !board.isSquareAttacked(59, true, this)
                        && !board.isSquareAttacked(58, true, this)) {
                    Move m = new Move(60, 58);
                    m.isCastling = true;
                    list.add(m);
                }
            }
        }
        return list;
    }
}
