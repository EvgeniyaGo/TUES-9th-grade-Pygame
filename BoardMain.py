# This is the main file. It is responsible for handling user input and current game state.

import pygame as p
import BoardEngine

# Constants for the pygame
WIDTH = HEIGHT = 500
DIMENTIONS = 5  # Board is 5x5
SQ_SIZE = WIDTH // DIMENTIONS
FPS = 25
IMAGES = {}

# Initialize global dictionary of images
def LoadImages():
    IMAGES['BN'] = p.image.load('images/bunny.png')

# Main function
def main():
    # Beginning setup
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = BoardEngine.GameState()  # Get access to the variables from BoardEngine.py
    LoadImages()
    
    # Variables
    sq_selected = [2, 2] # Keep track of the last click of the player (row, col)
    bunny_pos = [2, 2]
    
    game_on = True
    while game_on:
        for event in p.event.get():
            if event.type == p.QUIT:
                game_on = False
            
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x,y location of the mouse
                sq_selected[0] = location[1]//SQ_SIZE
                sq_selected[1] = location[0]//SQ_SIZE
                if sq_selected != bunny_pos:  # if we clicked not on position of the bunny move it
                    gs.board[bunny_pos[0]][bunny_pos[1]] = "--"
                    bunny_pos[0] = sq_selected[0]
                    bunny_pos[1] = sq_selected[1]
                    gs.board[sq_selected[0]][sq_selected[1]] = "BN"
                sq_selected = [int, int]

        drawGameState(screen, gs)
        clock.tick(FPS)
        p.display.flip()

# Handle rendering the graphics of the game
def drawGameState(screen, gs):
    drawBoard(screen)  # Draw the squares on the board
    drawPieces(screen, gs.board)  # Draw the pieces on top of the squares

def drawBoard(screen):
    colors = [(118, 180, 70), (129, 188, 88)]
    counter = 0
    for row in range(DIMENTIONS):  # top -> bottom
        for col in range(DIMENTIONS):  # left -> right
            color = colors[counter]
            counter += 1
            if counter > 1:
                counter = 0
            p.draw.rect(screen, color, p.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENTIONS):  # top -> bottom
        for col in range(DIMENTIONS):  # left -> right
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    col * SQ_SIZE + 18, row * SQ_SIZE + 18, SQ_SIZE, SQ_SIZE))

main()
