# Chess board represented as a dictionary:
#   key   = square coordinate, file 'a'-'h' + rank '1'-'8'  (e.g. 'e1')
#   value = 2-char piece code, colour 'w'/'b' + type K Q R B N P  (e.g. 'wK')

STARTING_PIECES = {
    'a8': 'bR', 'b8': 'bN', 'c8': 'bB', 'd8': 'bQ',
    'e8': 'bK', 'f8': 'bB', 'g8': 'bN', 'h8': 'bR',
    'a7': 'bP', 'b7': 'bP', 'c7': 'bP', 'd7': 'bP',
    'e7': 'bP', 'f7': 'bP', 'g7': 'bP', 'h7': 'bP',
    'a2': 'wP', 'b2': 'wP', 'c2': 'wP', 'd2': 'wP',
    'e2': 'wP', 'f2': 'wP', 'g2': 'wP', 'h2': 'wP',
    'a1': 'wR', 'b1': 'wN', 'c1': 'wB', 'd1': 'wQ',
    'e1': 'wK', 'f1': 'wB', 'g1': 'wN', 'h1': 'wR',
}

def print_chessboard(board):
    """Print the board from rank 8 (top) down to rank 1 (bottom)."""
    for rank in '87654321':
        row = []
        for file in 'abcdefgh':
            row.append(board.get(file + rank, '..'))
        print(rank, ' '.join(row))
    print('   a  b  c  d  e  f  g  h')

def is_valid_chess_board(board):
    """Return True if `board` is a legal arrangement, else False."""
    valid_files = 'abcdefgh'
    valid_ranks = '12345678'
    valid_types = 'KQRBNP'

    counts = {'w': 0, 'b': 0}
    kings = {'w': 0, 'b': 0}
    pawns = {'w': 0, 'b': 0}

    for square, piece in board.items():
        # square must be file+rank, both valid
        if len(square) != 2 or square[0] not in valid_files or square[1] not in valid_ranks:
            return False
        # piece must be colour + type, both valid
        if len(piece) != 2 or piece[0] not in 'wb' or piece[1] not in valid_types:
            return False

        colour, kind = piece[0], piece[1]
        counts[colour] += 1
        if kind == 'K':
            kings[colour] += 1
        elif kind == 'P':
            pawns[colour] += 1

    for colour in ('w', 'b'):
        if kings[colour] != 1:      # exactly one king per side
            return False
        if pawns[colour] > 8:       # at most 8 pawns per side
            return False
        if counts[colour] > 16:     # at most 16 pieces per side
            return False
    return True

# --- demo ---
print_chessboard(STARTING_PIECES)
print('Starting board valid? ', is_valid_chess_board(STARTING_PIECES))

# a few broken boards
print('No black king?        ', is_valid_chess_board({'e1': 'wK'}))
print('Bad square "z9"?      ', is_valid_chess_board({'e1': 'wK', 'e8': 'bK', 'z9': 'wP'}))
print('Nine white pawns?     ', is_valid_chess_board(
    {'e1': 'wK', 'e8': 'bK',
     'a2': 'wP', 'b2': 'wP', 'c2': 'wP', 'd2': 'wP',
     'e2': 'wP', 'f2': 'wP', 'g2': 'wP', 'h2': 'wP', 'a3': 'wP'}))






    

