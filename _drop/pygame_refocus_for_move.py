#pygame refocus
class Button_PG_tool():


    # colours for button and text
    padding = 4
    radius = 7
    off_col = '#19d1e5'
    off_col_h = '#29e1e6'
    on_col = '#81f900'
    on_col_h = '#82f102'
    spindown_col = '#ff9700'
    spindown_col_h = '#ff9801'
    text_col = '#16171d'
    width = button_width
    height = button_height
    status = False
    font = pygame.font.SysFont('meslolgsnf', 10, bold=True)
    #font = pygame.font.SysFont('Menlo', 20, bold=True)

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.button_rect = Rect(self.x+self.padding, self.y+self.padding,
                                self.width-(self.padding*2), self.height-(self.padding*2))

    def on(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col, self.button_rect,
                         border_radius=self.radius)

    def on_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col_h,
                         self.button_rect, border_radius=self.radius)

    def off(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col, self.button_rect,
                         border_radius=self.radius)

    def off_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col_h,
                         self.button_rect, border_radius=self.radius)

    def spindown(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.spindown_col,
                         self.button_rect, border_radius=self.radius)

    def spindown_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.spindown_col_h,
                         self.button_rect, border_radius=self.radius)

    def draw_button(self):
        global clicked
        action = False
        selected_tool = tools[self.name] # select the tool associated with this button

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.button_rect.collidepoint(pos):                             #mouse if over the button

            if pygame.mouse.get_pressed()[0] == 1:                       #mouse is pressed but not released
                clicked = True
                if selected_tool.status == 'on':
                    self.spindown_h()
                elif selected_tool.status == 'off':
                    self.on_h()
                elif selected_tool.status == 'spindown':
                    self.on_h()
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True: #mouse was just released
                if selected_tool.status == 'on':
                    selected_tool.override = False
                    selected_tool.spindown()
                    self.spindown_h()
                elif selected_tool.status != 'on':
                    selected_tool.turn_on()
                    selected_tool.override = True
                    self.on_h()

                clicked = False
                action = True
            else:                                                       #mouse is just over without click
                if selected_tool.status == 'on':
                    self.on_h()
                elif selected_tool.status == 'off':
                    self.off_h()
                elif selected_tool.status == 'spindown':
                    self.spindown_h()
        else:                                                           #mouse is not over button
            if selected_tool.status == 'on':
                self.on()
            elif selected_tool.status == 'off':
                self.off()
            elif selected_tool.status == 'spindown':
                self.spindown()

        # add text to button
        text_img = self.font.render(self.name, True, self.text_col)
        text_len = text_img.get_width()

        if selected_tool.status == 'spindown':
            info = str(round(selected_tool.spin_down_time - 
                                    (time.time() - selected_tool.last_used), 1))
        elif selected_tool.status == 'on':
            info = 'on'
        else:
            info = 'off'
        
        status_line = self.font.render(info, True, self.text_col)
        status_len = status_line.get_width()
        
        screen.blit(text_img, (self.x + int(self.width / 2) -
                    int(text_len / 2), self.y +12))
        screen.blit(status_line, (self.x + int(self.width / 2) -
                    int(status_len / 2), self.y +25))
        return action
