import pygame



def init_console():
    pygame.init()
    console_window = pygame.display.set_mode((400, 700))
    pygame.display.set_caption("CTD")
    return console_window


def update_console(console_window, score, Game_on, Terminate = False, Reset = False):
    console_window.fill((0,0,0))
    font = pygame.font.SysFont("Courier", 18)
    y = 20

    if not Game_on and score == 0:
        y += 18
        score_surface = font.render(f"Game Over! Score: {score}", True,  (255,255,255))
        console_window.blit(score_surface, (50,y))

    for i in range(1, score+1):
        score_surface = font.render(f"Score: {i}", True, (255,255,255))
        console_window.blit(score_surface, (50,y))
        
        if Game_on == False and i == score:
            y += 18
            score_surface = font.render(f"Game Over! Score: {score}", True,  (255,255,255))
            console_window.blit(score_surface, (50,y))
    
        y += 20
    

    if Terminate:
        y += 18
        score_surface = font.render(f"Goodbye! Score: {score}", True,  (255,255,255))
        console_window.blit(score_surface, (50,y))
    
    if Reset:
        y += 18
        score_surface = font.render(f"Starting Over!", True,  (255,255,255))
        console_window.blit(score_surface, (50,y))
    
    pygame.display.update()