# 🎮 Connect 4 — AI Project (Python + Pygame)

## 👥 Team Members
- **Bavly Hany**
- **Mina Saber**
- **Mohamed ElSafty**
- **Paula Moukhtar**

---

## 🎓 Course Information
**Course Name:** *Artificial Intelligence* 

**Instructor:** *Eng. Yousef Elbaroudy*

**Professor** *Dr. Sara Sweidan*

**University:** *Faculty of Computer Science and  Artificial Intelligence-Benha University*  

**Semester:** *Fall 2025 / AI Course Project*

---

## 📌 Project Overview & Requirements
This project is the first phase of a larger application named **“The Playground”**, a multi-game platform.  
Our goal for this phase is to implement a complete **Connect 4 game with a GUI and AI**, following the environment specifications given in the course.

### ✔ Project Requirements
The Connect 4 game must include:

- **Player vs Player** mode  
- **Player vs AI** mode  
- An AI using **Minimax algorithm**  
- **Alpha-Beta pruning** for optimization  
- Clear and accurate **environment classification**  
- Clean code structure and modular design  
- A full **graphical user interface (GUI)**  
- Documentation of the game logic and algorithms  

---

# 📘 Connect 4 Documentation

## 📌 Overview
Connect 4 is a two-player strategy game where players drop discs into a 6×7 grid.  
The first player to connect **four discs in a row** (horizontally, vertically, or diagonally) wins.

Our implementation uses:

- **Python**  
- **Pygame** for GUI  
- **Minimax + Alpha-Beta pruning** for AI decisions  

---

## 🧩 Environment Description (AI Perspective)

### **PEAS Framework**
| Component | Description |
|----------|-------------|
| **Performance Measure** | Winning the game, maximizing score, minimizing opponent moves |
| **Environment** | 6×7 Connect 4 grid (fully displayed in GUI) |
| **Actuators** | Drop disc into column |
| **Sensors** | Board state, valid columns, win/draw detection |

### **Environment Type Classification**
| Property | Type |
|----------|------|
| **Observability** | Fully Observable — the entire board is visible |
| **Agents** | Multi-agent (Competitive) — player vs AI |
| **Determinism** | Deterministic — same action always produces same result |
| **Episodic / Sequential** | Sequential — actions affect future states |
| **Static / Dynamic** | Static — environment doesn’t change without agent moves |
| **Discrete / Continuous** | Discrete — limited actions and states |

---

## 🎨 Graphical User Interface (GUI)
The game uses **Pygame** to create a visually appealing and interactive interface.

### GUI Features
- A 6×7 visual grid  
- Animated disc dropping  
- Column hover highlight  
- Turn indicators  
- Win highlighting (4 discs flashing or colored)  
- Restart and exit options  

#### Optional enhancements for UX :
- Background music  
- Column hover sound  
- Disc drop sound  
- Celebration animation when someone wins  

---

## 🧠 Artificial Intelligence

### 🟦 Minimax Algorithm
The AI evaluates future board states by simulating moves for both:
- **Maximizing agent (AI)**  
- **Minimizing agent (human)**

The algorithm:
1. Explores possible future moves (game tree)  
2. Evaluates board positions  
3. Chooses the move that makes the AI most likely to win  

---

### 🟥 Alpha-Beta Pruning
A performance enhancement to Minimax.

It:
- Cuts branches that do not influence the final decision  
- Makes the AI *much faster*  
- Allows deeper search levels  
- Reduces time from exponential to manageable  

---

### 🟨 Evaluation Function
The evaluation function scores the current board state using:

- **Center control bonus**  
- **Three-in-a-row with open fourth spot**  
- **Two-in-a-row patterns**  
- **Blocking opponent threats**  
- **Immediate win detection**  
- **Immediate loss prevention**

This helps the AI choose smart moves instead of random ones.

---

## 🧠 Game Logic Components
### ✔ Board Representation
- The board is represented as a 6×7 matrix
### ✔ Win Checking
The program checks for:
- Horizontal lines  
- Vertical lines  
- Positive diagonals  
- Negative diagonals  

### ✔ Valid Moves
A move is valid if:
- The chosen column is not full  
- The top cell is empty  

---

## 📁 File / Folder Structure

connect4/

│

├── main.py # Entry point, game loop, state management

├── board.py # Board logic (grid, moves, win detection)

├── gui.py # Graphics, drawing, animations

├── ai.py # Minimax + Alpha-Beta + evaluation function

│

└── assets/ # (Optional) images, sounds, fonts

