class MouseEvents:    
    def erase(self, current):
        for i in range(len(self.circle_list)):
            if self.level[self.circle_list[i][0] + current[0] - self.circle_radius][self.circle_list[i][1] + current[1] - self.circle_radius][0] in (4, 3):
                self.level[self.circle_list[i][0] + current[0] - self.circle_radius][self.circle_list[i][1] + current[1] - self.circle_radius] = [0, (0, 0, 0)]
                self.world.set_at((self.circle_list[i][1] + current[1] - self.circle_radius, self.circle_list[i][0] + current[0] - self.circle_radius), self.level[self.circle_list[i][0] + current[0] - self.circle_radius][self.circle_list[i][1] + current[1] - self.circle_radius][1])

    def draw(self, current):
        for i in range(len(self.circle_list)):
            if self.level[self.circle_list[i][0] + current[0] - self.circle_radius][self.circle_list[i][1] + current[1] - self.circle_radius][0] == 0:
                self.level[self.circle_list[i][0] + current[0] - self.circle_radius][self.circle_list[i][1] + current[1] - self.circle_radius] = [4, (124, 91, 68)]
                self.world.set_at((self.circle_list[i][1] + current[1] - self.circle_radius, self.circle_list[i][0] + current[0] - self.circle_radius), self.level[self.circle_list[i][0] + current[0] - self.circle_radius][self.circle_list[i][1] + current[1] - self.circle_radius][1])

    def handle_mouse_events(self):
        erase = [0, 0]
        draw = [0, 0]
        py = [0, 0]
        px = [0, 0]
        erase[1] = erase[0]
        draw[1] = draw[0]
        py[1] = py[0]
        px[1] = px[0]
        erase[0], thrash, draw[0] = pygame.mouse.get_pressed(num_buttons=3)
        px[0], py[0] = pygame.mouse.get_pos()
        if erase[0]:
            if erase[1]:
                if py[0] != py[1] or px[0] != px[1]:
                    current = [py[0], px[0]]
                    float_modifier = 0
                    float_number = 0
                    if py[0] > py[1]:
                        py_difference = py[0] - py[1]
                        py_modifier = 1
                    else:
                        py_difference = py[1] - py[0]
                        py_modifier = -1
                    if px[0] > px[1]:
                        px_difference = px[0] - px[1]
                        px_modifier = 1
                    else:
                        px_difference = px[1] - px[0]
                        px_modifier = -1
                    if py_difference > pxDifference:
                        float_modifier = pxDifference / py_difference
                        float_number = current[1]
                        for i in range(py_difference - pxDifference):
                            for j in range(len(self.circle_list)):
                                if self.level[self.circle_list[j][0] + current[0] - self.circle_radius][self.circle_list[j][1] + current[1] - self.circle_radius][0] in (4, 3):
                                    self.level[self.circle_list[j][0] + current[0] - self.circle_radius][self.circle_list[j][1] + current[1] - self.circle_radius] = [0, (0, 0, 0)]
                                    self.world.set_at((self.circle_list[j][1] + current[1] - self.circle_radius, self.circle_list[j][0] + current[0] - self.circle_radius), self.level[self.circle_list[j][0] + current[0] - self.circle_radius][self.circle_list[j][1] + current[1] - self.circle_radius][1])
                            current[0] += py_modifier
                            float_number += float_modifier
                            current[1] = round(float_number)
                    else:
                        float_modifier = py_difference / pxDifference
                        float_number = current[0]
                        for i in range(pxDifference - py_difference):
                            for j in range(len(self.circle_list)):
                                if self.level[self.circle_list[j][0] + current[0] - self.circle_radius][self.circle_list[j][1] + current[1] - self.circle_radius][0] in (4, 3):
                                    self.level[self.circle_list[j][0] + current[0] - self.circle_radius][self.circle_list[j][1] + current[1] - self.circle_radius] = [0, (0, 0, 0)]
                                    self.world.set_at((self.circle_list[j][1] + current[1] - self.circle_radius, self.circle_list[j][0] + current[0] - self.circle_radius), self.level[self.circle_list[j][0] + current[0] - self.circle_radius][self.circle_list[j][1] + current[1] - self.circle_radius][1])
                            current[1] += px_modifier
                            float_number += float_modifier
                            current[0] = round(float_number)
            else:
                for i in range(len(self.circle_list)):
                    if self.level[self.circle_list[i][0] + py[0] - self.circle_radius][self.circle_list[i][1] + px[0] - self.circle_radius][0] in (4, 3):
                        self.level[self.circle_list[i][0] + py[0] - self.circle_radius][self.circle_list[i][1] + px[0] - self.circle_radius] = [0, (0, 0, 0)]
                        self.world.set_at((self.circle_list[i][1] + px[0] - self.circle_radius, self.circle_list[i][0] + py[0] - self.circle_radius), self.level[self.circle_list[i][0] + py[0] - self.circle_radius][self.circle_list[i][1] + px[0] - self.circle_radius][1])

# This should be in main loop:
# self.handle_mouse_events()