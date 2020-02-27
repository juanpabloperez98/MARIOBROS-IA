import pygame
import random
from Libs import funciones as f
pygame.mixer.init()

#COLORES
VERDE=[0,255,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
ROJO=[255,0,0]
AZUL=[0,0,255]

#PANTALLA
width = 800
height = 600
screen = pygame.display.set_mode([width,height])

#CUADRICULA
ls_c=[]
ls_f=[]

#GRUPO DE SPRITES
todos = pygame.sprite.Group()


#VARIABLES JUEGO
end_game = False
algoritmo = True
#RELOJ
reloj = pygame.time.Clock()

#MARIO
limites = [7,7,7,7]
imagen_mario = 'imagenes/spritemario.png'
m_mario = f.Recortar(4,7,imagen_mario,limites,40,80)
MARIO_PLAYER = f.MARIO_BROS(m_mario)
todos.add(MARIO_PLAYER)
draw_first_time = False


#FOOD
imagen_honguito = 'imagenes/honguito.png'
limites = [1]
m_honguito = f.Recortar(1,1,imagen_honguito,limites,30,30)
draw_honguito = False
HONGUITO_FOOD = 0
x = 0
y = 0


#Algortimo
lm = []
algoritmo_start = True


#MUSICA 

sonido_dir = 'Sonido/fondo.mp3'
sonido = pygame.mixer.music.load(sonido_dir)
