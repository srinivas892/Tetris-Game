import pygame
import random
from pygame import mixer

pygame.init()
screen = width, height = 300, 500
win = pygame.display.set_mode(screen,pygame.NOFRAME)
clock = pygame.time.Clock()
FPS = 24
cell = 20
rows = (height-120)//cell
cols = width//cell

Font = pygame.font.Font('Fonts/Alternity-8w7J.ttf',50)
font2 = pygame.font.SysFont('cursive',25)
black = (21, 24, 29)
blue = (31, 25, 76)
red = (252, 91, 122)
white = (255, 255, 255)
img1 = pygame.image.load('Assets/1.png')
img2 = pygame.image.load('Assets/2.png')
img3 = pygame.image.load('Assets/3.png')
img4 = pygame.image.load('Assets/4.png')

Assets = {

   1: img1,
   2: img2,
   3: img3,
   4: img4 

}

class tetramion:
    
    #matrix 0 1 2 3
    #matrix 4 5 6 7
    #mtrix 8 9 10 11
    #matrix 12 13 14 15
    figures = {
       'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
       'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
       'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
       'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
       'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
       'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
       'O': [[1, 2, 5, 6]]
    }





    types = ['I','Z','S','L','J','T','O']



    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = random.choice(self.types)
        self.shape = self.figures[self.type]
        self.color = random.randint(1,4)
        self.rotation = 0 
    def image(self):
        return self.shape[self.rotation]  
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
    




class tetris:

 

    
    def __init__(self,row,col):
        mixer.music.load('background.mp3')
        mixer.music.play(-1)
        self.row = row
        self.col = col
        self.score = 0
        self.level = 1
        self.gameover = False
        self.next = None
        self.board = [[0 for j in range (col) ] for i in range (row)]
        self.new_figure()
  





    def draw_grid(self):
        for i in range(self.row+1)  :
            pygame.draw.line(win,white,(0,cell*i),(width,cell*i))      
        for j in range(self.col)  :
            pygame.draw.line(win,white,(cell*j, 0),(cell*j, height)) 
    def new_figure(self):
        if not self.next:
            self.next = tetramion(5,0)
        self.figure = self.next
        self.next = tetramion(5,0) 

    def intersect(self):           
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.row - 1 or \
                       j + self.figure.x > self.col - 1 or \
                       j + self.figure.x < 0 or \
                       self.board[i + self.figure.y][j + self.figure.x]>0:
                        intersection = True
        return intersection

    def remove_line(self):
        rerun = False
        for y in range(self.row - 1, 0, -1):
            is_full = True
            for x in range(0,self.col):
                if self.board[y][x] == 0:
                    is_full = False
            if is_full:
                clear = mixer.Sound('selection.wav')
                clear.play()
                del self.board[y]
                self.board.insert(0,[0 for i in range(self.col)])
                self.score += 1
                if self.score% 10 == 0:
                    self.level += 1
                rerun = True
        if rerun:
            self.remove_line()            


    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.remove_line()            
        self.new_figure()
        if self.intersect():
            self.gameover = True


        
    def go_down(self):
        self.figure.y += 1 
        if self.intersect():
            self.figure.y -= 1
            self.freeze() 
    def go_space(self):
        fall = mixer.Sound('fall.wav')
        fall.play()
        while not self.intersect():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_side(self,dx):
        self.figure.x += dx
        if self.intersect():
            self.figure.x -= dx 
    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate() 
      
counter = 0
move_down = False
canmove =True

tetris = tetris(rows,cols)
running = True
while  running:
    win.fill(black)
    
    
    counter += 1
    if counter >= 10000:
        counter = 0
    if canmove:   
        if counter % (FPS // (tetris.level * 2))  == 0 or move_down:
            if not tetris.gameover:
                tetris.go_down()


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                tetris.go_side (-1)  
            if event.key == pygame.K_RIGHT:
                tetris.go_side (1)  
            if event.key == pygame.K_UP:
                tetris.rotate() 
            if event.key == pygame.K_DOWN:
                move_down =True
            if event.key == pygame.K_SPACE:
                tetris.go_space()   
            if event.key == pygame.K_p:
                canmove = not canmove  
            if event.key == pygame.K_r:
                tetris.__init__(rows,cols) 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN: 
                move_down = False       


    # tetris.draw_grid()
    for x in range(rows):
        for y in range(cols):
            if tetris.board[x][y] > 0:
                val = tetris.board[x][y]
                img = Assets[val]
                win.blit(img, (y*cell , x*cell))
                pygame.draw.rect(win,white,(y*cell,x*cell,cell,cell), 1)
    for i in range(4):
        for j in range(4):
            if i*4 + j in tetris.figure.image():
                x = cell * (tetris.figure.x + j) 
                y = cell * (tetris.figure.y + i) 
                img  = Assets[tetris.figure.color]
                win.blit(img, (x, y))
                pygame.draw.rect(win,white,(x,y,cell,cell), 1)









    #gameover

    if tetris.gameover: 
        mixer.music.stop()       
        rect = pygame.Rect(50, 140, width-100, height-350)         
        pygame.draw.rect(win, black,rect)    
        pygame.draw.rect(win, red, rect ,2)    
        over = font2.render("Game Over",True,white)
        msg1 = font2.render("Press r to restart",True,white)
        msg2 = font2.render("Press q to Quit",True,white)

        win.blit(over, (rect.centerx-over.get_width()//2, rect.y+20))
        win.blit(msg1, (rect.centerx-msg1.get_width()//2, rect.y+80))
        win.blit(msg2, (rect.centerx-msg2.get_width()//2, rect.y+110))







   #HUD
    pygame.draw.rect(win,blue,(0,height-120,width,120)) 
    if tetris.next: 
        for i in range(4):
            for j in range(4):
                if i*4 + j in tetris.next.image():
                    x = cell * (tetris.next.x + j - 4) 
                    y = height -100 + cell * (tetris.next.y + i) 
                    img  = Assets[tetris.next.color]
                    win.blit(img, (x, y))            
                
    scoreimg = Font.render(f"{tetris.score}",True,white)
    levelimg = font2.render(f"Level : {tetris.level}",True,white)
    win.blit(scoreimg,(250-scoreimg.get_width()//2,height - 110))
    win.blit(levelimg,(250-levelimg.get_width()//2, height-30))

    pygame.draw.rect(win,blue,(0,0,width,height),2) 

    clock.tick(FPS)     
    pygame.display.update()


pygame.quit()


    

