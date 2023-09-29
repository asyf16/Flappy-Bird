# Aurora Shi
# Flappy bird
# Comp Sci 20 B2
# June 8, 2022

# This program is my own work - AS
# This program allows users to play Battleship against the computer
# This is only the code, the gui is made with pygame
# Pipe code and Bird code learned from tinyurl.com/599s586y
import pygame
import random
import pickle

pygame.mixer.init()

# setting up the screen and display
pygame.init()
display_width = 900
display_height = 900
gameDisplay = pygame.display.set_mode((display_width, display_height))
gameScene = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Flappy Bird')
done = False
clock = pygame.time.Clock()
pipeVelX = -8
playerVelY = -20
playerMaxVelY = 30
playerMinVelY = -22
playerAccY = 2
playerFlapAccv = -16  # velocity while flapping
playerFlapped = False  # It is true only wh
FPS = 60
FPSCLOCK = pygame.time.Clock()  # for controlling the FPS

# importing pictures
wins = pygame.mixer.Sound("win.mp3")
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1)
bg1 = pygame.image.load('bg1.png')
bg2 = pygame.image.load('bg2.png')
bg3 = pygame.image.load('bg3.png')
l = pygame.image.load('l.png')
ground = pygame.image.load('ground.png').convert()
bird1 = pygame.image.load('bird.png')
fish1 = pygame.image.load('fish.png')
sus1 = pygame.image.load('sus.png')
button = pygame.image.load('sb.png')
pipeu = pygame.image.load('pipeu.png')
piped = pygame.image.load('piped.png')
hit = pygame.mixer.Sound('hit.mp3')

gameDisplay.blit(bg1, (0, 0))

# setting up fonts
font1 = pygame.font.SysFont('Impact', 55)
font2 = pygame.font.SysFont('Impact', 40)
font3 = pygame.font.SysFont('Impact', 100)

# setting up scenes
menu = True
leaderboard = False
Game = False
game = False
select = False
lose = False

# setting up variables
score = 0
floor1=0
floor2=900
playery = 390
music_paused = False
bird = True
sus = False
fish = False

#  save the highscores to file
file_name = "scores.pkl"
open_file = open(file_name, "rb")
loaded_list = pickle.load(open_file)
open_file.close()


# function to sort the list of highscores from highest to lowest, then pop the last digit
def selection_sort(a_list):
    n = len(a_list)
    for end in range(n, 1, -1):  # Each pass starts here
        max_position = 0
        for i in range(1, end):
            if a_list[i] < a_list[max_position]:  # Perform comparison
                max_position = i
        temp = a_list[end - 1]  # Perform exchange
        a_list[end - 1] = a_list[max_position]
        a_list[max_position] = temp
    a_list.pop()
    return a_list


# function to generate two pipes with a random distance between them
def getRandomPipe():
    y1 = random.randrange(-610, -245)
    y2 = y1 + 667 + random.randrange(180, 280)
    pipeX = 900 + 10
    pipe = [
        {'x': pipeX, 'y': y1},  # Upper Pipes
        {'x': pipeX, 'y': y2}  # Lower Pipes
    ]
    return pipe


# generate the first two pipes and creates a dictionary with values of pipes
newPipe1 = getRandomPipe()
newPipe2 = getRandomPipe()
upperPipes = [
    {'x': 900 + 67, 'y': newPipe1[0]['y']},
    {'x': 900 + 90 + (900 / 2), 'y': newPipe2[0]['y']}
]

lowerPipes = [
    {'x': 900 + 67, 'y': newPipe1[1]['y']},
    {'x': 900 + 90 + (900 / 2), 'y': newPipe2[1]['y']}
]

while not done:
    FPSCLOCK.tick(FPS)  # sets frame rate
    mouse = pygame.mouse.get_pos()  # gets position from mouse
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if Game:  # when screen or space is pressed, the game starts
                Game = False
                game = True
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True

        if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse is pressed down
            if leaderboard:
                if (690 <= mouse[0] <= 854) and (807 <= mouse[1] <= 875):  # goes back to menu (back button)
                    leaderboard = False
                    menu = True
                    gameDisplay.blit(bg1, (0, 0))

            if Game:
                Game = False
                game = True
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True

            if (24 <= mouse[0] <= 103) and (800 <= mouse[1] <= 880):
                # Toggle the boolean variable.
                music_paused = not music_paused  # shuts off and on the music
                if music_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            if menu:  # in menu scene
                if (277 <= mouse[0] <= 621) and (352 <= mouse[1] <= 446):  # play button
                    menu = False  # opens the second page when play button is pressed
                    select = True
                    gameDisplay.blit(bg2, (0, 0))

                if (277 <= mouse[0] <= 621) and (494 <= mouse[1] <= 587):  # leaderboard button
                    gameDisplay.blit(l, (0, 0))  # when leaderboard button is pressed
                    menu = False
                    leaderboard = True

            if select:
                if sus or fish:
                    if (55 <= mouse[0] <= 250 - 45 + 55) and (590 <= mouse[1] <= 665):  # bird select
                        bird = True
                        fish = False
                        sus = False
                if fish or bird:
                    if (343 <= mouse[0] <= 250 - 45 + 343) and (590 <= mouse[1] <= 665):  # among us select
                        sus = True
                        fish = False
                        bird = False
                if sus or bird:
                    if (623 <= mouse[0] <= 250 - 45 + 623) and (590 <= mouse[1] <= 665):  # fish select
                        fish = True
                        sus = False
                        bird = False
                if (680 <= mouse[0] <= 870) and (800 <= mouse[1] <= 870):  # next button
                    select = False
                    Game = True
                    gameDisplay.blit(bg3, (0, 0))

            if lose:
                if (277 <= mouse[0] <= 621) and (352 <= mouse[1] <= 446):  # restart button
                    lose = False  # resets all values
                    Game = True
                    playery = 390
                    score = 0
                    gameDisplay.blit(bg3, (0, 0))
                    gameDisplay.blit(ground, (0, 780))

                    newPipe1 = getRandomPipe()  # gets the first two random pipes
                    newPipe2 = getRandomPipe()
                    upperPipes = [
                        {'x': 900 + 67, 'y': newPipe1[0]['y']},
                        {'x': 900 + 90 + (900 / 2), 'y': newPipe2[0]['y']}
                    ]

                    lowerPipes = [
                        {'x': 900 + 67, 'y': newPipe1[1]['y']},
                        {'x': 900 + 90 + (900 / 2), 'y': newPipe2[1]['y']}
                    ]
                if (277 <= mouse[0] <= 621) and (494 <= mouse[1] <= 587):  # main menu
                    lose = False  # resets all values
                    menu = True
                    playery = 390
                    score = 0
                    gameDisplay.blit(bg1, (0, 0))
                    newPipe1 = getRandomPipe()
                    newPipe2 = getRandomPipe()
                    upperPipes = [
                        {'x': 900 + 200, 'y': newPipe1[0]['y']},
                        {'x': 900 + 200 + (900 / 2), 'y': newPipe2[0]['y']}
                    ]

                    lowerPipes = [
                        {'x': 900 + 200, 'y': newPipe1[1]['y']},
                        {'x': 900 + 200 + (900 / 2), 'y': newPipe2[1]['y']}
                    ]
    if leaderboard:  # leaderboard screen
        gameDisplay.blit(l, (0, 0))
        if (690 <= mouse[0] <= 854) and (807 <= mouse[1] <= 875):  # creates the back button
            pygame.draw.rect(gameDisplay, (97, 141, 191), pygame.Rect(690, 807, 854 - 690, 875 - 807))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(690, 807, 854 - 690, 875 - 807), 6)
            text1 = font2.render('Back', True, (209, 227, 247))
        else:
            pygame.draw.rect(gameDisplay, (209, 227, 247), pygame.Rect(690, 807, 854 - 690, 875 - 807))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(690, 807, 854 - 690, 875 - 807), 6)
            text1 = font2.render('Back', True, (23, 57, 103))
        gameDisplay.blit(text1, (730, 815))  # writes the texts
        first = "First place: " + str(loaded_list[0])
        second = "Second place: " + str(loaded_list[1])
        third = "Third place: " + str(loaded_list[2])
        fourth = "Fourth place: " + str(loaded_list[3])
        fifth = "Fifth place: " + str(loaded_list[4])
        text2 = font1.render(first, True, (23, 57, 103))
        text3 = font1.render(second, True, (23, 57, 103))
        text4 = font1.render(third, True, (23, 57, 103))
        text5 = font1.render(fourth, True, (23, 57, 103))
        text6 = font1.render(fifth, True, (23, 57, 103))
        gameDisplay.blit(text2, (250, 270))
        gameDisplay.blit(text3, (250, 350))
        gameDisplay.blit(text4, (250, 430))
        gameDisplay.blit(text5, (250, 510))
        gameDisplay.blit(text6, (250, 590))



    if menu:
        #  play button
        if (277 <= mouse[0] <= 621) and (352 <= mouse[1] <= 446):
            pygame.draw.rect(gameDisplay, (53, 104, 162), pygame.Rect(277, 352, 621 - 277, 446 - 352))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(277, 352, 621 - 277, 446 - 352), 6)
            text1 = font1.render('Play', True, (209, 227, 247))
        else:
            pygame.draw.rect(gameDisplay, (209, 227, 247), pygame.Rect(277, 352, 621 - 277, 446 - 352))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(277, 352, 621 - 277, 446 - 352), 6)
            text1 = font1.render('Play', True, (23, 57, 103))

        # leaderboard button
        if (277 <= mouse[0] <= 621) and (494 <= mouse[1] <= 587):
            pygame.draw.rect(gameDisplay, (53, 104, 162), pygame.Rect(277, 494, 621 - 277, 587 - 494))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(277, 494, 621 - 277, 587 - 494), 6)
            text2 = font1.render('Leaderboard', True, (209, 227, 247))
        else:
            pygame.draw.rect(gameDisplay, (209, 227, 247), pygame.Rect(277, 494, 621 - 277, 587 - 494))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(277, 494, 621 - 277, 587 - 494), 6)
            text2 = font1.render('Leaderboard', True, (23, 57, 103))
        gameDisplay.blit(text1, (396, 361))
        gameDisplay.blit(text2, (304, 503))

    if select:
        text3 = font2.render('Select', True, (23, 57, 103))
        text4 = font2.render('Select', True, (209, 227, 247))
        # next button
        if (680 <= mouse[0] <= 870) and (800 <= mouse[1] <= 870):
            pygame.draw.rect(gameDisplay, (53, 104, 162), pygame.Rect(680, 800, 870 - 680, 870 - 800))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(680, 800, 870 - 680, 870 - 800), 6)
            text5 = font1.render('Next', True, (209, 227, 247))
        else:
            pygame.draw.rect(gameDisplay, (209, 227, 247), pygame.Rect(680, 800, 870 - 680, 870 - 800))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(680, 800, 870 - 680, 870 - 800), 6)
            text5 = font1.render('Next', True, (23, 57, 103))
        gameDisplay.blit(text5, (724, 800))
        # select buttons
        if not bird:  # makes the select button colored
            pygame.draw.rect(gameDisplay, (209, 227, 247), pygame.Rect(55, 590, 250 - 45, 665 - 590))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(55, 590, 250 - 45, 665 - 590), 6)
            gameDisplay.blit(text3, (103, 600))

        if bird:
            pygame.draw.rect(gameDisplay, (53, 104, 162), pygame.Rect(55, 590, 250 - 45, 665 - 590))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(55, 590, 250 - 45, 665 - 590), 6)
            gameDisplay.blit(text4, (103, 600))

        if not sus:
            pygame.draw.rect(gameDisplay, (209, 227, 247), pygame.Rect(343, 590, 250 - 45, 665 - 590))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(343, 590, 250 - 45, 665 - 590), 6)
            gameDisplay.blit(text3, (391, 600))

        if sus:
            pygame.draw.rect(gameDisplay, (53, 104, 162), pygame.Rect(343, 590, 250 - 45, 665 - 590))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(343, 590, 250 - 45, 665 - 590), 6)
            gameDisplay.blit(text4, (391, 600))

        if not fish:
            pygame.draw.rect(gameDisplay, (209, 227, 247), pygame.Rect(623, 590, 250 - 45, 665 - 590))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(623, 590, 250 - 45, 665 - 590), 6)
            gameDisplay.blit(text3, (671, 600))

        if fish:
            pygame.draw.rect(gameDisplay, (53, 104, 162), pygame.Rect(623, 590, 250 - 45, 665 - 590))
            pygame.draw.rect(gameDisplay, (23, 57, 103), pygame.Rect(623, 590, 250 - 45, 665 - 590), 6)
            gameDisplay.blit(text4, (671, 600))

    if Game:
        gameDisplay.blit(bg3, (0, 0))
        text8 = font1.render("Press to Start!", True, (26, 23, 62))
        gameDisplay.blit(text8, (300, 250))
        gameDisplay.blit(ground, (0, 780))
        if bird:
            gameDisplay.blit(bird1, (400, 390))  # displays character based on choice
        if sus:
            gameDisplay.blit(sus1, (400, 390))
        if fish:
            gameDisplay.blit(fish1, (400, 390))
        gameDisplay.blit(button, (22, 798))

    if game:  # real game
        FPSCLOCK.tick(FPS)
        gameDisplay.blit(bg3, (0, 0))
        s = "Score: " + str(score)  # displays score
        text7 = font2.render(s, True, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if playery > 0:  # while bird is flapping
                    playerVelY = playerFlapAccv
                    playerFlapped = True

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerMaxVelY = playerMaxVelY * 1.005  # acceleration as bird falls
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
            playerMaxVelY = 30  # bird falling is reset
        playery = playery + playerVelY

        playerMidPos = 400 + (67 / 2)  # character width divided by 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + (67 / 2)  # pipe position plus character width divided by 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:  # if character location is between pipe, score increases
                score += 1  # senses passing through the pipes
                wins.play()
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            pipeVelX = pipeVelX
            upperPipe['x'] += pipeVelX  # moving the pipes
            lowerPipe['x'] += pipeVelX

        #  adds a new pipe when the old pipe is 10 away from the edge
        if 0 < upperPipes[0]['x'] < 10:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #  deletes the pipe after it goes to the edge
        if upperPipes[0]['x'] < -97:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #  display the pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            gameDisplay.blit(piped, (upperPipe['x'], upperPipe['y']))
            gameDisplay.blit(pipeu, (lowerPipe['x'], lowerPipe['y']))

        # displays character based on choice
        if bird:
            gameDisplay.blit(bird1, (400, playery))
        if sus:
            gameDisplay.blit(sus1, (400, playery))
        if fish:
            gameDisplay.blit(fish1, (400, playery))
        # checks for collisions with ceiling and ground
        if playery > 720 - 23 or playery < -5:
            game = False
            lose = True
            hit.play()  # when game ends, the score is added and then sorted
            loaded_list.append(int(score))
            selection_sort(loaded_list)
            open_file = open(file_name, "wb")
            pickle.dump(loaded_list, open_file)
            open_file.close()
        # displays ground and score above the pipes

        if floor1 > -900:
            floor1 = floor1 - 8
        if floor2 > -8:
            floor2 = floor2 -8
        if floor1 < -900:
            floor1 = 0
        if floor2 < 0:
            floor2 = 900
        gameDisplay.blit(ground, (floor1, 780))
        gameDisplay.blit(ground, (floor2, 780))
        gameDisplay.blit(button, (22, 798))
        gameDisplay.blit(text7, (710, 830))

        #  checks for collisions
        for pipe in upperPipes:
            if playery < 667 + pipe['y'] and abs(400 - pipe['x']) < 97 - 20:  # checks if it hits upper pipe
                game = False
                lose = True
                hit.play()
                loaded_list.append(int(score))
                selection_sort(loaded_list)
                open_file = open(file_name, "wb")
                pickle.dump(loaded_list, open_file)
                open_file.close()

        for pipe in lowerPipes:
            if (playery + 87 > pipe['y']) and abs(400 - pipe['x']) < 97 - 20:  # checks if it hits lower pipe
                game = False
                lose = True
                hit.play()
                loaded_list.append(int(score))
                selection_sort(loaded_list)
                open_file = open(file_name, "wb")
                pickle.dump(loaded_list, open_file)
                open_file.close()
    if lose:
        # restart
        if (277 <= mouse[0] <= 621) and (352 <= mouse[1] <= 446):
            pygame.draw.rect(gameDisplay, (100, 114, 161), pygame.Rect(277, 352, 621 - 277, 446 - 352))
            pygame.draw.rect(gameDisplay, (26, 23, 62), pygame.Rect(277, 352, 621 - 277, 446 - 352), 6)
            text1 = font1.render('Restart', True, (235, 226, 251))
        else:
            pygame.draw.rect(gameDisplay, (235, 226, 251), pygame.Rect(277, 352, 621 - 277, 446 - 352))
            pygame.draw.rect(gameDisplay, (26, 23, 62), pygame.Rect(277, 352, 621 - 277, 446 - 352), 6)
            text1 = font1.render('Restart', True, (26, 23, 62))
        # main menu
        if (277 <= mouse[0] <= 621) and (494 <= mouse[1] <= 587):
            pygame.draw.rect(gameDisplay, (100, 114, 161), pygame.Rect(277, 494, 621 - 277, 587 - 494))
            pygame.draw.rect(gameDisplay, (26, 23, 62), pygame.Rect(277, 494, 621 - 277, 587 - 494), 6)
            text = font1.render('Main Menu', True, (235, 226, 251))
        else:
            pygame.draw.rect(gameDisplay, (235, 226, 251), pygame.Rect(277, 494, 621 - 277, 587 - 494))
            pygame.draw.rect(gameDisplay, (26, 23, 62), pygame.Rect(277, 494, 621 - 277, 587 - 494), 6)
            text = font1.render('Main Menu', True, (26, 23, 62))
        gameDisplay.blit(text, (325, 503))
        gameDisplay.blit(text1, (365, 361))
        text3 = font3.render('You Lost!', True, (26, 23, 62))
        gameDisplay.blit(text3, (270, 200))

        pygame.display.update()
    pygame.display.flip()  # updates the scenes
pygame.quit()
