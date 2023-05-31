# This is the main file. It is responsible for handling user input and current game state.

import pygame as p
import random
import time

# Constants for the pygame
# For the game screen size (630 so it can be devided by 5, 7 and 9 squares)
WIDTH = HEIGHT = 630  # For the game screen size
BORDER = 30  # For spacing left and right
REAL_HEIGHT = HEIGHT + BORDER * 4 + 150  # For game real screen size (900)
REAL_WIDTH = WIDTH + BORDER * 2  # For game real screen size (690)

DIMENTIONS = 3  # Board is DIMENTIONSxDIMENTIONS
SQ_SIZE = WIDTH // DIMENTIONS
SPACING = SQ_SIZE // 6
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
        while counter < DIMENTIONS // 2:
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
            if piece != "--":  # if it's not empty slot
                if piece == "CR":  # if it's a carrot - make it smaller
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
def renderText(screen, font, score_this, text_surface, spacing, levels_passed, player_name):
    screen.fill((110, 170, 75), (0, spacing,
                REAL_WIDTH, text_surface.get_height()))
    text_surface = font.render(player_name + " | Level " + str(
        levels_passed) + "  |  Score: " + str(score_this), True, (255, 255, 255))
    screen.blit(
        text_surface, ((REAL_WIDTH - text_surface.get_width()) // 2, BORDER))

# Show input-name-screen before game starts
def welcome_screen(screen):
    # Set up the input field
    input_rect = p.Rect(REAL_WIDTH // 2 - 150, REAL_HEIGHT // 2, 300, 40)
    input_color = (255, 255, 255)
    font = p.font.Font(None, 32)
    player_name = ""

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                return False
            elif event.type == p.KEYDOWN:
                if event.key == p.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == p.K_RETURN:
                    running = False
                else:
                    # Limit the input to the width of the input field
                    if input_rect.width > font.size(player_name)[0] + 30:
                        player_name += event.unicode

        # Fill the screen with a background color
        screen.fill((110, 170, 75))

        # Render the "Welcome!" message and input
        font = p.font.Font(None, WIDTH // 6)
        welcome_text = font.render("Welcome!", True, (255, 255, 255))
        welcome_rect = welcome_text.get_rect(
            center=(REAL_WIDTH // 2, REAL_HEIGHT // 3))
        screen.blit(welcome_text, welcome_rect)

        # Render the small text above the input field
        small_font = p.font.Font(None, BORDER)
        small_text = small_font.render(
            "Input your name and press enter:", True, (255, 255, 255))
        small_rect = small_text.get_rect(
            center=(REAL_WIDTH // 2, REAL_HEIGHT // 2 - 30))
        screen.blit(small_text, small_rect)

        p.draw.rect(screen, input_color, input_rect, 2)

        # Render the player's name
        font = p.font.Font(None, WIDTH // 12)
        input_text = font.render(player_name, True, (255, 255, 255))
        screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        p.display.update()

    return player_name

# End the game screen with buttons to try again or quit
def endGame(screen, cause_of_death):
    # Create black-to-green transition
    frame_count = 0
    while frame_count < 2000:
        current_color = p.Color.lerp(
            p.Color(0, 0, 0), p.Color(60, 90, 40), frame_count / 2000)
        screen.fill(current_color)
        p.display.update()
        frame_count += 1

    # Create the 'You died' message
    font = p.font.Font(None, WIDTH//5)
    you_died_text = font.render("You died!", True, (255, 255, 255))
    you_died_rect = you_died_text.get_rect(
        center=(REAL_WIDTH // 2, REAL_HEIGHT // 3))

    # Create the 'Cause of death: unknown' text
    font = p.font.Font(None, WIDTH//14)
    cause_of_death_text = font.render("Cause of death:", True, (255, 255, 255))
    cause_of_death_rect = cause_of_death_text.get_rect(
        center=(REAL_WIDTH // 2, REAL_HEIGHT // 3 + WIDTH // 12 + BORDER * 2))
    font = p.font.Font(None, WIDTH//10)
    cause_of_death_text_2 = font.render(cause_of_death, True, (255, 90, 90))
    cause_of_death_rect_2 = cause_of_death_text_2.get_rect(
        center=(REAL_WIDTH // 2, REAL_HEIGHT // 3 + WIDTH // 6.5 + BORDER * 2))

    # Create the 'Leave' button
    leave_button = p.Rect(REAL_WIDTH // 2 - 100,
                          REAL_HEIGHT // 2 + 180, 200, 50)
    leave_text = font.render("Leave", True, (255, 255, 255))
    leave_rect = leave_text.get_rect(center=leave_button.center)

    # Create the 'Try Again' button
    try_again_button = p.Rect(REAL_WIDTH // 2 - 100,
                              REAL_HEIGHT // 2 + 110, 200, 50)
    try_again_text = font.render("Try Again", True, (255, 255, 255))
    try_again_rect = try_again_text.get_rect(center=try_again_button.center)

    # Display the elements on the screen
    screen.blit(you_died_text, you_died_rect)
    screen.blit(cause_of_death_text, cause_of_death_rect)
    screen.blit(cause_of_death_text_2, cause_of_death_rect_2)
    p.draw.rect(screen, (129, 188, 88), leave_button)
    screen.blit(leave_text, leave_rect)
    p.draw.rect(screen, (129, 188, 88), try_again_button)
    screen.blit(try_again_text, try_again_rect)
    p.display.update()

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return
            elif event.type == p.MOUSEBUTTONDOWN:
                if leave_button.collidepoint(event.pos):
                    p.quit()
                    return False
                elif try_again_button.collidepoint(event.pos):
                    # Restart the game
                    return True

# For winners
def survivedGame(screen, score, scores):
    screen.fill((116, 171, 73))
    font = p.font.Font(None, WIDTH // 7)

    # Create the 'Your score' message
    font = p.font.Font(None, WIDTH // 8)
    score_label_text = font.render("Score: ", True, (255, 255, 255))
    score_value_text = font.render(str(score), True, (168, 218, 255))
    # Calculate position
    group_width = score_label_text.get_width() + score_value_text.get_width()
    group_left = (REAL_WIDTH - group_width) // 2
    group_top = REAL_HEIGHT // 5 + BORDER
    score_label_rect = score_label_text.get_rect(
        topleft=(group_left, group_top))
    score_value_rect = score_value_text.get_rect(
        topleft=(score_label_rect.right, group_top))

    # Create the 'Leave' button
    leave_button = p.Rect(REAL_WIDTH // 2 - 100,
                          REAL_HEIGHT // 2 + 200, 200, 50)
    leave_text = font.render("Leave", True, (255, 255, 255))
    leave_rect = leave_text.get_rect(center=leave_button.center)

    # Create the 'Try Again' button
    try_again_button = p.Rect(REAL_WIDTH // 2 - 100,
                              REAL_HEIGHT // 2 + 130, 200, 50)
    try_again_text = font.render("Try Again", True, (255, 255, 255))
    try_again_rect = try_again_text.get_rect(center=try_again_button.center)

    # Create the top three winners text
    font = p.font.Font(None, WIDTH // 14)
    top_three_text = font.render("Top Three Winners:", True, (255, 255, 255))
    top_three_rect = top_three_text.get_rect(
        center=(REAL_WIDTH // 2, REAL_HEIGHT // 2 - 100))

    # Create the font for displaying scores
    font = p.font.Font(None, WIDTH // 20)

    # Display the elements on the screen
    screen.blit(score_label_text, score_label_rect)
    screen.blit(score_value_text, score_value_rect)
    screen.blit(top_three_text, top_three_rect)
    p.draw.rect(screen, (129, 188, 88), leave_button)
    screen.blit(leave_text, leave_rect)
    p.draw.rect(screen, (129, 188, 88), try_again_button)
    screen.blit(try_again_text, try_again_rect)

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Render the top three winners
    y_offset = REAL_HEIGHT // 2 - 50
    for i, (name, score) in enumerate(sorted_scores[:3]):
        winner_text = font.render(f"{name}: {score}", True, (255, 255, 255))
        winner_rect = winner_text.get_rect(
            center=(REAL_WIDTH // 2, y_offset + i * 50))
        screen.blit(winner_text, winner_rect)
    p.display.update()

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return
            elif event.type == p.MOUSEBUTTONDOWN:
                if leave_button.collidepoint(event.pos):
                    p.quit()
                    return False
                elif try_again_button.collidepoint(event.pos):
                    # Restart the game
                    return True
        p.display.update()

# For saving results
def load_scores():
    scores = {}
    with open("scores_table.txt", 'r') as file:
        for line in file:
            name, score = line.strip().split(':')
            scores[name] = int(score)
    return scores

def save_scores(scores):
    with open("scores_table.txt", 'w') as file:
        for name, score in scores.items():
            file.write(f"{name}:{score}\n")

# Main function
def main():
    # Beginning setup
    p.init()
    p.mixer.init()
    p.mixer.music.load("./music.mp3")
    sound_effect_collected = p.mixer.Sound("./collected.mp3")
    global DIMENTIONS
    global SQ_SIZE
    global SPACING
    screen = p.display.set_mode((REAL_WIDTH, REAL_HEIGHT))
    start_time = p.time.get_ticks()
    screen.fill((110, 170, 75))

    # Variables
    # Keep track of the last click of the player (row, col)
    sq_selected = [0, 0]
    score_this = 0
    moves_left = int(DIMENTIONS * 1.5)
    levels_passed = 0

    player_name = welcome_screen(screen)
    if player_name == False:
        p.quit()
        return
    # Functions before game starts
    LoadImages()
    scores = load_scores()
    try:
        highest_score = max(scores.values())
    except:
        highest_score = 0
    board = emptyBoard()
    # Generates random setting and returns the pos. of the bunny
    bunny_pos = generateGame(screen, board, levels_passed)

    # Texts initialization
    font = p.font.Font(None, int(BORDER * 1.5))
    text_score_surface = font.render(player_name + " | Level " + str(
        levels_passed) + "  |  Score: " + str(score_this), True, (255, 255, 255))
    screen.blit(text_score_surface,
                ((REAL_WIDTH - text_score_surface.get_width()) // 2, BORDER))
    font_small = p.font.Font(None, int(BORDER))
    time_left = 30 - p.time.get_ticks() // 1000
    text_info_surface = font_small.render(
        "Moves left: " + str(moves_left) + "\nTime: " + str(time_left), True, (255, 255, 255))
    screen.blit(text_info_surface, ((
        REAL_WIDTH - text_score_surface.get_width()) // 2, BORDER * 4 + HEIGHT))

    # Main game logic
    game_on = True
    p.mixer.music.play(-1)
    while game_on:
        if moves_left <= 0:
            game_on = endGame(screen, "Ran out of moves")
            if game_on:
                # Restart the game
                board = emptyBoard()
                screen.fill((110, 170, 75))
                score_this = 0
                bunny_pos = generateGame(screen, board, levels_passed)
                moves_left = int(DIMENTIONS * 1.5)
                screen.blit(text_score_surface, ((
                    REAL_WIDTH - text_score_surface.get_width()) // 2, BORDER))
                font_small = p.font.Font(None, int(BORDER))
                start_time = p.time.get_ticks()
                text_info_surface = font_small.render(
                    "Moves left: " + str(moves_left) + "\nTime: " + str(time_left), True, (255, 255, 255))
                screen.blit(text_info_surface, ((
                    REAL_WIDTH - text_score_surface.get_width()) // 2, BORDER * 4 + HEIGHT))
            else:
                break
        elif time_left <= 0:
            scores[player_name] = score_this
            save_scores(scores)
            game_on = survivedGame(screen, score_this, scores)
            moves_left = 0
            continue

        for event in p.event.get():
            if event.type == p.QUIT:
                game_on = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x,y location of the mouse
                # gets the selected square index
                sq_selected[0] = (location[1] - BORDER * 3) // SQ_SIZE
                sq_selected[1] = (location[0] - BORDER) // SQ_SIZE
                if (sq_selected[0] > bunny_pos[0] + 1 or sq_selected[0] < bunny_pos[0] - 1) or (sq_selected[1] > bunny_pos[1] + 1 or sq_selected[1] < bunny_pos[1] - 1):  # if can't move there
                    break
                # if it's out of the board
                if ((sq_selected[0] > DIMENTIONS - 1 or sq_selected[0] < 0) or (sq_selected[1] > DIMENTIONS - 1 or sq_selected[1] < 0)):
                    break
                if sq_selected != bunny_pos:  # if we clicked not on position of the bunny -> move it
                    # if we are going to the burrow
                    if board[sq_selected[0]][sq_selected[1]] == "HM":
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
                        score_this += 1
                        moves_left = int(DIMENTIONS * 1.5)
                        renderText(screen, font, score_this, text_score_surface,
                                   BORDER, levels_passed, player_name)

                    else:
                        # if we stepped on a carrot
                        if board[sq_selected[0]][sq_selected[1]] == "CR":
                            score_this += 10
                            sound_effect_collected.play()
                            renderText(
                                screen, font, score_this, text_score_surface, BORDER, levels_passed, player_name)
                        # move the bunny
                        board[bunny_pos[0]][bunny_pos[1]] = "--"
                        bunny_pos[0] = sq_selected[0]
                        bunny_pos[1] = sq_selected[1]
                        board[sq_selected[0]][sq_selected[1]] = "BN"
                        moves_left -= 1
        # Rendering information below the game. Out of the loop so it can count time smooth
        screen.fill((110, 170, 75), (0, BORDER * 4 + HEIGHT,
                    REAL_WIDTH, text_info_surface.get_height()))
        text_info_surface = font_small.render(
            "Moves left: " + str(moves_left), True, (255, 255, 255))
        screen.blit(text_info_surface, (BORDER, BORDER * 4 + HEIGHT))
        text_info_surface = font_small.render(
            "Time: " + str(time_left), True, (255, 255, 255))
        screen.blit(text_info_surface, (BORDER + WIDTH -
                    text_info_surface.get_width(), BORDER * 4 + HEIGHT))
        text_info_surface = font_small.render(
            "Highest score: " + str(highest_score), True, (255, 255, 255))
        screen.blit(text_info_surface, (BORDER + WIDTH // 2 -
                    text_info_surface.get_width() // 2, BORDER * 4 + HEIGHT))
        drawGameState(screen, board, bunny_pos)
        time_left = 30 - p.time.get_ticks() // 1000
        p.display.flip()
    scores[player_name] = score_this
    save_scores(scores)
    p.quit()


main()
