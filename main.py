import argparse

import chess

import next_move

def main(fen, color, turn):
    print('Welcome to a game against Rawfish!\n')

    if fen:
        board = chess.Board(fen)
    else:
        board = chess.Board()

    print(board)
    print()

    if not color:
        color = 2
        while color not in [0, 1]:
            color = int(input('\nChoose your color (0 for WHITE, 1 for BLACK): '))

        print('\nYou chose {}.\n'.format('WHITE' if color == 0 else 'BLACK'))

    if not turn:
        turn = 0

    if turn != 0:
        board.turn = not board.turn

    play(board, (color+1)%2, turn)

def get_fish_move(board):
    return next_move.get_next_move(board)

def play(board, fish, turn):
    game_over = False

    while not game_over:
        if turn == fish:
            move = get_fish_move(board)
            print('Rawfish move: {}\n'.format(move))
            board.push(move)
        else:
            move = None
            while not move or not board.is_legal(move):
                print(board.legal_moves)
                move = input('\nPlease enter a legal move: ')
                move = chess.Move.from_uci(move)
                print()

            board.push(move)
            
        print(board)
        print()
            
        if board.is_checkmate():
            print('Game over!\n')
            print('{} wins by checkmate!\n'.format('WHITE' if turn == 0 else 'BLACK'))
            game_over = True
        elif board.is_game_over():
            print('Game over!\n')
            print('It is a draw!\n')
            game_over = True

        turn = (turn+1)%2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fen', type=str, default=None, help='Board initial state.')
    parser.add_argument('--color', type=int, default=None, help='Player color.')
    parser.add_argument('--turn', type=int, default=None, help='Turn number.')
    args = parser.parse_args()

    main(args.fen, args.color, args.turn)
