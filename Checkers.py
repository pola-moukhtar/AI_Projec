import pygame
import sys
import math
import random

pygame.init()

# ================= CONFIG =================
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
CELL = WIDTH // COLS

WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
RED   = (200, 60, 60)
BLUE  = (60, 120, 200)
GREEN = (0, 200, 0)
GOLD  = (255, 215, 0)
GRAY  = (100, 100, 100)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
FONT = pygame.font.SysFont("arial", 26)
BIG_FONT = pygame.font.SysFont("arial", 40)
clock = pygame.time.Clock()

# ================= PIECE =================
class Piece:
    def __init__(self, r, c, color):
        self.row = r
        self.col = c
        self.color = color
        self.king = False

    def draw(self):
        x = self.col * CELL + CELL // 2
        y = self.row * CELL + CELL // 2
        pygame.draw.circle(screen, self.color, (x, y), CELL // 2 - 10)
        if self.king:
            pygame.draw.circle(screen, GOLD, (x, y), 10)

# ================= BOARD =================
class Board:
    def __init__(self):
        self.board = [[None]*COLS for _ in range(ROWS)]
        self.create()

    def create(self):
        for r in range(ROWS):
            for c in range(COLS):
                if (r+c)%2 != 0:
                    if r < 3:
                        self.board[r][c] = Piece(r, c, BLUE)
                    elif r > 4:
                        self.board[r][c] = Piece(r, c, RED)

    def draw(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = WHITE if (r+c)%2==0 else BLACK
                pygame.draw.rect(screen, color, (c*CELL, r*CELL, CELL, CELL))
                if self.board[r][c]:
                    self.board[r][c].draw()

    def get_piece(self, r, c):
        return self.board[r][c]

    def move(self, piece, r, c):
        self.board[piece.row][piece.col] = None
        piece.row, piece.col = r, c
        self.board[r][c] = piece
        # رفع الملك عند الصف النهائي
        if piece.color == RED and piece.row == 0:
            piece.king = True
        elif piece.color == BLUE and piece.row == ROWS - 1:
            piece.king = True

    def get_all(self, color):
        return [self.board[r][c] for r in range(ROWS) for c in range(COLS)
                if self.board[r][c] and self.board[r][c].color == color]

    def evaluate(self):
        score = 0
        for row in self.board:
            for p in row:
                if p:
                    value = 2 if p.king else 1
                    score += value if p.color == BLUE else -value
        return score

    def copy(self):
        b = Board()
        b.board = [[None]*COLS for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p:
                    cp = Piece(p.row, p.col, p.color)
                    cp.king = p.king
                    b.board[r][c] = cp
        return b

# ================= MOVES =================
def get_moves(board, piece):
    moves = {}
    directions = [-1,1] if piece.king else ([-1] if piece.color==RED else [1])
    for d in directions:
        for dc in [-1,1]:
            r,c = piece.row + d, piece.col + dc
            if 0<=r<ROWS and 0<=c<COLS:
                target = board.get_piece(r,c)
                if target is None:
                    moves[(r,c)] = []
                elif target.color != piece.color:
                    jr,jc = r+d, c+dc
                    if 0<=jr<ROWS and 0<=jc<COLS and board.get_piece(jr,jc) is None:
                        moves[(jr,jc)] = [target]
    return moves

def simulate(board, piece, move, skip):
    board.move(piece, *move)
    for s in skip:
        board.board[s.row][s.col] = None
    return board

# ================= MINIMAX =================
def minimax(board, depth, alpha, beta, max_player):
    if depth == 0:
        return board.evaluate(), board

    best = None
    if max_player:
        max_eval = -math.inf
        for p in board.get_all(BLUE):
            for move, skip in get_moves(board, p).items():
                b = board.copy()
                np = b.get_piece(p.row, p.col)
                simulate(b, np, move, skip)
                val,_ = minimax(b, depth-1, alpha, beta, False)
                if val > max_eval:
                    max_eval, best = val, b
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
        return max_eval, best
    else:
        min_eval = math.inf
        for p in board.get_all(RED):
            for move, skip in get_moves(board, p).items():
                b = board.copy()
                np = b.get_piece(p.row, p.col)
                simulate(b, np, move, skip)
                val,_ = minimax(b, depth-1, alpha, beta, True)
                if val < min_eval:
                    min_eval, best = val, b
                beta = min(beta, val)
                if alpha >= beta:
                    break
        return min_eval, best

# ================= GAME =================
class Game:
    def __init__(self, mode):
        self.board = Board()
        self.turn = RED
        self.mode = mode
        self.selected = None
        self.valid_moves = {}
        self.ai_timer = 0

    def update(self):
        self.board.draw()
        self.draw_moves()
        pygame.display.update()

    def draw_moves(self):
        for (r,c) in self.valid_moves:
            x = c*CELL + CELL // 2
            y = r*CELL + CELL // 2
            pygame.draw.circle(screen, GREEN, (x, y), 12)

    def select(self, r, c):
        piece = self.board.get_piece(r, c)
        if self.selected is None:
            if piece and piece.color == self.turn and get_moves(self.board, piece):
                self.selected = piece
                self.valid_moves = get_moves(self.board, piece)
            return

        if (r,c) in self.valid_moves:
            self.board.move(self.selected, r, c)
            for p in self.valid_moves[(r,c)]:
                self.board.board[p.row][p.col] = None
            self.selected = None
            self.valid_moves = {}
            self.turn = BLUE if self.turn==RED else RED
            return

        self.selected = None
        self.valid_moves = {}

    def ai_move(self, color):
        pieces = self.board.get_all(color)
        movable = [p for p in pieces if get_moves(self.board, p)]
        if not movable:
            return

        if game.mode == "AVA":
            if color == BLUE:
                
                depth = 3
                max_player = True
                _, new_board = minimax(self.board, depth, -math.inf, math.inf, max_player)
                if new_board:
                    self.board = new_board
            else:
                
                piece = random.choice(movable)
                moves = list(get_moves(self.board, piece).keys())
                if moves:
                    move = random.choice(moves)
                    skips = get_moves(self.board, piece)[move]
                    simulate(self.board, piece, move, skips)
        else:
            
            depth = 3
            max_player = (color==BLUE)
            _, new_board = minimax(self.board, depth, -math.inf, math.inf, max_player)
            if new_board:
                self.board = new_board

        self.turn = RED if color==BLUE else BLUE

    def winner(self):
        red_pieces = self.board.get_all(RED)
        blue_pieces = self.board.get_all(BLUE)
        if not red_pieces: return "BLUE"
        if not blue_pieces: return "RED"

        red_moves = any(get_moves(self.board, p) for p in red_pieces)
        blue_moves = any(get_moves(self.board, p) for p in blue_pieces)

        if not red_moves and not blue_moves:
            return "DRAW"
        if not red_moves: return "BLUE"
        if not blue_moves: return "RED"

        return None

# ================= MENU =================
def menu():
    while True:
        screen.fill(GRAY)
        title = BIG_FONT.render("CHECKERS", 1, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        buttons = [
            {"text":"Player vs Player", "rect":pygame.Rect(200, 220, 200, 50), "mode":"PVP"},
            {"text":"Player vs AI", "rect":pygame.Rect(200, 300, 200, 50), "mode":"PVA"},
            {"text":"AI vs AI", "rect":pygame.Rect(200, 380, 200, 50), "mode":"AVA"}
        ]

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for b in buttons:
            color = GREEN if b["rect"].collidepoint(mouse) else BLUE
            pygame.draw.rect(screen, color, b["rect"])
            text = FONT.render(b["text"], 1, WHITE)
            screen.blit(text, (b["rect"].x + b["rect"].width//2 - text.get_width()//2,
                               b["rect"].y + b["rect"].height//2 - text.get_height()//2))
            if b["rect"].collidepoint(mouse) and click[0]:
                pygame.time.delay(200)
                return b["mode"]

        pygame.display.update()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                print("Game closed by user.")
                pygame.quit(); sys.exit()

# ================= MAIN =================
def main():
    global game
    mode = menu()
    game = Game(mode)

    while True:
        clock.tick(30)
        game.update()

        winner = game.winner()
        if winner:
            screen.fill(GRAY)
            if winner == "DRAW":
                msg_text = "Draw!"
            else:
                msg_text = f"{winner} Wins!"
            msg = BIG_FONT.render(msg_text, 1, YELLOW)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            main()

        current_time = pygame.time.get_ticks()

        # AI moves
        if game.mode == "AVA":
            if current_time - game.ai_timer > 500:
                game.ai_move(game.turn)
                game.ai_timer = current_time
        elif game.mode == "PVA" and game.turn == BLUE:
            if current_time - game.ai_timer > 500:
                game.ai_move(BLUE)
                game.ai_timer = current_time

        # Player moves
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("Game closed by user.")
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if game.mode == "PVP" or (game.mode == "PVA" and game.turn == RED):
                    x, y = pygame.mouse.get_pos()
                    game.select(y//CELL, x//CELL)

main()
