import pygame
import sys
import math
import random

pygame.init()

# ================= CONFIG =================
WIDTH, HEIGHT = 700, 700
ROWS, COLS = 6, 7
CELL = WIDTH // COLS
RADIUS = CELL // 2 - 6

BG = (18, 20, 35)
BOARD = (50, 70, 140)
EMPTY = (25, 25, 25)
X_COLOR = (255, 90, 90)
O_COLOR = (90, 200, 255)
TEXT = (240, 240, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 – AI Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32, bold=True)
small = pygame.font.SysFont("arial", 22)

# ================= LOGIC ENGINE =================
class Connect4:
    ROWS = 6
    COLS = 7

    def initial_state(self):
     return [[" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "]]

    def current_player(self, state):
        count_X = 0
        count_O = 0
        for row in range(6):
            for col in range(7):
                symbol = state[row][col]
                if symbol == 'X':
                    count_X += 1
                elif symbol == 'O':
                    count_O += 1

        # If they are the same, it's player X's turn
        if count_X == count_O:
            return 'X'
        # Otherwise, it's player O's turn
        return 'O'

    def available_actions(self, state):
        player = self.current_player(state)
        return [(player, c) for c in range(self.COLS) if state[0][c] == " "]

    def take_action(self, state, action):
        player, col = action
        new = [row[:] for row in state]
        for r in reversed(range(self.ROWS)):
            if new[r][col] == " ":
                new[r][col] = player
                break
        return new

    def terminal(self, state):
        terminal = False
        full = False
        player = None
        for row in range(6):
            for col in range(4):
                if state[row][col] == state[row][col+1] == state[row][col+2] == state[row][col+3] and state[row][col] != " ":
                    terminal = True
                    player = state[row][col]
                    break
            if terminal:
                break

        if  terminal==False:
            for col in range(7):
                for row in range(3):  
                    if state[row][col] == state[row+1][col] == state[row+2][col] == state[row+3][col] and state[row][col] != " ":
                        terminal = True
                        player = state[row][col]
                        break
                if terminal:
                    break

        if terminal==False:
            for row in range(3): #    \
                for col in range(4):
                    if state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3] and state[row][col] != " ":
                        terminal = True
                        player = state[row][col]
                        break
                if terminal:
                    break

        if terminal==False:
            for row in range(3):#0->2 /    row+1
                for col in range(3, 7):# 3->6      col-1        
                    if state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3] and state[row][col] != " ":
                        terminal = True
                        player = state[row][col]
                        break
                if terminal:
                    break

        if terminal==False:
            empty_count = 0
            for row in range(6):
                for col in range(7):
                    if state[row][col] == " ":
                        empty_count += 1
            if empty_count == 0:
                full = True

        if terminal:
            if player == "X":
                return 1
            elif player == "O":
                return -1
        elif full:
            return 0
        else:
            return None


    def heuristic(self, state):
        score = 0
        center = [state[r][self.COLS // 2] for r in range(self.ROWS)]
        score += center.count('X') * 3
        score -= center.count('O') * 3
        return score

    def minimax(self, state, depth, alpha, beta, maximizing):
        term = self.terminal(state)
        if term is not None or depth == 0:
            return term if term is not None else self.heuristic(state)

        if maximizing:
            value = -math.inf
            for a in self.available_actions(state):
                value = max(value, self.minimax(
                    self.take_action(state, a), depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta: break
            return value
        else:
            value = math.inf
            for a in self.available_actions(state):
                value = min(value, self.minimax(
                    self.take_action(state, a), depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta: break
            return value

    def best_action(self, state, depth):
        player = self.current_player(state)
        actions = self.available_actions(state)
        best = -math.inf if player == 'X' else math.inf
        choice = random.choice(actions)

        for a in actions:
            val = self.minimax(self.take_action(state, a),
                               depth-1, -math.inf, math.inf,
                               player == 'O')
            if player == 'X' and val > best:
                best, choice = val, a
            if player == 'O' and val < best:
                best, choice = val, a
        return choice

# ================= GUI =================
def draw(state, msg=""):
    screen.fill(BG)
    pygame.draw.rect(screen, BOARD, (0, CELL, WIDTH, HEIGHT))

    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL + CELL // 2
            y = (r + 1) * CELL + CELL // 2
            color = EMPTY
            if state[r][c] == 'X': color = X_COLOR
            if state[r][c] == 'O': color = O_COLOR
            pygame.draw.circle(screen, color, (x, y), RADIUS)

    label = small.render(msg, True, TEXT)
    screen.blit(label, (10, 10))
    pygame.display.update()

# ================= MENU =================
def menu():
    mode = None
    depth = 4

    while True:
        screen.fill(BG)
        title = font.render("CONNECT 4", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        options = [
            "1 - Human vs Human",
            "2 - Human vs AI",
            "3 - AI vs AI",
            f"AI Depth: {depth}  (UP / DOWN)",
            "Press Number to Start"
        ]

        for i, txt in enumerate(options):
            t = small.render(txt, True, TEXT)
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 220 + i*40))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: mode = 1
                if e.key == pygame.K_2: mode = 2
                if e.key == pygame.K_3: mode = 3
                if e.key == pygame.K_UP and depth < 6: depth += 1
                if e.key == pygame.K_DOWN and depth > 1: depth -= 1
                if mode:
                    return mode, depth

# ================= MAIN =================
def main():
    mode, depth = menu()
    game = Connect4()
    state = game.initial_state()

    while True:
        clock.tick(60)
        draw(state)

        player = game.current_player(state)
        ai_turn = (mode == 3) or (mode == 2 and player == 'O')

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if not ai_turn and e.type == pygame.MOUSEBUTTONDOWN:
                col = e.pos[0] // CELL
                if col in [c for _, c in game.available_actions(state)]:
                    state = game.take_action(state, (player, col))

        if ai_turn:
            draw(state, "AI thinking...")
            pygame.time.wait(300)
            state = game.take_action(state, game.best_action(state, depth))

        result = game.terminal(state)
        if result is not None:
            msg = "Draw" if result == 0 else ("X Wins" if result == 1 else "O Wins")
            draw(state, msg)
            pygame.time.wait(3000)
            return

main()