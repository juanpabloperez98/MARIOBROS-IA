import pygame
from Libs import variables as v
from Libs import funciones as f


def start():
    pygame.init()
    pygame.mixer.music.play(-1)
    v.screen
    while not v.end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v.end_game = True
            if event.type == pygame.KEYDOWN:
                
                if not v.algoritmo:

                    v.MARIO_PLAYER.start = True

                    if event.key == pygame.K_DOWN:
                        f.do_movement(1)         
                    if event.key == pygame.K_UP:
                        f.do_movement(2)     
                    if event.key == pygame.K_RIGHT:
                        f.do_movement(3)   
                    if event.key == pygame.K_LEFT:
                        f.do_movement(4)
       
        v.screen.fill(v.NEGRO)
        v.ls_f,v.ls_c = f.draw_cuadricule()
        if not v.draw_first_time:
            f.create_bros()
            v.draw_first_time = True
        if not v.draw_honguito:
            f.create_honguito()
            v.draw_honguito = True        
        
        
        if v.algoritmo:
            v.MARIO_PLAYER.start = True
            if v.algoritmo_start:
                v.lm = f.createProblem(v.MARIO_PLAYER.vx,v.MARIO_PLAYER.vy,v.x,v.y)
                v.algoritmo_start = False
                

                
        if v.lm:
            punto = v.lm.pop()
            if(punto[0]=='r'):
                f.do_movement(3)
            elif(punto[0]=='l'):
                f.do_movement(4)
            elif(punto[0]=='d'):
                f.do_movement(1)
            elif(punto[0]=='u'):
                f.do_movement(2)
        else:
            v.algoritmo_start = True    
        f.comer()
        v.todos.draw(v.screen)
        v.todos.update()
        pygame.display.flip()
        v.reloj.tick(4)



    


if __name__ == "__main__":
    start()
    
