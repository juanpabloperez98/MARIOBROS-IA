import pygame
import random
import time
from Libs import variables as v
from simpleai.search import SearchProblem, astar, depth_first, breadth_first

COSTS = {
        "up": 1.0,
        "down": 1.0,
        "left": 1.0,
        "right": 1.0,
}

#CLASE MARIO
class MARIO_BROS(pygame.sprite.Sprite):
    def __init__(self,m):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.action = 0
        self.i = 0
        self.image = self.m[self.action][self.i]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.vx = 0
        self.vy = 0
        self.x = 0
        self.y = 0
        self.start = False
    
    def update(self):

        if self.x != 0 or self.y !=0:
            self.vx += self.x               
            self.vy += self.y
            self.rect.x = v.ls_c[self.vx]
            self.rect.y = v.ls_f[self.vy]
            
        
        self.i += 1
        #print("jugador: ",self.vx,"jugador: ",self.vy)
        if self.i >= len(self.m[self.action]):
            if self.action == 1:                    
                self.i = 1
            else:
                self.i = 0
        
        if not self.start:
            self.i = 0
        
        self.image = self.m[self.action][self.i]

#DRAW CUADRICULE
def draw_cuadricule():

    lista_f = []
    lista_c = []
    nv = 0
    mario = MARIO_BROS(v.m_mario)
    for f in range(v.height):
        if(f%mario.rect.height == 0):
            #pygame.draw.line(v.screen,v.BLANCO,[0,f],[v.width,f],2)
            if nv <= 0:                    
                for c in range(v.width):
                    if(c%mario.rect.width == 0):
                        #pygame.draw.line(v.screen,v.BLANCO,[c,0],[c,v.height],2)
                        lista_c.append(c)
            
                nv += 1
            lista_f.append(f)
    
    #print(len(lista_f),len(lista_c))
    return lista_f,lista_c

#CUTOUT FUNCTION
def Recortar(nf,nc,imagen,limites,sx,sy):
    image=pygame.image.load(imagen)
    info=image.get_rect()
    an_imagen=info[2]
    al_imagen=info[3]
    an_corte=int(an_imagen/nc)
    al_corte=int(al_imagen/nf)
    m=[]
    for y in range(nf):
        fila=[]
        for x in range(limites[y]):
            cuadro=image.subsurface(x*an_corte,y*al_corte,an_corte,al_corte)
            cuadro=pygame.transform.scale(cuadro,(sx,sy))
            fila.append(cuadro)
        m.append(fila)
    return m
        
#CREAR MARIO BROS
def create_bros():
    x = random.randrange(len(v.ls_c))
    y = random.randrange(len(v.ls_f))
    #x=2
    #y=5
    v.MARIO_PLAYER.vx = x
    v.MARIO_PLAYER.vy = y
    v.MARIO_PLAYER.rect.x = v.ls_c[x]
    v.MARIO_PLAYER.rect.y = v.ls_f[y]
    #print(v.MARIO_PLAYER.rect.x,v.MARIO_PLAYER.rect.y)

#DO MOVEMENT
def do_movement(i):
    if (i==1):
        if v.algoritmo:                
            v.MARIO_PLAYER.y = 1     
            v.MARIO_PLAYER.x = 0      
            v.MARIO_PLAYER.action = 0            
        else:
            v.MARIO_PLAYER.y = 1     
            v.MARIO_PLAYER.x = 0      
            v.MARIO_PLAYER.action = 0
            v.MARIO_PLAYER.i = 0
    if (i==2):
        if v.algoritmo:                
            v.MARIO_PLAYER.y = -1                    
            v.MARIO_PLAYER.action = 3
            v.MARIO_PLAYER.x = 0
        else:
            v.MARIO_PLAYER.y = -1                    
            v.MARIO_PLAYER.action = 3
            v.MARIO_PLAYER.x = 0
            v.MARIO_PLAYER.i = 0

    if (i==3):

        if v.algoritmo:                
            v.MARIO_PLAYER.y = 0
            v.MARIO_PLAYER.action = 1             
            v.MARIO_PLAYER.x = 1
        else:
            v.MARIO_PLAYER.y = 0
            v.MARIO_PLAYER.action = 1             
            v.MARIO_PLAYER.x = 1
            v.MARIO_PLAYER.i = 0

    if (i==4):
    
        if v.algoritmo:                    
            v.MARIO_PLAYER.x = -1
            v.MARIO_PLAYER.action = 2                     
            v.MARIO_PLAYER.y = 0
        else:
            v.MARIO_PLAYER.x = -1
            v.MARIO_PLAYER.action = 2                     
            v.MARIO_PLAYER.y = 0
            v.MARIO_PLAYER.i = 0


#DRAW FOOD
class FOOD(pygame.sprite.Sprite):
    def __init__(self,m):
        pygame.sprite.Sprite.__init__(self)
        self.action = 0
        self.i = 0
        self.m = m
        self.image = self.m[self.action][self.i]
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('Sonido/hongo_sonido.ogg')

def create_honguito():
    v.HONGUITO_FOOD = FOOD(v.m_honguito)
    v.x = random.randrange(len(v.ls_c))
    v.y = random.randrange(len(v.ls_f)-1)
    v.HONGUITO_FOOD.rect.x = v.ls_c[v.x] + v.HONGUITO_FOOD.rect.width/2 - 10
    v.HONGUITO_FOOD.rect.y = v.ls_f[v.y] + v.HONGUITO_FOOD.rect.height/2 + 10
    v.todos.add(v.HONGUITO_FOOD)

#EAT
def comer():    
    #print("COMIDA X:",v.x,"COMIDA Y: ",v.y)
    
    if (v.ls_c[v.MARIO_PLAYER.vx] == v.ls_c[v.x-1] and v.ls_f[v.MARIO_PLAYER.vy] == v.ls_f[v.y]) or  (v.ls_c[v.MARIO_PLAYER.vx] == v.ls_c[v.x+1] and v.ls_f[v.MARIO_PLAYER.vy] == v.ls_f[v.y]) or (v.ls_c[v.MARIO_PLAYER.vx] == v.ls_c[v.x] and v.ls_f[v.MARIO_PLAYER.vy] == v.ls_f[v.y+1]) or (v.ls_c[v.MARIO_PLAYER.vx] == v.ls_c[v.x] and v.ls_f[v.MARIO_PLAYER.vy] == v.ls_f[v.y-1]):
        v.HONGUITO_FOOD.sound.play()
    if (v.MARIO_PLAYER.vx == v.x and v.MARIO_PLAYER.vy ==v.y):        
        #v.HONGUITO_FOOD.sound.play()
        #time.sleep(1)
        v.todos.remove(v.HONGUITO_FOOD)
        v.draw_honguito = False

class MarioGame(SearchProblem):


    def __init__(self,initial,goal):
        self.initial = initial
        self.goal = goal

        super(MarioGame, self).__init__(initial_state=self.initial)
    

    def actions(self, state):    

        actions = []
        for action in list(COSTS.keys()):
                newx, newy = self.result(state, action)
                if (newx < len(v.ls_c)) and (newx >= 0) and (newy < len(v.ls_f)) and (newy >= 0):
                    actions.append(action)
        return actions

    def result(self, state, action):
    
        x, y = state

        if action.count("up"):
                y -= 1
        if action.count("down"):
                y += 1
        if action.count("left"):
                x -= 1
        if action.count("right"):
                x += 1

        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    """def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)"""



def createProblem(vx,vy,x_comida,y_comida):
    problem = MarioGame((vx,vy),(x_comida,y_comida))
    result = breadth_first(problem,graph_search=True)
    path = [x[1] for x in result.path()]
    moves =  result.path()
    moves = moves[1:]
    lm = []

    for i in moves:
        lm.append(i[0])

    
    lm.reverse()
    return lm


     

    

        
 
