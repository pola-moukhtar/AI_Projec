import pygame
import subprocess
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font(None, 48)

games = [
    ("Connect 4", "Connect4.py"),
    ("Memory Game", "MemoryGame.py"),
    ("Checkers", "Checkers.py")
]

running = True
while running:
    screen.fill((30, 30, 30))
    y = 50
    for i, (name, file) in enumerate(games):
        label = font.render(f"{i+1}. {name}", True, (255,255,255))
        rect = label.get_rect(center=(300, y))
        screen.blit(label, rect)
        y += 70

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                subprocess.Popen([sys.executable, games[0][1]])
            if event.key == pygame.K_2:
                subprocess.Popen([sys.executable, games[1][1]])
            if event.key == pygame.K_3:
                subprocess.Popen([sys.executable, games[2][1]])

pygame.quit()
