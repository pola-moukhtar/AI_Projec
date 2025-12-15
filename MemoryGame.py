import tkinter as tk
from tkinter import messagebox
import copy
import random

class MemoryGameMinMax:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Game with MinMax")

        letters = [chr(i) for i in range(65, 73)] * 2
        random.shuffle(letters)
        self.grid = [[letters[i*4 + j] for j in range(4)] for i in range(4)]
        self.revealed = [[False]*4 for _ in range(4)]
        self.buttons = [[None]*4 for _ in range(4)]

        self.first_choice = None
        self.second_choice = None
        self.turn = "human"

        self.create_buttons()
        self.root.mainloop()

    #________________________________________________________________________________________________________
    def create_buttons(self):
        for r in range(4):
            for c in range(4):
                btn = tk.Button(self.root, text=" ", width=6, height=3,
                                command=lambda row=r, col=c: self.human_click(row, col))
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = btn

    #________________________________________________________________________________________________________
    def human_click(self, r, c):
        if self.revealed[r][c] or self.turn != "human":
            return
        self.reveal_cell(r, c)
        if not self.first_choice:
            self.first_choice = (r, c)
        else:
            self.second_choice = (r, c)
            self.root.after(500, self.check_match)

    #________________________________________________________________________________________________________
    def reveal_cell(self, r, c):
        self.buttons[r][c]['text'] = self.grid[r][c]
        self.revealed[r][c] = True

    def hide_cell(self, r, c):
        self.buttons[r][c]['text'] = " "
        self.revealed[r][c] = False

    #________________________________________________________________________________________________________
    def check_match(self):
        r1, c1 = self.first_choice
        r2, c2 = self.second_choice
        if self.grid[r1][c1] != self.grid[r2][c2]:
            self.hide_cell(r1, c1)
            self.hide_cell(r2, c2)
        self.first_choice = None
        self.second_choice = None

        if self.check_terminal():
            messagebox.showinfo("Game Over", "All cells revealed! Game finished!")
        else:
            self.turn = "computer"
            self.root.after(500, self.computer_play)

    #________________________________________________________________________________________________________
    def available_actions(self, state, revealed):
        hidden = [(r, c) for r in range(4) for c in range(4) if not revealed[r][c]]
        actions = []
        for i in range(len(hidden)):
            for j in range(i+1, len(hidden)):
                actions.append((hidden[i], hidden[j]))
        return actions

    #________________________________________________________________________________________________________
    def take_action(self, state, revealed, action):
        new_state = copy.deepcopy(state)
        new_revealed = copy.deepcopy(revealed)
        (r1, c1), (r2, c2) = action
        new_revealed[r1][c1] = True
        new_revealed[r2][c2] = True
        match = new_state[r1][c1] == new_state[r2][c2]
        if not match:
            new_revealed[r1][c1] = False
            new_revealed[r2][c2] = False
        return new_state, new_revealed, match

    #________________________________________________________________________________________________________
    def check_terminal_state(self, revealed):
        for row in revealed:
            if False in row:
                return False
        return True

    #________________________________________________________________________________________________________
    def MinMax(self, state, revealed, is_computer, depth=0):
        if self.check_terminal_state(revealed) or depth >= 3:  # depth limit
            return 0
        # باقي الكود
        for action in actions:
            new_state, new_revealed, match = self.take_action(state, revealed, action)
            if match:
                score = (1 if not is_computer else -1) + self.MinMax(new_state, new_revealed, is_computer, depth+1)
            else:
                score = self.MinMax(new_state, new_revealed, not is_computer, depth+1)


    #________________________________________________________________________________________________________
    def computer_play(self):
        actions = self.available_actions(self.grid, self.revealed)
        best_score = float('inf')
        best_action = None

        for action in actions:
            new_state, new_revealed, match = self.take_action(self.grid, self.revealed, action)
            score = self.MinMax(new_state, new_revealed, True)
            if score < best_score:
                best_score = score
                best_action = action

        (r1, c1), (r2, c2) = best_action
        self.reveal_cell(r1, c1)
        self.reveal_cell(r2, c2)
        self.root.update()
        self.root.after(500, lambda: self.check_computer_match(r1, c1, r2, c2))

    #________________________________________________________________________________________________________
    def check_computer_match(self, r1, c1, r2, c2):
        if self.grid[r1][c1] != self.grid[r2][c2]:
            self.hide_cell(r1, c1)
            self.hide_cell(r2, c2)

        if self.check_terminal():
            messagebox.showinfo("Game Over", "All cells revealed! Game finished!")
        else:
            self.turn = "human"

    #________________________________________________________________________________________________________
    def check_terminal(self):
        for row in self.revealed:
            if False in row:
                return False
        return True

# Run the game
MemoryGameMinMax()
