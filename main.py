import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours
BACKGROUND = (0, 0, 0)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Bird Game')
 
 
#player class
class Bird:
	def __init__(self,player_image,gravity,jump_h,posx,posy):
		self.image=pygame.image.load(player_image).convert_alpha()
		self.rect=self.image.get_rect()
		self.gravity=gravity
		self.acc=0
		self.jump_height=jump_h
		self.rect.y=posy
		self.rect.x=posx
		self.dy=-self.jump_height
		self.jumping=False
	def draw(self):
		WINDOW.blit(self.image,self.rect)
	def jump(self):
		if self.jumping:
				
			self.dy+=self.gravity
			self.rect.y += self.dy
			if self.dy>=0:
				self.jumping=False
				self.dy=0
			

	def g_force(self):
		if self.rect.y < WINDOW_HEIGHT - self.rect.height:  # Prevent falling
			self.dy += self.gravity
			self.rect.y += self.dy
		else:
			self.rect.y = WINDOW_HEIGHT - self.rect.height

#coloumn class
class coloumn:
	def __init__(self,width):
		self.width=width
		self.height1=random.randint(30,WINDOW_HEIGHT - 150 - 30)
		self.height2=WINDOW_HEIGHT -30 -self.height1 
		self.rect_up=Rect(WINDOW_WIDTH,0,self.width,self.height1)
		self.rect_down=Rect(WINDOW_WIDTH,self.height1+150,self.width,self.height2)
	def draw(self):
		pygame.draw.rect(WINDOW,(255,0,0),self.rect_up)
		pygame.draw.rect(WINDOW,(255,0,0),self.rect_down)
		self.rect_up.move_ip(-2,0)
		self.rect_down.move_ip(-2,0)

# The main function that controls the game
def run_game() :
	
	#player init
	flappy=Bird("images/bird.png",1,8,200,10)
	
	#coloumn init
	
	obs=[]
	for i in range(1000):
		obs.append(coloumn(50))
	cnt=0
	run = True
	score=0
	cs=True
  	#The main game loop
	while run:
		WINDOW.fill(BACKGROUND)
		#keyboard input
		key=pygame.key.get_pressed()
		if key[pygame.K_SPACE]:
			#print('works key space')
			flappy.jumping = True
			flappy.dy = -flappy.jump_height
		# Get inputs
		for event in pygame.event.get() :
			if event.type == QUIT :
				pygame.quit()
				sys.exit()
    
		# Processing
		flappy.draw()
		obs[cnt].draw()
		if obs[cnt].rect_up.x<=flappy.rect.x +150:
			obs[cnt+1].draw()
		if obs[cnt].rect_up.x<0:
			cs=True
			cnt+=1
		if cs and obs[cnt].rect_up.x<flappy.rect.x-70:
			score+=1
			cs=False
		
		if flappy.rect.colliderect(obs[cnt].rect_up) or flappy.rect.colliderect(obs[cnt].rect_down) or flappy.rect.colliderect(obs[cnt+1].rect_up) or flappy.rect.colliderect(obs[cnt+1].rect_down):
			print("You lost! Your score is :",cnt)
			with open("data/score.txt",'a') as score_file:
				score_file.write(str(score)+'\n')
			run=False
		if cnt==999 and obs[999].rect_up.x<flappy.rect.x -70:
			print("you won")
			run=False
		if flappy.jumping:
			flappy.jump()
		else:
			flappy.g_force()
		
		font = pygame.font.Font('freesansbold.ttf', 32)
		text=font.render("score: "+str(score), True,(255,255,255),(0,0,0))
		textRect=text.get_rect()
		textRect.y=0
		textRect.x=0
		
		# Render elements of the game
		WINDOW.blit(text, textRect)
		pygame.display.update()
		fpsClock.tick(FPS)

run_game()
