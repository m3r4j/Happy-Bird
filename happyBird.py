import pygame
import sys
import random
import os

def checkData():
	if not os.path.exists('data'):
		os.mkdir('data')

	if not os.path.exists('data/bestscore.log'):
		with open('data/bestscore.log', 'w', errors='ignore', encoding='utf-8') as file:
			file.write('0')


def getScore():
	try:
		with open('data/bestscore.log', 'r', errors='ignore', encoding='utf-8') as file:
			data = file.readlines()
			for i in data:
				return int(i)
	except:
		return 0


def saveScore(score):
	with open('data/bestscore.log', 'w', errors='ignore', encoding='utf-8') as file:
		file.write(str(score))


pygame.init()
pygame.mixer.init()
pygame.font.init()

font = pygame.font.SysFont(None, 30)

black = (0, 0, 0)
grey = (192, 192, 192)
white = (255, 255, 255)
cyan = (0, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

width, height = 800, 600

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('Happy Bird')

game_icon = pygame.image.load('icon.png')

try:
	pygame.display.set_icon(game_icon)

except:
	pass


fps = 60

clock = pygame.time.Clock()

text_color = red

class sounds:
	pass

def draw_score(score):
	score_text = font.render(f'SCORE: {score}', True, text_color)
	window.blit(score_text, (0, 0))


def draw_best_score(best_score):
	best_text = font.render(f'BEST: {best_score}', True, text_color)
	window.blit(best_text, (0, 20))


def draw_instructions():
	instruction_text = font.render("PRESS 'SPACE' TO BEGIN", True, text_color)
	window.blit(instruction_text, (width // 2, height // 2))


character_width = 35
character_height = 35

character = pygame.image.load('sprites/character.png')
character = pygame.transform.scale(character, (character_width, character_height))




def main():
	block_speed = 0.10
	block_speed_add = 0.02
	
	floor_width = width
	floor_height = 100
	floor_color = grey

	line_width = width
	line_height = 10
	line_color = cyan

	floor_down_x = 0
	floor_down_y = height - floor_height

	line_down_x = 0
	line_down_y = floor_down_y - line_height


	floor_up_x = 0
	floor_up_y = 0

	line_up_x = 0
	line_up_y = floor_height

	checkData()
	score = 0
	best_score = getScore()

	block_color = red

	block_range_1, block_range_2 = 50, 150

	block_down_width = 50
	block_down_height = random.randint(block_range_1, block_range_2)
	#block_down_height = 115

	block_up_width = 50
	block_up_height = random.randint(block_range_1, block_range_2)
	#block_up_height = 115

	
	

	character_x = 100
	character_y = height // 2.15

	block_down_x = width - block_down_width
	block_down_y = line_down_y - block_down_height

	block_up_x = width - block_up_width
	block_up_y = line_up_y + line_height

	character_gravity = 0.10
	game_started = False
	game_over = False


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_started = True
					character_y -= 50
					

		window.fill(black)

		floor_down_rect = pygame.Rect(floor_down_x, floor_down_y, floor_width, floor_height)
		line_down_rect = pygame.Rect(line_down_x, line_down_y, line_width, line_height)
		pygame.draw.rect(window, floor_color, floor_down_rect)
		pygame.draw.rect(window, line_color, line_down_rect)

		floor_up_rect = pygame.Rect(floor_up_x, floor_up_y, floor_width, floor_height)
		line_up_rect = pygame.Rect(line_up_x, line_up_y, line_width, line_height)
		pygame.draw.rect(window, floor_color, floor_up_rect)
		pygame.draw.rect(window, line_color, line_up_rect)

		draw_score(score)
		draw_best_score(best_score)

		if game_started:
			block_down_rect = pygame.Rect(block_down_x, block_down_y, block_down_width, block_down_height)
			pygame.draw.rect(window, red, block_down_rect)

			block_up_rect = pygame.Rect(block_up_x, block_up_y, block_up_width, block_up_height)
			pygame.draw.rect(window, red, block_up_rect)

		window.blit(character, (character_x, character_y))
		character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

		if game_started:
			block_down_x -= block_speed
			block_up_x -= block_speed


		if block_down_x < -block_down_width:
			block_down_x = width - block_down_width
			block_up_x = width - block_up_width

			block_down_height = random.randint(block_range_1, block_range_2)
			block_up_height = random.randint(block_range_1, block_range_2)

			block_down_y = line_down_y - block_down_height
			block_up_y = line_up_y + line_height

			block_speed += block_speed_add
			score += 1

		if game_started: # Check if the game has started
			if character_y >= line_down_y - character_height or character_y <= line_up_y + line_height or character_rect.colliderect(block_up_rect) or character_rect.colliderect(block_down_rect):
				game_over = True

			character_y += character_gravity # Gravity pulling down the bird


		if score > best_score:
			saveScore(score)
			best_score = score


		if game_started == False:
			draw_instructions()


		if game_over: # If the game is over then:
			pygame.display.update()
			pygame.time.delay(2000)
			main()


		pygame.display.update()
main()