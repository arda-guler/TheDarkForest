import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_x,
    K_z,
)
import time

from galaxy import *
from warden import *

SCREEN_X = 1280
SCREEN_Y = 720

SCREEN_X_2 = SCREEN_X * 0.5
SCREEN_Y_2 = SCREEN_Y * 0.5

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
    pygame.display.set_caption("The Dark Forest")
    pygame.font.init()
    default_font = pygame.font.SysFont("Times New Roman", 20)

    energy_text_placement = (int(SCREEN_X * 0.05), SCREEN_Y - 30)
    ship_name_placement = (int(SCREEN_X * 0.05), SCREEN_Y - 60)
    int_class_placement = (int(SCREEN_X_2), SCREEN_Y - 70)
    win_text_placement = (int(SCREEN_X_2), SCREEN_Y - 40)

    universe_size = [42, 20] # [85, 42]
    universe = Galaxy(universe_size)
    grid_size = min(SCREEN_X / universe_size[0], SCREEN_Y / universe_size[1])

    player = Warden([1, 1], 0, 5, grid_size)
    player_sect = universe.sectors[player.pos[1]][player.pos[0]]
    travel_expense = 0.6
    gathering_expense = 0.2
    projectiles = []

    running = True
    player_move = False
    turns = 0
    while running:

            if player_move:
                for proj in projectiles:
                    proj.move()

                player_sect = universe.sectors[player.pos[1]][player.pos[0]]
                player_sect.explored = True

                if player_sect.intelligence:
                    if player_sect.intelligence_class == "EXPANSIONIST":
                        player.energy -= player_sect.progress * random.uniform(0.5, 1.5) / 10

                for idx_y in range(len(universe.sectors)):
                    for idx_x in range(len(universe.sectors[0])):
                        sector = universe.sectors[idx_y][idx_x]
                        sector.do_progress()

                        dist_to_player = ((player.pos[0] - sector.pos[0])**2 + (player.pos[1] - sector.pos[1])**2)**0.5
                        if sector.intelligence and dist_to_player < sector.signal_strength / 10 - 1:
                            sector.explored = True

                        for proj in projectiles:
                            if sector.resource and sector.pos == proj.pos:
                                if type(proj) == type(Photoid([0, 0], 0, 0)):
                                    sector.intelligence = 0
                                    sector.progress = 0
                                    sector.life = 0
                                    projectiles.remove(proj)
                                    del proj

                if player.energy <= 0:
                    win_text_surface = default_font.render("STARSHIP OUT OF ENERGY - GAME OVER", False,
                                                           (255, 0, 0))
                    screen.blit(win_text_surface, win_text_placement)
                    pygame.display.flip()
                    time.sleep(8)
                    running = False

                unexplored_sectors_num = 0
                dangerous_sectors_num = 0
                for idx_y in range(len(universe.sectors)):
                    for idx_x in range(len(universe.sectors[0])):
                        sector = universe.sectors[idx_y][idx_x]
                        if sector.intelligence and not sector.intelligence_class == "TOMB":
                            dangerous_sectors_num += 1

                        if sector.resource and not sector.explored:
                            unexplored_sectors_num += 1

                if (not unexplored_sectors_num) and (not dangerous_sectors_num):
                    win_text_surface = default_font.render("MISSION ACCOMPLISHED - ALL THREATS ELIMINATED", False, (0, 255, 0))
                    screen.blit(win_text_surface, win_text_placement)
                    pygame.display.flip()
                    time.sleep(8)
                    running = False

            player_move = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == KEYDOWN:
                    player_move = True
                    turns += 1
                    if event.key == K_UP and player.pos[1] > 0:
                        player.pos[1] -= 1
                        player.dir = 0
                        player.energy -= travel_expense
                    elif event.key == K_DOWN and player.pos[1] < universe.size[1] - 1:
                        player.pos[1] += 1
                        player.dir = 2
                        player.energy -= travel_expense
                    elif event.key == K_LEFT and player.pos[0] > 0:
                        player.pos[0] -= 1
                        player.dir = 3
                        player.energy -= travel_expense
                    elif event.key == K_RIGHT and player.pos[0] < universe.size[0] - 1:
                        player.pos[0] += 1
                        player.dir = 1
                        player.energy -= travel_expense
                    elif event.key == K_x:
                        if player_sect.resource and player_sect.resource_amount > 1:
                            player.energy -= gathering_expense
                            player.energy += player_sect.resource_amount - 1
                            player_sect.resource_amount = 1
                    elif event.key == K_z:
                        if player.energy > 5:
                            player.energy -= 5
                            if player.dir == 0:
                                new_photoid_pos = [player.pos[0], player.pos[1]-1]
                            elif player.dir == 1:
                                new_photoid_pos = [player.pos[0]+1, player.pos[1]]
                            elif player.dir == 2:
                                new_photoid_pos = [player.pos[0], player.pos[1]+1]
                            else:
                                new_photoid_pos = [player.pos[0]-1, player.pos[1]]

                            new_photoid = Photoid(new_photoid_pos, player.dir, grid_size)
                            projectiles.append(new_photoid)

            screen.fill((0, 0, 0))

            # draw the galaxy
            for idx_y in range(len(universe.sectors)):
                for idx_x in range(len(universe.sectors[0])):
                    current_draw_sector = universe.sectors[idx_y][idx_x]

                    if current_draw_sector.explored:
                        if current_draw_sector.intelligence:
                            pygame.draw.circle(screen, (255, 0, 255), (grid_size * (idx_x + 0.5), grid_size * (idx_y + 0.5)),
                                               int(grid_size / 5))
                        elif current_draw_sector.life:
                            pygame.draw.circle(screen, (0, 255, 0), (grid_size * (idx_x + 0.5), grid_size * (idx_y + 0.5)),
                                               int(grid_size / 5))
                        elif current_draw_sector.resource:
                            pygame.draw.circle(screen, (255, 255, 0), (grid_size * (idx_x + 0.5), grid_size * (idx_y + 0.5)),
                                               int(grid_size/5))

                    elif current_draw_sector.resource:
                        pygame.draw.circle(screen, (255, 255, 255),
                                           (grid_size * (idx_x + 0.5), grid_size * (idx_y + 0.5)),
                                           int(grid_size / 5))


            player_rect = pygame.Rect((grid_size * (player.pos[0]), grid_size * (player.pos[1]),
                                       grid_size, grid_size))
            screen.blit(player.images[player.dir], player_rect)

            energy_text_surface = default_font.render("Energy: " + str(round(player.energy, 1)), False, (255, 0, 0))
            screen.blit(energy_text_surface, energy_text_placement)

            ship_name_surface = default_font.render("Starship " + player.ship_name, False, (255, 0, 0))
            screen.blit(ship_name_surface, ship_name_placement)

            for proj in projectiles:
                if type(proj) == type(Photoid([0, 0], 0, 0)):
                    proj_rect = pygame.Rect((grid_size * (proj.pos[0]), grid_size * (proj.pos[1]),
                                        grid_size, grid_size))
                    screen.blit(proj.images[proj.dir], proj_rect)

            if universe.sectors[player.pos[1]][player.pos[0]].intelligence:
                sect = universe.sectors[player.pos[1]][player.pos[0]]
                int_class_surface = default_font.render(sect.intelligence_class + ", POPULATION: " + str(sect.population), False, (255, 0, 0))
                screen.blit(int_class_surface, int_class_placement)

            pygame.display.flip()

            time.sleep(0.1)

    pygame.quit()

main()
