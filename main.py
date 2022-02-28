import sys
import pygame
import random
import math

# initializing pygame
pygame.init()

# creating the screen
screen_height = 800
screen_width = 600
screen = pygame.display.set_mode((screen_height, screen_width))

# background image
background = pygame.image.load('./media/images/background.png')

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./media/images/spaceicon.png')
pygame.display.set_icon(icon)

# score value, font, position.
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_x_coordinate = 10
score_y_coordinate = 10

# game over font
game_over_font = pygame.font.Font('freesansbold.ttf', 40)


# global variables for the game.
laser_state = "ready"


def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (270, 200))


# for checking if objects are colliding.
def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) +
                         ((math.pow(enemyY - laserY, 2))))
    if distance < 27:
        return True
    else:
        return False


# player
playerImg = pygame.image.load('./media/images/spaceship.png')


def player(x, y):
    screen.blit(playerImg, (x, y))


# level select buttons.
def select_level():

    screen.blit(background, (0, 0))
    button_width = 140
    button_height = 70
    left = screen_width / 2 - (button_width * 3 / 2) + 100
    top = screen_height / 2 - button_height / 2 - 125

    # getting coordinates of the mouse.
    mouse = pygame.mouse.get_pos()

    font = pygame.font.Font('freesansbold.ttf', 28)
    easy_button = pygame.Rect(left, top, button_width, button_height)
    medium_button = pygame.Rect(
        left + button_width, top, button_width, button_height)
    hard_button = pygame.Rect(
        left + (button_width * 2) + 20, top, button_width, button_height)

    easy_button_text = font.render('Easy', True, (0, 0, 0))
    medium_button_text = font.render('Medium', True, (0, 0, 0))
    hard_button_text = font.render('Hard', True, (0, 0, 0))

    if(easy_button.collidepoint(mouse)):
        pygame.draw.rect(screen, (255, 255, 255), easy_button)
        if(pygame.mouse.get_pressed()[0]):
            start_game(1)
        else:
            pygame.draw.rect(screen, (176, 224, 230), easy_button)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    elif(medium_button.collidepoint(mouse)):
        pygame.draw.rect(screen, (255, 255, 255), medium_button)
        if(pygame.mouse.get_pressed()[0]):
            start_game(2)
        else:
            pygame.draw.rect(screen, (176, 224, 230), medium_button)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    elif(hard_button.collidepoint(mouse)):
        pygame.draw.rect(screen, (255, 255, 255), hard_button)
        if(pygame.mouse.get_pressed()[0]):
            start_game(3)
        else:
            pygame.draw.rect(screen, (176, 224, 230), hard_button)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
    screen.blit(easy_button_text, (left + 40, top + 20))
    screen.blit(medium_button_text, (left + button_width + 15, top + 20))
    screen.blit(hard_button_text, (left + (button_width * 2) + 60, top + 20))

# for displaying the start game button, used when user wants to start game or restart after losing.


def start_game_button():
    # rendering the level select buttons.
    select_level()
    # setting width and height of the button.
    button_width = 350
    button_height = 70
    left = screen_width / 2 - button_width / 2 + 100
    top = screen_height / 2 - button_height / 2 - 300

    # creating button rectangle.
    start_button = pygame.Rect(left, top, button_width, button_height)
    font = pygame.font.Font('freesansbold.ttf', 36)
    restart_text = font.render("New Game", True, (255, 255, 255))

    pygame.draw.rect(screen, (0, 50, 210), start_button)
    screen.blit(restart_text, (left+90, top+20))

# for starting the game.


def start_game(level=1):
    # initializing the game.
    game_loop = True

    # resetting score value.
    global score_value
    score_value = 0

    # enemy values.
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 5 * level

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('./media/images/ufo.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4 * level)
        enemyY_change.append(40)

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    # laser properties.
    laserImg = pygame.image.load('./media/images/laser.png')
    laserX = 0
    laserY = 480
    laserX_change = 0
    laserY_change = level * 5

    def fire_laser(x, y):
        global laser_state
        laser_state = "fire"
        screen.blit(laserImg, (x + 16, y + 10))

    # player properties.
    playerX = 370
    playerY = 480
    playerX_change = 0

    while game_loop:
        global laser_state
        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window()

            # if keystroke is being pressed or not
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -6
                if event.key == pygame.K_RIGHT:
                    playerX_change = 6

                if event.key == pygame.K_SPACE:
                    if laser_state == "ready":
                        laserX = playerX
                        fire_laser(playerX, laserY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
        # boundaries
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # enemy movement
        enemyX += enemyX_change
        for i in range(num_of_enemies):

            # if enemy reaches the end of the screen ending game.
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over()
                start_game_button()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

                # laser collision with enemy.
            collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
            if collision:
                laserY = 480
                laser_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            # rendering enemies on the screen.
            enemy(enemyX[i], enemyY[i], i)

        # bullet movement
        if laserY <= 0:
            laserY = 480
            laser_state = "ready"

        if laser_state == "fire":
            fire_laser(laserX, laserY)
            laserY -= laserY_change

        player(playerX, playerY)
        show_score(score_x_coordinate, score_y_coordinate)
        pygame.display.update()


# handling game over.
def game_over():
    game_over_text()
    global game_loop
    game_loop = False


# closes the complete app and stops the game.
def close_window():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


# for tracking the state of whole application.
main_loop = True


# the main loop of the entire game application.
def main():
    while main_loop:
        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window()
        start_game_button()
        pygame.display.update()


# running the main app.
main()
