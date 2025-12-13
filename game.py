class Connect4:
    ROWS = 6
    COLS = 7

    def __init__(self):
        self.initial_grid = [[" " for _ in range(self.COLS)] for _ in range(self.ROWS)]

    # ____________________________________________________________________
    def display_grid(self, state):
        print()
        for r in range(self.ROWS):
            print("|", end="")
            for c in range(self.COLS):
                print(f" {state[r][c]} |", end="")
            print()
        print(" " + "--- " * self.COLS)
        print(" ", end="")
        for c in range(self.COLS):
            print(f" {c}  ", end="")
        print("\n")

    # ____________________________________________________________________
    def current_player(self, state):
        count_X = sum(row.count('X') for row in state)
        count_O = sum(row.count('O') for row in state)
        return 'X' if count_X == count_O else 'O'

    # ____________________________________________________________________
    def available_actions(self, state):
        player = self.current_player(state)
        return [(player, c) for c in range(self.COLS) if state[0][c] == " "]

    # ____________________________________________________________________
    def take_action(self, state, action):
        player, col = action
        new_state = [row[:] for row in state]
        for r in reversed(range(self.ROWS)):
            if new_state[r][col] == " ":
                new_state[r][col] = player
                break
        return new_state

    # ____________________________________________________________________
    def check_terminal(self, state):
        def winner(p): return 1 if p == 'X' else -1

        # Horizontal & Vertical
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if state[r][c] != " " and all(state[r][c+i] == state[r][c] for i in range(4)):
                    return winner(state[r][c])
        for c in range(self.COLS):
            for r in range(self.ROWS - 3):
                if state[r][c] != " " and all(state[r+i][c] == state[r][c] for i in range(4)):
                    return winner(state[r][c])

        # Diagonals
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if state[r][c] != " " and all(state[r+i][c+i] == state[r][c] for i in range(4)):
                    return winner(state[r][c])
                if state[r+3][c] != " " and all(state[r+3-i][c+i] == state[r+3][c] for i in range(4)):
                    return winner(state[r+3][c])

        if all(state[0][c] != " " for c in range(self.COLS)):
            return 0

        return "Not terminal"

     # ____________________________________________________________________
    def heuristic(self, state):
        score = 0
        center = [state[r][self.COLS // 2] for r in range(self.ROWS)]
        score += center.count('X') * 3
        score -= center.count('O') * 3
        return score

    # ____________________________________________________________________
    def MinMax(self, state, depth, alpha, beta, maximizing):
        terminal = self.check_terminal(state)
        if terminal != "Not terminal" or depth == 0:
            return terminal if terminal != "Not terminal" else self.heuristic(state)

        if maximizing:
            value = -float('inf')
            for action in self.available_actions(state):
                value = max(value, self.MinMax(self.take_action(state, action), depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for action in self.available_actions(state):
                value = min(value, self.MinMax(self.take_action(state, action), depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    # ____________________________________________________________________
    def computer_play(self, state, depth=4):
        player = self.current_player(state)
        print(f"Computer ({player}) turn")
        actions = self.available_actions(state)
        scores = []
        for action in actions:
            next_state = self.take_action(state, action)
            score = self.MinMax(next_state, depth, -float('inf'), float('inf'), player == 'O')
            scores.append(score)
        best = max(scores) if player == 'X' else min(scores)
        index = scores.index(best)
        new_state = self.take_action(state, actions[index])
        self.display_grid(new_state)
        return new_state

    # ____________________________________________________________________
    def human_play(self, state):
        self.display_grid(state)
        player = self.current_player(state)
        col = int(input(f"Player {player}, choose column: "))
        return self.take_action(state, (player, col))


# ============================ GAME LOOP ============================

game = Connect4()
state = game.initial_grid

print("Choose mode:\n1) Human vs Human\n2) Human vs AI\n3) AI vs AI")
mode = int(input("Your choice: "))

while game.check_terminal(state) == "Not terminal":
    if mode == 1:
        state = game.human_play(state)
    elif mode == 2:
        if game.current_player(state) == 'X':
            state = game.human_play(state)
        else:
            state = game.computer_play(state)
    else:
        state = game.computer_play(state)

result = game.check_terminal(state)
if result == 1:
    print("X wins!")
elif result == -1:
    print("O wins!")
else:
    print("Draw!")
