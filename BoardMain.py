# This is the main file. It is responsible for handling user input and current game state.

import pygame as p
import random
import time 

# Constants for the pygame
# For the game screen size (630 so it can be devided by 5, 7 and 9 squares)
WIDTH = 630
HEIGHT = 630  # For the game screen size
BORDER = 30  # For spacing left and right
REAL_HEIGHT = HEIGHT + BORDER * 4 + 150  # For game real screen size (900)
REAL_WIDTH = WIDTH + BORDER * 2  # For game real screen size (690)

DIMENTIONS = 3  # Board is DIMENTIONSxDIMENTIONS
SQ_SIZE = WIDTH // DIMENTIONS
SPACING = SQ_SIZE // 6
FPS = 25
IMAGES = {}

# Initialize global dictionary of images. Runned once
def LoadImages():
    IMAGES['BN'] = p.image.load('images/bunny.png')
    IMAGES['CR'] = p.image.load('images/carrot.png')
    IMAGES['HM'] = p.image.load('images/cave.png')

# Handles rendering the graphics of the game
def drawGameState(screen, board, bunny_pos):
    drawBoard(screen)
    drawPieces(screen, board, bunny_pos)

# Handles adding element (home, carrot, e.t.c) to the new generated game
def addElement(screen, board, element):
    pos_x = random.randint(0, DIMENTIONS-1)
    pos_y = random.randint(0, DIMENTIONS-1)
    while (board[pos_x][pos_y] != "--"):
        pos_x = random.randint(0, DIMENTIONS-1)
        pos_y = random.randint(0, DIMENTIONS-1)
    board[pos_x][pos_y] = element
    return [pos_x, pos_y]  # Needed only for having the position of the bunny

# Generates new random game set (house, carrots, e.t.c). Returns the new position of the bunny
def generateGame(screen, board, levels_passed):
    bunny_pos = addElement(screen, board, "BN")
    counter = 0
    if DIMENTIONS > 9:
        while counter < 5:
            counter += 1
            addElement(screen, board, "CR")
    elif DIMENTIONS > 3:
        while counter < 3:
            counter += 1
            addElement(screen, board, "CR")
    elif levels_passed > 0:
        addElement(screen, board, "CR")
    addElement(screen, board, "HM")
    return bunny_pos

# Draw the board DIMENTIONS x DIMENTIONS
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
                BORDER + col * SQ_SIZE, BORDER * 3 + row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Add all pieces to the board
def drawPieces(screen, board, bunny_pos):
    for row in range(DIMENTIONS):  # top -> bottom
        for col in range(DIMENTIONS):  # left -> right
            piece = board[row][col]
            if piece != "--": # if it's not empty slot
                if piece == "CR": # if it's a carrot - make it smaller
                    spacing_for_piece = SPACING * 3
                else:
                    spacing_for_piece = SPACING * 2
                resized_image = p.transform.scale(
                    IMAGES[piece], (SQ_SIZE - spacing_for_piece, SQ_SIZE - spacing_for_piece))
                screen.blit(resized_image, p.Rect(
                    BORDER + col * SQ_SIZE + spacing_for_piece // 2, BORDER * 3 + row * SQ_SIZE + spacing_for_piece // 2, SQ_SIZE, SQ_SIZE))
                if piece == "BN":
                    # This draws the circles where bunny can go. The code below generates a circle directly at the position of the bunny and is used as beginning point:
                    # p.draw.circle(screen, (156, 206, 121), (bunny_pos[1] * SQ_SIZE + SQ_SIZE // 2 + BORDER, bunny_pos[0] * SQ_SIZE + BORDER * 3 + SQ_SIZE // 2), 8)
                    count_vert = -SQ_SIZE
                    while count_vert <= SQ_SIZE:
                        count_horz = -SQ_SIZE
                        while count_horz <= SQ_SIZE:
                            if count_horz == 0 and count_vert == 0:
                                pass
                            else:
                                circle_pos_x = bunny_pos[1] * SQ_SIZE + \
                                    SQ_SIZE // 2 + BORDER + count_horz
                                circle_pos_y = bunny_pos[0] * SQ_SIZE + \
                                    BORDER * 3 + SQ_SIZE // 2 + count_vert
                                if circle_pos_x < WIDTH + BORDER and circle_pos_x > BORDER and circle_pos_y > BORDER * 3 and circle_pos_y < HEIGHT + BORDER * 3:
                                    p.draw.circle(
                                        screen, (156, 206, 121), (circle_pos_x, circle_pos_y), 8)
                            count_horz += SQ_SIZE
                        count_vert += SQ_SIZE

# Return a new 2d array filled with "--"
def emptyBoard():
    board = []
    row = col = 0
    while row < DIMENTIONS:
        board.append([])
        while col < DIMENTIONS:
            board[row].append("--")
            col += 1
        row += 1
        col = 0
    return board

# Rerender the top part of the screen where is "Score: ..."
def renderText(screen, font, score_this, text_surface, spacing, levels_passed):
    screen.fill((110, 170, 75), (0, spacing, REAL_WIDTH, text_surface.get_height()))
    text_surface = font.render("Level " + str(levels_passed) + "  |  Score: " + str(score_this), True, (255, 255, 255))
    screen.blit(text_surface, ((REAL_WIDTH - text_surface.get_width()) // 2, BORDER))                        

def endGame(screen):
    frame_count = 0
    while frame_count < 2000:
        current_color = p.Color.lerp(p.Color(0, 0, 0), p.Color(60, 90, 40), frame_count / 2000)
        screen.fill(current_color)
        p.display.update()
        frame_count += 1
    
    while(True): 
        pass

# Main function
def main():
    # Beginning setup
    p.init()
    global DIMENTIONS
    global SQ_SIZE
    global SPACING

    screen = p.display.set_mode((REAL_WIDTH, REAL_HEIGHT))
    clock = p.time.Clock()
    screen.fill((110, 170, 75))

    # Variables
    sq_selected = [0, 0] # Keep track of the last click of the player (row, col)
    score_this = 0
    moves_left = int(DIMENTIONS * 1.5)
    levels_passed = 0

    # Functions before game starts
    LoadImages()
    board = emptyBoard()
    bunny_pos = generateGame(screen, board, levels_passed) # Generates random setting and returns the pos. of the bunny

    # Texts initialization
    font = p.font.Font(None, int(BORDER * 1.5))
    text_score_surface = font.render("Level " + str(levels_passed) + "  |  Score: " + str(score_this), True, (255, 255, 255))
    screen.blit(text_score_surface, ((REAL_WIDTH - text_score_surface.get_width()) // 2, BORDER))
    font_small = p.font.Font(None, int(BORDER ))
    text_info_surface = font_small.render("Moves left: " + str(moves_left) + "\nTime: " + str(clock.get_time), True, (255, 255, 255))
    screen.blit(text_info_surface, ((REAL_WIDTH - text_score_surface.get_width()) // 2, BORDER * 4 + HEIGHT))

    # Main game logic
    game_on = True
    while game_on:
        for event in p.event.get():
            if event.type == p.QUIT:
                game_on = False
            if moves_left <= 0:
                endGame(screen)
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x,y location of the mouse
                # gets the selected square index
                sq_selected[0] = (location[1] - BORDER * 3) // SQ_SIZE
                sq_selected[1] = (location[0] - BORDER) // SQ_SIZE
                if (sq_selected[0] > bunny_pos[0] + 1 or sq_selected[0] < bunny_pos[0] - 1) or (sq_selected[1] > bunny_pos[1] + 1 or sq_selected[1] < bunny_pos[1] - 1):  # if can't move there
                    break
                if ((sq_selected[0] > DIMENTIONS - 1 or sq_selected[0] < 0) or (sq_selected[1] > DIMENTIONS - 1 or sq_selected[1] < 0)): # if it's out of the board
                    break
                if sq_selected != bunny_pos:  # if we clicked not on position of the bunny -> move it
                    if board[sq_selected[0]][sq_selected[1]] == "HM":  # if we are going to the burrow
                        levels_passed += 1
                        if levels_passed <= 20:
                            if levels_passed % 5 == 0:
                                DIMENTIONS += 2
                                SQ_SIZE = WIDTH // DIMENTIONS
                                SPACING = SQ_SIZE // 6
                        else:
                            if levels_passed % 15 == 0:
                                DIMENTIONS += 2
                                SQ_SIZE = WIDTH // DIMENTIONS
                                SPACING = SQ_SIZE // 6
                        board = emptyBoard()
                        bunny_pos = generateGame(screen, board, levels_passed)
                        score_this += moves_left // 2
                        moves_left = int(DIMENTIONS * 1.5)
                        renderText(screen, font, score_this, text_score_surface, BORDER, levels_passed)

                    else:
                        # if we stepped on a carrot
                        if board[sq_selected[0]][sq_selected[1]] == "CR":
                            score_this += 10
                            renderText(screen, font, score_this, text_score_surface, BORDER, levels_passed)
                        # move the bunny
                        board[bunny_pos[0]][bunny_pos[1]] = "--"
                        bunny_pos[0] = sq_selected[0]
                        bunny_pos[1] = sq_selected[1]
                        board[sq_selected[0]][sq_selected[1]] = "BN"
                        moves_left -= 1
        # Rendering information below the game. Out of the loop so it can count time smooth
        screen.fill((110, 170, 75), (0, BORDER * 4 + HEIGHT, REAL_WIDTH, text_info_surface.get_height()))
        text_info_surface = font_small.render("Moves left: " + str(moves_left), True, (255, 255, 255))
        screen.blit(text_info_surface, (BORDER, BORDER * 4 + HEIGHT))
        text_info_surface = font_small.render("Time: " + str(p.time.get_ticks() // 1000), True, (255, 255, 255))
        screen.blit(text_info_surface, (BORDER + WIDTH - text_info_surface.get_width(), BORDER * 4 + HEIGHT))
        text_info_surface = font_small.render("Highest score: 0", True, (255, 255, 255))
        screen.blit(text_info_surface, (BORDER + WIDTH // 2 - text_info_surface.get_width() // 2, BORDER * 4 + HEIGHT))
        drawGameState(screen, board, bunny_pos)
        clock.tick(FPS)
        p.display.flip()

main()