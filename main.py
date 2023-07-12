import pygame
from tetrominoes import Tetrominoes


# draws game stats for keeping track of progress
def draw_board(screen, font, score, line_count):
    pygame.draw.rect(screen, (155, 155, 255), (600, 50, 250, 50), 0, 5)
    screen.blit(font.render("SCORE", True, (50, 50, 50)), (665, 60))
    screen.blit(font.render(str(score), True, (255, 255, 255)), (675, 125))
    pygame.draw.rect(screen, (155, 155, 255), (600, 175, 250, 50), 0, 2)
    screen.blit(font.render("LINES", True, (50, 50, 50)), (665, 185))
    screen.blit(font.render(str(line_count), True, (255, 255, 255)), (675, 250))
    pygame.draw.rect(screen, (155, 155, 255), (600, 295, 250, 50), 0, 2)
    screen.blit(font.render("NEXT BLOCK", True, (50, 50, 50)), (620, 305))
    pygame.draw.rect(screen, (155, 155, 255), (600, 50, 250, 550), 3, 5)


# draws game over menu to allow for replaying
def draw_menu(screen, font):
    pygame.draw.rect(screen, (155, 155, 255), (200, 300, 200, 50))
    pygame.draw.rect(screen, (155, 155, 255), (200, 350, 200, 50))
    screen.blit(font.render("G   A   M   E", True, (50, 50, 50)), (212, 310))
    screen.blit(font.render("O   V   E   R", True, (50, 50, 50)), (213, 360))
    pygame.draw.rect(screen, (155, 155, 255), (150, 500, 300, 50), 0)
    screen.blit(font.render("R   E   P    L   A   Y", True, (50, 50, 50)), (163, 510))


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()
    block = Tetrominoes()

    score = 0
    line_count = 0

    paused = False
    pause_sound = pygame.mixer.Sound('sounds/pause-sound.wav')
    play_icon = pygame.image.load('images/play-icon.png')
    play_icon = pygame.transform.scale(play_icon, (80, 80))
    paused_icon = pygame.image.load('images/paused-icon.png')
    paused_icon = pygame.transform.scale(paused_icon, (80, 80))

    muted = False
    mute_sound = pygame.mixer.Sound('sounds/mute-sound.wav')
    sound_icon = pygame.image.load('images/sound-icon.png')
    sound_icon = pygame.transform.scale(sound_icon, (92, 64))
    muted_icon = pygame.image.load('images/muted_icon.png')
    muted_icon = pygame.transform.scale(muted_icon, (80, 64))

    game_over = False
    game_over_sound = pygame.mixer.Sound('sounds/game-over-sound.wav')
    block_timer = 1
    time_divisor = 500
    font = pygame.font.Font('freesansbold.ttf', 32)

    running = True

    while running:
        screen.fill((50, 50, 50))
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not paused:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    block.control_block('left', muted)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    block.control_block('right', muted)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    block.control_block('rotate', muted)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # reduces the time for moving the block downwards
                    time_divisor -= 250
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s and time_divisor == 250:
                    # increases the time for moving the block downwards to the original speed
                    time_divisor += 250
                elif event.key == pygame.K_p and not game_over:
                    paused = not paused

                    if not muted:
                        pygame.mixer.Sound.play(pause_sound)
                elif event.key == pygame.K_m:
                    muted = not muted
                    pygame.mixer.Sound.play(mute_sound)
                elif event.key == pygame.K_RETURN and game_over:
                    # resets the game if user uses enter key on the menu to replay
                    block = Tetrominoes()
                    score = 0
                    paused = False
                    game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # resets the game if user uses mouse on the menu to replay
                mouse_pressed = pygame.mouse.get_pressed()

                if mouse_pressed[0] and game_over:
                    # position of the replay button on the game over menu
                    pos_x1 = 150
                    pos_y1 = 500

                    # checks for left mouse click within the replay button area to restart
                    if pos_x1 < pygame.mouse.get_pos()[0] < pos_x1 + 300 \
                            and pos_y1 < pygame.mouse.get_pos()[1] < pos_y1 + 50:
                        block = Tetrominoes()
                        score = 0
                        line_count = 0
                        paused = False
                        game_over = False

        screen.blit(font.render("P - ", True, (255, 255, 255)), (650, 700))
        screen.blit(font.render("M - ", True, (255, 255, 255)), (650, 815))

        if not paused:
            # updates block position every second
            if pygame.time.get_ticks()//time_divisor > block_timer:
                if time_divisor != 250:
                    block_timer += 1

                state = block.move_block(muted)

                if state:
                    paused = True
                    game_over = True

                    if not muted:
                        pygame.mixer.Sound.play(game_over_sound)

                if block.score_tracker(muted):
                    score += 40
                    line_count += 1

            screen.blit(paused_icon, (700, 675))
        else:
            if pygame.time.get_ticks()//time_divisor > block_timer:
                if time_divisor != 250:
                    block_timer += 1

            screen.blit(play_icon, (700, 675))

        if not muted:
            screen.blit(sound_icon, (710, 800))
        else:
            screen.blit(muted_icon, (710, 800))

        # draws the purple board base and the grey background space of the game board
        pygame.draw.rect(screen, (40, 40, 40), (50, 0, 500, 900))
        pygame.draw.rect(screen, (155, 155, 255), (50, 852, 500, 50), 0, 3)

        block.draw_blocks(screen)
        # calls function to draw the next block
        block.next_bloc(screen)

        if game_over:
            draw_menu(screen, font)

        draw_board(screen, font, score, line_count)

        pygame.display.flip()

    pygame.quit()


main()
