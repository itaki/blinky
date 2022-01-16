import pygame
from pygame.locals import *






pygame.init()

#Number of TOOLS
num_of_tools = 10
#raplace this later

screen_width = 240
screen_height = 320
buffer = 5
buttons_width = screen_width - 50 
buttons_height = screen_height - 20
button_width = buttons_width/2 - buffer
button_height = buttons_height/num_of_tools - buffer


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('BLINKY')

font = pygame.font.SysFont('Menlo', 10)
#define colours
bg = '#16171d'
red = '#19d1e5'
black = (0, 0, 0)
white = (255, 255, 255)

#define global variable
clicked = False
counter = 0

class Button():
		
	#colours for button and text
	button_col = '#19d1e5'
	hover_col = (75, 225, 255)
	click_col = '#81f900'
	text_col = black
	width = button_width
	height = button_height

	def __init__(self, x, y, text):
		self.x = x
		self.y = y
		self.text = text

	def draw_button(self):

		global clicked
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#create pygame Rect object for the button
		button_rect = Rect(self.x, self.y, self.width, self.height)
		
		#check mouseover and clicked conditions
		if button_rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				clicked = True
				pygame.draw.rect(screen, self.click_col, button_rect)
			elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
				clicked = False
				action = True
			else:
				pygame.draw.rect(screen, self.hover_col, button_rect,border_radius = 12)
		else:
			pygame.draw.rect(screen, self.button_col, button_rect,border_radius = 12)
		
		#add shading to button
		# pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
		# pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
		# pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
		# pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

		#add text to button
		text_img = font.render(self.text, True, self.text_col)
		text_len = text_img.get_width()
		screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
		return action

buttons = []



again = Button(10, 10, 'Play Again?')
quit = Button(200, 10, 'Quit?')
down = Button(10, 250, 'Down')
up = Button(200, 250, 'Up')


run = True
while run:

	screen.fill(bg)

	if again.draw_button():
		print('Again')
		counter = 0
	if quit.draw_button():
		print('Quit')
	if up.draw_button():
		print('Up')
		counter += 1
	if down.draw_button():
		print('Down')
		counter -= 1

	counter_img = font.render(str(counter), True, red)
	screen.blit(counter_img, (200, 250))


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False	


	pygame.display.update()


pygame.quit()
