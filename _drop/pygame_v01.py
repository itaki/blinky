import pygame

pygame.init() #

win = pygame.display.set_mode((240,320))

pygame.display.set_caption('BLINKY')

x = 120
y = 160
radius = 15
velocity = 5
run = True

while run:
    win.fill((0,0,0))
    
    pygame.draw.circle(win, (255, 0, 0), (int(x), int(y)), radius)

    for event in pygame.event.get(): #
        if event.type == pygame.QUIT: #QUIT PUGAME
            run = False


    userInput = pygame.key.get_pressed() #

    if userInput[pygame.K_LEFT] and x > 0:
        x-=velocity
    if userInput[pygame.K_RIGHT] and x < 240:
        x+=velocity
    if userInput[pygame.K_UP] and y > 0:
        y-=velocity
    if userInput[pygame.K_DOWN] and y < 320:
        y+=velocity

    pygame.time.delay(10)

    pygame.display.update()



