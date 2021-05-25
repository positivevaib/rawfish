import chess

piece_val = {
    chess.PAWN: 200,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

piece_sqr_table = {
    chess.PAWN: [
         0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ],

    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],

    chess.BISHOP: [ 
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],

    chess.ROOK: [ 
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         0,  0,  0,  5,  5,  0,  0,  0
    ],

    chess.QUEEN: [ 
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],

    chess.KING: [
        [ 
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20
        ],
        [
            -50,-40,-30,-20,-20,-30,-40,-50,
            -30,-20,-10,  0,  0,-10,-20,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-30,  0,  0,  0,  0,-30,-30,
            -50,-30,-30,-30,-30,-30,-30,-50
        ]
    ]
}

def get_piece_sqr_table(board, piece):
    if piece.piece_type == chess.KING:
        table = piece_sqr_table[piece.piece_type][0 if not is_end_game(board) else 1]
    else:
        table = piece_sqr_table[piece.piece_type]

    return table if piece.color == chess.WHITE else list(reversed(table))


def get_piece_sqr_val(board, piece, sqr):
    return get_piece_sqr_table(board, piece)[sqr]


def eval_board(board):
    val = 0

    for sqr in chess.SQUARES:
        piece = board.piece_at(sqr)
        if piece:
            val += (piece_val[piece.piece_type] + get_piece_sqr_val(board, piece, sqr)) * (1 if piece.color == chess.WHITE else -1)

    return val


def eval_move(board, move):
    if move.promotion:
        return float('inf') * (1 if board.turn == chess.WHITE else -1)

    position_change_val = get_piece_sqr_val(board, board.piece_at(move.from_square), move.to_square) - get_piece_sqr_val(board, board.piece_at(move.from_square), move.from_square)
    capture_val = 0 if not board.is_capture(move) else eval_capture(board, move)

    return (position_change_val + capture_val) * (1 if board.turn == chess.WHITE else -1)


def eval_capture(board, move):
    if board.is_en_passant(move):
        return piece_val[chess.PAWN]

    return piece_val[board.piece_at(move.to_square).piece_type] - piece_val[board.piece_at(move.from_square).piece_type]


def is_end_game(board):
    queens = [0, 0]
    minors = [0, 0]
    pieces = [0, 0]

    for sqr in chess.SQUARES:
        piece = board.piece_at(sqr)
        if piece:
            if piece.piece_type == chess.QUEEN:
                queens[0 if piece.color == chess.WHITE else 1] += 1
            else:
                pieces[0 if piece.color == chess.WHITE else 1] += 1
                if piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
                    minors[0 if piece.color == chess.WHITE else 1] += 1

    end_game = False

    if sum(queens) == 0:
        end_game = True
    else:
        end_game = True
        for i in range(2):
            if not (queens[i] == 1 and (pieces[i] == 0 or minors[i] == 1)):
                end_game = False

    return end_game
