import pygame
import random
from copy import deepcopy


class Tetrominoes:
    def __init__(self):
        self.board = []  # list to track block positions within the game board
        self.complete_line = False  # checks for complete lines within the game
        self.line_pos = 0  # tracks the position of the complete line
        self.time_tracker = 1

        self.movement_sound = pygame.mixer.Sound('sounds/movement-sound.wav')
        self.collision_sound = pygame.mixer.Sound('sounds/collision-sound.wav')
        self.line_sound = pygame.mixer.Sound('sounds/line-sound.wav')

        # populates the list with zeros to set the board as empty
        for i in range(0, 17):
            block = []
            for j in range(0, 10):
                block.append(0)
            self.board.append(block)

        # list stores the blocks as they are created
        self.blocks = []

        # tracks the rotation of the current block
        self.rotation = 0

        # list for storing all the block types
        self.block_types = []

        # list stores the color of the block type and the rectangles that make it up
        self.i_block = [(0, 0, 255), pygame.Rect(252, -148, 48, 48), pygame.Rect(252, -198, 48, 48),
                        pygame.Rect(252, -98, 48, 48), pygame.Rect(252, -48, 48, 48)]

        self.l_block = [(255, 165, 0), pygame.Rect(252, -98, 48, 48), pygame.Rect(252, -148, 48, 48),
                        pygame.Rect(252, -48, 48, 48), pygame.Rect(302, -48, 48, 48)]

        self.o_block = [(255, 255, 0), pygame.Rect(252, -98, 48, 48), pygame.Rect(302, -98, 48, 48),
                        pygame.Rect(302, -48, 48, 48), pygame.Rect(252, -48, 48, 48)]

        self.s_block = [(0, 255, 0), pygame.Rect(252, -98, 48, 48), pygame.Rect(302, -98, 48, 48),
                        pygame.Rect(252, -48, 48, 48), pygame.Rect(202, -48, 48, 48)]

        self.t_block = [(128, 0, 128), pygame.Rect(252, -48, 48, 48), pygame.Rect(252, -98, 48, 48),
                        pygame.Rect(302, -48, 48, 48), pygame.Rect(202, -48, 48, 48)]

        # (x, y) values to increment the block position according to the rotation
        self.i_rotations = [[(50, 50), (-50, -50), (-100, -100)],
                            [(-50, -50), (50, 50), (100, 100)],
                            [(50, 50), (-50, -50), (-100, -100)],
                            [(-50, -50), (50, 50), (100, 100)]]

        self.l_rotations = [[(50, 50), (-50, -50), (-100, 0)],
                            [(-50, 50), (50, -50), (0, -100)],
                            [(-50, -50), (50, 50), (100, 0)],
                            [(50, -50), (-50, 50), (0, 100)]]

        self.s_rotations = [[(-50, 50), (-50, -50), (0, -100)],
                            [(50, -50), (50, 50), (0, 100)],
                            [(-50, 50), (-50, -50), (0, -100)],
                            [(50, -50), (50, 50), (0, 100)]]

        self.t_rotations = [[(50, 50), (-50, 50), (50, -50)],
                            [(-50, 50), (-50, -50), (50, 50)],
                            [(-50, -50), (50, -50), (-50, 50)],
                            [(50, -50), (50, 50), (-50, -50)]]

        self.block_types.append(self.i_block)
        self.block_types.append(self.l_block)
        self.block_types.append(self.o_block)
        self.block_types.append(self.s_block)
        self.block_types.append(self.t_block)

        self.current_block = 0  # tracks the position of the current block
        self.next_block = list(range(0, 5))  # list stores the
        random.shuffle(self.next_block)  # shuffles the list to randomize selection
        self.next = self.next_block.pop()  # used to create the next block type from the randomized list of types above
        self.collision = False  # checks for block collision

    def draw_blocks(self, screen):
        if self.complete_line:
            # draws the blocks with the complete line as a different color
            if (pygame.time.get_ticks()//1000)-self.time_tracker != 1:
                for j in range(0, len(self.blocks)):
                    for i in range(1, len(self.blocks[j])):
                        if 0 <= self.blocks[j][i].y <= 850 and 50 <= self.blocks[j][i].x <= 550:
                            if self.blocks[j][i].y == (self.line_pos*50)+2:
                                pygame.draw.rect(screen, (155, 155, 255), self.blocks[j][i], 1, 3)
                            else:
                                pygame.draw.rect(screen, self.blocks[j][0], self.blocks[j][i], 0, 3)
            else:
                # calls functions to remove complete lines and reset bool
                self.update_board()
                self.complete_line = False
        else:
            for j in range(0, len(self.blocks)):
                for i in range(1, len(self.blocks[j])):
                    if 0 <= self.blocks[j][i].y <= 850 and 50 <= self.blocks[j][i].x <= 550:
                        pygame.draw.rect(screen, self.blocks[j][0], self.blocks[j][i], 0, 3)

    def move_block(self, muted):
        if self.blocks:
            current = self.current_block
            self.block_collision()

            if self.collision is not True:
                for i in range(1, 5):
                    self.blocks[current][i].y += 50
            else:

                for i in range(1, len(self.blocks[current])):
                    # checks for complete vertical line and ends game
                    if self.blocks[current][i].y < 0:
                        return True

                    # gets value from block current block position
                    k = (self.blocks[current][i].y - 2) // 50
                    j = (self.blocks[current][i].x - 2) // 50

                    if k < 0:
                        k = 0

                    # sets board list value as occupied after collision
                    self.board[k][j - 1] = 1

                # plays sound when block collides
                if not self.complete_line and not muted:
                    pygame.mixer.Sound.play(self.collision_sound)

                if self.next_block:
                    # adds a copy of a new block type to the blocks list
                    self.blocks.append(deepcopy(self.block_types[self.next]))
                else:
                    # repopulates the list with new randomized block types
                    self.next_block = list(range(0, 5))
                    random.shuffle(self.next_block)
                    self.blocks.append(deepcopy(self.block_types[self.next]))

                # sets the current block to the newly added block and resets tracking values
                self.current_block = len(self.blocks) - 1
                self.next = self.next_block.pop()
                self.collision = False
                self.rotation = 0
        else:
            self.blocks.append(deepcopy(self.block_types[self.next]))

            self.current_block = len(self.blocks)-1
            self.next = self.next_block.pop()

    def block_collision(self):
        current = self.current_block

        if self.blocks:
            for i in range(1, len(self.blocks[current])):
                k = (self.blocks[current][i].y + 48) // 50
                j = (self.blocks[current][i].x - 2) // 50

                # checks if the current block hits the bottom of the board or an occupied position
                if self.blocks[current][i].y >= 0 and (self.blocks[current][i].y == 802 or self.board[k][j-1] == 1):
                    self.collision = True
                    return True

    # draws the next block on the stat board
    def next_bloc(self, screen):
        i_block = [pygame.Rect(700, 370, 48, 48), pygame.Rect(700, 420, 48, 48),
                   pygame.Rect(700, 470, 48, 48), pygame.Rect(700, 520, 48, 48)]
        l_block = [pygame.Rect(690, 400, 48, 48), pygame.Rect(690, 450, 48, 48),
                   pygame.Rect(690, 500, 48, 48), pygame.Rect(740, 500, 48, 48)]
        o_block = [pygame.Rect(680, 425, 48, 48), pygame.Rect(730, 425, 48, 48),
                   pygame.Rect(680, 475, 48, 48), pygame.Rect(730, 475, 48, 48)]
        s_block = [pygame.Rect(700, 425, 48, 48), pygame.Rect(750, 425, 48, 48),
                   pygame.Rect(650, 475, 48, 48), pygame.Rect(700, 475, 48, 48)]
        t_block = [pygame.Rect(700, 430, 48, 48), pygame.Rect(650, 480, 48, 48),
                   pygame.Rect(700, 480, 48, 48), pygame.Rect(750, 480, 48, 48)]

        if self.blocks:
            for i in range(0, 4):
                if self.next == 0:
                    pygame.draw.rect(screen, self.i_block[0], i_block[i], 0, 3)
                elif self.next == 1:
                    pygame.draw.rect(screen, self.l_block[0], l_block[i], 0, 3)
                elif self.next == 2:
                    pygame.draw.rect(screen, self.o_block[0], o_block[i], 0, 3)
                elif self.next == 3:
                    pygame.draw.rect(screen, self.s_block[0], s_block[i], 0, 3)
                elif self.next == 4:
                    pygame.draw.rect(screen, self.t_block[0], t_block[i], 0, 3)

    def control_block(self, key, muted):
        if self.blocks and self.collision is not True:
            current = self.current_block

            if key == 'down':
                for i in range(1, len(self.blocks[current])):
                    self.blocks[current][i].y += 50
            elif key == 'left' and self.blocks[current][2].x-50 >= 52 and self.blocks[current][3].x-50 >= 52 \
                    and self.blocks[current][4].x-50 >= 52:
                safe = False
                i = 1
                while i < 5:
                    # checks if all rectangles within a shape have space to move
                    if safe is False:
                        k = (self.blocks[current][i].y - 2) // 50
                        j = (self.blocks[current][i].x - 2) // 50

                        if self.board[k][j - 2] == 1:
                            break

                        if i == 4:
                            i = 0
                            safe = True
                    else:
                        self.blocks[current][i].x -= 50

                    i += 1
            elif key == 'right' and self.blocks[current][2].x+50 <= 502 and self.blocks[current][4].x+50 <= 502 \
                    and self.blocks[current][3].x+50 <= 502:
                safe = False
                i = 1
                while i < 5:
                    # checks if all rectangles within a shape have space to move
                    if safe is False:
                        k = (self.blocks[current][i].y - 2) // 50
                        j = (self.blocks[current][i].x - 2) // 50

                        if self.board[k][j] == 1:
                            break

                        if i == 4:
                            i = 0
                            safe = True
                    else:
                        self.blocks[current][i].x += 50

                    i += 1
            if key == 'rotate' and self.blocks[current][0] != (255, 255, 0) and 100 < self.blocks[current][1].x < 500:
                if self.blocks[current][0] == (0, 0, 255) and self.blocks[current][1].x < 152:
                    return
                else:
                    safe = False
                    i = 2
                    k = 0
                    j = 0

                    # checks if all rectangles within a shape have space to rotate
                    while i < 5:
                        if safe is False:
                            if self.blocks[current][0] == (0, 0, 255):
                                j = (self.blocks[current][i].x + (self.i_rotations[self.rotation][i - 2][0] - 2)) // 50
                                k = (self.blocks[current][i].y + (self.i_rotations[self.rotation][i - 2][1] - 2)) // 50
                            elif self.blocks[current][0] == (255, 165, 0):
                                j = (self.blocks[current][i].x + (self.l_rotations[self.rotation][i - 2][0] - 2)) // 50
                                k = (self.blocks[current][i].y + (self.l_rotations[self.rotation][i - 2][1] - 2)) // 50
                            elif self.blocks[current][0] == (0, 255, 0):
                                j = (self.blocks[current][i].x + (self.s_rotations[self.rotation][i - 2][0] - 2)) // 50
                                k = (self.blocks[current][i].y + (self.s_rotations[self.rotation][i - 2][1] - 2)) // 50
                            elif self.blocks[current][0] == (128, 0, 128):
                                j = (self.blocks[current][i].x + (self.t_rotations[self.rotation][i - 2][0] - 2)) // 50
                                k = (self.blocks[current][i].y + (self.t_rotations[self.rotation][i - 2][1] - 2)) // 50

                            if self.board[k][j-1] == 1:
                                break

                            if i == 4:
                                i = 1
                                safe = True
                        else:
                            break

                        i += 1

                    if safe:
                        for j in range(2, 5):
                            if self.blocks[current][0] == (0, 0, 255):
                                self.blocks[current][j].x += self.i_rotations[self.rotation][j-2][0]
                                self.blocks[current][j].y += self.i_rotations[self.rotation][j-2][1]
                            elif self.blocks[current][0] == (255, 165, 0):
                                self.blocks[current][j].x += self.l_rotations[self.rotation][j-2][0]
                                self.blocks[current][j].y += self.l_rotations[self.rotation][j-2][1]
                            elif self.blocks[current][0] == (0, 255, 0):
                                self.blocks[current][j].x += self.s_rotations[self.rotation][j-2][0]
                                self.blocks[current][j].y += self.s_rotations[self.rotation][j-2][1]
                            elif self.blocks[current][0] == (128, 0, 128):
                                self.blocks[current][j].x += self.t_rotations[self.rotation][j-2][0]
                                self.blocks[current][j].y += self.t_rotations[self.rotation][j-2][1]

                        if self.rotation == 3:
                            self.rotation = 0
                        else:
                            self.rotation += 1

                        if not muted:
                            pygame.mixer.Sound.play(self.movement_sound)

    def score_tracker(self, muted):
        count = 0
        line = 0

        for i in range(0, 17):
            for j in range(0, 10):
                # checks if a horizontal line in the board list is occupied
                if self.board[i][j] == 1:
                    count += 1
                else:
                    count = 0
                    break
            if count == 10:
                line = i
                break

        # if a complete line occurs a sound is played and values are set accordingly
        if count == 10 and not self.complete_line:
            if not muted:
                pygame.mixer.Sound.play(self.line_sound)

            self.complete_line = True
            self.line_pos = line
            self.time_tracker = pygame.time.get_ticks()//1000

            return True

        return False

    def update_board(self):
        # removes the rectangles within the complete line position
        n = len(self.blocks) - 1
        while n >= 0:
            blocks = [self.blocks[n][0]]
            for k in range(1, len(self.blocks[n])):
                if self.blocks[n][k].y == (self.line_pos * 50) + 2:
                    py = (self.blocks[n][k].y - 2) // 50
                    px = (self.blocks[n][k].x - 2) // 50

                    self.board[py][px - 1] = 0
                else:
                    blocks.append(self.blocks[n][k])

            self.blocks[n] = blocks

            if len(self.blocks[n]) == 1:
                self.blocks.pop(n)
                self.current_block = len(self.blocks) - 1
                n = len(self.blocks) - 1
            n -= 1

        # moves all blocks above the line position down to fill in space
        n = 0
        while n < len(self.blocks) - 1:
            for k in range(1, len(self.blocks[n])):
                if self.blocks[n][k].y < (self.line_pos * 50) + 2:
                    py = (self.blocks[n][k].y - 2) // 50
                    px = (self.blocks[n][k].x - 2) // 50
                    self.board[py][px - 1] = 0

                    self.blocks[n][k].y += 50

                    py = (self.blocks[n][k].y - 2) // 50

                    self.board[py][px-1] = 1
            if n == len(self.blocks) - 2 and self.line_pos != 1:
                self.line_pos -= 1
                n = 0

            if self.line_pos == 1:
                break

            n += 1
