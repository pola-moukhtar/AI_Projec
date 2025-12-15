import tkinter as tk
from tkinter import messagebox
import random
import time

WINDOW_SIZE = "500x600"
BG = "#0f172a"
CARD_BACK = "#1e293b"
CARD_FRONT = "#38bdf8"
TEXT = "#e5e7eb"
ACCENT = "#22c55e"
DANGER = "#ef4444"

# ================== AI ==================
class AIPlayer:
    def __init__(self, depth=3):
        self.memory = {} 
        self.depth = depth

    def remember(self, pos, value):
        self.memory.setdefault(value, set()).add(pos)

    def evaluate(self, score_diff, known_pairs):
        return score_diff * 10 + known_pairs * 2

    def minimax(self, available, memory, depth, maximizing, alpha, beta):
        if depth == 0 or len(available) < 2:
            known_pairs = sum(1 for v in memory.values() if len(v) >= 2)
            return self.evaluate(0, known_pairs), None

        best_move = None

        moves = []
        av = list(available)
        for i in range(len(av)):
            for j in range(i + 1, len(av)):
                moves.append((av[i], av[j]))

        if maximizing:
            max_eval = -float("inf")
            for m in moves:
                eval_score = self.simulate(m, memory, depth, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = m
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for m in moves:
                eval_score = self.simulate(m, memory, depth, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = m
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    # ---------------- SIMULATION ----------------
    def simulate(self, move, memory, depth, maximizing, alpha, beta):
        new_memory = {k: set(v) for k, v in memory.items()}

        for pos in move:
            for v, poses in new_memory.items():
                if pos in poses:
                    break
            else:
                new_memory.setdefault("?", set()).add(pos)

        score_diff = 1 if maximizing else -1
        eval_score, _ = self.minimax(
            set(), new_memory, depth - 1, maximizing, alpha, beta
        )
        return eval_score + score_diff

    # ---------------- PUBLIC MOVE ----------------
    def choose(self, available):
        for value, poses in self.memory.items():
            valid = [p for p in poses if p in available]
            if len(valid) >= 2:
                return valid[0], valid[1]

        _, move = self.minimax(
            available,
            self.memory,
            self.depth,
            True,
            -float("inf"),
            float("inf"),
        )

        if move:
            return move

        return random.sample(list(available), 2)

# ================== GAME ==================
class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.root.geometry(WINDOW_SIZE)
        self.root.config(bg=BG)
        self.root.resizable(False, False)

        self.mode = tk.StringVar(value="PVP")
        self.size = tk.StringVar(value="4x4")

        self.game_id = 0
        self.menu_screen()

    # ================= MENU =================
    def menu_screen(self):
        self.game_id += 1
        self.clear()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Label(frame, text="🧠 Memory Game",
                 fg=TEXT, bg=BG,
                 font=("Arial", 22, "bold")).pack(pady=15)

        tk.Label(frame, text="Game Mode",
                 fg=ACCENT, bg=BG,
                 font=("Arial", 14, "bold")).pack()

        for text, val in [("Player vs Player", "PVP"),
                          ("Player vs Computer", "PVC"),
                          ("Computer vs Computer", "CVC")]:
            tk.Radiobutton(frame, text=text, value=val,
                           variable=self.mode,
                           fg=TEXT, bg=BG,
                           selectcolor="#020617",
                           font=("Arial", 12)).pack(anchor="w", padx=80)

        tk.Label(frame, text="Difficulty",
                 fg=ACCENT, bg=BG,
                 font=("Arial", 14, "bold")).pack(pady=(10, 0))

        for text, val in [("4 x 4", "4x4"), ("6 x 6", "6x6")]:
            tk.Radiobutton(frame, text=text, value=val,
                           variable=self.size,
                           fg=TEXT, bg=BG,
                           selectcolor="#020617",
                           font=("Arial", 12)).pack(anchor="w", padx=80)

        tk.Button(frame, text="Start Game",
                  bg=ACCENT, fg="black",
                  font=("Arial", 14, "bold"),
                  width=15,
                  command=self.start).pack(pady=20)

    # ================= START =================
    def start(self):
        self.game_id += 1
        self.clear()

        self.rows, self.cols = (4, 4) if self.size.get() == "4x4" else (6, 6)
        self.total_pairs = (self.rows * self.cols) // 2

        self.turn = 1
        self.scores = {1: 0, 2: 0}
        self.first = self.second = None
        self.lock = False

        self.ai1 = AIPlayer()
        self.ai2 = AIPlayer()

        self.timer_start = time.time()

        self.top_ui()
        self.create_board()
        self.update_timer(self.game_id)

        if self.mode.get() == "CVC":
            self.root.after(800, self.ai_move, self.game_id)

    # ================= TOP UI =================
    def top_ui(self):
        top = tk.Frame(self.root, bg=BG)
        top.pack()

        self.info = tk.Label(top, text="Player 1 Turn",
                             fg=TEXT, bg=BG,
                             font=("Arial", 12))
        self.info.pack()

        self.timer = tk.Label(top, text="Time: 0s",
                              fg=TEXT, bg=BG)
        self.timer.pack()

        score = tk.Frame(self.root, bg=BG)
        score.pack()

        self.s1 = tk.Label(score, text="P1: 0", fg=TEXT, bg=BG)
        self.s1.pack(side="left", padx=30)

        self.s2 = tk.Label(score, text="P2: 0", fg=TEXT, bg=BG)
        self.s2.pack(side="right", padx=30)

        btns = tk.Frame(self.root, bg=BG)
        btns.pack(pady=5)

        tk.Button(btns, text="🔁 Restart",
                  bg=ACCENT, width=10,
                  command=self.start).pack(side="left", padx=5)

        tk.Button(btns, text="⬅ Menu",
                  bg=DANGER, width=10,
                  command=self.menu_screen).pack(side="left", padx=5)

    # ================= BOARD =================
    def create_board(self):
        self.board = tk.Frame(self.root, bg=BG)
        self.board.pack(pady=10)

        values = list(range(1, self.total_pairs + 1)) * 2
        random.shuffle(values)

        self.cards = {}
        idx = 0

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.board, text="",
                                width=6, height=3,
                                bg=CARD_BACK,
                                font=("Arial", 16, "bold"),
                                command=lambda p=(r, c): self.flip(p))
                btn.grid(row=r, column=c, padx=4, pady=4)
                self.cards[(r, c)] = {
                    "value": values[idx],
                    "btn": btn,
                    "open": False
                }
                idx += 1

    # ================= ANIMATION =================
    def animate_flip(self, pos, show=True, step=0):
        card = self.cards[pos]
        btn = card["btn"]

        if step <= 5:
            btn.config(width=6-step)
            self.root.after(30, self.animate_flip, pos, show, step+1)
        elif step <= 10:
            if show:
                btn.config(text=str(card["value"]), bg=CARD_FRONT)
            else:
                btn.config(text="", bg=CARD_BACK)
            btn.config(width=step-4)
            self.root.after(30, self.animate_flip, pos, show, step+1)
        else:
            card["open"] = show

    # ================= GAME LOGIC =================
    def flip(self, pos):
        if self.lock or self.cards[pos]["open"]:
            return

        self.animate_flip(pos, True)

        self.ai1.remember(pos, self.cards[pos]["value"])
        self.ai2.remember(pos, self.cards[pos]["value"])

        if not self.first:
            self.first = pos
        else:
            self.second = pos
            self.lock = True
            self.root.after(700, self.check)

    def check(self):
        c1 = self.cards[self.first]
        c2 = self.cards[self.second]

        if c1["value"] == c2["value"]:
            self.scores[self.turn] += 1
        else:
            self.animate_flip(self.first, False)
            self.animate_flip(self.second, False)
            self.turn = 2 if self.turn == 1 else 1

        self.first = self.second = None
        self.lock = False
        self.update_labels()
        self.check_end()

        if self.mode.get() == "CVC" or (self.mode.get() == "PVC" and self.turn == 2):
            self.root.after(600, self.ai_move, self.game_id)

    # ================= AI =================
    def ai_move(self, gid):
        if gid != self.game_id:
            return

        available = {p for p, v in self.cards.items() if not v["open"]}
        if len(available) < 2:
            return

        ai = self.ai2 if self.turn == 2 else self.ai1
        p1, p2 = ai.choose(available)

        self.flip(p1)
        self.root.after(400, lambda: self.flip(p2))

    # ================= UTILS =================
    def update_labels(self):
        self.info.config(text=f"Player {self.turn} Turn")
        self.s1.config(text=f"P1: {self.scores[1]}")
        self.s2.config(text=f"P2: {self.scores[2]}")

    def update_timer(self, gid):
        if gid != self.game_id:
            return
        self.timer.config(text=f"Time: {int(time.time()-self.timer_start)}s")
        self.root.after(1000, self.update_timer, gid)

    def check_end(self):
        if sum(self.scores.values()) == self.total_pairs:
            msg = "Draw!"
            if self.scores[1] > self.scores[2]:
                msg = "Player 1 Wins 🎉"
            elif self.scores[2] > self.scores[1]:
                msg = "Player 2 Wins 🎉"
            messagebox.showinfo("Game Over", msg)

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    MemoryGame(root)
    root.mainloop()
