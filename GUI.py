import pygame
import sys
import math
import random

pygame.init()

# ============================ CONFIG ============================
WIDTH, HEIGHT = 700, 700
ROWS, COLS = 6, 7
CELL_SIZE = WIDTH // COLS
RADIUS = CELL_SIZE // 2 - 5

BG_COLOR = (18, 20, 35)
BOARD_COLOR = (50, 70, 140)
EMPTY_COLOR = (25, 25, 25)
X_COLOR = (255, 90, 90)
O_COLOR = (90, 200, 255)
TEXT_COLOR = (240, 240, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 – Modern AI Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30, bold=True)
small_font = pygame.font.SysFont("arial", 22)

# ============================ GAME LOGIC ============================
class Connect4:
    def __init__(self):
        self.grid = [[" " for _ in range(COLS)] for _ in range(ROWS)]

    def copy(self):
        g = Connect4()
        g.grid = [row[:] for row in self.grid]
        return g

    def current_player(self):
        x = sum(row.count('X') for row in self.grid)
        o = sum(row.count('O') for row in self.grid)
        return 'X' if x == o else 'O'

    def available_cols(self):
        return [c for c in range(COLS) if self.grid[0][c] == " "]

    def drop_piece(self, col, player):
        for r in reversed(range(ROWS)):
            if self.grid[r][col] == " ":
                self.grid[r][col] = player
                return r

    def check_terminal(self):
        def win(p): return 1 if p == 'X' else -1

        for r in range(ROWS):
            for c in range(COLS - 3):
                if self.grid[r][c] != " " and all(self.grid[r][c+i] == self.grid[r][c] for i in range(4)):
                    return win(self.grid[r][c])
        for c in range(COLS):
            for r in range(ROWS - 3):
                if self.grid[r][c] != " " and all(self.grid[r+i][c] == self.grid[r][c] for i in range(4)):
                    return win(self.grid[r][c])
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if self.grid[r][c] != " " and all(self.grid[r+i][c+i] == self.grid[r][c] for i in range(4)):
                    return win(self.grid[r][c])
                if self.grid[r+3][c] != " " and all(self.grid[r+3-i][c+i] == self.grid[r+3][c] for i in range(4)):
                    return win(self.grid[r+3][c])

        if all(self.grid[0][c] != " " for c in range(COLS)):
            return 0
        return None

    # ============================ AI ============================
    def heuristic(self):
        score = 0
        center = [self.grid[r][COLS // 2] for r in range(ROWS)]
        score += center.count('X') * 3
        score -= center.count('O') * 3
        return score

    def minimax(self, depth, alpha, beta, maximizing):
        terminal = self.check_terminal()
        if terminal is not None or depth == 0:
            return terminal if terminal is not None else self.heuristic()

        if maximizing:
            value = -math.inf
            for col in self.available_cols():
                g = self.copy()
                g.drop_piece(col, 'X')
                value = max(value, g.minimax(depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for col in self.available_cols():
                g = self.copy()
                g.drop_piece(col, 'O')
                value = min(value, g.minimax(depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def best_move(self, depth):
        player = self.current_player()
        best_val = -math.inf if player == 'X' else math.inf
        best_col = random.choice(self.available_cols())

        for col in self.available_cols():
            g = self.copy()
            g.drop_piece(col, player)
            val = g.minimax(depth-1, -math.inf, math.inf, player == 'O')
            if player == 'X' and val > best_val:
                best_val, best_col = val, col
            if player == 'O' and val < best_val:
                best_val, best_col = val, col
        return best_col

# ============================ DRAWING ============================
def draw_board(game, falling=None, info=""):
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BOARD_COLOR, (0, CELL_SIZE, WIDTH, HEIGHT))

    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = (r + 1) * CELL_SIZE + CELL_SIZE // 2
            color = EMPTY_COLOR
            if game.grid[r][c] == 'X': color = X_COLOR
            if game.grid[r][c] == 'O': color = O_COLOR
            pygame.draw.circle(screen, color, (x, y), RADIUS)

    if falling:
        col, y, player = falling
        x = col * CELL_SIZE + CELL_SIZE // 2
        color = X_COLOR if player == 'X' else O_COLOR
        pygame.draw.circle(screen, color, (x, y), RADIUS)

    label = small_font.render(info, True, TEXT_COLOR)
    screen.blit(label, (10, 10))
    pygame.display.update()

# ============================ ANIMATION ============================
def animate_drop(game, col, row, player, info=""):
    y = CELL_SIZE // 2
    target_y = (row + 1) * CELL_SIZE + CELL_SIZE // 2
    while y < target_y:
        y += 25
        draw_board(game, (col, y, player), info)
        clock.tick(60)

# ============================ MENU ============================
def menu():
    while True:
        screen.fill(BG_COLOR)
        title = font.render("CONNECT 4", True, TEXT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        options = ["1 - Human vs Human", "2 - Human vs AI", "3 - AI vs AI", "Press 1 / 2 / 3"]
        for i, text in enumerate(options):
            t = small_font.render(text, True, TEXT_COLOR)
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 220 + i*40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return 1
                if event.key == pygame.K_2: return 2
                if event.key == pygame.K_3: return 3

# ============================ MAIN LOOP ============================
def main():
    mode = menu()
    depth = 4
    game = Connect4()
    running = True

    while running:
        clock.tick(60)
        draw_board(game)

        player = game.current_player()
        ai_turn = (mode == 3) or (mode == 2 and player == 'O')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if not ai_turn and event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL_SIZE
                if col in game.available_cols():
                    row = game.drop_piece(col, player)
                    animate_drop(game, col, row, player)

        if ai_turn:
            draw_board(game, info="AI thinking...")
            pygame.time.wait(400)
            col = game.best_move(depth)
            row = game.drop_piece(col, player)
            animate_drop(game, col, row, player, "AI played")

        result = game.check_terminal()
        if result is not None:
            text = "Draw" if result == 0 else ("X Wins" if result == 1 else "O Wins")
            label = font.render(text, True, TEXT_COLOR)
            screen.blit(label, (WIDTH//2 - label.get_width()//2, 20))
            pygame.display.update()
            pygame.time.wait(3000)
            return

main()