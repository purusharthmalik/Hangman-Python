import pygame
import math
import random
from nltk.corpus import words, wordnet



def main():
    # display
    pygame.init()
    WIDTH, HEIGHT = 800, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman Game")

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    # load_images
    images = []
    for i in range(7):
        images.append(pygame.image.load("/home/purusharth/PycharmProjects/PythonProject/Hangman/images/hangman{}.png".format(i)))

    #colors
    BLACK = (0, 0, 0)
    BKGROUND = (102, 204, 204)

    # buttons
    RADIUS = 20
    GAP = 15
    letters = []
    startx, starty = round((WIDTH-(RADIUS*2 + GAP)*13)/2), 400
    A = 65
    for i in range(26):
        x = startx + GAP*2 + ((RADIUS*2 + GAP)*(i%13))
        y = starty + ((i//13) * (GAP + RADIUS*2))
        letters.append([x, y, chr(A + i), True])

    #fonts
    LETTER_FONT = pygame.font.SysFont('comicsans', 40)
    WORD_FONT = pygame.font.SysFont('comicsans', 60)
    TITLE_FONT = pygame.font.SysFont('comicsans', 80)
    HINT_FONT = pygame.font.SysFont('comicsans', 25)
    HOME_FONT = pygame.font.SysFont('comicsans', 100)

    # game-variables
    hangman_status = 0
    WORD = random.choice(words.words('en-basic')).upper()
    guessed = []

    def home():
        win.fill(BKGROUND)
        win.blit(pygame.image.load("/home/purusharth/PycharmProjects/PythonProject/Hangman/images/hangman6.png"), (100, 80))        
        text = HOME_FONT.render("HANGMAN!", 1, BLACK)
        win.blit(text, (350,150))
        pygame.draw.ellipse(win, BLACK, [460,235,150,70], 5)
        text = LETTER_FONT.render("START", 1, BLACK)
        win.blit(text, (487,257))
        text = LETTER_FONT.render("RULES:",1, BLACK)
        win.blit(text, (40, 340))
        text = HINT_FONT.render("1 - You will be given a random word and you have to guess it.", 1, BLACK)
        win.blit(text, (40,380))
        text = HINT_FONT.render("2 - You can only make 5 mistakes or else the man will be HANGED!",1, BLACK)
        win.blit(text, (40,405))
        text = HINT_FONT.render("3 - You will be given 2 hints (Different meanings of that word)",1,BLACK)
        win.blit(text, (40,430))
        pygame.display.update()
        x = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] in range(460,610) and pygame.mouse.get_pos()[1] in range(235,305):
                        x = 1
                        break
            if x == 1:
                break
            

    # gameloop


    home()
    def draw():
        win.fill(BKGROUND)

        # title
        text = TITLE_FONT.render("HANGMAN!", 1, BLACK)
        win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

        # draw word
        display_word = ""
        for letter in WORD:
            if letter in guessed:
                display_word += letter + " "
            else:
                display_word += "_ "
        text = WORD_FONT.render(display_word, 1, BLACK)
        win.blit(text, (400,200))

        for letter in letters:
            x, y, l,visible = letter
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            if visible:
                text = LETTER_FONT.render(l, 1, (0,0,0))
                win.blit(text, (x - (text.get_width())/2, y - (text.get_height())/2))

        win.blit(images[hangman_status], (150, 100))

        text = HINT_FONT.render(wordnet.synsets(WORD)[0].definition().split(",")[0], 1, BLACK)
        win.blit(text, (90, 325))
        try:
            text = HINT_FONT.render(wordnet.synsets(WORD)[1].definition().split(",")[0], 1, BLACK)
            win.blit(text, (90, 350))
        except:
            pass
        text = HINT_FONT.render("1 - ", 1, BLACK)
        win.blit(text, (65, 325))
        text = HINT_FONT.render("2 - ", 1, BLACK)
        win.blit(text, (65, 350))
        pygame.display.update()


    def display_message(message):
        pygame.time.delay(1000)
        win.fill(BKGROUND)
        text = WORD_FONT.render(message, 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, l, visible = letter
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if visible:
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(l)
                            if l not in WORD:
                                hangman_status +=1
        draw()

        if all(x in guessed for x in WORD):
            display_message("You WON!!!")
            break

        if hangman_status == 6:
            display_message("You LOST! Word was '{}'".format(WORD.upper()))
            break
        

    win.fill(BKGROUND)
    text = WORD_FONT.render("Do you want to play again?", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.draw.circle(win, BLACK, (300,340), 50, 3)
    text = WORD_FONT.render("YES", 1, BLACK)
    win.blit(text, (260,320))
    pygame.draw.circle(win, BLACK, (500,340), 50, 3)
    text = WORD_FONT.render("NO", 1, (0,0,0))
    win.blit(text, (470,320))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x in range(270, 321) and y in range(326, 377):
                    main()
                elif x in range(470, 521) and y in range(326, 377):
                    win.fill(BKGROUND)
                    text = WORD_FONT.render("GOODBYE!", 1, BLACK)
                    win.blit(text, (WIDTH/2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    pygame.quit()
            


if __name__ == "__main__":
    main()