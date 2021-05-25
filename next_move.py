import chess

from eval import eval_board, eval_move

def get_next_move(board, depth=3):
    max_player = board.turn == chess.WHITE

    best_val = float('inf') * (-1 if max_player else 1)

    moves = get_ordered_moves(board)
    best_move = moves[0]

    for move in moves:
        val = 0

        board.push(move)
        if not board.can_claim_draw():
            val = minimax(board, depth-1, -float('inf'), float('inf'), not max_player)
        board.pop()

        if (max_player and val >= best_val) or (not max_player and val <= best_val):
            best_val = val
            best_move = move

    return best_move

def get_ordered_moves(board):
    def sort_func(move):
        return eval_move(board, move)

    return list(sorted(board.legal_moves, key=sort_func, reverse=(board.turn == chess.WHITE)))

def minimax(board, depth, alpha, beta, max_player):
    if board.is_checkmate():
        return float('inf') * (1 if not max_player else -1)
    
    if board.is_game_over():
        return 0

    if depth == 0:
        return eval_board(board)

    if max_player:
        max_eval = -float('inf')
        moves = get_ordered_moves(board)

        for move in moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        return max_eval
    else:
        min_eval = float('inf')
        moves = get_ordered_moves(board)

        for move in moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval
