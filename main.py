from pygame import *
from random import randint, choice

class GameSprite(sprite.Sprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__()
        self.image = image.load(pl_im)
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def reset(self): 
        win.blit(self.image, (self.rect.x, self.rect.y)) 
        
class Player(GameSprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        
    def update_r(self):
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.bottom < 500:
            self.rect.y += self.speed  
    
    def update_l(self):
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.bottom < 500:
            self.rect.y += self.speed    
  
class Ball(GameSprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        self.speedx = pl_speed
        self.speedy = pl_speed
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        

           
             
       
size_w = 700
size_h = 500
FPS = 60
mode = 'menu'
label_text = 'CLICK PLAY'

win = display.set_mode((size_w, size_h))
win_icon = image.load('icon_win.png')
display.set_icon(win_icon)
display.set_caption('Ping pong')
background = transform.scale(image.load('background.jpg'), (size_w, size_h))

font.init()
font_0 = font.SysFont('Book Antiqua', 70)
font_1 = font.SysFont('Book Antiqua', 40)
butt = Rect(210, 230, 275, 50)
play = font_1.render('PLAY', True, (0,0,0))
space = font_1.render('Нажмите пробел', True, (255,255,255))


mixer.init()
kick = mixer.Sound('kick.ogg')


player_r = Player(600, randint(200, 400), 'player.png', 10 )
player_l = Player(50, randint(200, 400), 'player.png', 10 )
ball = Ball(randint(200, 400), randint(200, 400), 'tennis.png', 0)


def start():
    global check_r, check_l, live_r, live_l, ball_play
    global player_l, player_r, ball
    check_r = 0
    check_l = 0
    live_r = 3
    live_l = 3
    ball_play = True
    player_r = Player(600, randint(200, 400), 'player.png', 10 )
    player_l = Player(50, randint(200, 400), 'player.png', 10 )
    ball = Ball(300, 300, 'tennis.png', 0)
    

    
start()    
clock = time.Clock()
while mode != 'end':
    win.blit(background, (0,0))
    if mode == 'menu':
        draw.rect(win, (221, 245, 84), butt)   
        win.blit(play, (300,230))
        label = font_1.render(label_text, True, (0,0,0))
        if label_text == 'CLICK PLAY':
            win.blit(label, (235, 150))
        else:
            win.blit(label, (195, 150))
                  
    elif mode == 'game':
        left_player = font_1.render(str(check_l), True, (255, 255, 255))
        right_player = font_1.render(str(check_r), True, (255, 255, 255))

        win.blit(left_player, (50, 30))
        win.blit(right_player, (600, 30))
        
    
        
        player_l.reset()
        player_r.reset()
        
        player_l.update_l()
        player_r.update_r()     
        
        ball.reset()
        ball.update()
        
        if ball.rect.colliderect(player_r.rect):
            kick.play()
            ball.speedx *= -1
  
        elif ball.rect.colliderect(player_l.rect):
            kick.play()
            ball.speedx *= -1  

        elif ball.rect.y < 0 or ball.rect.bottom > 500:
            ball.speedy *= -1 
        
        elif ball.rect.x > 700:
            ball.rect.x = 300
            ball.rect.y = 300
            check_l += 1 
            ball.speedx = 0
            ball.speedy = 0
            ball_play = True
        
        elif ball.rect.x < 0:
            ball.rect.x = 300
            ball.rect.y = 300
            check_r += 1 
            ball.speedx = 0
            ball.speedy = 0
            ball_play = True    
        

        if check_l >= 10:
            mode = 'win_l' 
            
            
        elif check_r >= 10:
            mode = 'win_r'
              
        if ball_play:
            win.blit(space, (235, 150))      
            
    
     
    
    elif mode == 'win_r':
        label_text = 'RIGHT PLAYER WIN!'
        start()
        mode = 'menu'
    
    elif mode == 'win_l':
        label_text = 'LEFT PLAYER WIN!'
        start() 
        mode = 'menu'     
        
    
    
    for e in event.get():
        if e.type == QUIT:
            mode = 'end'
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1 and mode == 'menu':
                if butt.collidepoint(e.pos):        
                    mode = 'game'
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and mode == 'game' and ball_play:
                ball.speedx = choice([5, -5, 3, -3])  
                ball.speedy = choice([5, -5, 3, -3]) 
                ball_play = False
                        
            
        
                
    clock.tick(FPS)
    display.update()
    
    

